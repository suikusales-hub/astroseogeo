import olefile
from pathlib import Path

SRC = Path(r"E:\CodexChatGPTMigrated\SEOGEO\.hermes\desktop-attachments\新建 DOC 文档 (2).doc")
SLUG = "2026-independent-site-b2b-b2c-difference"
DST = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public\images\posts") / SLUG
DST.mkdir(parents=True, exist_ok=True)

ole = olefile.OleFileIO(SRC)

# List all entries to find images
for entry in ole.listdir():
    path = "/".join(entry)
    size = ole.get_size(entry)
    print(f"  {path} ({size} bytes)")

# Extract any PNG/JPG from the OLE streams
# In .doc files, images are often in the Data stream or as ObjectPool entries
count = 0
for entry in ole.listdir():
    path = "/".join(entry)
    try:
        data = ole.openstream(entry).read()
        # Check for PNG
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            ext = 'png'
            count += 1
            fname = f"image-{count:03d}.{ext}"
            (DST / fname).write_bytes(data)
            print(f"  PNG found in {path} -> {fname} ({len(data)} bytes)")
        # Check for JPEG
        elif data[:2] == b'\xff\xd8':
            ext = 'jpg'
            count += 1
            fname = f"image-{count:03d}.{ext}"
            (DST / fname).write_bytes(data)
            print(f"  JPEG found in {path} -> {fname} ({len(data)} bytes)")
    except:
        pass

# Also scan the Data stream for embedded images
if ole.exists('Data'):
    data = ole.openstream('Data').read()
    pos = 0
    while pos < len(data) - 8:
        if data[pos:pos+8] == b'\x89PNG\r\n\x1a\n':
            # Find end of PNG (IEND chunk)
            end = data.find(b'IEND\xaeB`\x82', pos)
            if end > 0:
                png_data = data[pos:end+8]
                count += 1
                fname = f"image-{count:03d}.png"
                (DST / fname).write_bytes(png_data)
                print(f"  PNG in Data stream at offset {pos} -> {fname} ({len(png_data)} bytes)")
                pos = end + 8
                continue
        elif data[pos:pos+2] == b'\xff\xd8':
            # Find end of JPEG
            end = data.find(b'\xff\xd9', pos + 2)
            if end > 0:
                jpg_data = data[pos:end+2]
                count += 1
                fname = f"image-{count:03d}.jpg"
                (DST / fname).write_bytes(jpg_data)
                print(f"  JPEG in Data stream at offset {pos} -> {fname} ({len(jpg_data)} bytes)")
                pos = end + 2
                continue
        pos += 1

print(f"\nTotal images extracted: {count}")
ole.close()
