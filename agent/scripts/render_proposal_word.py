"""Use the packaged render_docx.py PNG pipeline with native Word PDF conversion.

Windows fallback when LibreOffice is absent. No managed skill files are modified.
Run with bundled Python; pass the ordinary render_docx.py CLI arguments.
"""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[2]
SKILL = Path('C:/Users/asus/.codex/plugins/cache/openai-primary-runtime/documents/26.1112.11217/skills/documents')
work = ROOT / 'reports/proposals/render_tmp'
work.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(work)
spec = importlib.util.spec_from_file_location('packaged_render_docx', SKILL / 'render_docx.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

def word_convert(doc_path, user_profile, convert_tmp_dir, stem, verbose):
    output = Path(convert_tmp_dir) / (stem + '.pdf')
    staging_doc = Path(convert_tmp_dir) / (stem + '.docx')
    shutil.copyfile(doc_path, staging_doc)
    proc = subprocess.run([
        'powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
        '-File', str(ROOT / 'agent/scripts/export_docx_word.ps1'),
        '-InputPath', str(staging_doc.resolve()), '-OutputPath', str(output.resolve())
    ], capture_output=True, text=True, timeout=150)
    log = proc.stdout + proc.stderr
    if proc.returncode or not output.exists():
        raise RuntimeError('Native Word PDF export failed: ' + log)
    print(log.strip())
    return str(output), log

renderer.convert_to_pdf = word_convert
if __name__ == '__main__':
    renderer.main()
