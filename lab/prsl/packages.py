"""Offline, pinned environment-manager prototype. No network auto-updater yet.

Imports only the two recognized archives; creates a fresh, verified workspace.
Never applies the laboratory hook to a game. User source archives stay untouched.
"""
from __future__ import annotations
import hashlib, ipaddress, json, os, re, shutil, stat, subprocess, tempfile, zipfile
from pathlib import Path, PurePosixPath
from .binary150 import Image150, BASE_ZIP_SHA256, PATCH_SHA256, ENGINE_SHA256, BASE_ENGINE_SHA256

class PackageError(ValueError): pass


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def safe_relative(name: str) -> Path:
    if not name or '\\' in name or ':' in name or any(ord(c)<32 for c in name):
        raise PackageError(f'Unsafe archive path: {name!r}')
    p=PurePosixPath(name)
    if p.is_absolute() or any(x in ('','.', '..') for x in name.rstrip('/').split('/')):
        raise PackageError(f'Unsafe archive path: {name!r}')
    # Avoid aliases/device paths on Windows as well as traversal on Unix.
    reserved={'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}
    if any(x.endswith((' ','.')) or x.split('.')[0].upper() in reserved for x in p.parts):
        raise PackageError(f'Nonportable archive path: {name!r}')
    return Path(*p.parts)


def safe_extract(archive: Path, destination: Path, prefix: str,
                 *, max_bytes: int = 1024**3, max_files: int = 10000) -> list[str]:
    """Refuse duplicate names, symlinks, traversal, overwrites, and oversized data.

    Destination must be owned by this operation; not safe against a concurrently
    malicious local process mutating its ancestors (not a privilege boundary).
    """
    destination.mkdir(parents=True,exist_ok=True)
    if destination.is_symlink(): raise PackageError('Destination cannot be a symlink')
    with zipfile.ZipFile(archive) as z:
        selected=[]; seen=set(); total=0
        for entry in z.infolist():
            if not entry.filename.startswith(prefix): continue
            tail=entry.filename[len(prefix):]
            if not tail: continue
            rel=safe_relative(tail); mode=(entry.external_attr>>16)&0xffff
            if stat.S_ISLNK(mode): raise PackageError('Archive symlinks are forbidden')
            if entry.flag_bits & 1: raise PackageError('Encrypted archive entry')
            if entry.is_dir(): continue
            key=rel.as_posix().casefold()
            if key in seen: raise PackageError('Duplicate/case-colliding archive member')
            seen.add(key);total+=entry.file_size
            if total>max_bytes or len(seen)>max_files: raise PackageError('Archive exceeds extraction limits')
            selected.append((entry,rel))
        if not selected: raise PackageError('Expected archive subtree is missing')
        written=[]
        for entry,rel in selected:
            target=destination/rel
            # Refuse even case-only collisions from a previous overlay.
            for ancestor in (target.parent,*target.parent.parents):
                if ancestor==destination.parent: break
                if ancestor.is_symlink(): raise PackageError('Symlink in extraction path')
            target.parent.mkdir(parents=True,exist_ok=True)
            if any(x.name.casefold()==target.name.casefold() for x in target.parent.iterdir()):
                raise PackageError(f'Refusing existing file/case alias: {rel}')
            with z.open(entry) as source,target.open('xb') as sink:
                size=0
                while block:=source.read(1024*1024):
                    size+=len(block)
                    if size>entry.file_size: raise PackageError('Entry exceeds declared length')
                    sink.write(block)
            if size!=entry.file_size: raise PackageError('Entry length mismatch')
            written.append(rel.as_posix())
    return written


def mutable(name: str) -> bool:
    p=PurePosixPath(name)
    return p.suffix.lower() in {'.gam','.cfg','.ini','.log'} or name.lower().startswith('150/builds/')


def build(base: Path, patch: Path, destination: Path) -> dict:
    base=base.resolve();patch=patch.resolve();destination=destination.absolute()
    if destination.exists() or destination.is_symlink(): raise PackageError('Destination already exists; choose a new bundle directory')
    if sha256(base)!=BASE_ZIP_SHA256: raise PackageError('Unrecognized base archive; only the supplied 1.31 archive is supported')
    if sha256(patch)!=PATCH_SHA256: raise PackageError('Unrecognized community archive; no implicit latest-version upgrade')
    destination.parent.mkdir(parents=True,exist_ok=True)
    temp=Path(tempfile.mkdtemp(prefix='.prsl-stage-',dir=destination.parent))
    try:
        game=temp/'game';base_names=safe_extract(base,game,'Master of Orion 2/')
        baseline={name:sha256(game/name) for name in base_names}
        patch_names=safe_extract(patch,game,'MOO2-1.50.26/patch/')
        changed=[name for name,digest in baseline.items() if sha256(game/name)!=digest]
        if changed: raise PackageError('Community overlay changed original source files')
        if sha256(game/'ORION2.EXE')!=BASE_ENGINE_SHA256: raise PackageError('Wrong base executable')
        adapter=Image150.read(game/'ORION150.EXE').target_map()
        entries={name:{'sha256':sha256(game/name),'size':(game/name).stat().st_size,
                       'mutable':mutable(name),'source':'base' if name in baseline else 'community'}
                 for name in sorted(base_names+patch_names)}
        manifest={'schema':1,'bundle_id':'moo2-15026-prsl-research-0.2.0','community_version':'1.50.26',
                  'engine_sha256':ENGINE_SHA256,'source_archives':{'base':BASE_ZIP_SHA256,'patch':PATCH_SHA256},
                  'original_files_changed':changed,'files':entries,
                  'prsl':{'version':'0.2.0','runtime_certified':False,'installable_adapter':False,
                          'reason':'Only isolated instruction tests; no live DOSBox/IPX certification'}}
        (temp/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (temp/'adapter-research.json').write_text(json.dumps(adapter,indent=2)+'\n')
        if not verify(temp)['ok']: raise PackageError('Staging verification failed')
        # Re-check source integrity before activation. No source archive is written.
        if sha256(base)!=BASE_ZIP_SHA256 or sha256(patch)!=PATCH_SHA256: raise PackageError('Source changed during import')
        os.rename(temp,destination)
        return manifest
    except BaseException:
        shutil.rmtree(temp,ignore_errors=True);raise


def verify(bundle: Path) -> dict:
    manifest_path=bundle/'manifest.json'
    if manifest_path.stat().st_size>8*1024*1024: raise PackageError('Manifest too large')
    manifest=json.loads(manifest_path.read_text())
    if manifest.get('schema')!=1 or len(manifest.get('files',{}))>10000: raise PackageError('Unsupported manifest')
    bad=[];user_changes=[]
    game=bundle/'game'
    for name,record in manifest['files'].items():
        path=game/safe_relative(name)
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p!=bundle.parent):
            bad.append(name);continue
        changed=not path.is_file() or sha256(path)!=record['sha256']
        if changed:
            (user_changes if record.get('mutable') else bad).append(name)
    engine=game/'ORION150.EXE'
    if not engine.is_file() or engine.is_symlink() or sha256(engine)!=ENGINE_SHA256:
        if 'ORION150.EXE' not in bad: bad.append('ORION150.EXE')
    extras=[p.relative_to(game).as_posix() for p in game.rglob('*') if p.is_file() and p.relative_to(game).as_posix() not in manifest['files']]
    unexpected_code=[n for n in extras if PurePosixPath(n).suffix.lower() in {'.exe','.lbx','.lua','.cfg'}]
    return {'ok':not bad and not unexpected_code,'immutable_failures':bad,'user_changes':user_changes,
            'extra_files':extras,'unexpected_code_or_assets':unexpected_code,
            'files_checked':len(manifest['files']),'prsl_runtime_certified':False}


def dosbox_config(game: Path, role: str='standalone', host: str|None=None, port: int=21300) -> str:
    path=str(game.resolve())
    if any(c in path for c in ('"','\n','\r')): raise PackageError('Path cannot be represented safely in DOSBox configuration')
    if type(port) is not int or not 1024<=port<=65535: raise PackageError('Port must be 1024..65535')
    if role not in {'standalone','host','join'}: raise PackageError('Unknown network role')
    commands=[]
    if role=='host': commands=[f'IPXNET STARTSERVER {port}']
    if role=='join':
        try: address=ipaddress.IPv4Address(host)
        except (ipaddress.AddressValueError,TypeError): raise PackageError('Join requires a numeric IPv4 address') from None
        commands=[f'IPXNET CONNECT {address} {port}']
    return '\n'.join(['# Generated community-mode profile; PRSL is not injected.',
                      '[sdl]','fullscreen=false','[cpu]','core=normal','cycles=auto',
                      '[ipx]','ipx=true','[autoexec]',f'mount c "{path}"','c:',
                      *commands,'ORION150.EXE','exit',''])


def launch(bundle: Path, dosbox: Path, *, mode: str='community',role: str='standalone',host: str|None=None,
           port: int=21300,dry_run: bool=True) -> dict:
    # Hard-coded capability boundary: editing metadata cannot enable unsafe hooks.
    if mode!='community': raise PackageError('PRSL runtime adapter is not certified or implemented; laboratory code will not be installed')
    report=verify(bundle)
    if not report['ok']: raise PackageError('Bundle verification failed: '+json.dumps(report))
    config=dosbox_config(bundle/'game',role,host,port)
    executable=dosbox.expanduser().resolve();config_path=(bundle/'community-dosbox.conf').resolve()
    argv=[str(executable),'-conf',str(config_path)]
    result={'argv':argv,'configuration':config,'mode':'community','executed':False}
    if dry_run: return result
    if not executable.is_file(): raise PackageError('DOSBox executable not found')
    lock=bundle/'running.lock'
    try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError: raise PackageError('Bundle already running or stale running.lock; inspect before removal') from None
    try:
        with os.fdopen(fd,'w') as f:f.write(str(os.getpid()))
        config_path.write_text(config)
        completed=subprocess.run(argv,cwd=bundle,check=False)
        result.update(executed=True,returncode=completed.returncode)
        return result
    finally: lock.unlink(missing_ok=True)
