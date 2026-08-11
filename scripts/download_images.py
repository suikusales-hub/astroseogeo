"""
Download ALL images from the 7 imported WeChat articles and update img src to local paths.
"""
import re
import os
import urllib.request
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
img_base = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public\images\posts")

new_articles = [
    "2026-ai-agent-583120",
    "2026-ai-codex-wordpress-0fe71a",
    "2026-ai-d9b2d8",
    "2026-ai-seo-geo-00aee5",
    "2026-article-d6ed50",
    "2026-seo-2dfcbe",
    "2026-seo-geo-ai-d0cb61",
]

total_downloaded = 0

for slug in new_articles:
    f = posts_dir / f"{slug}.md"
    if not f.exists():
        continue
    
    text = f.read_text(encoding='utf-8')
    
    # Find all external image URLs
    img_pattern = re.compile(r'<img[^>]*src="(https://[^"]+)"[^>]*>')
    matches = list(img_pattern.finditer(text))
    
    if not matches:
        print(f"{slug}: no external images")
        continue
    
    # Create image directory for this article
    post_img_dir = img_base / slug
    post_img_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = []
    for idx, m in enumerate(matches):
        url = m.group(1)
        
        # Determine extension
        ext = url.split('.')[-1].split('?')[0]
        if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif', 'svg'):
            # Check URL for format hints
            if 'wx_fmt=png' in url:
                ext = 'png'
            elif 'wx_fmt=jpeg' in url or 'wx_fmt=jpg' in url:
                ext = 'jpg'
            else:
                ext = 'jpg'  # default
        
        local_filename = f"image-{idx+1:03d}.{ext}"
        local_path = post_img_dir / local_filename
        local_ref = f"/images/posts/{slug}/{local_filename}"
        
        if local_path.exists():
            print(f"  [{slug}] SKIP (exists): {local_filename}")
        else:
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://mp.weixin.qq.com/'
                })
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                    local_path.write_bytes(data)
                print(f"  [{slug}] DOWNLOADED: {local_filename} ({len(data)} bytes)")
                total_downloaded += 1
            except Exception as e:
                print(f"  [{slug}] FAILED: {url[:60]}... -> {e}")
                continue
        
        downloaded.append((url, local_ref))
    
    # Replace URLs in text
    for url, local_ref in downloaded:
        text = text.replace(f'src="{url}"', f'src="{local_ref}"')
    
    f.write_text(text, encoding='utf-8')
    print(f"  [{slug}] Updated {len(downloaded)} images")

print(f"\nTotal downloaded: {total_downloaded} images")
