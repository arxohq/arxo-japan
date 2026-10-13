#!/usr/bin/env python3
"""Download only the pinned standalone CLI release, verify SHA-256, then extract."""
import argparse,hashlib,json,platform,subprocess,tarfile,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 target={('Darwin','arm64'):'aarch64-apple-darwin',('Linux','x86_64'):'x86_64-unknown-linux-gnu'}.get((platform.system(),platform.machine()))
 lock=json.loads((ROOT/'toolchain.lock.json').read_text());row=lock['targets'].get(target)
 if row is None:raise SystemExit('Unsupported platform; this release supports macOS arm64 and Linux x86_64')
 if a.out.exists():raise SystemExit('Output must be a new directory; existing installations are preserved')
 with tempfile.TemporaryDirectory(prefix='arxo-japan-cli-') as tmp:
  archive=Path(tmp)/'cli.tar.gz';subprocess.run(['curl','--fail','--location','--silent','--show-error',row['url'],'--output',str(archive)],check=True)
  digest=hashlib.sha256(archive.read_bytes()).hexdigest()
  if digest!=row['sha256']:raise SystemExit('CLI archive SHA-256 mismatch')
  a.out.mkdir(parents=True)
  with tarfile.open(archive) as tar:tar.extractall(a.out,filter='data')
 binary=a.out/'law'
 manifest=json.loads((a.out/'law-dist-manifest.json').read_text())
 if manifest['tool']!=lock['tool'] or hashlib.sha256(binary.read_bytes()).hexdigest()!=manifest['sha256']:raise SystemExit('CLI binary or version differs from its distribution manifest')
 subprocess.run([str(binary.resolve()),'version','--json'],check=True)
 print('Verified CLI:',binary.resolve())
if __name__=='__main__':main()
