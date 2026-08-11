import re
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")

new_articles = [
    "2026-ai-agent-583120",
    "2026-ai-codex-wordpress-0fe71a",
    "2026-ai-d9b2d8",
    "2026-ai-seo-geo-00aee5",
    "2026-article-d6ed50",
    "2026-seo-2dfcbe",
    "2026-seo-geo-ai-d0cb61",
]

def compact_spaces(s):
    """Replace multiple whitespace with single space, strip."""
    return re.sub(r"\s+", " ", s).strip()

for slug in new_articles:
    f = posts_dir / f"{slug}.md"
    if not f.exists():
        continue
    text = f.read_text(encoding='utf-8')
    parts = text.split('---')
    if len(parts) < 3:
        continue
    fm = parts[1]
    body = "---".join(parts[2:])
    
    # 1. Strip leading whitespace from every line (fix markdown code-block issue)
    lines = [line.lstrip() for line in body.split('\n')]
    body = '\n'.join(lines)
    
    # 2. Remove empty/invalid tags
    body = re.sub(r'<h2>\s*</h2>', '', body)
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'<section>\s*</section>', '', body)
    body = re.sub(r'<span text="">', '', body)
    body = re.sub(r'<span text>', '', body)
    body = re.sub(r'<section nodeleaf="">', '', body)
    
    # 3. Compact internal whitespace inside <p>, <b>, <h2> tags
    def compact_p(m):
        return '<p>' + compact_spaces(m.group(1)) + '</p>'
    body = re.sub(r'<p>(.*?)</p>', compact_p, body, flags=re.DOTALL)
    
    def compact_b(m):
        return '<b>' + compact_spaces(m.group(1)) + '</b>'
    body = re.sub(r'<b>(.*?)</b>', compact_b, body, flags=re.DOTALL)
    
    def compact_h2(m):
        return '<h2>' + compact_spaces(m.group(1)) + '</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', compact_h2, body, flags=re.DOTALL)
    
    # 4. Remove empty lines, merge consecutive blank lines
    lines = [line for line in body.split('\n') if line.strip()]
    body = '\n'.join(lines)
    body = re.sub(r'\n{3,}', '\n\n', body)
    
    new_text = '---' + fm + '---\n\n' + body.strip()
    f.write_text(new_text, encoding='utf-8')
    print(f"FIXED: {slug} [{len(body)} chars]")
