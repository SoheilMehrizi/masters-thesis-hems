"""Generate editable SVG sources for the proposal's two engineering diagrams.

Rasterize with the bundled sharp library for Word insertion. Persian remains
Unicode text in the SVG sources; no claims of implemented components are made.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'docs/proposals/assets'
ASSETS.mkdir(parents=True, exist_ok=True)

class Diagram:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
          '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 Z" fill="#314b61"/></marker></defs>',
          f'<rect width="{width}" height="{height}" fill="white"/>']
    def text(self,x,y,lines,size=32,bold=False,color='#142a3a',gap=44):
        for i,line in enumerate(lines):
            self.parts.append(f'<text x="{x}" y="{y+i*gap}" text-anchor="middle" direction="rtl" unicode-bidi="plaintext" font-family="Vazirmatn, Tahoma, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(line)}</text>')
    def box(self,x,y,w,h,lines,fill='#f2f6fa',stroke='#728aa0',size=32,gap=44,dashed=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2.5"'+(' stroke-dasharray="12 8"' if dashed else '')+'/>')
        self.text(x+w/2,y+h/2-(len(lines)-1)*gap/2+size*.34,lines,size,False,gap=gap)
    def arrow(self,points,dashed=False,color='#314b61'):
        self.parts.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="3.5" marker-end="url(#arrow)"'+(' stroke-dasharray="12 9"' if dashed else '')+'/>')
    def save(self,name):
        (ASSETS/name).write_text('\n'.join(self.parts+['</svg>']),encoding='utf-8')

d=Diagram(1800,1480)
d.box(100,40,680,125,['شواهد مجاز و پیش‌بینی‌های صادرشده','داده زمان‌دار و تاریخچه محدود'],fill='#edf4f8')
d.box(1020,40,680,125,['ساکن و ترجیحات تأییدشده','قیود سخت و اولویت‌های نرم'],fill='#edf4f8')
d.box(550,230,700,135,['هماهنگ‌کننده و عامل‌های زبانی','تفسیر درخواست و هدایت ابزارها'],fill='#e8f1f5',stroke='#325d78',size=35)
d.arrow([(440,165),(440,195),(720,195),(720,230)])
d.arrow([(1360,165),(1360,195),(1080,195),(1080,230)])
d.box(100,440,680,210,['ابزار دوقلوهای دیجیتال','مرجع با پارامترهای ثابت','عملیاتی نسخه‌بندی‌شده'],size=34)
d.box(1020,440,680,210,['ابزار مدل علّی ساختاری پویا','علت‌های رقیب و عدم‌قطعیت','ناشناخته یا امتناع از تشخیص'],size=34)
d.arrow([(720,365),(720,400),(440,400),(440,440)])
d.arrow([(1080,365),(1080,400),(1360,400),(1360,440)])
d.box(550,720,700,120,['تشخیص و طرح اصلاحی شرطی','انتخاب با شواهد و آزمون دوقلو'],fill='#e9f3ef',stroke='#4a7b65',size=34)
d.arrow([(440,650),(440,685),(720,685),(720,720)])
d.arrow([(1360,650),(1360,685),(1080,685),(1080,720)])
d.box(100,920,680,130,['بهینه‌ساز عددی مقید','افق لغزان و مدل خطی یا قطعه‌ای'],size=34)
d.box(1020,920,680,130,['اعتبارسنج مستقل','ایمنی و اختیار و تازگی نسخه'],fill='#f6f1e8',stroke='#9a8052',size=34)
d.arrow([(900,840),(900,880),(440,880),(440,920)])
d.arrow([(780,985),(1020,985)])
d.text(900,962,['برنامه'],size=28)
d.box(550,1150,700,130,['اجرای گام معتبر در خانه شبیه‌سازی‌شده','مشاهده و تأیید پیامد واقعی'],fill='#e9f3ef',stroke='#4a7b65',size=32)
d.arrow([(1360,1050),(1360,1100),(900,1100),(900,1150)])
d.arrow([(550,1215),(40,1215),(40,102),(100,102)],True,'#4a7b65')
d.text(295,1180,['بازخورد اجرای واقعی'],size=28,color='#355e4b')
d.box(100,1360,1600,90,['ارزیاب مستقل   حقیقت تزریق و آینده واقعی فقط برای ارزیابی'],fill='#faf6f3',stroke='#aa8270',size=31,dashed=True)
d.arrow([(900,1280),(900,1360)],True,'#aa8270')
d.save('method_architecture_fa.svg')

d=Diagram(1800,1580)
stages=[
 ('۱','تثبیت مسئله و طراحی پژوهش','P0 مصوب   پرسش‌ها و سناریوها و قراردادها'),
 ('۲','بازتولید و اعتبارسنجی شبیه‌ساز','گام بعد P1.4   اندازه‌گذاری و زمان و کانال‌ها'),
 ('۳','ساخت و اعتبارسنجی سناریوهای افت','کنترل سالم   علت منفرد   هم‌زمانی و زنجیره'),
 ('۴','پیاده‌سازی هسته روش','ترجیحات   بهینه‌ساز   دوقلوها   مدل علّی   اجرا'),
 ('۵','پیاده‌سازی مبناها و حذف مؤلفه‌ها','شواهد و سناریو و حدود اختیار قابل مقایسه'),
 ('۶','پایلوت مستقل و تثبیت مانیفست','شدت و آستانه و تکرار و بودجه پیش از آزمون'),
 ('۷','اجرای آزمون نهایی کنارگذاشته‌شده','بازیابی   پیشگیری   مدیریت ناممکنی'),
 ('۸','تحلیل زوجی و گزارش پژوهش','فاصله عدم‌قطعیت   شکست‌ها   محدودیت‌ها   بازتولید')
]
for i,(number,title,sub) in enumerate(stages):
    y=25+i*192
    fill='#e9f3ef' if i==0 else ('#edf3fa' if i==1 else '#f6f8fa')
    d.box(165,y,1450,145,[],fill=fill,stroke='#5c7b68' if i==0 else '#8296a8')
    d.text(850,y+54,[title],size=36,bold=True)
    d.text(850,y+109,[sub],size=29,color='#425666')
    d.parts.append(f'<circle cx="1665" cy="{y+72}" r="43" fill="#284f68"/>')
    d.text(1665,y+85,[number],size=37,bold=True,color='white')
    if i<7:
        d.arrow([(900,y+145),(900,y+186)])
d.save('research_workflow_fa.svg')
print('Generated two SVG diagram sources:',ASSETS)
