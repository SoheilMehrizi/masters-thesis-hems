"""Extract figure views using source PDF image geometry; retain safe page fallbacks."""
import json,re
from pathlib import Path
import pdfplumber
from PIL import Image,ImageDraw,ImageOps

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/literature'
inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
manifest={}
manual_views={
    ('article-06','1'):(.06,.09,.94,.435),
    ('article-07','1'):(.06,.065,.94,.305),
    ('article-11','1'):(.52,.70,.94,.905),
}
cover_preferences={'article-16':'2','article-15':'3'}
def norm(value):return re.sub(r'[^a-z0-9]','',str(value).lower())
for item in inventory:
    identity=item['id'];folder='huang' if identity=='article-02' else identity
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
