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

# WeChat footer junk patterns (ordered: longest match first)
wechat_junk = [
    r'<span>预览时标签不可点</span>',
    r'<span>微信扫一扫</span>\s*<span>关注该公众号</span>',
    r'<span>知道了</span>',
    r'<span>微信扫一扫</span>\s*<span>使用小程序</span>',
    r'<span>取消</span>\s*<span>允许</span>',
    r'<span>取消</span>\s*<span>允许</span>\s*<span>取消</span>\s*<span>允许</span>',
    r'<span>× 分析</span>',
    r'<span>配图</span>',
    r'<span>微信扫一扫可打开此内容，</span>\s*<span>使用完整服务</span>',
    r'<span>视频</span>\s*<span>小程序</span>\s*<span>赞</span>.*?</span>',
    r'<span>轻点两下取消赞</span>',
    r'<span>在看</span>',
    r'<span>轻点两下取消在看</span>',
    r'<span>分享</span>',
    r'<span>留言</span>',
    r'<span>收藏</span>',
    r'<span>听过</span>',
    r'<span>\s*:\s*</span>',
]

for slug in new_articles:
    f = posts_dir / f"{slug}.md"
    if not f.exists():
        continue
    text = f.read_text(encoding='utf-8')
    
    count = 0
    for pattern in wechat_junk:
        new_text = re.sub(pattern, '', text, flags=re.DOTALL)
        if new_text != text:
            count += len(re.findall(pattern, text, flags=re.DOTALL))
            text = new_text
    
    # Also remove lines that are just commas or emoji tags
    text = re.sub(r'<p>\s*</p>', '', text)
    text = re.sub(r'<p>\s*[：:，,。\.\s]+\s*</p>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    if count:
        f.write_text(text, encoding='utf-8')
        print(f"{slug}: removed {count} junk fragments")
    else:
        print(f"{slug}: nothing to clean")
