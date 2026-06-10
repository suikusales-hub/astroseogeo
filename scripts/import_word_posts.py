from __future__ import annotations

import hashlib
import json
import re
import shutil
from io import BytesIO
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(
    'C:/Users/Administrator/Documents/xwechat_files/ping8758_23ac/msg/file/2026-06/'
    'SEO\u5c0f\u5e73(1)word/SEO\u5c0f\u5e73'
)
POSTS_DIR = ROOT / 'src' / 'content' / 'posts'
IMAGES_DIR = ROOT / 'public' / 'images'
POST_IMAGES_DIR = IMAGES_DIR / 'posts'
DEFAULT_IMAGE = IMAGES_DIR / 'default-post.png'
REPORT_PATH = ROOT / 'import-report.json'

CATEGORIES = {
    'seo-tutorial': 'SEO基础教程',
    'google-algorithm': '谷歌算法更新',
    'ai-geo': 'AI与GEO',
    'multilingual-seo': '小语种SEO',
    'website-building': '独立站建站',
    'keyword-content': '关键词与内容',
    'technical-seo': '技术SEO工具',
    'case-study': '案例与陪跑',
}

RESERVED_SLUGS = set(CATEGORIES) | {'about', 'contact', 'index'}

CATEGORY_RULES = [
    (
        'keyword-content',
        ['关键词', '长尾词', '内容', '写作', '写文章', '博客', '文章', 'freshness', '调研', '布局', '质量内容', '提示词', '客户反馈'],
    ),
    (
        'ai-geo',
        [
            'ai',
            'geo',
            'chatgpt',
            'deepseek',
            'gemini',
            'codex',
            'claude',
            'notebooklm',
            'nano banana',
            'openclaw',
            'moltbot',
            'clawdbot',
            'agents.md',
            'aigc',
            '豆包',
            '生成式',
        ],
    ),
    (
        'multilingual-seo',
        [
            '小语种',
            '纯血',
            '多语种',
            '西班牙语',
            '越南语',
            '翻译插件',
            '翻译url',
            'native-first',
            'niche language',
        ],
    ),
    (
        'google-algorithm',
        [
            '算法',
            '核心更新',
            'core update',
            '排名掉',
            '流量断崖',
            '谷歌3月',
            'google内部',
            '屠刀',
            '需要多久',
            '权重值',
            'reddit',
            '实操建议',
        ],
    ),
    (
        'case-study',
        [
            '案例',
            '学员',
            '陪跑',
            '培训',
            '沙龙',
            '圆满',
            '开课',
            '报名',
            '大会',
            '受邀',
            '询盘',
            '订单',
            '复盘',
            'meetup',
            'partnerboost',
            '网贸会',
            '师范大学',
        ],
    ),
    (
        'website-building',
        ['wordpress', 'shopify', '建站', '主题', '服务器', '主机', 'cloudflare', '网站服务器'],
    ),
    (
        'technical-seo',
        [
            'gsc',
            'html',
            'xml',
            'txt',
            'robots',
            'screaming frog',
            '收录',
            'webp',
            '站点地图',
            '二级域名',
            '二级目录',
            '搜索指令',
            '代码',
            '技术seo',
            'core web vitals',
        ],
    ),
]

SLUG_KEYWORDS = [
    ('谷歌', 'google'),
    ('独立站', 'independent-site'),
    ('外贸', 'foreign-trade'),
    ('跨境', 'cross-border'),
    ('关键词', 'keyword'),
    ('外链', 'link-building'),
    ('内链', 'internal-links'),
    ('算法', 'algorithm'),
    ('收录', 'indexing'),
    ('排名', 'ranking'),
    ('流量', 'traffic'),
    ('询盘', 'inquiry'),
    ('案例', 'case-study'),
    ('陪跑', 'coaching'),
    ('培训', 'training'),
    ('小语种', 'multilingual'),
    ('纯血', 'native'),
    ('建站', 'website-building'),
    ('服务器', 'hosting'),
    ('站点地图', 'sitemap'),
    ('写作', 'writing'),
    ('内容', 'content'),
    ('博客', 'blog'),
    ('工具', 'tools'),
    ('免费', 'free'),
    ('教程', 'guide'),
    ('指南', 'guide'),
    ('误区', 'mistakes'),
    ('问题', 'faq'),
    ('基础', 'basics'),
    ('实操', 'practice'),
    ('策略', 'strategy'),
    ('诊断', 'audit'),
    ('转化率', 'conversion'),
    ('亚马逊', 'amazon'),
    ('联盟营销', 'affiliate'),
    ('关税', 'tariff'),
    ('网站', 'website'),
    ('代码', 'code'),
    ('主题', 'theme'),
]

