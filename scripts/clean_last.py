import re
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")

for f in posts_dir.glob("2026-*.md"):
    text = f.read_text(encoding='utf-8')
    old = len(text)

    text = re.sub(r'<button>\s*\x00\s*</button>\s*<button>\s*\S+\s*</button>', '', text)
    text = re.sub(r'<button>\s*×\s*</button>', '', text)
    text = re.sub(r'<button>\s*分析\s*</button>', '', text)
    text = re.sub(r'<div[^>]*id="js_jump_wx_qrcode_dialog"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<p>微信扫一扫可打开此内容[^<]*使用完整服务</p>', '', text)
    text = re.sub(r'<span>\s*× 分析\s*</span>', '', text)
    text = re.sub(r'(\n?</div>\n?){4,}$', '\n', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = text.rstrip() + '\n'

    if len(text) != old:
        f.write_text(text, encoding='utf-8')
        print(f"OK: {f.stem}")
