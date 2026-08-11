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

for slug in new_articles:
    f = posts_dir / f"{slug}.md"
    if not f.exists():
        continue
    text = f.read_text(encoding='utf-8')
    
    # Remove all <span aria-hidden="true" ...>...</span> chains that are WeChat a11y junk
    # These are continuously nested with no actual content
    text = re.sub(r'<span aria-hidden="true"[^>]*>', '', text)
    
    # Remove leftover </span> closers that are now empty
    # Do this a few times to clean up the nesting
    for _ in range(5):
        text = re.sub(r'<span>\s*</span>', '', text)
        text = re.sub(r'<span>\s*(\n\s*)*</span>', '', text)
    
    # Clean extra blank lines from span removal
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove trailing commas/colons/periods that are on their own line after cleanup
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just WeChat leftover characters
        if stripped in ('：', '，', '。', ':', ',', '.', '',):
            continue
        # Skip empty span wrappers
        if stripped == '</body>':
            continue
        cleaned.append(line)
    
    text = '\n'.join(cleaned)
    text = text.rstrip() + '\n'
    
    f.write_text(text, encoding='utf-8')
    print(f"Cleaned: {slug}")
