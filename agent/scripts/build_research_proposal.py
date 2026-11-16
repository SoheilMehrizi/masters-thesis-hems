"""Create the Persian three-page proposal from the agreed P0 design.

Run with the bundled document Python. Render and inspect every page before delivery.
References are checked against local full-text article extractions, not inferred
from abbreviated titles in historical planning notes.
"""
from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'docs/proposals/HEMS_Proposal_FA.docx'
FONT = 'Vazirmatn'
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(1.55), Cm(1.55)
sec.left_margin = sec.right_margin = Cm(1.75)
sec.header_distance = sec.footer_distance = Cm(0.65)

def flag(parent, name, value='1'):
    node = parent.find(qn('w:'+name))
    if node is None:
        node = OxmlElement('w:'+name)
        parent.append(node)
    node.set(qn('w:val'), value)
    return node

def font_run(run, size=11.2, bold=False, rtl=True):
    run.font.name = FONT if rtl else 'Arial'
    run.font.size, run.font.bold = Pt(size), bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    pr = run._element.get_or_add_rPr()
    for kind in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
        pr.rFonts.set(qn('w:'+kind), FONT if rtl else 'Arial')
    flag(pr, 'rtl', '1' if rtl else '0')
    flag(pr, 'szCs', str(round(size*2)))
    flag(pr, 'bCs', '1' if bold else '0')
    lang = flag(pr, 'lang', 'fa-IR' if rtl else 'en-US')
    lang.set(qn('w:bidi'), 'fa-IR')
    return run

def text_runs(p, text, size=11.2, bold=False):
    # Latin runs get explicit LTR formatting inside Persian RTL paragraphs.
    for part in re.split(r'([A-Za-z][A-Za-z0-9 /+−().–-]*[A-Za-z0-9)]|\[[0-9، ,–-]+\])', text):
        if part:
            font_run(p.add_run(part), size, bold, not bool(re.match(r'[A-Za-z\[]', part)))

def paragraph(text='', style=None, size=11.2, bold=False, after=4, before=0, keep=False):
    p = doc.add_paragraph(style=style)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    flag(p._p.get_or_add_pPr(), 'bidi')
    flag(p._p.get_or_add_pPr(), 'jc', 'start')
    f = p.paragraph_format
    f.space_after, f.space_before = Pt(after), Pt(before)
    f.line_spacing = Pt(16.2)
    f.keep_with_next = keep
    f.widow_control = True
    text_runs(p, text, size, bold)
    return p

def heading(text):
    p = paragraph(text, 'Heading 1', 12, True, 3, 7, True)
    p.paragraph_format.line_spacing = Pt(17)
    return p

for sty in ['Normal', 'Title', 'Heading 1', 'Heading 2']:
    st = doc.styles[sty]
    st.font.name, st.font.color.rgb = FONT, RGBColor(0, 0, 0)
    flag(st.element.get_or_add_pPr(), 'bidi')
    rpr = st.element.get_or_add_rPr()
    for kind in ['ascii','hAnsi','eastAsia','cs']:
        rpr.rFonts.set(qn('w:'+kind), FONT)
    flag(rpr, 'szCs', '21')
    borders = st.element.get_or_add_pPr().find(qn('w:pBdr'))
    if borders is not None:
        borders.getparent().remove(borders)

doc.core_properties.title = 'تشخیص علّی و سازگاری هدایت‌شده با دوقلوی دیجیتال برای مدیریت انرژی خانگی مبتنی بر ترجیحات با عامل‌های مدل زبانی بزرگ'
doc.core_properties.author = 'سهیل مهریزی و ساناز محمدی'
doc.core_properties.subject = 'پروپوزال پژوهشی بر اساس طراحی مصوب P0'
doc.core_properties.language = 'fa-IR'

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
flag(footer._p.get_or_add_pPr(), 'bidi')
font_run(footer.add_run('سهیل مهریزی و ساناز محمدی  |  صفحه '), 8)
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)

# PAGE 1: purpose, questions, hypotheses and scope.
p = paragraph('تشخیص علّی و سازگاری هدایت‌شده با دوقلوی دیجیتال برای مدیریت انرژی خانگی مبتنی بر ترجیحات با عامل‌های مدل زبانی بزرگ', 'Title', 15, True, 6, keep=True)
p.paragraph_format.line_spacing = Pt(22)
paragraph('پیشنهاد پژوهش  |  سهیل مهریزی و ساناز محمدی', size=9.5, after=7)

