#!/usr/bin/env python3
"""Addressed delivery checks. Does not discover or execute any other corpus package."""
import argparse, hashlib, json, os, subprocess, tempfile, sys
from pathlib import Path
from example import replay
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--law',default=os.environ.get('LAW_BIN','law'));p.add_argument('--package',choices=['constitution','kanpo'],action='append');p.add_argument('--examples-only',action='store_true');a=p.parse_args()
 for row in json.loads((ROOT/'source-pin.json').read_text())['files']:
  raw=(ROOT/row['path']).read_bytes();assert len(raw)==row['size'] and 'sha256:'+hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 manifest=json.loads((ROOT/'CANON-MANIFEST.json').read_text())
 for row in manifest['files']:
  raw=(ROOT/row['path']).read_bytes();assert len(raw)==row['size'] and 'sha256:'+hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 selected=a.package or ['constitution','kanpo']; failed=False
 for name in ([] if a.examples_only else selected):
  with tempfile.TemporaryDirectory(prefix='arxo-japan-tests-') as tmp:
   import shutil
   package=Path(tmp)/name;shutil.copytree(ROOT/'packages'/name,package,ignore=shutil.ignore_patterns('.law','__pycache__'))
   run=subprocess.run([a.law,'test',str(package)])
   failed=failed or run.returncode!=0
 for row in json.loads((ROOT/'examples/index.json').read_text()):
  if row['package'].split('@')[0].split('.')[1] not in selected:continue
  actual=replay(row['name'],a.law);expected=json.loads((ROOT/'examples'/row['name']/'result.json').read_text())
  assert actual==expected,row['name']+' canonical document differs'
  assert replay(row['name'],a.law)==actual,row['name']+' is not reproducible'
  native=json.loads(subprocess.check_output([a.law,'eval',str(ROOT/'examples'/row['name'])],text=True));assert native==expected,row['name']+' native law eval differs'
  print('REPLAY PASS',row['name'],actual['resultHash'])
 return 1 if failed else 0
if __name__=='__main__':sys.exit(main())
