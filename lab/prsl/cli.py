"""python -m prsl.cli --help"""
import argparse,json,sys,time
from pathlib import Path
from .binary150 import Image150
from .packages import build,verify,launch,PackageError

def main():
    parser=argparse.ArgumentParser(description='PRSL research environment manager 0.2.0; no live PRSL adapter')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('catalog-check');p.add_argument('envelope',type=Path);p.add_argument('--trusted-key',type=Path,required=True);p.add_argument('--highest-revision',type=int,required=True)
    p=sub.add_parser('inspect');p.add_argument('engine',type=Path)
    p=sub.add_parser('build');p.add_argument('--base',type=Path,required=True);p.add_argument('--patch',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('verify');p.add_argument('bundle',type=Path)
    p=sub.add_parser('launch');p.add_argument('bundle',type=Path);p.add_argument('--dosbox',type=Path,required=True)
    p.add_argument('--mode',choices=['community','prsl'],default='community');p.add_argument('--role',choices=['standalone','host','join'],default='standalone')
    p.add_argument('--host');p.add_argument('--port',type=int,default=21300);p.add_argument('--execute',action='store_true',help='Default is dry-run only')
    args=parser.parse_args()
    try:
        if args.command=='catalog-check':
            from .updates import verify_catalog,local_eligibility
            if args.envelope.stat().st_size>256000 or args.trusted_key.stat().st_size!=32:
                raise PackageError('Invalid catalog/key file size')
            result=verify_catalog(args.envelope.read_bytes(),args.trusted_key.read_bytes(),now=time.time(),highest_revision=args.highest_revision)
            result={'catalog':result,'local_eligibility':[local_eligibility(b) for b in result['bundles']],
                    'note':'Verification only; caller must persist trusted revision; no download or activation'}
        elif args.command=='inspect':result=Image150.read(args.engine).target_map()
        elif args.command=='build':
            manifest=build(args.base,args.patch,args.out)
            result={'destination':str(args.out),'files':len(manifest['files']),'original_files_changed':manifest['original_files_changed'],'prsl':manifest['prsl']}
        elif args.command=='verify': result=verify(args.bundle)
        else:result=launch(args.bundle,args.dosbox,mode=args.mode,role=args.role,host=args.host,port=args.port,dry_run=not args.execute)
        print(json.dumps(result,indent=2))
        if args.command=='verify' and not result['ok']:raise SystemExit(1)
    except (ValueError,OSError,KeyError) as e:
        parser.exit(2,f'Error: {e}\n')
if __name__=='__main__':main()