heading('مسئله و هدف پژوهش')
paragraph('در این پژوهش بررسی می‌کنیم آیا تشخیص علتِ برآورده‌نشدن خواسته‌های ساکن و آزمودن مداخلات در دوقلوی دیجیتال، انتخاب اقدام اصلاحی را نسبت به بازبرنامه‌ریزی بدون تشخیص بهبود می‌دهد. نشانه‌ای مانند خروج دما از محدوده یا خطر نرسیدن شارژ خودرو می‌تواند از خطای پیش‌بینی، افت عملکرد تجهیز، خطای مدل یا شکست هماهنگی ناشی شود؛ بنابراین یک نشانه را معادل یک علت قطعی نمی‌گیریم. تغییر تأییدشده ترجیح ساکن نیز رویدادی مشروع است، نه خرابی تجهیز.')
paragraph('پیشینه منتخب، سازگاری ترجیحات با یادگیری تقویتی تقویت‌شده با مدل زبانی [1]، زمان‌بندی خانگی عامل‌محور [7]، تشخیص علّی و بیزی [2، 3]، تشخیص مبتنی بر قواعد [5]، دوقلوی تطبیقی STAR [4] و بررسی و اصلاح قیود در DARC [6] را پوشش می‌دهد. سهم پیشنهادی ما آزمون یک زنجیره تشخیص علّی پویا، ارزیابی مداخله و تأیید بازیابی واقعی است؛ برتری یا تقدم این ترکیب هنوز نتیجه اثبات‌شده نیست.')

heading('پرسش‌های پژوهش و فرضیه‌ها')
paragraph('پرسش اصلی این است که آیا تشخیص علّی همراه با انتخاب مداخله آزموده‌شده در دوقلو، نرخ بازیابی تأییدشده الزامات را در مقایسه با برنامه‌ریز زبانیِ بدون تشخیص افزایش می‌دهد؟ پرسش‌های مکمل، ارزش افزوده مدل علّی نسبت به تشخیص بیزی و قاعده‌ای، نقش آزمون مداخله در دوقلو، فایده پروب انتخابی نسبت به تشخیص غیرفعال، و مداخله چندمرحله‌ای نسبت به تک‌اقدام را بررسی می‌کنند.')
paragraph('فرضیه اصلی، مثبت‌بودن اختلاف نرخ بازیابی سامانه کامل و برنامه‌ریز بدون تشخیص است. فرضیه‌های ثانویه، بهبود پیامد مداخلات با ارزیابی دوقلو و برنامه‌های شرطی چندمرحله‌ای و بهبود تشخیص یا بازیابی با پروب انتخابی را می‌آزمایند؛ سربار پروب جداگانه گزارش می‌شود. حداقل اثر معنادار عملی، تعداد تکرارها و آستانه‌ها از پایلوت مستقل تعیین خواهند شد؛ درصد بهبود از پیش ادعا نمی‌کنیم.')

heading('دامنه و قرارداد ترجیحات')
paragraph('مطالعه اولیه یک خانه در CityLearn 3.2.0 با داده Alameda، سامانه گرمایش و سرمایش، شارژ خودروی برقی، پنل خورشیدی، باتری ثابت و بارهای ثابت است. ورودی زبان طبیعی به قیود سخت و اولویت‌های نرم تبدیل و تأیید می‌شود. در نمونه مصوب، هدف دما ۲۳ درجه سلسیوس و باند سخت هنگام حضور ۲۲٫۵ تا ۲۳٫۵ درجه است؛ زمان خروج و هدف شارژ خودرو باید روشن و تأیید شوند. نقض باند از شروع بازه فعال شمرده می‌شود و مهلت ارفاق ضمنی نداریم. در نبود اولویت دیگر، هزینه برق کمینه می‌شود؛ تعارض قیود گزارش و تغییر الزام سخت تنها با اجازه ساکن انجام می‌شود.')

doc.add_page_break()

