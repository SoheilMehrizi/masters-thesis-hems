"""Integrate independently reviewed article records into the shared local library.

Called by build_literature_site.py after the original two report builders.
"""
from PIL import Image

ANALYSES=ROOT/'reports/literature/analyses'
def page_citation(identity,p,label='Source'):
    folder='huang' if identity=='article-02' else identity
    return f'<a class="cite" href="assets/{folder}/page-{p:02}.png" target="_blank">{esc(label)} · PDF p. {p}</a>'
def bilingual(value):return pair(esc(value['en']),esc(value['fa']))
def paragraph(identity,value):
    return '<p>'+bilingual(value)+' '+''.join(page_citation(identity,int(p)) for p in value.get('pages',[]))+'</p>'
role_questions=[('importance','Why is it important to our research?','چرا برای پژوهش ما مهم است؟'),('contribution','What does it contribute to our research?','چه سهمی در پژوهش ما دارد؟'),('employment','How can we employ it?','چگونه از آن استفاده کنیم؟'),('baseline','Should we implement it as a baseline?','آیا باید آن را به‌عنوان خط‌مبنا پیاده کنیم؟')]
def role_section(identity,role):
    return '<section id="research-role" class="panel"><h2>'+pair('Role in our research','نقش مقاله در پژوهش ما')+'</h2><div class="notice critical">'+pair('Project-specific assessment grounded in the cited evidence. These are proposed uses and baseline recommendations, not claims made by the article’s authors or approved changes to our methodology.','ارزیابی اختصاصی پروژه بر اساس شواهد ارجاع‌شده است. کاربردها و خط‌مبناها پیشنهادند؛ ادعای نویسندگان یا تغییر تأییدشده روش پژوهش نیستند.')+'</div>'+''.join('<h3>'+pair(en,fa)+'</h3>'+paragraph(identity,role[key]) for key,en,fa in role_questions)+'</section>'

roles=json.loads((ANALYSES/'existing-roles.json').read_text(encoding='utf-8'))
for identity,role in roles.items():
    path=OUT/f'{identity}.html';content=path.read_text(encoding='utf-8')
    content=content.replace('<section id="references"',role_section(identity,role)+'<section id="references"',1)
    content=content.replace('<a href="#references">','<a href="#research-role">'+pair('Role in our research','نقش در پژوهش ما')+'</a><a href="#references">',1)
    path.write_text(content,encoding='utf-8')

def bibliography(record,source_pages):
    start=int(record['bibliography_start_page'])
    end=int(record.get('bibliography_end_page',len(source_pages)))
    text='\n'.join(source_pages[start-1:end])
    heading=re.search(r'(?im)^\s*(?:references|bibliography)\s*$',text)
    if heading:text=text[heading.end():]
    # Preserve the complete transcript; do not silently infer missing entries.
    numbered=list(re.finditer(r'(?m)^\s*\[(\d+)\]\s+',text))
    if not numbered:numbered=list(re.finditer(r'(?m)^\s*(\d{1,3})\.\s+(?=[A-ZÀ-Ž])',text))
    # DOI fragments and publication years at line starts are not numbered refs.
    # A nonsequential list is preserved verbatim instead of silently dropping text.
    if numbered and [int(m[1]) for m in numbered]!=list(range(1,len(numbered)+1)):
        numbered=[]
    output='<p>'+pair('Full bibliography transcribed from the source PDF. Original reference pages are the authority for formatting and extraction ambiguities; cited works were not independently analyzed just because they appear here.','کتاب‌نامه کامل از PDF منبع استخراج شده است. صفحه اصلی مرجع نگارش و ابهام استخراج است؛ درج منبع به معنی تحلیل مستقل آن اثر نیست.')+'</p>'
    if numbered:
        for i,m in enumerate(numbered):
            entry=' '.join(text[m.end():numbered[i+1].start() if i+1<len(numbered) else len(text)].split())
            output+=f'<div class="reference" id="ref-{m[1]}"><b>[{m[1]}]</b> {esc(entry)}</div>'
    else:output+='<pre>'+esc(text)+'</pre>'
    output+='<p>'+''.join(page_citation(record['id'],p,'Bibliography') for p in range(start,end+1))+'</p>'
    return output, len(numbered)

