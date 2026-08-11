"""
Extract WeChat articles from E:\下载\SEO小平 and create Astro blog posts.
"""
import re, os, json
from pathlib import Path

SRC = Path(r"E:\下载\SEO小平")
DST = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
IMG_DIR = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public\images\posts")

# Mapping: filename stem -> (category, tags)
META = {
    "AIAgent的普及才是导致公司裁员的开始": ("ai-geo", ["AI Agent", "AI与GEO", "裁员", "谷歌SEO", "独立站SEO"]),
    "AI建站新手适合Codex接管WordPress": ("website-building", ["Codex", "AI建站", "WordPress", "独立站建站", "谷歌SEO"]),
    "纯血小语种SEOGEOAI建站圆满收官": ("multilingual-seo", ["纯血小语种", "SEO培训", "GEO", "AI建站", "独立站SEO"]),
    "独立站课程AI建站纯血小语种SEOGEO": ("multilingual-seo", ["独立站课程", "小语种SEO", "GEO", "AI建站", "培训陪跑"]),
    "紧急避雷别让翻译插件毁掉你的独立站SEO": ("multilingual-seo", ["翻译插件", "多语言SEO", "独立站SEO", "小语种", "谷歌SEO误区"]),
    "日语专业老大哥大学别选小语种专业": ("multilingual-seo", ["日语专业", "小语种专业", "SEO职业", "谷歌SEO", "独立站"]),
    "未来10年AI独立站的红利在这里": ("website-building", ["AI独立站", "红利", "未来趋势", "独立站SEO", "谷歌SEO"]),
}

def extract_content(html_text):
    """Extract title, description, date, and content HTML from WeChat article."""
    # Title
    title_m = re.search(r'<span class="js_title_inner">\s*(.*?)\s*</span>', html_text, re.DOTALL)
    title = title_m.group(1).strip() if title_m else "未命名文章"
    # Clean title
    title = re.sub(r'\s+', ' ', title)

    # Description (meta description)
    desc_m = re.search(r'name="description"\s*content="([^"]*)"', html_text)
    # Fallback: use first content text
    if desc_m and desc_m.group(1).strip():
        desc = desc_m.group(1).strip()[:150]
    else:
        desc = title

    # Publish date
    date_m = re.search(r'id="publish_time">\s*(\d{4})年(\d{2})月(\d{2})日', html_text)
    if date_m:
        pub_date = f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}"
    else:
        pub_date = "2026-07-30"

    # Content area - find js_content div
    content_start = html_text.find('id="js_content"')
    if content_start > 0:
        # Find the actual div start
        div_start = html_text.rfind('<', content_start, content_start + 200)
        if div_start < 0:
            div_start = content_start
        # Find closing div (matching)
        depth = 0
        in_tag = False
        content_end = div_start
        for i in range(div_start, len(html_text)):
            ch = html_text[i]
            if ch == '<':
                in_tag = True
                if html_text[i:i+4] == '<!--':
                    end = html_text.find('-->', i+4)
                    if end > 0:
                        i = end + 2
                        continue
                if html_text[i:i+3] == '</' and html_text[i+2] != ' ':
                    depth -= 1
                    if depth < 0:
                        content_end = i
                        break
                elif html_text[i+1:i+2] != '/':
                    if html_text[i:i+2] not in ('</', '<!', '<?'):
                        # Self-closing check
                        end_c = html_text.find('>', i)
                        if end_c > 0 and html_text[end_c-1] == '/':
                            pass
                        else:
                            depth += 1
                content_end = i + 1
            elif ch == '>':
                in_tag = False
                content_end = i + 1
            else:
                content_end = i + 1

        raw_html = html_text[div_start:content_end]
    else:
        raw_html = "<p>内容未找到</p>"

    # Clean up the HTML - remove WeChat-specific stuff but preserve structure and images
    content = raw_html

    # Remove empty sections
    content = re.sub(r'<section[^>]*>\s*</section>', '', content)
    content = re.sub(r'<span[^>]*>\s*</span>', '', content)
    content = re.sub(r'<br\s*/?>', '\n', content)

    # Process images - download and replace src
    def process_img(m):
        src = m.group(1)
        alt = m.group(2) or "配图"
        ext = src.split('.')[-1].split('?')[0] if '.' in src else 'jpg'
        if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
            ext = 'jpg'
        return f'<img src="{src}" alt="{alt}" loading="lazy" />'

    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>', process_img, content)
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', lambda m: f'<img src="{m.group(1)}" alt="配图" loading="lazy" />', content)

    # Convert p tags with spans to clean text
    content = re.sub(r'<span\s+leaf="">', '', content)
    content = re.sub(r'</span>', '', content)

    # Clean up WeChat-injected attrs
    content = re.sub(r'\s*style="[^"]*"', '', content)
    content = re.sub(r'\s*data-[a-z_]+="[^"]*"', '', content)
    content = re.sub(r'\s*class="[^"]*"', '', content)

    # Remove empty tags
    content = re.sub(r'<p>\s*</p>', '', content)
    content = re.sub(r'<section>\s*</section>', '', content)
    content = re.sub(r'<p>\s*<br\s*/?>\s*</p>', '', content)

    # Convert to markdown-friendly format
    # Keep as HTML but strip outer wrapper if it's just a single section
    content = content.strip()
    if content.startswith('<section>') and content.endswith('</section>'):
        inner = content[9:-10].strip()
        if inner:
            content = inner

    return title, desc, pub_date, content

