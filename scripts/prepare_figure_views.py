"""Extract figure views using source PDF image geometry; retain safe page fallbacks."""
import json,re,sys
from pathlib import Path
import pdfplumber
from PIL import Image,ImageDraw,ImageOps

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/literature'
inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
selected=set(sys.argv[1:])
manifest=json.loads((OUT/'figure-views.json').read_text(encoding='utf-8')) if selected else {}
manual_views={
    ('article-06','1'):(.06,.09,.94,.435),
    ('article-07','1'):(.06,.065,.94,.305),
    ('article-11','1'):(.52,.70,.94,.905),
    # Source-page crops checked against the Jev manuscript contact sheets.
    ('article-24','1'):(.09,.12,.94,.45),
    ('article-24','2'):(.10,.13,.93,.51),
    ('article-24','3'):(.10,.13,.93,.39),
    ('article-24','4'):(.10,.14,.93,.35),
    ('article-24','5'):(.10,.12,.93,.49),
    ('article-24','6'):(.10,.12,.93,.60),
    ('article-24','7'):(.10,.12,.93,.40),
    ('article-24','8'):(.10,.44,.93,.68),
    ('article-24','9'):(.10,.12,.93,.43),
    ('article-24','10'):(.10,.12,.93,.50),
    ('article-24','11'):(.10,.12,.93,.73),
    ('article-25','1'):(.50,.27,.94,.56),
    ('article-25','2'):(.10,.08,.93,.35),
    ('article-25','3'):(.10,.11,.93,.30),
    ('article-25','4'):(.50,.08,.94,.61),
    ('article-25','5'):(.10,.42,.50,.65),
    ('article-25','6'):(.50,.44,.94,.70),
    ('article-25','7'):(.10,.40,.94,.62),
    ('article-25','8'):(.50,.29,.94,.51),
    ('article-25','9'):(.50,.06,.94,.23),
    ('article-25','10'):(.10,.28,.50,.52),
    ('article-25','11'):(.10,.05,.94,.43),
    ('article-25','12'):(.10,.45,.94,.91),
    ('article-25','13'):(.10,.07,.94,.46),
    ('article-26','1'):(.10,.12,.94,.30),
    ('article-26','2'):(.10,.08,.50,.34),
    ('article-26','3'):(.50,.24,.94,.52),
    ('article-26','4'):(.50,.08,.94,.34),
    ('article-26','5'):(.10,.08,.94,.33),
    ('article-26','6'):(.10,.08,.94,.36),
    ('article-27','1'):(.10,.12,.93,.26),
    ('article-27','2'):(.10,.12,.93,.43),
    ('article-27','3'):(.10,.32,.93,.65),
    ('article-27','4'):(.10,.12,.93,.36),
    ('article-27','5'):(.10,.12,.93,.54),
    ('article-27','6'):(.10,.12,.93,.48),
    ('article-28','1'):(.10,.34,.50,.63),
    ('article-28','2'):(.50,.08,.94,.38),
    ('article-28','3'):(.10,.07,.94,.32),
    ('article-28','4'):(.10,.33,.94,.58),
    ('article-28','5'):(.10,.49,.50,.72),
    ('article-28','6'):(.50,.49,.94,.72),
    ('article-28','7'):(.50,.08,.94,.30),
    ('article-29','1'):(.10,.07,.50,.33),
    ('article-29','2'):(.10,.57,.50,.84),
    ('article-29','3'):(.10,.08,.94,.33),
    ('article-29','4'):(.50,.36,.94,.60),
    ('article-29','5'):(.50,.07,.94,.32),
    ('article-29','6'):(.10,.07,.94,.31),
}
cover_preferences={'article-16':'2','article-15':'3','article-25':'2','article-26':'1','article-27':'2','article-28':'2','article-29':'3'}
# Keep titles, axis labels and legends inside the focused Jev views. The initial
# tight bounds were compared against the full pages before adding this margin.
for key,box in list(manual_views.items()):
    if key[0] in {f'article-{n}' for n in range(24,30)}:
        manual_views[key]=(box[0],max(.04,box[1]-.055),box[2],min(.96,box[3]+.035))
