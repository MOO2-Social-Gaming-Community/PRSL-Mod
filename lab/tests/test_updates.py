import base64,json,unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from prsl.binary150 import PATCH_SHA256,ENGINE_SHA256
from prsl.updates import verify_catalog,local_eligibility,CatalogError

class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.key=Ed25519PrivateKey.generate()
        self.pub=self.key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
        self.bundle={'patch_sha256':PATCH_SHA256,'engine_sha256':ENGINE_SHA256,'patch_size':12105924}
        self.catalog={'schema':1,'revision':3,'expires_unix':200,'bundles':[self.bundle]}
    def envelope(self):
        payload=json.dumps(self.catalog,sort_keys=True).encode()
        return json.dumps({'payload':base64.b64encode(payload).decode(),'signature':base64.b64encode(self.key.sign(payload)).decode()}).encode()
    def test_valid_signature(self):self.assertEqual(verify_catalog(self.envelope(),self.pub,now=100,highest_revision=3),self.catalog)
    def test_tampered_payload(self):
        doc=json.loads(self.envelope());doc['payload']=base64.b64encode(b'{}').decode()
        with self.assertRaises(CatalogError):verify_catalog(json.dumps(doc).encode(),self.pub,now=100,highest_revision=0)
    def test_wrong_key(self):
        other=Ed25519PrivateKey.generate().public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
        with self.assertRaises(CatalogError):verify_catalog(self.envelope(),other,now=100,highest_revision=0)
    def test_expired(self):
        with self.assertRaises(CatalogError):verify_catalog(self.envelope(),self.pub,now=200,highest_revision=0)
    def test_rollback(self):
        with self.assertRaises(CatalogError):verify_catalog(self.envelope(),self.pub,now=100,highest_revision=4)
    def test_signed_but_unsupported_engine_stays_disabled(self):
        self.bundle['engine_sha256']='0'*64
        catalog=verify_catalog(self.envelope(),self.pub,now=100,highest_revision=0)
        self.assertFalse(local_eligibility(catalog['bundles'][0])['install_allowed'])
    def test_catalog_cannot_override_local_prsl_safety(self):
        self.bundle['runtime_certified']=True
        self.assertFalse(local_eligibility(self.bundle,'prsl')['install_allowed'])
    def test_recognized_community_allowed(self):self.assertTrue(local_eligibility(self.bundle)['install_allowed'])
    def test_oversized_metadata(self):
        with self.assertRaises(CatalogError):verify_catalog(b' '*256001,self.pub,now=100,highest_revision=0)
    def test_invalid_package_size(self):
        self.bundle['patch_size']=True
        with self.assertRaises(CatalogError):verify_catalog(self.envelope(),self.pub,now=100,highest_revision=0)
