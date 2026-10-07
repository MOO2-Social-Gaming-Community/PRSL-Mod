#!/usr/bin/env python3
"""Reconstruct and execute isolated original instructions; Linux x86-64 only.
Usage: PYTHONPATH=. python tools/run_native_probe.py /path/to/ORION150.EXE
User-owned binary data stays in a temporary directory and is not redistributed.
"""
import argparse, json, pathlib, platform, subprocess, tempfile
from prsl.binary150 import Image150
from prsl.lab_gate import build_gate

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('engine',type=pathlib.Path); p.add_argument('--log',type=pathlib.Path)
    args=p.parse_args()
    if platform.system()!='Linux' or platform.machine()!='x86_64':
        p.error('Native probe requires Linux x86-64; use structural tests elsewhere.')
    image=Image150.read(args.engine)
    with tempfile.TemporaryDirectory(prefix='prsl-native-') as d:
        root=pathlib.Path(d)
        for suffix,apply in [('pre',False),('post',True)]:
            for name,data in zip(('code','data','extension'),image.lab_images(apply)):
                (root/f'{name}_{suffix}.bin').write_bytes(data)
        (root/'gate.bin').write_bytes(build_gate())
        probe=root/'native_probe'
        subprocess.run(['gcc','-std=c11','-O0','-no-pie','-Wall','-Wextra',str(pathlib.Path(__file__).with_name('native_probe.c')),'-o',str(probe)],check=True,timeout=30)
        result=subprocess.run([str(probe),str(root)],capture_output=True,text=True,timeout=15)
        log=result.stdout+result.stderr
        print(log,end='')
        if args.log:
            args.log.parent.mkdir(parents=True,exist_ok=True); args.log.write_text(log)
        if result.returncode:
            raise SystemExit(f'Probe failed/unsupported environment: {result.returncode}')
if __name__=='__main__': main()