summary=[]
all_roles=dict(roles)
for path in sorted(ANALYSES.glob('article-*.json')):
    record=json.loads(path.read_text(encoding='utf-8'));identity=record['id']
    all_roles[identity]=record['role']
    metadata=next(x for x in inventory if x['id']==identity)
    assets=OUT/'assets'/identity
    source_pages=json.loads((assets/'source-text.json').read_text(encoding='utf-8'))
    blocks=[]
    def block(key,en,fa,content):blocks.append((key,en,fa,f'<section id="{key}" class="panel"><h2>{pair(en,fa)}</h2>{content}</section>'))
    doi_link=f' <a href="https://doi.org/{esc(metadata["doi"])}">{esc(metadata["doi"])}</a>' if metadata['doi'] else ''
    block('coverage','Source & review coverage','منبع و پوشش مرور','<p>'+bilingual(record['coverage_notes'])+'</p><p>'+page_citation(identity,1,'Article')+doi_link+'</p>')
    for section in record['sections']:
        block(section['id'],section['title']['en'],section['title']['fa'],''.join(paragraph(identity,p) for p in section['paragraphs']))
    if record.get('key_results'):block('key-results','Key reported results','نتایج کلیدی گزارش‌شده',''.join(paragraph(identity,p) for p in record['key_results']))
    figures=''
    for figure in record['figures']:
        number=str(figure['id']);p=int(figure['page'])
        filename=f'figure-{re.sub(r"[^a-zA-Z0-9_-]","-",number)}.png'
        cropped=bool(figure.get('crop'))
        if cropped:
            image=Image.open(assets/f'page-{p:02}.png');w,h=image.size
            image.crop(tuple(int(v*(w if j%2==0 else h)) for j,v in enumerate(figure['crop']))).save(assets/filename)
        image_path=f'assets/{identity}/{filename if cropped else f"page-{p:02}.png"}'
        figures+=f'<figure id="fig-{esc(number)}"><h3>Figure {esc(number)}</h3><a href="{image_path}" target="_blank"><img loading="lazy" src="{image_path}" alt="{esc(figure["caption"]["en"])}"></a><figcaption>'+bilingual(figure['caption'])+page_citation(identity,p,'Figure '+number)+'</figcaption>'
        if not cropped:figures+='<p class="muted">'+pair('Original source-page image: includes the figure and surrounding context.','تصویر صفحه اصلی شامل شکل و بافت پیرامون آن است.')+'</p>'
        figures+='<p>'+bilingual(figure['explanation'])+'</p><div class="notice">'+bilingual(figure['data'])+'</div></figure>'
    block('figures','Figures, captions & extracted evidence','شکل‌ها، عنوان‌ها و شواهد استخراج‌شده',figures or '<p>'+pair('No numbered figures are reported in this source.','در این منبع شکل شماره‌دار گزارش نشده است.')+'</p>')
    table_content=''
    for table in record['tables']:
        p=int(table['page']);number=str(table['id'])
        table_content+='<details><summary>Table '+esc(number)+' · '+bilingual(table['title'])+'</summary><p>'+bilingual(table['summary'])+'</p>'+page_citation(identity,p,'Table '+number)+f'<a href="assets/{identity}/page-{p:02}.png" target="_blank"><img loading="lazy" style="width:100%" src="assets/{identity}/page-{p:02}.png" alt="Source Table {esc(number)}"></a></details>'
    block('tables','Tables & numerical evidence','جدول‌ها و شواهد عددی',table_content or '<p>'+pair('No numbered tables are reported in this source.','در این منبع جدول شماره‌دار گزارش نشده است.')+'</p>')
    block('critical','Critical analysis — reviewer assessment','تحلیل انتقادی — ارزیابی مرورگر','<div class="notice critical">'+pair('The following is separately labeled reviewer assessment, grounded in the cited passages.','موارد زیر ارزیابی مستقل مرورگر بر پایه متن ارجاع‌شده است.')+'</div>'+''.join(paragraph(identity,p) for p in record.get('critical',[])))
    blocks.append(('research-role','Role in our research','نقش مقاله در پژوهش ما',role_section(identity,record['role'])))
    block('pages','Original source pages','صفحات اصلی منبع',''.join(f'<details><summary>PDF page {p}</summary><a href="assets/{identity}/page-{p:02}.png" target="_blank"><img loading="lazy" style="width:100%" src="assets/{identity}/page-{p:02}.png" alt="Original PDF page {p}"></a></details>' for p in range(1,len(source_pages)+1)))
    bib,count=bibliography(record,source_pages)
    block('references','Full bibliography','کتاب‌نامه کامل',bib)
    # Link only citations that actually have a bibliography anchor.
    ref_ids=set(re.findall(r'id="ref-(\d+)"',bib))
    def link_ref(match):
        n=match[1];return f'<a href="#ref-{n}">[{n}]</a>' if n in ref_ids else match[0]
    blocks=[(key,en,fa,''.join(part if part.startswith('<') else re.sub(r'\[(\d{1,3})\]',link_ref,part) for part in re.split(r'(<[^>]+>)',content)) if key!='references' else content) for key,en,fa,content in blocks]
    toc=''.join('<a href="#'+key+'">'+pair(en,fa)+'</a>' for key,en,fa,_ in blocks)
    title=record['title']
    body='<div class="hero"><span class="eyebrow">'+esc(metadata['category']).upper()+'</span><h1>'+esc(record['short_title'])+'</h1><p class="sub">'+bilingual(title)+'</p><span class="pill">'+f'{len(record["figures"])} figure views · {len(record["tables"])} tables · {len(source_pages)} pages'+'</span></div><div class="layout"><aside class="toc">'+toc+'</aside><article class="report">'+''.join(b[3] for b in blocks)+'</article></div>'
    (OUT/f'{identity}.html').write_text(shell(title['en'],body),encoding='utf-8')
    summary.append(dict(id=identity,figures=len(record['figures']),tables=len(record['tables']),pages=len(source_pages),bibliography_entries=count or None,bibliography_format='numbered' if count else 'full transcript',status='Report available'))
