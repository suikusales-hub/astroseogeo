import re, urllib.request, os
from pathlib import Path

SRC = Path(r"E:\下载\SEO小平\谷歌新功能单独统计社媒视频内容的SEO数据.html")
POSTS = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
IMGS  = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public\images\posts")

html = SRC.read_text(encoding='utf-8', errors='replace')

# --- Extract metadata ---
title_m = re.search(r'property="og:title"\s*content="([^"]*)"', html)
title = title_m.group(1) if title_m else "谷歌新功能：单独统计社媒视频内容的SEO数据"

desc_m = re.search(r'name="description"\s*content="([^"]*)"', html)
desc = desc_m.group(1)[:150] if desc_m else title

date_m = re.search(r'id="publish_time">\s*(\d{4})年(\d{2})月(\d{2})日', html)
pub_date = f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}" if date_m else "2026-07-30"

# --- Extract body from rich_media_content ---
js_start = html.find('id="js_content"')
div_start = html.rfind('<', js_start - 200, js_start)
if div_start < 0:
    div_start = js_start - 200

# Find matching </div>
depth = 0
end_pos = div_start
for i in range(div_start, len(html)):
    ch = html[i]
    if html[i:i+4] == '<!--':
        end = html.find('-->', i+4)
        i = end + 2 if end > 0 else i
        continue
    if html[i:i+2] == '</' and html[i+2] not in (' ', '>'):
        depth -= 1
        if depth < 0:
            end_pos = i
            break
    elif html[i] == '<' and html[i+1:i+2] not in ('/', '!', '?'):
        end_c = html.find('>', i)
        if end_c > 0 and html[end_c-1] != '/':
            depth += 1

raw = html[div_start:end_pos]

# --- Clean WeChat junk ---
# Remove script/style tags
raw = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
raw = re.sub(r'<style[^>]*>.*?</style>', '', raw, flags=re.DOTALL)

# Remove WeChat attrs
raw = re.sub(r'\s*data-[a-z_-]+="[^"]*"', '', raw)
raw = re.sub(r'\s*leaf=""', '', raw)
raw = re.sub(r'\s*nodeleaf=""', '', raw)
raw = re.sub(r'\s*text=""', '', raw)
raw = re.sub(r'\s*deep="[^"]*"', '', raw)
raw = re.sub(r'\s*aria-hidden="[^"]*"', '', raw)

# Remove empty tags
raw = re.sub(r'<section>\s*</section>', '', raw)
raw = re.sub(r'<p>\s*</p>', '', raw)
raw = re.sub(r'<h2>\s*</h2>', '', raw)
raw = re.sub(r'<span[^>]*>\s*</span>', '', raw)

# Create slug
import hashlib
h = hashlib.md5(title.encode()).hexdigest()[:6]
slug = f"2026-gsc-social-video-seo-{h}"

# --- Download images ---
img_dir = IMGS / slug
img_dir.mkdir(parents=True, exist_ok=True)
img_pattern = re.compile(r'<img[^>]*src="(https://[^"]+)"[^>]*>')

for idx, m in enumerate(img_pattern.finditer(raw)):
    url = m.group(1)
    ext = 'png' if 'wx_fmt=png' in url else ('jpg' if 'wx_fmt=jpeg' in url else 'jpg')
    fname = f"image-{idx+1:03d}.{ext}"
    fpath = img_dir / fname
    if not fpath.exists():
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://mp.weixin.qq.com/'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                fpath.write_bytes(resp.read())
            print(f"  Downloaded: {fname}")
        except Exception as e:
            print(f"  FAILED: {url[:60]}... -> {e}")
    raw = raw.replace(f'src="{url}"', f'src="/images/posts/{slug}/{fname}"')

# --- Compact whitespace inside p/b/h2 tags ---
def compact_inner(m):
    tag = m.group(1)
    inner = re.sub(r'\s+', ' ', m.group(2)).strip()
    return f'<{tag}>{inner}</{tag}>'

raw = re.sub(r'<(p)>(.*?)</\1>', compact_inner, raw, flags=re.DOTALL)
raw = re.sub(r'<(b)>(.*?)</\1>', compact_inner, raw, flags=re.DOTALL)
raw = re.sub(r'<(h2)>(.*?)</\1>', compact_inner, raw, flags=re.DOTALL)

# --- Build markdown ---
md = f'''---
title: "{title}"
description: "{desc}"
pubDate: {pub_date}
updatedDate: {pub_date}
heroImage: "/images/default-post.png"
category: "google-algorithm"
tags:
  - "谷歌算法更新"
  - "谷歌SEO"
  - "GSC"
  - "社媒SEO"
  - "视频SEO"
  - "独立站SEO"
---

{raw.strip()}
'''

out = POSTS / f"{slug}.md"
out.write_text(md, encoding='utf-8')
print(f"\nCreated: {slug}.md ({len(md)} chars)")
