"""Apply source-derived covers and structured figure reading panels to all reports."""
import html as html_module

view_manifest=json.loads((OUT/'figure-views.json').read_text(encoding='utf-8'))
def plain(value):return html_module.unescape(re.sub('<[^>]+>',' ',value))
def guide_for(value):
    text=plain(value).lower()
    choices=[
    (r'posterior|probabilit', 'Probabilistic evidence','شواهد احتمالاتی','Compare the hypotheses using the legend and the displayed cases. A posterior is the model’s belief; assess it alongside the reported diagnostic outcomes, rather than treating confidence alone as correctness.','فرضیه‌ها را با راهنمای رنگ و حالت‌های نمایش‌داده‌شده مقایسه کنید. پسین باور مدل است؛ آن را همراه نتیجه تشخیص بسنجید و اطمینان را به‌تنهایی معادل صحت نگیرید.'),
    (r'prisma|screening|study.selection', 'Study selection','گزینش مطالعات','Follow the selection stages and distinguish retrieved, screened, excluded and included records. These counts describe the literature corpus, not experimental participants or controller trials.','مراحل انتخاب را دنبال و رکورد بازیابی‌شده، غربال‌شده، حذف‌شده و پذیرفته‌شده را جدا کنید. این شمارش مربوط به پیکره منابع است، نه شرکت‌کننده یا آزمون کنترل‌گر.'),
    (r'bayesian|\bdbn\b|\bdag\b|ontology|causal.graph', 'Graph & dependencies','گراف و وابستگی‌ها','Start with the node types and follow the connections using the paper’s notation. Distinguish faults, observed evidence and intermediate variables; graph connectivity alone is not a measured intervention effect.','ابتدا نوع گره را با نمادگذاری مقاله مشخص و سپس اتصال‌ها را دنبال کنید. خطا، شاهد مشاهده‌شده و متغیر میانی را جدا کنید؛ اتصال گراف به‌تنهایی اثر اندازه‌گیری‌شده مداخله نیست.'),
    (r'interface|screenshot|dashboard|web.interface|photograph|target.office', 'Interface / study setting','رابط یا بستر مطالعه','Identify the inputs, outputs or physical setting visible in the original. Use the caption to distinguish an illustrative screen or setup from a measured experimental result.','ورودی، خروجی یا بستر فیزیکی نمایش‌داده‌شده را مشخص کنید. با عنوان شکل، تصویر نمونه رابط یا تجهیزات را از نتیجه آزمایش اندازه‌گیری‌شده جدا کنید.'),
    (r'trajector|time.series|soc|hour.by.hour|charging.profile|grid.exchange|convergence', 'Time & behavior','زمان و رفتار','Read the time window and units before comparing traces. Match each curve to its legend and the same operating conditions; unlabeled samples are not numerical measurements extracted by this report.','پیش از مقایسه مسیرها، بازه زمان و واحدها را بخوانید. هر منحنی را به راهنما و شرایط یکسان وصل کنید؛ نمونه بدون برچسب، اندازه‌گیری عددی استخراج‌شده در این گزارش نیست.'),
    (r'compar|ablation|sensitivity|performance|error|accuracy|radar|heatmap|wir|rcr|distribution|ranking', 'Comparison & results','مقایسه و نتایج','Check the axes, units, panel labels and the caption’s definition of better performance. Compare methods under the stated conditions; keep uncertainty, tradeoffs and normalization separate from headline gains.','محور، واحد، پنل و تعریف عملکرد بهتر در عنوان را بررسی کنید. روش‌ها را در شرایط بیان‌شده مقایسه و عدم‌قطعیت، مصالحه و نرمال‌سازی را از بهبود شاخص اصلی جدا نگه دارید.'),
    (r'taxonomy|roadmap|bibliometric|keyword|timeline|research.landscape', 'Synthesis & context','ترکیب شواهد و زمینه','Read this as an organization of concepts, dates or literature evidence. Categories and proposed directions should not be interpreted as experimental proof of a new controller or diagnostic method.','این تصویر سازمان‌دهی مفهوم‌ها، تاریخ‌ها یا شواهد منابع است. دسته‌ها و جهت‌های پیشنهادی را اثبات آزمایشی کنترل‌گر یا روش تشخیصی جدید تلقی نکنید.'),
    (r'architecture|framework|workflow|schematic|process|model|pipeline|system', 'Mechanism & workflow','سازوکار و گردش کار','Trace the inputs, processing stages and outputs, then look for feedback or validation paths. Use the accompanying explanation to distinguish the proposed design from components actually tested in the paper.','ورودی، مرحله پردازش و خروجی را دنبال و مسیر بازخورد یا اعتبارسنجی را پیدا کنید. با توضیح همراه، طراحی پیشنهادی را از مؤلفه واقعاً آزموده‌شده جدا کنید.')]
    for pattern,kind,fa,en,fa_guide in choices:
        if re.search(pattern,text):return kind,fa,en,fa_guide
    return ('Source visual','تصویر منبع','Read the original labels and caption first, then use the explanation and evidence note below. Printed quantities are preserved separately from reviewer interpretation.','ابتدا برچسب‌ها و عنوان اصلی را بخوانید و سپس توضیح و یادداشت شاهد را بررسی کنید. مقدار چاپ‌شده از تفسیر مرورگر جدا نگه داشته شده است.')

