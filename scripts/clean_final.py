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

wechat_footer_texts = [
    "微信扫一扫可打开此内容",
    "使用完整服务",
    "视频", "小程序", "赞", "轻点两下取消赞",
    "在看", "轻点两下取消在看",
    "分享", "留言", "收藏", "听过",
]

for slug in new_articles:
    f = posts_dir / f"{slug}.md"
    if not f.exists():
        continue
    text = f.read_text(encoding='utf-8')

    # Remove lines containing WeChat footer phrases
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip WeChat footer lines
        if any(term in stripped for term in wechat_footer_texts):
            continue
        # Skip empty div wrappers from WeChat
        if stripped in ('<div>', '</div>', '<div id="unlogin_bottom_bar">', '</div>'):
            continue
        # Skip orphaned closing tags
        if stripped in ('</span>', '</body>', '</html>'):
            continue
        cleaned.append(line)
    
    text = '\n'.join(cleaned)
    
    # Clean up orphaned </div>* at the end
    text = re.sub(r'(</div>\s*){3,}$', lambda m: '\n' + '</div>\n</div>\n' + '</div>\n', text)
    
    # Remove triple+ blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # Trim trailing whitespace and ensure one trailing newline
    text = text.rstrip() + '\n'
    
    f.write_text(text, encoding='utf-8')
    print(f"Done: {slug}")
