from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / 'src' / 'content' / 'posts'
IMAGES_DIR = ROOT / 'public' / 'images'
POST_IMAGES_DIR = IMAGES_DIR / 'posts'
DEFAULT_HERO = '/images/default-post.png'


@dataclass(frozen=True)
class PostConfig:
    source: str
    slug: str
    title: str
    description: str
    pub_date: str
    updated_date: str
    category: str
    tags: tuple[str, ...]


SELECTED_POSTS: tuple[PostConfig, ...] = (
    PostConfig(
        source=r'C:\Users\Administrator\Downloads\外贸B2B Instagram从找客户到拿询盘完整开发教程.docx',
        slug='b2b-instagram-lead-generation-inquiry-guide',
        title='外贸B2B Instagram从找客户到拿询盘完整开发教程',
        description='面向外贸 B2B 实操团队，系统拆解 Instagram 从账号搭建、精准找客、内容种草、私信转化到广告放大的完整链路，帮助传统行业把社媒流量真正转成询盘。',
        pub_date='2026-06-30',
        updated_date='2026-06-30',
        category='seo-tutorial',
        tags=('Instagram获客', '外贸B2B', '社媒开发', '询盘增长', '独立站运营', '海外客户开发'),
    ),
    PostConfig(
        source=r'C:\Users\Administrator\Downloads\AI Agent时代的SEO与Agent Commerce前沿思考：独立站流量与交易的未来壁垒 (1).docx',
        slug='ai-agent-seo-agent-commerce-future-moat',
        title='AI Agent时代的SEO与Agent Commerce前沿思考：独立站流量与交易的未来壁垒',
        description='从 AI Agent 抓取、机器可读数据、API 接口到 Agent Commerce 成交链路，系统梳理独立站在 AI 时代为什么必须从“页面竞争”升级为“数据与接口竞争”。',
        pub_date='2026-06-29',
        updated_date='2026-06-29',
        category='ai-geo',
        tags=('AI Agent', 'Agent Commerce', '机器可读数据', 'GEO', '独立站未来', 'API接口'),
    ),
    PostConfig(
        source=r'C:\Users\Administrator\Downloads\放弃传统外链思维：Reddit的GEO引用为何决定了AI时代的品牌曝光？.docx',
        slug='reddit-geo-brand-exposure-ai-era',
        title='放弃传统外链思维：Reddit的GEO引用为何决定了AI时代的品牌曝光？',
        description='围绕 Reddit 在 AI 搜索时代的引用价值，拆解为什么传统粗放外链思维正在失灵，以及出海品牌如何通过真实社区讨论进入大模型的推荐与引用链路。',
        pub_date='2026-06-28',
        updated_date='2026-06-28',
        category='ai-geo',
        tags=('Reddit GEO', '品牌曝光', 'AI搜索', '外链策略', 'UGC社区', '出海品牌'),
    ),
    PostConfig(
        source=r'C:\Users\Administrator\Downloads\谷歌核心算法演变史：从 PageRank 到 2026 年最新核心算法更新（Core Updates）.docx',
        slug='google-core-algorithm-evolution-pagerank-2026',
        title='谷歌核心算法演变史：从 PageRank 到 2026 年最新核心算法更新（Core Updates）',
        description='系统回顾 Google 核心算法从 PageRank 到 2026 年 Core Updates 的演变脉络，帮助独立站运营者理解算法关注点为何从链接投票走向内容质量、语义理解与 AI 时代的信息增益。',
        pub_date='2026-06-27',
        updated_date='2026-06-27',
        category='google-algorithm',
        tags=('Google算法', 'PageRank', 'Core Updates', '算法演变', '搜索排名', 'SEO认知'),
    ),
    PostConfig(
        source=r'C:\Users\Administrator\Downloads\谷歌搜索引擎工作原理：抓取（Crawling）、索引（Indexing）与排名（Ranking）全解析.docx',
        slug='google-search-crawling-indexing-ranking-explained',
        title='谷歌搜索引擎工作原理：抓取（Crawling）、索引（Indexing）与排名（Ranking）全解析',
        description='从抓取、索引、排名三大流程出发，讲清 Google 搜索引擎如何发现、筛选与排序网页，并结合外贸独立站常见问题给出可执行的 SEO 优化思路。',
        pub_date='2026-06-26',
        updated_date='2026-06-26',
        category='technical-seo',
        tags=('Google抓取', 'Google索引', 'Google排名', '技术SEO', 'Googlebot', 'SEO基础'),
    ),
    PostConfig(
        source=r'C:\Users\Administrator\Downloads\纯血版小语种SEO实战：TranslatePress与Gtranslate该怎么选？.docx',
        slug='translatepress-vs-gtranslate-multilingual-seo-guide',
        title='纯血版小语种SEO实战：TranslatePress与Gtranslate该怎么选？',
        description='从纯血版小语种 SEO 的实战视角，对比 TranslatePress 与 Gtranslate 的底层架构、收录表现与流量风险，帮助独立站选择更适合长期小语种获流的方案。',
        pub_date='2026-06-25',
        updated_date='2026-06-25',
        category='multilingual-seo',
        tags=('TranslatePress', 'Gtranslate', '小语种SEO', '多语言建站', '纯血小语种', '收录优化'),
    ),
)


