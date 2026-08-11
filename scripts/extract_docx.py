import zipfile, os, shutil
from pathlib import Path

DOCX = r"E:\CodexChatGPTMigrated\SEOGEO\.hermes\desktop-attachments\新建 DOCX 文档 (2).docx"
SLUG = "2026-product-demand-validation"
DST = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public\images\posts") / SLUG
DST.mkdir(parents=True, exist_ok=True)

zf = zipfile.ZipFile(DOCX)
media_files = sorted([n for n in zf.namelist() if 'media' in n and 'image' in n])
print(f"Found {len(media_files)} images")

for idx, mf in enumerate(media_files):
    ext = os.path.splitext(mf)[1]
    fname = f"image-{idx+1:03d}{ext}"
    with zf.open(mf) as src:
        (DST / fname).write_bytes(src.read())
    print(f"  Extracted: {fname}")

zf.close()