def slugify(text):
    """Create URL-friendly slug from Chinese title."""
    import hashlib
    # Use filename-based approach
    return None  # We'll use the filename as slug base

results = []
seen_descriptions = set()

for f in sorted(SRC.glob("*.html")):
    stem = f.stem
    text = f.read_text(encoding='utf-8', errors='replace')
    
    title, desc, pub_date, content = extract_content(text)
    
    # Unique description
    base_desc = desc[:140] if len(desc) > 140 else desc
    desc_final = base_desc
    counter = 1
    while desc_final in seen_descriptions:
        desc_final = base_desc + "（之二）" if counter == 1 else base_desc.rstrip("）") + f"之{counter}）"
        counter += 1
    seen_descriptions.add(desc_final)
    
    meta = META.get(stem, ("seo-tutorial", ["谷歌SEO", "独立站SEO"]))
    category, tags = meta
    
    # Create simple slug from title
    title_clean = re.sub(r'[^\w]', '', title.replace(' ', ''))
    slug = f"2026-wechat-{stem[:40]}"
    slug = re.sub(r'[^\w-]', '', slug).lower()
    if not slug:
        slug = f"article-{len(results)+1}"
    
    # Build frontmatter
    tags_yaml = '\n'.join(f'  - "{t}"' for t in tags)
    hero_path = f"/images/posts/{slug}/cover.png"
    
    fm = f'''---
title: "{title}"
description: "{desc_final}"
pubDate: {pub_date}
updatedDate: {pub_date}
heroImage: "{hero_path}"
category: "{category}"
tags:
{tags_yaml}
---
'''
    
    body = f'''
<p class="article-kicker text-primary font-bold mb-6" style="font-size:1.05rem;letter-spacing:0.04em">SEO小平</p>

<h1 class="text-4xl font-black leading-tight tracking-tight mb-6" style="color:var(--color-text)">{title}</h1>

<p class="text-lg leading-8 mb-8" style="color:rgba(255,255,255,0.76)">{desc_final}</p>

---

{content}
'''

    md_content = fm + body
    
    md_path = DST / f"{slug}.md"
    md_path.write_text(md_content, encoding='utf-8')
    
    # Create placeholder cover image dir
    img_subdir = IMG_DIR / slug
    img_subdir.mkdir(parents=True, exist_ok=True)
    cover_path = img_subdir / "cover.png"
    if not cover_path.exists():
        # Copy reference cover or create placeholder
        import shutil
        ref = IMG_DIR / "cosine-similarity-seo-content-writing-guide" / "cover.png"
        if ref.exists():
            shutil.copy(ref, cover_path)
        else:
            # Write minimal PNG
            cover_path.write_bytes(b'')
    
    results.append((slug, title, category))
    print(f"✅ {slug} | {title[:40]}... | {category}")

print(f"\n🎉 Created {len(results)} blog posts")
print("\n".join(f"  /{r[0]}" for r in results))
