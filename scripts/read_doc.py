import olefile
from pathlib import Path

SRC = Path(r"E:\CodexChatGPTMigrated\SEOGEO\.hermes\desktop-attachments\新建 DOC 文档 (2).doc")
ole = olefile.OleFileIO(SRC)

# List all streams
for s in ole.listdir():
    print("/".join(s))

# Try to read the WordDocument stream
if ole.exists('WordDocument'):
    print(f"\nWordDocument size: {ole.get_size('WordDocument')}")
    
# Check for text in 1Table or 0Table
for tbl in ['1Table', '0Table']:
    if ole.exists(tbl):
        data = ole.openstream(tbl).read()
        print(f"\n{tbl}: {len(data)} bytes")
        # Try to decode as UTF-16LE
        print(data[:500])

ole.close()