# PAGE 2: operational methodology and experiment structure.
heading('روش پیشنهادی و تقسیم مسئولیت‌ها')
paragraph('معماری اصلی سلسله‌مراتبی است: عامل هماهنگ‌کننده و نقش‌های تخصصیِ تفسیر ترجیح، تشخیص و انتخاب مداخله از ابزارها استفاده می‌کنند. مدل علّی ساختاری پویا، روابط زمان‌مند علت و مشاهده و فرض‌های خود را صریح می‌کند؛ عامل‌ها می‌توانند چند علت رقیب، علت ناشناخته یا امتناع از تشخیص اعلام کنند. وجود گراف به‌تنهایی شناسایی‌پذیری علّی را اثبات نمی‌کند؛ مکانیزم‌ها، استنباط و عدم‌قطعیت باید مشخص و اعتبارسنجی شوند.')
paragraph('دوقلوی مرجع، پارامترهای مدل سالم را ثابت نگه می‌دارد و دوقلوی عملیاتی نسخه‌بندی می‌شود. حالت هر دو از مشاهدات و تاریخچه مجاز تخمین زده می‌شود؛ حالت پنهان سامانه فیزیکی یا پارامتر واقعی خرابی به آن‌ها کپی نمی‌شود. رول‌اوت فرضی از اجرای واقعی جداست. برازش و آزمون نامزد دوقلوی عملیاتی خودکار است، اما ارتقای نسخه فعال در مرحله اولیه به تأیید نیاز دارد و امکان بازگشت باید حفظ شود.')
paragraph('بهینه‌ساز با تقریب خطی یا خطی‌قطعه‌ای و LP/MILP، توازن توان، حدود تجهیزات و انرژی، راندمان، آسایش و هدف شارژ در موعد را مدل می‌کند. در افق لغزان تنها بازه بعدی اجرا می‌شود؛ افق یا شرط انتهایی باید دسترس‌پذیری هدف خودرو را پوشش دهد. اعتبارسنج مستقل، قیود، اختیار، تازگی و نسخه‌ها را پیش از هر گام کنترل می‌کند. پایش قطعی هر بازه و تشخیص زبانی بر اثر نقض، خطر پیش‌بینی‌شده، باقیمانده مهم یا شکست اجرا فعال می‌شود. برنامه اصلاحی می‌تواند شرطی و چندمرحله‌ای باشد و پس از هر گام با مشاهده واقعی بررسی شود.')
paragraph('زمان‌بندی معتبر گرمایش و سرمایش، خودرو و باتری در حدود ثابت خودکار است. پروبِ تغییردهنده عملکرد تجهیز فقط زیر سیاست محدودِ صریحاً مصوبِ دامنه، مدت و بودجه مجاز خواهد بود. شکست عامل، حل‌گر یا اعتبارسنج، کنترل پشتیبان قطعی و معتبر و گزارش شکست را فعال می‌کند؛ راه‌حل قدیمی فقط در صورت اعتبار جاری بازاستفاده می‌شود. پیش‌بینی موفق دوقلو یا اجرای پشتیبان، تضمین بازیابی نیست.')

heading('سناریوها و جداسازی اطلاعات')
paragraph('پنج خانواده شامل تغییر صریح ترجیح، خطای پیش‌بینی خورشید و دمای بیرون و بار ثابت، خطای مدل حرارتی یا راندمان باتری در دوقلوی عملیاتی، افت تجهیز، و تأخیر یا فقدان تحویل برنامه و نسخه کهنه است. افت تجهیز از ابتدا کاهش ظرفیت گرمایش و سرمایش، توان شارژ خودرو، توان تخلیه باتری، تولید خورشیدی در هوای یکسان، ظرفیت انرژی باتری و راندمان شارژ و تخلیه آن را پوشش می‌دهد. افت ظرفیت، انرژی ذخیره‌شده را حفظ می‌کند و فقط در حالت سازگار با ظرفیت جدید تزریق می‌شود؛ حذف یا ایجاد پنهانی انرژی مجاز نیست.')
paragraph('ابتدا کنترل سالم و علت‌های منفرد، سپس هم‌زمانی‌های منتخب و زنجیره‌ها آزموده می‌شوند؛ از جمله افت گرمایش و سرمایش با خطای پیش‌بینی خورشید، افت ظرفیت باتری با خطای مدل راندمان، و خروج زودتر خودرو با تأخیر برنامه. زنجیره اثر افت گرمایش و سرمایش بر خطر شارژ خودرو، مشروط به اعتبارسنجی حد برق مشترک است. تغییرات ابتدا ناگهانی و ماندگار و سپس منتخبِ تدریجی و موقت خواهند بود. حالت‌های قابل‌بازیابی و ناممکن با کنترل متناظر بررسی می‌شوند؛ علامت پایین‌دستی، علت مستقل دیگری محسوب نمی‌شود.')
paragraph('برچسب و شدت و زمان تزریق، پارامتر حقیقی افت، آینده تحقق‌یافته و نتیجه امکان‌سنجی ممتاز فقط نزد ارزیاب می‌ماند. عامل‌ها از مخزن شواهد زمان‌دار با نماهای نقش‌محور، تاریخچه اخیر محدود و بازیابی محدود گذشته استفاده می‌کنند. برنامه حضور و اتصال آینده، اظهار ساکن است و ابهام آن پرسیده می‌شود. ابتدا سنجه‌های دقیق مجاز و سپس نویز، فقدان و تأخیر منتخب آزموده می‌شوند؛ کانال‌های ناموجود فرض نمی‌شوند.')

