#!/usr/bin/env python3
"""Replay an exported case with the pinned model; all legal computation belongs to Arxo."""
import argparse, json, os, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def replay(name, law):
    rows=json.loads((ROOT/'examples/index.json').read_text())
    row=next((r for r in rows if r['name']==name),None)
    if row is None: raise ValueError('Unknown example; choose: '+', '.join(r['name'] for r in rows))
    package=row['package'].split('@')[0].replace('.','-')
    folder=ROOT/'examples'/name
    request={'schemaVersion':'law.core.evaluation-request/0.2',
             'semanticVersion':'0.2.11', 'ir':json.loads((ROOT/'registry'/f'{package}.lawir.json').read_text()),
             'case':json.loads((folder/'case.json').read_text()), 'query':json.loads((folder/'query.json').read_text())}
    with tempfile.TemporaryDirectory(prefix='arxo-japan-case-') as scratch:
        Path(scratch,'request.json').write_text(json.dumps(request,ensure_ascii=False))
        run=subprocess.run([law,'engine','eval',scratch],capture_output=True,text=True)
    if run.returncode: raise RuntimeError(run.stdout or run.stderr)
    return json.loads(run.stdout)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('name');p.add_argument('--law',default=os.environ.get('LAW_BIN','law'));p.add_argument('--json',action='store_true');a=p.parse_args()
    result=replay(a.name,a.law)
    if a.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for r in result['results']:
            print(r['evaluationStatus'],r.get('truthStatus',r.get('value')))
            print('Source anchors:',json.dumps(r.get('sourceAnchors',[]),ensure_ascii=False))
            for j in r.get('judgmentRequests',[]):print('Judgment required:',j['predicate'],'—',j['authority'])
        print('Canonical result hash:',result['resultHash'])
if __name__=='__main__':main()