def main() -> None:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    POST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    written = []

    for config in SELECTED_POSTS:
        source = Path(config.source)
        if not source.exists():
            raise FileNotFoundError(source)

        image_dir = POST_IMAGES_DIR / config.slug
        if image_dir.exists():
            shutil.rmtree(image_dir)
        image_dir.mkdir(parents=True, exist_ok=True)

        body, image_urls = convert_docx(source, config.title, config.slug, image_dir)
        hero_image = image_urls[0] if image_urls else DEFAULT_HERO

        output = POSTS_DIR / f'{config.slug}.md'
        output.write_text(build_post(config, hero_image, body), encoding='utf-8')
        written.append(
            {
                'title': config.title,
                'slug': config.slug,
                'images': len(image_urls),
                'output': str(output.relative_to(ROOT)),
            }
        )

    print(json.dumps(written, ensure_ascii=False, indent=2))


def convert_docx(source: Path, title: str, slug: str, image_dir: Path) -> tuple[str, list[str]]:
    doc = Document(source)
    saved_images: dict[str, str] = {}
    image_urls: list[str] = []
    elements: list[dict[str, str]] = []

    for block in iter_blocks(doc):
        if isinstance(block, Paragraph):
            text = normalize_text(block.text)
            image_refs = get_image_refs(block)

            if text and normalize_for_compare(text) != normalize_for_compare(title):
                elements.append({'type': 'paragraph', 'text': text})

            for rel_id in image_refs:
                url = save_image(doc, rel_id, image_dir, slug, saved_images)
                if url:
                    image_urls.append(url)
                    elements.append({'type': 'image', 'url': url})

        elif isinstance(block, Table):
            table_md = format_table(block)
            if table_md:
                elements.append({'type': 'table', 'text': table_md})

    intro_indexes = find_intro_indexes(elements)
    intro_index_set = set(intro_indexes)
    parts: list[str] = []

    if intro_indexes:
        intro_html = '\n'.join(
            f'  <p>{escape_html(elements[index]["text"])}</p>' for index in intro_indexes
        )
        parts.append(f'<div class="content-lead">\n{intro_html}\n</div>')

    for index, element in enumerate(elements):
        if index in intro_index_set:
            continue

        element_type = element['type']
        if element_type == 'paragraph':
            next_text = next_paragraph_text(elements, index)
            parts.append(format_paragraph(element['text'], next_text))
        elif element_type == 'image':
            parts.append(
                '\n'.join(
                    [
                        '<figure class="figure-card">',
                        f'  <img src="{element["url"]}" alt="{escape_attribute(title)}" loading="lazy" decoding="async" />',
                        '</figure>',
                    ]
                )
            )
        elif element_type == 'table':
            parts.append(element['text'])

    return '\n\n'.join(part for part in parts if part.strip()), image_urls


def find_intro_indexes(elements: list[dict[str, str]]) -> list[int]:
    indexes: list[int] = []

    for index, element in enumerate(elements):
        if element['type'] != 'paragraph':
            continue

        next_text = next_paragraph_text(elements, index)
        if infer_paragraph_kind(element['text'], next_text).startswith('h'):
            break

        indexes.append(index)
        if len(indexes) == 2:
            break

    return indexes