doc.add_page_break()

# PAGE 3: comparisons, metrics, protocol and selected bibliography.
heading('خطوط مبنا و آزمون حذف مؤلفه')
paragraph('همه مقایسه‌ها روی سناریوها و شواهد همسان، حدود تجهیز و اختیار ثبت‌شده انجام می‌شوند. پیوندهای زیر منشأ اقتباس را نشان می‌دهند، نه ادعای بازتولید دقیق مقاله؛ تغییرات لازم برای خانه، خودرو و باتری مستند خواهند شد.', size=9.8, after=4)

rows = [
    ('روش مقایسه', 'نقش و ارتباط با مقالات'),
    ('کنترل قاعده‌ای و بهینه‌ساز تنها', 'دو مرجع مهندسی؛ بدون زنجیره تشخیص زبانی. DARC [6] مرجع بررسی قیود است، نه پیاده‌سازی عین این مبناها.'),
    ('بازبرنامه‌ریزی زبانی بدون تشخیص', 'مرجع اصلی فرضیه؛ الهام معماری از HEMS عامل‌محور [7]، با حذف تشخیص علّی و زمان‌بندی عددی مشترک.'),
    ('تشخیص بیزی و تشخیص قاعده‌ای', 'دو مبنای اقتباسی با جایگزینی موتور تشخیص؛ منابع بیزی و علّی [2، 3] و قواعد عامل‌محور AFDD [5].'),
]
table = doc.add_table(rows=0, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
table.columns[0].width, table.columns[1].width = Cm(5.1), Cm(12.4)
pr = table._tbl.tblPr
flag(pr, 'bidiVisual')
borders = OxmlElement('w:tblBorders')
for edge in ['top','left','bottom','right','insideH','insideV']:
    e = OxmlElement('w:'+edge)
    e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:color'),'D9D9D9')
    borders.append(e)
pr.append(borders)
margins = OxmlElement('w:tblCellMar')
for edge in ['top','bottom','left','right']:
    e=OxmlElement('w:'+edge); e.set(qn('w:w'),'65'); e.set(qn('w:type'),'dxa'); margins.append(e)
pr.append(margins)
for i, data in enumerate(rows):
    row = table.add_row()
    flag(row._tr.get_or_add_trPr(),'cantSplit')
    if i == 0:
        flag(row._tr.get_or_add_trPr(),'tblHeader')
    for j, text in enumerate(data):
        cell = row.cells[j]
        cell.width = Cm(5.1 if j == 0 else 12.4)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        shade=OxmlElement('w:shd'); shade.set(qn('w:fill'), 'E9EDF1' if i==0 else ('F6F7F8' if i%2==0 else 'FFFFFF')); cell._tc.get_or_add_tcPr().append(shade)
        p=cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
        flag(p._p.get_or_add_pPr(),'bidi')
        flag(p._p.get_or_add_pPr(),'jc','start')
        p.paragraph_format.space_after=Pt(1); p.paragraph_format.line_spacing=Pt(13)
        text_runs(p,text,9.5,i==0)
paragraph('حذف‌ها شامل بدون SCM، بدون رتبه‌بندی مداخله با رول‌اوت دوقلو، تشخیص غیرفعال، و تک‌اقدام است؛ مدل پیش‌بینی بهینه‌ساز در حذف دوقلو حفظ می‌شود. LA-UPAHEM [1] مرجع سازگاری ترجیحات است و بازتولید آن مبنای اصلی مصوب نیست. مقایسه توپولوژی‌ها و Jev پس از هسته، مکمل‌اند.', size=9.5, after=3)

heading('معیار موفقیت و پروتکل ارزیابی')
paragraph('مجموعه اصلی از حالت مشترکِ ازپیش ناقض ولی قابل‌بازیابی شروع می‌شود؛ پیشگیری فعال و مدیریت ناممکنی جداگانه سنجیده می‌شوند. موفقیت مستلزم بازگشت مشاهده‌شده تا مهلت ثابت، پایداری در پنجره تأیید و تحقق هدف خودرو در موعد مربوط است. نقض ایمنی یا تغییر غیرمجاز موفقیت را باطل می‌کند؛ توافق بر کاهش الزام، بازیابی الزام اصلی نیست. شکست‌ها و اتمام زمان از مخرج حذف نمی‌شوند.', size=9.7, after=3)
p=paragraph('نرخ بازیابی تأییدشده = تعداد اپیزودهای موفق ÷ کل اپیزودهای واجد شرایطِ تخصیص‌یافته', size=10, bold=True, after=4)
p.alignment=WD_ALIGN_PARAGRAPH.CENTER
paragraph('معیارهای مکمل: نقض آسایش بر حسب درجه‌ساعت و مدت نقض، کسری انرژی خودرو در موعد، زمان بازیابی با لحاظ عدم‌بازیابی، تشخیص چندعلتی و ناشناخته و امتناع، مداخلات اجتناب‌پذیر، هزینه و انرژی، فراخوان و توکن، زمان حل و رول‌اوت و انتظار تأیید انسانی. برازش، پایلوت و آزمون نهایی از نظر بازه و بذر جدا می‌شوند؛ شدت‌ها و ترکیب‌های منتخب کنار گذاشته می‌شوند. اختلاف‌های زوجی با فاصله عدم‌قطعیت ۹۵٪ و تفکیک خانواده و شدت گزارش می‌شوند؛ هم‌بستگی بازه‌های آب‌وهوا لحاظ می‌شود. حمایت از فرضیه اصلی نیازمند اثر مثبت با تحلیل ازپیش‌تعیین‌شده است؛ اندازه اثر عملی، تکرارها و آزمون آماری از پایلوت مستقل نهایی می‌شوند.', size=9.7, after=3)
paragraph('پیش از آزمون، شناسه داده و کد، نسخه مدل‌ها و ابزارها، پرامپت، شکاف‌های زمانی، بودجه، شدت و زمان تزریق، فرمول‌ها و سیاست تأیید در مانیفست ثابت ثبت می‌شوند. تنظیم پس از نتیجه، نسخه مطالعه جدید می‌خواهد. دامنه تک‌خانه، داده مصنوعی تعرفه و خودرو، و اعتبارسنجی ناتمام تقویم و کانال‌ها محدودیت‌اند. فعلاً P0 مصوب و P1.1 تا P1.3 دارای شواهد راه‌اندازی است؛ گام بعد P1.4، بازتولید اندازه‌گذاری سالانه است و نتایج روش پیشنهادی هنوز تولید نشده‌اند.', size=9.4, after=3)

heading('منابع منتخب')
references = [
    '[1] Du X et al. (2026). Adaptive home energy management to self-motivated user preferences via iterative LLM-augmented reinforcement learning. Applied Energy, 415, 127976. doi:10.1016/j.apenergy.2026.127976',
    '[2] Huang J et al. (2024). An entropy-based causality framework for cross-level faults diagnosis and isolation in building HVAC systems. Energy and Buildings, 317, 114378. doi:10.1016/j.enbuild.2024.114378',
    '[3] Mosteiro-Romero M et al. (2026). Whole building HVAC diagnostic Bayesian networks for comfort-related fault detection and diagnosis: Application, evaluation and operational testing. Building and Environment, 305, 115265. doi:10.1016/j.buildenv.2026.115265',
    '[4] Jia C et al. (2026). A data-driven iterative digital twin framework for dynamic building energy performance: Integrating virtual sensing and anomaly diagnosis. doi:10.1016/j.enbuild.2026.117763',
    '[5] Li J et al. (2026). Agentic fault detection and diagnosis for building HVAC systems using AI agent, ontology, and diagnosis rules. Building and Environment, 289, 114104. doi:10.1016/j.buildenv.2025.114104',
    '[6] Li B et al. (2026). DARC: A Constraint-Diagnostic LLM Agent Framework for Day-Ahead Dispatch of Campus-Level Integrated Energy Microgrids Under Natural-Language Preferences and Forecast Uncertainty. Energies, 19, 3817. doi:10.3390/en19163817',
    '[7] El Makroum R et al. (2026). Agentic AI home energy management system: A large language model framework for residential load scheduling. Results in Engineering, 29, 109857. doi:10.1016/j.rineng.2026.109857',
]
for ref in references:
    p=doc.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    flag(p._p.get_or_add_pPr(),'bidi','0')
    p.paragraph_format.space_after=Pt(2)
    p.paragraph_format.line_spacing=Pt(10.2)
    p.paragraph_format.widow_control=True
    font_run(p.add_run(ref),8,False,False)

OUTPUT.parent.mkdir(parents=True,exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)