ASCII_STOPWORDS = {
    'or',
    'and',
    'the',
    'with',
    'vs',
    'ok',
    'why',
    'near',
    'me',
}


def main() -> None:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(SOURCE_DIR)

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    POST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    ensure_default_image()

    files = sorted(path for path in SOURCE_DIR.glob('*.docx') if not path.name.startswith('~$'))
    used_slugs = set(RESERVED_SLUGS)
    report = []

    for index, path in enumerate(files, start=1):
        meta = parse_file_name(path)
        category = classify(meta['title'])
        slug = build_slug(meta['date'], meta['title'], category, used_slugs)
        used_slugs.add(slug)

        post_dir = POST_IMAGES_DIR / slug
        if post_dir.exists():
            shutil.rmtree(post_dir)
        post_dir.mkdir(parents=True, exist_ok=True)

        markdown, image_urls, text_blocks = convert_docx(path, slug, post_dir, meta['title'])
        hero_image = image_urls[0] if image_urls else '/images/default-post.png'
        description = build_description(text_blocks, meta['title'])
        tags = build_tags(meta['title'], category)
        output_path = POSTS_DIR / f'{slug}.md'

        output_path.write_text(
            build_markdown(meta, description, hero_image, category, tags, markdown),
            encoding='utf-8',
        )

        report.append(
            {
                'source': str(path),
                'output': str(output_path.relative_to(ROOT)),
                'title': meta['title'],
                'slug': slug,
                'category': category,
                'images': len(image_urls),
            }
        )

        if index % 25 == 0:
            print(f'Imported {index}/{len(files)} posts')

    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Imported {len(report)} posts')
    print(f'Report: {REPORT_PATH}')


def parse_file_name(path: Path) -> dict[str, str]:
    match = re.match(r'(?P<date>\d{4}-\d{2}-\d{2})_(?P<title>.+)\.docx$', path.name, re.IGNORECASE)
    if not match:
        raise ValueError(f'Unexpected Word file name: {path.name}')

    title = normalize_text(match.group('title'))
    return {'date': match.group('date'), 'title': title}


def classify(title: str) -> str:
    lowered = title.lower().replace(' ', '')
    readable_lowered = title.lower()

    for category, keywords in CATEGORY_RULES:
        if any(keyword.replace(' ', '') in lowered or keyword in readable_lowered for keyword in keywords):
            return category

    return 'seo-tutorial'


def build_slug(date_value: str, title: str, category: str, used_slugs: set[str]) -> str:
    lowered = title.lower()
    tokens: list[str] = []

    for text, token in SLUG_KEYWORDS:
        if text.lower() in lowered:
            tokens.extend(token.split('-'))

    for token in re.findall(r'[a-z0-9]+', lowered):
        if token not in ASCII_STOPWORDS:
            tokens.append(token)

    if not tokens:
        tokens.extend(category.split('-'))

    compact_tokens = dedupe(tokens)[:6]
    base = clean_slug(f'{date_value}-{"-".join(compact_tokens)}')
    slug = base
    suffix = 2

    while slug in used_slugs:
        slug = f'{base}-{suffix}'
        suffix += 1

    return slug


def clean_slug(value: str) -> str:
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', value.lower())).strip('-')


