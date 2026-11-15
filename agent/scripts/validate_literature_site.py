"""Check evidence integrity, source links and review completion labels."""
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/literature'
class Document(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.images=[];self.classes=Counter()
    def handle_starttag(self,tag,attributes):
        attributes=dict(attributes)
        self.classes.update(attributes.get('class','').split())
        if tag=='img':self.images.append(attributes)
        if 'id' in attributes:self.ids.append(attributes['id'])
        self.links.extend(attributes[k] for k in ('href','src') if k in attributes)
errors=[]
documents={}
for path in OUT.glob('*.html'):
    document=Document();document.feed(path.read_text(encoding='utf-8'));documents[path.name]=document
    duplicates=[k for k,v in Counter(document.ids).items() if v>1]
    if duplicates:errors.append(f'{path.name}: duplicate IDs {duplicates}')
for name,document in documents.items():
    for link in document.links:
        if link.startswith(('https:','http:','file:')):continue
        file,_,anchor=link.partition('#');file=file.split('?',1)[0];target=(OUT/file) if file else OUT/name
        if not target.exists():errors.append(f'{name}: missing {link}');continue
        target_doc=documents.get(target.name) if target.parent==OUT else None
        if anchor and target_doc and anchor not in target_doc.ids:errors.append(f'{name}: missing anchor {link}')
inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
available={x['id'] for x in inventory if x['status']=='Report available'}
record_ids={'la-upahem','article-02'}
for path in (ROOT/'reports/literature/analyses').glob('article-*.json'):
    record=json.loads(path.read_text(encoding='utf-8'));identity=record['id'];record_ids.add(identity)
    pages=next(x['pages'] for x in inventory if x['id']==identity)
    for kind in ('figures','tables'):
        ids=[str(x['id']) for x in record[kind]]
        if len(ids)!=len(set(ids)):errors.append(f'{identity}: duplicate {kind} records')
        for item in record[kind]:
            if not 1<=item['page']<=pages:errors.append(f'{identity}: invalid {kind} source page')
            fields=('caption','explanation','data') if kind=='figures' else ('title','summary')
            for field in fields:
                if any(not item.get(field,{}).get(lang,'').strip() for lang in ('en','fa')):
                    errors.append(f'{identity}: missing bilingual {kind} {field}')
    for question in ('importance','contribution','employment','baseline'):
        answer=record['role'].get(question,{})
        if not answer.get('en') or not answer.get('fa') or not answer.get('pages'):errors.append(f'{identity}: incomplete role answer {question}')
    def check_citations(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k=='pages' and isinstance(v,list):
                    if any(not isinstance(n,int) or not 1<=n<=pages for n in v):errors.append(f'{identity}: citation outside PDF {v}')
                else:check_citations(v)
        elif isinstance(value,list):
            for v in value:check_citations(v)
    check_citations(record)
for identity in available:
    if 'research-role' not in documents[f'{identity}.html'].ids:errors.append(f'{identity}: missing project-role section')
manifest=json.loads((OUT/'figure-views.json').read_text(encoding='utf-8'))
figure_count=0
if documents['index.html'].classes['card-image']!=len(inventory):errors.append('Landing: missing article card images')
for identity in available:
    document=documents[f'{identity}.html'];expected=len(manifest[identity]['views'])
    figure_count+=expected
    for class_name in ('figure-card','reading-guide','figure-explanation','enlarge-figure'):
        if document.classes[class_name]!=expected:errors.append(f'{identity}: incomplete {class_name} presentation')
    if 'figure-jump' not in document.ids:errors.append(f'{identity}: missing figure navigator')
    for img in document.images:
        if '<' in img.get('alt',''):errors.append(f'{identity}: markup inside image alt text')
if available!=record_ids:errors.append('Landing status does not match available report records')
result={'available_reports':len(available),'inventoried_articles':len(inventory),'figure_views':figure_count,'pending_articles':len(inventory)-len(available),'errors':errors,'status':'PASS' if not errors else 'FAIL'}
(ROOT/'reports/literature/site_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
if errors:raise SystemExit(1)