(OUT/'coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Integrated {len(summary)} additional article analyses and research-role sections for both original reports.')

research_map='<div class="hero"><span class="eyebrow">P0 / RESEARCH DECISION SUPPORT</span><h1>'+pair('How the literature serves our project','کاربرد منابع در پروژه ما')+'</h1><p class="sub">'+pair('Article-specific relevance, contributions, implementation uses and baseline recommendations. These assessments support future research decisions; they do not approve a baseline or change the architecture.','ارتباط، سهم، کاربرد پیاده‌سازی و پیشنهاد خط‌مبنا برای هر مقاله؛ این ارزیابی‌ها از تصمیم‌های بعدی پشتیبانی می‌کنند و تأیید خط‌مبنا یا تغییر معماری نیستند.')+'</p></div>'
for item in inventory:
    identity=item['id']
    if identity not in all_roles:continue
    research_map+='<section class="panel" style="margin-bottom:20px"><h2><a href="'+identity+'.html#research-role">'+esc(item['title'])+'</a></h2><p class="muted">'+esc(item['category'])+'</p>'
    for key,en,fa in role_questions:
        research_map+='<details'+(' open' if key=='baseline' else '')+'><summary>'+pair(en,fa)+'</summary>'+paragraph(identity,all_roles[identity][key])+'</details>'
    research_map+='</section>'
(OUT/'research-map.html').write_text(shell('Role of the literature in our research',research_map),encoding='utf-8')
index_path=OUT/'index.html'
content=index_path.read_text(encoding='utf-8')
content=content.replace('<div class="toolbar">','<p><a class="btn" href="research-map.html">'+pair('Explore the research-role & baseline map →','مشاهده نقش منابع و نقشه خط‌مبناها ←')+'</a></p><div class="toolbar">',1)
index_path.write_text(content,encoding='utf-8')

exec(compile((ROOT/'scripts/enhance_figure_presentation.py').read_text(encoding='utf-8'), 'enhance_figure_presentation.py', 'exec'), globals())

# Reserve original image proportions before lazy loading so anchor targets stay put.
image_sizes={}
for html_path in OUT.glob('*.html'):
    def reserve_image(match):
        tag=match[0]
        src=re.search(r'\bsrc="([^"]+)"',tag)
        if not src or re.search(r'\bwidth="',tag):return tag
        image_path=OUT/src[1]
        if not image_path.is_file():return tag
        if str(image_path) not in image_sizes:
            with Image.open(image_path) as original:image_sizes[str(image_path)]=original.size
        w,h=image_sizes[str(image_path)]
        return tag[:-1]+f' width="{w}" height="{h}">'
    html_path.write_text(re.sub(r'<img\b[^>]*>',reserve_image,html_path.read_text(encoding='utf-8')),encoding='utf-8')
