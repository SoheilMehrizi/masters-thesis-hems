"""Render local source evidence without modifying original PDFs."""
import concurrent.futures
import json
import subprocess
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/literature'
inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
(ROOT/'reports/literature/analyses').mkdir(exist_ok=True)
def prepare(item):
    identity=item['id']; target=OUT/'assets'/identity
    if identity in ('la-upahem','article-02'):return f'{identity}: existing verified source assets retained'
    target.mkdir(parents=True,exist_ok=True)
    reader=PdfReader(item['path'])
    pages=[page.extract_text() or '' for page in reader.pages]
    (target/'source-text.json').write_text(json.dumps(pages,ensure_ascii=False),encoding='utf-8')
    if len(list(target.glob('page-*.png')))!=len(pages):
        result=subprocess.run(['pdftoppm','-scale-to','1400','-png',item['path'],str(target/'page')],capture_output=True,text=True)
        if result.returncode:raise RuntimeError(f'{identity}: {result.stderr[-500:]}')
    return f'{identity}: {len(pages)} original pages rendered'
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(prepare,inventory):print(result,flush=True)