def next_paragraph_text(elements: list[dict[str, str]], start: int) -> str:
    for element in elements[start + 1 :]:
        if element['type'] == 'paragraph':
            return element['text']
    return ''


def infer_paragraph_kind(text: str, next_text: str) -> str:
    if re.match(r'^[一二三四五六七八九十百零]+[、.．]\s*', text):
        return 'h2'
    if re.match(r'^\d+[.、．)]\s*', text):
        return 'h3'
    if re.match(r'^[（(]\d+[)）]\s*', text):
        return 'h4'

    if (
        len(text) <= 46
        and next_text
        and len(next_text) >= 50
        and not re.search(r'[。！？!?]$', text)
    ):
        return 'h3'

    return 'p'


def format_paragraph(text: str, next_text: str) -> str:
    kind = infer_paragraph_kind(text, next_text)
    escaped = escape_html(text)
    if kind == 'h2':
        return f'## {escaped}'
    if kind == 'h3':
        return f'### {escaped}'
    if kind == 'h4':
        return f'#### {escaped}'
    return escaped


def format_table(table: Table) -> str:
    rows: list[list[str]] = []
    for row in table.rows:
        cells = [escape_markdown(normalize_text(cell.text)).replace('|', '\\|') for cell in row.cells]
        if any(cells):
            rows.append(cells)

    if not rows:
        return ''

    width = max(len(row) for row in rows)
    normalized = [row + [''] * (width - len(row)) for row in rows]
    header = '| ' + ' | '.join(normalized[0]) + ' |'
    divider = '| ' + ' | '.join(['---'] * width) + ' |'
    body = ['| ' + ' | '.join(row) + ' |' for row in normalized[1:]]
    return '\n'.join([header, divider, *body])


def iter_blocks(doc: Document):
    for child in doc.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, doc)
        elif child.tag == qn('w:tbl'):
            yield Table(child, doc)


def get_image_refs(paragraph: Paragraph) -> list[str]:
    refs: list[str] = []
    for element in paragraph._element.iter():
        if element.tag.endswith('}blip'):
            rel_id = element.get(qn('r:embed')) or element.get(qn('r:link'))
            if rel_id:
                refs.append(rel_id)
    return refs


def save_image(
    doc: Document,
    rel_id: str,
    image_dir: Path,
    slug: str,
    saved_images: dict[str, str],
) -> str:
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

    output_name = f'image-{len(saved_images) + 1:03d}-{digest}.{ext or "png"}'
    output_path = image_dir / output_name

    if ext in {'png', 'jpg', 'webp', 'avif'}:
        output_path.write_bytes(blob)
    else:
        with Image.open(BytesIO(blob)) as image:
            if image.mode not in {'RGB', 'RGBA'}:
                image = image.convert('RGB')
            image.save(output_path)

    url = f'/images/posts/{slug}/{output_name}'
    saved_images[rel_id] = url
    return url


def build_post(config: PostConfig, hero_image: str, body: str) -> str:
    frontmatter = [
        '---',
        f'title: {yaml_string(config.title)}',
        f'description: {yaml_string(config.description)}',
        f'pubDate: {config.pub_date}',
        f'updatedDate: {config.updated_date}',
        f'heroImage: {yaml_string(hero_image)}',
        f'category: {yaml_string(config.category)}',
        'tags:',
        *[f'  - {yaml_string(tag)}' for tag in config.tags],
        '---',
        '',
    ]
    return '\n'.join(frontmatter) + body.strip() + '\n'


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_text(text: str) -> str:
    return re.sub(r'[ \t\r\f\v]+', ' ', text.replace('\u00a0', ' ')).strip()


def normalize_for_compare(text: str) -> str:
    return re.sub(r'[\W_]+', '', text.lower(), flags=re.UNICODE)


def escape_html(text: str) -> str:
    return html.escape(text, quote=False)


def escape_attribute(text: str) -> str:
    return html.escape(text, quote=True)


def escape_markdown(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


if __name__ == '__main__':
    main()