def dedupe(values: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        clean = clean_slug(value)
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


def convert_docx(path: Path, slug: str, image_dir: Path, title: str) -> tuple[str, list[str], list[str]]:
    doc = Document(path)
    parts: list[str] = []
    image_urls: list[str] = []
    saved_images: dict[str, str] = {}
    text_blocks: list[str] = []
    seen_first_content = False

    for block in iter_blocks(doc):
        if isinstance(block, Paragraph):
            text = normalize_text(block.text)
            image_refs = get_image_refs(block)

            if text:
                if should_skip_paragraph(text, title, seen_first_content):
                    seen_first_content = True
                    text = ''
                else:
                    seen_first_content = True
                    text_blocks.append(text)
                    parts.append(format_paragraph(block, text))

            for rel_id in image_refs:
                image_url = save_image(doc, rel_id, image_dir, slug, saved_images)
                if image_url:
                    image_urls.append(image_url)
                    parts.append(f'![{escape_markdown(title)} 配图]({image_url})')

        elif isinstance(block, Table):
            table_markdown = format_table(block)
            if table_markdown:
                parts.append(table_markdown)

    markdown = '\n\n'.join(part for part in parts if part.strip())
    return markdown, image_urls, text_blocks


def iter_blocks(doc: Document):
    for child in doc.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, doc)
        elif child.tag == qn('w:tbl'):
            yield Table(child, doc)


def should_skip_paragraph(text: str, title: str, seen_first_content: bool) -> bool:
    if not seen_first_content and normalize_for_compare(text) == normalize_for_compare(title):
        return True

    if re.search(r'\d{4}-\d{2}-\d{2}', text) and ('SEO小平' in text or '谷歌SEO小平' in text or '原创' in text):
        return True

    return False


def format_paragraph(paragraph: Paragraph, text: str) -> str:
    style_name = (paragraph.style.name or '').lower()
    safe_text = escape_markdown_text(text)
    heading_level = None

    if 'heading 1' in style_name or '标题 1' in style_name:
        heading_level = 2
    elif 'heading 2' in style_name or '标题 2' in style_name:
        heading_level = 3
    elif 'heading 3' in style_name or '标题 3' in style_name:
        heading_level = 4

    if heading_level:
        return f'{"#" * heading_level} {safe_text}'

    return safe_text


def format_table(table: Table) -> str:
    rows = []
    for row in table.rows:
        cells = [escape_markdown_text(normalize_text(cell.text)).replace('|', '\\|') for cell in row.cells]
        if any(cells):
            rows.append(cells)

    if not rows:
        return ''

    width = max(len(row) for row in rows)
    normalized_rows = [row + [''] * (width - len(row)) for row in rows]
    header = '| ' + ' | '.join(normalized_rows[0]) + ' |'
    divider = '| ' + ' | '.join(['---'] * width) + ' |'
    body = ['| ' + ' | '.join(row) + ' |' for row in normalized_rows[1:]]
    return '\n'.join([header, divider, *body])


def get_image_refs(paragraph: Paragraph) -> list[str]:
    refs = []
    for element in paragraph._element.iter():
        if element.tag.endswith('}blip'):
            rel_id = element.get(qn('r:embed')) or element.get(qn('r:link'))
            if rel_id:
                refs.append(rel_id)
    return refs


def save_image(doc: Document, rel_id: str, image_dir: Path, slug: str, saved_images: dict[str, str]) -> str:
    if rel_id in saved_images:
        return saved_images[rel_id]

    part = doc.part.related_parts.get(rel_id)
    if part is None:
        return ''

    blob = part.blob
    digest = hashlib.sha1(blob).hexdigest()[:10]
    content_type = getattr(part, 'content_type', '')
    ext = {
        'image/png': 'png',
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/webp': 'webp',
        'image/avif': 'avif',
    }.get(content_type, '')

    image_index = len(saved_images) + 1
    if ext in {'png', 'jpg', 'jpeg', 'webp', 'avif'}:
        output_name = f'image-{image_index:03d}-{digest}.{ext}'
        output_path = image_dir / output_name
        output_path.write_bytes(blob)
    else:
        output_name = f'image-{image_index:03d}-{digest}.png'
        output_path = image_dir / output_name
        with Image.open(BytesIO(blob)) as image:
            if image.mode not in {'RGB', 'RGBA'}:
                image = image.convert('RGB')
            image.save(output_path)

    url = f'/images/posts/{slug}/{output_name}'
    saved_images[rel_id] = url
    return url


