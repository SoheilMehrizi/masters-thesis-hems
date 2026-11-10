from pathlib import Path
import hashlib,json,zipfile

source=Path('C:/Users/asus/Documents/ChatGPT/Master Thesis 2/thermal_audit')
destination=Path(__file__).resolve().parent/'custom_alameda_complete.zip'
files=[]
for folder in ['custom_alameda','frozen_alameda']:
    files.extend(p for p in (source/folder).rglob('*') if p.is_file())
for name in ['manifest.json','environment.json','verification.json','requirements-lock.txt','README.md','demo.py','freeze_sizing.py','probe.py','extensions.py','verify.py','targeted.py','manifest.py','scan.py']:
    path=source/name
    if path.is_file():files.append(path)
manifest={'format':1,'files':{},'note':'Original files preserved byte-for-byte. frozen_alameda contains annual equipment-sizing references, not an independent calibrated thermal model.'}
with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for path in sorted(files):
        relative=path.relative_to(source).as_posix();payload=path.read_bytes()
        archive.writestr(relative,payload)
        manifest['files'][relative]={'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
    archive.writestr('PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    archive.writestr('PACKAGE_README_FA.txt',
        'تمام فایل‌های custom_alameda بدون تغییر در این بسته قرار دارند.\n'
        'frozen_alameda شامل داده‌ها و تنظیمات اندازه‌گذاری سالانه تجهیزات است. فایل کالیبراسیون مستقل دیگری در منبع یافت نشد؛ وزن LSTM همان مدل همراه دیتاست است.\n'
        'manifest.json و provenance.json اصلی حفظ شده‌اند؛ PACKAGE_MANIFEST.json هش فایل‌های داخل همین بسته را ثبت می‌کند.\n'
        'EV و تعرفه مصنوعی‌اند. برخی مسیرهای schema و manifest، مسیر اجرای اولیه هستند. demo.py هنگام اجرا مسیر اصلی سناریو را به محل استخراج فعلی تنظیم می‌کند؛ راهنمای وابستگی‌ها در README.md است.\n')
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    for name,metadata in manifest['files'].items():
        assert hashlib.sha256(archive.read(name)).hexdigest()==metadata['sha256'],name
    expected={p.relative_to(source).as_posix() for p in (source/'custom_alameda').rglob('*') if p.is_file()}
    assert expected.issubset(archive.namelist())
print(json.dumps({'archive':str(destination),'bytes':destination.stat().st_size,'source_files':len(files),'custom_alameda_files':len(expected),'verified':True},indent=2))
