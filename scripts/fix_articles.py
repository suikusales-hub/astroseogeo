import re, shutil
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
img_src = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public\images\default-post.png")

# Reference image path from the user's example
FALLBACK_HERO = "/images/default-post.png"

for f in sorted(posts_dir.glob("2026-*.md")):
    text = f.read_text(encoding='utf-8')
    parts = text.split('---')
    if len(parts) < 3:
        continue
    fm = parts[1]
    body = '---'.join(parts[2:])
    
    # 1. Strip the redundant kicker/h1/desc section and second ---
    if '<p class="article-kicker' in body:
        sec_sep = body.find('\n---\n')
        if sec_sep >= 0:
            body = body[sec_sep + 5:]
    
    # 2. Clean WeChat artifacts
    body = re.sub(r'\s*data-path-to-node="[^"]*"', '', body)
    body = re.sub(r'\s*data-index-in-node="[^"]*"', '', body)
    body = re.sub(r'\s*leaf=""', '', body)
    body = re.sub(r'\s*nodeleaf=""', '', body)
    body = re.sub(r'\s*text=""', '', body)
    body = re.sub(r'\s*deep="[^"]*"', '', body)
    body = re.sub(r'\s*class="[^"]*"', '', body)
    body = re.sub(r'\s*style="[^"]*"', '', body)
    body = re.sub(r'<span[^>]*>\s*</span>', '', body)
    body = re.sub(r'<section[^>]*>\s*</section>', '', body)
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'\n\s*\n\s*\n', '\n\n', body)
    
    # 3. Extract first image for hero
    img_match = re.search(r'<img[^>]+src="(https://[^"]+|/[^"]+)"', body)
    if img_match:
        hero_path = img_match.group(1)
        # Keep absolute URLs as-is, Pagefind/Cloudflare will serve them
        print(f"  {f.stem}: found image in body -> {hero_path[:60]}...")
    else:
        hero_path = FALLBACK_HERO
        print(f"  {f.stem}: no image found, using fallback")
    
    # 4. Update description to first meaningful text
    body_text = re.sub(r'<[^>]+>', '', body).strip()
    first_line = body_text[:140].replace('\n', ' ').strip()
    if first_line and len(first_line) > 15:
        fm = re.sub(r'^description: ".*"', f'description: "{first_line}"', fm, flags=re.M)
    
    # 5. Update heroImage
    fm = re.sub(r'^heroImage: ".*"', f'heroImage: "{hero_path}"', fm, flags=re.M)
    
    # 6. Preserve img src for external URLs (download not needed on Cloudflare)
    
    new_text = '---' + fm + '---\n\n' + body.strip()
    f.write_text(new_text, encoding='utf-8')
    print(f"✅ {f.stem}")
