"""Offline signed-catalog verification primitive, NOT a complete updater.

Public key and highest observed revision must come from trusted local state,
not from the downloaded envelope. Production key rotation, durable rollback
state, transport, scheduling, runtime delivery, and activation remain unbuilt.
"""
from __future__ import annotations
import base64, hashlib, json, math, re
from .binary150 import PATCH_SHA256, ENGINE_SHA256

class CatalogError(ValueError): pass

def _unique(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise CatalogError('Duplicate JSON key')
        result[key]=value
    return result

def verify_catalog(envelope: bytes, trusted_key: bytes, *, now: float, highest_revision: int) -> dict:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    if len(envelope)>256_000 or len(trusted_key)!=32: raise CatalogError('Envelope/key size invalid')
    if not math.isfinite(now) or type(highest_revision) is not int or highest_revision<0: raise CatalogError('Invalid trusted state')
    try:
        doc=json.loads(envelope,object_pairs_hook=_unique)
        if set(doc)!={'payload','signature'}: raise CatalogError('Unknown envelope format')
        payload=base64.b64decode(doc['payload'],validate=True)
        signature=base64.b64decode(doc['signature'],validate=True)
        if len(payload)>128_000 or len(signature)!=64: raise CatalogError('Payload/signature size invalid')
        Ed25519PublicKey.from_public_bytes(trusted_key).verify(signature,payload)
        catalog=json.loads(payload,object_pairs_hook=_unique)
    except (InvalidSignature,ValueError,TypeError,KeyError) as e:
        raise CatalogError('Invalid catalog or signature') from e
    if not isinstance(catalog,dict): raise CatalogError('Catalog must be an object')
    if catalog.get('schema')!=1: raise CatalogError('Unsupported catalog schema')
    revision=catalog.get('revision');expires=catalog.get('expires_unix')
    if type(revision) is not int or revision<highest_revision: raise CatalogError('Metadata rollback')
    if type(expires) not in (int,float) or not math.isfinite(expires) or expires<=now: raise CatalogError('Expired catalog')
    bundles=catalog.get('bundles')
    if not isinstance(bundles,list) or len(bundles)>100: raise CatalogError('Invalid bundle list')
    for b in bundles:
        if not isinstance(b,dict): raise CatalogError('Invalid bundle record')
        for field in ('patch_sha256','engine_sha256'):
            if not isinstance(b.get(field),str) or not re.fullmatch('[0-9a-f]{64}',b[field]): raise CatalogError('Invalid digest')
        if type(b.get('patch_size')) is not int or not 0<b['patch_size']<=1024**3: raise CatalogError('Invalid package size')
    return catalog

def local_eligibility(bundle: dict, mode: str='community') -> dict:
    if mode not in {'community','prsl'}: raise CatalogError('Unknown launch mode')
    recognized=(bundle.get('patch_sha256')==PATCH_SHA256 and bundle.get('engine_sha256')==ENGINE_SHA256)
    allowed=recognized and mode=='community'
    return {'recognized_engine_bundle':recognized,'install_allowed':allowed,
            'prsl_runtime_certified':False,
            'reason':'Pinned community bundle' if allowed else 'No certified live PRSL adapter or unsupported upstream build'}