def build_description(text_blocks: list[str], title: str) -> str:
    for text in text_blocks:
        clean = re.sub(r'\s+', ' ', text).strip()
        if len(clean) >= 28:
            return truncate(clean, 150)

    return truncate(title, 150)


def build_tags(title: str, category: str) -> list[str]:
    tags = [CATEGORIES[category], '谷歌SEO', '独立站SEO']
    lowered = title.lower()

    tag_rules = [
        ('ai', 'AI'),
        ('geo', 'GEO'),
        ('gsc', 'GSC'),
        ('wordpress', 'WordPress'),
        ('shopify', 'Shopify'),
        ('semrush', 'Semrush'),
        ('ahrefs', 'Ahrefs'),
        ('外链', '外链建设'),
        ('关键词', '关键词研究'),
        ('小语种', '小语种SEO'),
        ('算法', '谷歌算法'),
        ('建站', '独立站建站'),
        ('内容', 'SEO内容'),
        ('写作', 'SEO写作'),
        ('案例', 'SEO案例'),
        ('陪跑', 'SEO陪跑'),
    ]

    for keyword, tag in tag_rules:
        if keyword in lowered and tag not in tags:
            tags.append(tag)

    return tags[:6]


def build_markdown(
    meta: dict[str, str],
    description: str,
    hero_image: str,
    category: str,
    tags: list[str],
    body: str,
) -> str:
    frontmatter = [
        '---',
        f'title: {yaml_string(meta["title"])}',
        f'description: {yaml_string(description)}',
        f'pubDate: {meta["date"]}',
        f'updatedDate: {meta["date"]}',
        f'heroImage: {yaml_string(hero_image)}',
        f'category: {yaml_string(category)}',
        'tags:',
        *[f'  - {yaml_string(tag)}' for tag in tags],
        '---',
        '',
    ]

    return '\n'.join(frontmatter) + (body.strip() + '\n' if body.strip() else '')


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_text(value: str) -> str:
    return re.sub(r'[ \t\r\f\v]+', ' ', value.replace('\u00a0', ' ')).strip()


def normalize_for_compare(value: str) -> str:
    return re.sub(r'[\W_]+', '', value.lower(), flags=re.UNICODE)


def truncate(value: str, length: int) -> str:
    value = value.strip()
    if len(value) <= length:
        return value
    return value[: length - 1].rstrip() + '…'


def escape_markdown(value: str) -> str:
    return value.replace('[', '\\[').replace(']', '\\]')


def escape_markdown_text(value: str) -> str:
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def ensure_default_image() -> None:
    if DEFAULT_IMAGE.exists():
        return

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 1200, 630
    image = Image.new('RGB', (width, height), '#FCF6F0')
    draw = ImageDraw.Draw(image)

    for y in range(height):
        ratio = y / height
        r = int(252 * (1 - ratio) + 239 * ratio)
        g = int(246 * (1 - ratio) + 125 * ratio)
        b = int(240 * (1 - ratio) + 0 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    draw.ellipse((-180, -120, 500, 560), fill=(255, 190, 90))
    draw.ellipse((780, 180, 1380, 780), fill=(255, 228, 133))
    draw.rectangle((90, 80, width - 90, height - 80), outline=(255, 255, 255), width=4)
    draw.text((130, 210), 'SEO XIAOPING', fill=(31, 21, 15))
    draw.text((130, 270), 'Google SEO · AI Search · Content Engineering', fill=(31, 21, 15))
    image.save(DEFAULT_IMAGE)


if __name__ == '__main__':
    main()