for item in inventory:
    identity=item['id'];path=OUT/f'{identity}.html';content=path.read_text(encoding='utf-8')
    figure_options=[]
    def improve(match):
        original=match[0];number=re.search(r'id="fig-([^"]+)"',original)[1]
        heading=re.search(r'<h3>.*?</h3>',original,re.S)[0]
        caption=re.search(r'<figcaption>(.*?)</figcaption>',original,re.S)[1]
        image=re.search(r'<a\s+href="[^"]+"[^>]*>\s*<img\b[^>]*>\s*</a>',original,re.S)[0]
        view=view_manifest[identity]['views'].get(number)
        if view:
            image=re.sub(r'(href|src)="[^"]+"',lambda m:m[1]+'="'+view['image']+'"',image)
        image=image.replace('<a ','<a class="figure-image-link" ',1)
        tail=original.split('</figcaption>',1)[1].rsplit('</figure>',1)[0]
        tail=re.sub(r'<p class="muted">.*?</p>','',tail,flags=re.S)
        # Keep reviewed explanations and values intact; only change their presentation.
        evidence=re.search(r'<div class="notice">(.*?)</div>',tail,re.S)
        evidence_html=evidence[1] if evidence else ''
        explanation=re.sub(r'<div class="notice">.*?</div>','',tail,flags=re.S).strip()
        kind,fa_kind,guide_en,guide_fa=guide_for(caption+' '+explanation)
        source=re.search(r'<a class="cite"[^>]*>.*?</a>',caption,re.S)
        source_link=source[0] if source else ''
        image_kind=pair('Focused original figure','تصویر اصلی با نمای متمرکز') if view and view['kind']=='figure' else pair('Original page · full context','صفحه اصلی با بافت کامل')
        en_title=re.search(r'<span class="en">(.*?)</span>',caption,re.S)
        fa_title=re.search(r'<span class="fa"[^>]*>(.*?)</span>',caption,re.S)
        title_text=' '.join(plain(en_title[1] if en_title else caption.split('<a class="cite"')[0]).split())
        fa_text=' '.join(plain(fa_title[1] if fa_title else title_text).split())
        figure_options.append((number,title_text[:105],fa_text[:105]))
        notes='<div class="reading-guide"><h4>'+pair('How to read this figure','راهنمای خواندن شکل')+'</h4><p>'+pair(guide_en,guide_fa)+'</p><small>'+pair('Reader guidance · not an additional author claim','راهنمای مطالعه · ادعای اضافی نویسنده نیست')+'</small></div>'
        notes+='<div class="figure-explanation"><h4>'+pair('What this figure shows','این شکل چه نشان می‌دهد؟')+'</h4>'+explanation+'</div>'
        if evidence_html:
            if plain(evidence_html).strip()==plain(explanation).strip():
                evidence_html=pair('The explanation above summarizes the visual. Inspect the original labels for its full details; no additional values have been inferred.','توضیح بالا تصویر را خلاصه می‌کند. جزئیات کامل در برچسب اصلی است و مقدار اضافی استنباط نشده است.')
            notes+='<div class="figure-evidence"><h4>'+pair('Reported values & evidence limits','مقادیر گزارش‌شده و حدود شواهد')+'</h4><p>'+evidence_html+'</p></div>'
        return f'<figure id="fig-{number}" class="figure-card" data-figure-kind="{esc(kind)}"><header class="figure-heading">{heading}<span class="figure-kind">'+pair(kind,fa_kind)+'</span></header><div class="figure-layout"><div class="figure-visual">'+image+'<div class="figure-actions"><span>'+image_kind+'</span><button type="button" class="enlarge-figure">'+pair('Enlarge figure ↗','بزرگ‌نمایی شکل ↗')+'</button>'+source_link+'</div><figcaption>'+caption+'</figcaption></div><div class="figure-insights">'+notes+'</div></div></figure>'
    content=re.sub(r'<figure\s+id="fig-[^"]+"[^>]*>.*?</figure>',improve,content,flags=re.S)
    if figure_options:
        toolbar='<div class="figure-toolbar"><label for="figure-jump">'+pair('Figure navigator','مرور شکل‌ها')+'</label><select id="figure-jump"><option value="" data-en="Choose a figure" data-fa="انتخاب شکل">Choose a figure</option>'+''.join(f'<option value="fig-{esc(n)}" data-en="{esc(n)} · {esc(title)}" data-fa="{esc(n)} · {esc(fa_title)}">{esc(n)} · {esc(title)}</option>' for n,title,fa_title in figure_options)+'</select><button type="button" id="figure-mode" aria-pressed="false">'+pair('Images only','فقط تصاویر')+'</button></div>'
        content=content.replace('<figure id=',toolbar+'<figure id=',1)
    path.write_text(content,encoding='utf-8')

# Every card gets an image tied to its actual source figure.
path=OUT/'index.html';content=path.read_text(encoding='utf-8')
def cover_card(match):
    card=match[0]
    destination=re.search(r'class="btn" href="([^"]+)"',card)
    if not destination:return card
    identity=destination[1].replace('.html','')
    if identity not in view_manifest:return card
    card=re.sub(r'<img class="cover"[^>]*>','',card)
    view=view_manifest[identity]
    preview='<a class="card-image" href="'+identity+'.html#fig-'+esc(view['cover_figure'])+'"><img class="cover" loading="lazy" src="'+view['cover']+'" alt="'+esc(next(x['title'] for x in inventory if x['id']==identity))+' · original paper visual"><span>'+pair('Explore the original visual ↗','مشاهده تصویر اصلی ↗')+'</span></a>'
    return card.replace('<h3>',preview+'<h3>',1)
content=re.sub(r'<article class="card"[^>]*>.*?</article>',cover_card,content,flags=re.S)
path.write_text(content,encoding='utf-8')
