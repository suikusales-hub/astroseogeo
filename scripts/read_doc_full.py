import olefile, re
from pathlib import Path

SRC = Path(r"E:\CodexChatGPTMigrated\SEOGEO\.hermes\desktop-attachments\新建 DOC 文档 (2)-2.doc")
ole = olefile.OleFileIO(SRC)
wd = ole.openstream('WordDocument').read()
text = wd.decode('utf-16-le', errors='ignore')

# Extract all readable CJK+ASCII runs
lines = re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffefa-zA-Z0-9\s.,;:!?()（）【】《》\"\'\-+/\|=@#$%^&*\[\]{}_~\r\n%]+', text)

# Filter to meaningful lines
content_lines = []
for line in lines:
    stripped = line.strip()
    if len(stripped) > 2:
        content_lines.append(stripped)

full_text = '\n'.join(content_lines)

# Save to temp file for reading
out = Path(r"E:\CodexChatGPTMigrated\SEOGEO\tmp\doc_full_text.txt")
out.parent.mkdir(exist_ok=True)
out.write_text(full_text, encoding='utf-8')
print(f"Extracted {len(full_text)} chars, {len(content_lines)} lines")
print("First 500 chars:")
print(full_text[:500])
ole.close()