manual_views[('article-25','10')]=(.10,.32,.50,.68)
manual_views[('article-25','12')]=(.10,.51,.94,.94)
manual_views[('article-28','5')]=(.10,.40,.50,.755)
manual_views[('article-28','6')]=(.50,.40,.94,.755)
manual_views[('article-29','2')]=(.10,.49,.50,.86)
def norm(value):return re.sub(r'[^a-z0-9]','',str(value).lower())
for item in inventory:
    identity=item['id'];folder='huang' if identity=='article-02' else identity
    if selected and identity not in selected:continue
    if identity in ('la-upahem','article-02'):
        count=9 if identity=='la-upahem' else 16
        views={str(n):dict(image=f'assets/{folder}/figure-{n}.png',kind='figure') for n in range(1,count+1)}
        cover='2' if identity=='la-upahem' else '7'
    else:
        record=json.loads((ROOT/'reports/literature/analyses'/f'{identity}.json').read_text(encoding='utf-8'))
        views={}
        with pdfplumber.open(item['path']) as pdf:
            for figure in record['figures']:
                number=str(figure['id']);page_num=figure['page'];page=pdf.pages[page_num-1]
                image_path=f'assets/{identity}/page-{page_num:02}.png'
                view=dict(image=image_path,kind='page',page=page_num)
                candidates=[x for x in page.images if (x['x1']-x['x0'])*(x['bottom']-x['top'])>page.width*page.height*.018 and x['top']>20]
                captions=page.search(r'(?:Fig(?:ure)?\.?)\s*([A-Z]?\s*\.?\s*\d+(?:\.\d+)?)\s*[\.:]',case=False) or []
                desired=norm(number.split('-continued')[0])
                matching=[c for c in captions if norm(c['groups'][0])==desired]
                box=None
                ranked=[]
                for caption in matching:
                    nearest=[im for im in candidates if 0<=caption['top']-im['bottom']<32 and min(im['x1'],caption['x1'])-max(im['x0'],caption['x0'])>min(im['x1']-im['x0'],caption['x1']-caption['x0'])*.25]
                    for anchor in nearest:
                        group=[anchor]; changed=True
                        while changed:
                            changed=False
                            for im in candidates:
                                if im in group or im['bottom']>caption['top']+2:continue
                                if any(max(0,max(im['x0'],g['x0'])-min(im['x1'],g['x1']))<20 and max(0,max(im['top'],g['top'])-min(im['bottom'],g['bottom']))<14 for g in group):
                                    group.append(im);changed=True
                        x0=min(i['x0'] for i in group);top=min(i['top'] for i in group);x1=max(i['x1'] for i in group);bottom=max(i['bottom'] for i in group)
                        ranked.append(((x1-x0)*(bottom-top),[x0,top,x1,bottom]))
                if ranked:box=max(ranked,key=lambda x:x[0])[1]
                if not box and ('abstract' in str(figure['caption']['en']).lower() or desired in ('ga','graphicalabstract')) and candidates:
                    biggest=max(candidates,key=lambda i:(i['x1']-i['x0'])*(i['bottom']-i['top']))
                    box=[biggest['x0'],biggest['top'],biggest['x1'],biggest['bottom']]
                # Mixed raster/vector graphics can have icons outside the image box.
                # Preserve their full source page unless a crop was visually checked.
                if len(page.rects)+len(page.curves)>60:box=None
                manual=manual_views.get((identity,number))
                if manual:box=[manual[0]*page.width,manual[1]*page.height,manual[2]*page.width,manual[3]*page.height]
                if box:
                    x0,top,x1,bottom=box
                    box=[max(0,x0-7),max(22,top-7),min(page.width,x1+7),min(page.height,bottom+7)]
                    src=Image.open(OUT/image_path);w,h=src.size
                    pixels=(round(box[0]/page.width*w),round(box[1]/page.height*h),round(box[2]/page.width*w),round(box[3]/page.height*h))
                    filename='view-'+re.sub(r'[^a-zA-Z0-9_-]','-',number)+'.png'
                    src.crop(pixels).save(OUT/'assets'/identity/filename)
                    view=dict(image=f'assets/{identity}/{filename}',kind='figure',page=page_num,source_box=box)
                views[number]=view
        cover=cover_preferences.get(identity) or next((str(f['id']) for f in record['figures'] if views[str(f['id'])]['kind']=='figure'),str(record['figures'][0]['id']))
    # Downsample a source-derived cover; do not stretch the original artwork.
    image=Image.open(OUT/views[cover]['image']).convert('RGB')
    image=ImageOps.contain(image,(900,600),method=Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(960,640),'#ffffff');canvas.paste(image,((960-image.width)//2,(640-image.height)//2))
    canvas.save(OUT/'assets'/folder/'card-cover.jpg',quality=90)
    manifest[identity]=dict(cover=f'assets/{folder}/card-cover.jpg',cover_figure=cover,views=views)
(OUT/'figure-views.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Figure views:',sum(v['kind']=='figure' for a in manifest.values() for v in a['views'].values()),'focused;',sum(v['kind']=='page' for a in manifest.values() for v in a['views'].values()),'source-page fallbacks')
# Contact sheets support checking covers and crops against the originals.
for group_start in range(0,len(inventory),8):
    sheet=Image.new('RGB',(1280,540),'#e1e6eb');draw=ImageDraw.Draw(sheet)
    for k,item in enumerate(inventory[group_start:group_start+8]):
        x=(k%4)*320;y=(k//4)*270
        image=Image.open(OUT/manifest[item['id']]['cover']);image.thumbnail((304,225));sheet.paste(image,(x+8,y+25));draw.text((x+9,y+7),item['id'],fill='#102437')
    sheet.save(ROOT/'reports/literature'/f'covers-{group_start//8}.jpg')
