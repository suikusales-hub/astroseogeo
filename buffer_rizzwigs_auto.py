#!/usr/bin/env python3
"""
RizzWigs → Buffer → Pinterest 自动发布脚本

功能:
  1. 抓取 rizzwigs.com 所有博客文章
  2. 自动为每篇文章生成 Pinterest-friendly 的 Pin 内容
  3. 通过 Buffer API 创建/排期 Pinterest 帖子
  4. 记录已发布文章，避免重复

使用方法:
  # 第一次运行：获取账号信息
  python buffer_rizzwigs_auto.py --api-key YOUR_BUFFER_API_KEY --discover

  # 查看所有文章（不发布）
  python buffer_rizzwigs_auto.py --api-key YOUR_BUFFER_API_KEY --list

  # 发布一篇文章（测试）
  python buffer_rizzwigs_auto.py --api-key YOUR_BUFFER_API_KEY --publish-one

  # 批量发布5篇到队列
  python buffer_rizzwigs_auto.py --api-key YOUR_BUFFER_API_KEY --publish 5

  # 批量发布所有未发布文章
  python buffer_rizzwigs_auto.py --api-key YOUR_BUFFER_API_KEY --publish-all
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# ============================================================
# 配置 - 修改这里
# ============================================================
BUFFER_API_URL = "https://api.buffer.com/graphql"
BLOG_LIST_PAGES = [
    "https://rizzwigs.com/blog-list-1.html",
    "https://rizzwigs.com/blog-list-2.html",
    "https://rizzwigs.com/blog-list-3.html",
    "https://rizzwigs.com/blog-list-4.html",
    "https://rizzwigs.com/blog-list-5.html",
]
# 已发布记录文件
POSTED_ARTICLES_FILE = Path(__file__).parent / ".buffer_posted_articles.json"
# 组织/频道配置文件
CONFIG_FILE = Path(__file__).parent / ".buffer_config.json"

# Pinterest 帖子模板
PIN_TEMPLATES = [
    "{title}\n\n{description_short}\n\nRead the full guide 👇\n{url}\n\n#wigs #hairtips #wigguide",
    "Looking for wig advice? 🤔\n\n{title}\n\n{description_short}\n\n👉 Full article: {url}\n\n#wiginfo #hairhelp",
    "📌 Wig Tip:\n{title}\n\n{description_short}\n\n🔗 {url}\n\n#wigcare #hairgoals",
    "Everything you need to know about wigs:\n\n{title}\n\n{description_short}\n\nRead more → {url}\n\n#wigtips #hair",
]


# ============================================================
# 工具函数
# ============================================================

def fetch_url(url: str, retries: int = 3) -> str:
    """获取 URL 内容，带重试"""
    last_error = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(2)
    raise last_error


def extract_articles_from_page(html: str) -> list[dict]:
    """从 blog-list 页面提取文章链接"""
    articles = []
    # 匹配 blog-list 页面中的文章链接 (相对路径)
    links = re.findall(
        r'<a\s+href="(/[a-z0-9][^"]*\.html)"[^>]*>([^<]+)</a>',
        html
    )
    seen = set()
    for url, name in links:
        # 排除非文章页面
        skip_patterns = [
            "product-category", "blog-list", "categories",
            "blog-categories", "hot-wigs", "wig-article-index",
            "wishlist", "cart", "checkout", "account",
            "contact", "about", "privacy", "faq",
            "shipping", "return", "payment", "logout",
            "login", "register",
        ]
        if any(p in url for p in skip_patterns):
            continue
        if url in seen:
            continue
        seen.add(url)
        articles.append({
            "url": f"https://rizzwigs.com{url}",
            "title_raw": name.strip(),
        })
    return articles


def extract_article_detail(url: str) -> dict | None:
    """从文章页面提取详细信息"""
    try:
        html = fetch_url(url)
    except Exception as e:
        print(f"  ⚠️ 获取失败: {url} - {e}")
        return None

    # 提取标题
    title_match = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not title_match:
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    # 清理 HTML 标签
    title = re.sub(r'<[^>]+>', '', title).strip()

    # 提取 meta description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = desc_match.group(1) if desc_match else ""

    # 提取主图片 (文章主图src为空，使用产品图)
    image_url = ""
    # 尝试 og:image
    og_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    if og_match and og_match.group(1):
        image_url = og_match.group(1)
    else:
        # 获取所有 uploads 图片，排除头像和缩略图
        img_matches = re.findall(r'<img[^>]*src="(/uploads/[^"]+)"[^>]*>', html)
        for img in img_matches:
            # 排除 Jesica 头像 (65x65, alt~Jesica)
            if 'Jesica' in img:
                continue
            # 排除 related post 缩略图 (70x70)
            if 'max-width="70"' in img or 'height="70"' in img:
                continue
            image_url = f"https://rizzwigs.com{img}"
            break
        # 如果还是没有，用第一个非头像的 uploads 图片
        if not image_url:
            for img in img_matches:
                if 'Jesica' not in img:
                    image_url = f"https://rizzwigs.com{img}"
                    break

    return {
        "url": url,
        "title": title,
        "description": description,
        "image_url": image_url,
    }


def graphql_request(api_key: str, query: str, variables: dict | None = None) -> dict:
    """发送 GraphQL 请求到 Buffer API"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BUFFER_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def discover_account(api_key: str) -> dict | None:
    """发现 Organization 和 Channel"""
    print("\n🔍 正在查询你的 Buffer 账号信息...\n")

    # 查询 Organization
    query_org = """
    query {
      account {
        organizations {
          id
          name
        }
      }
    }
    """
    try:
        result = graphql_request(api_key, query_org)
        orgs = result.get("data", {}).get("account", {}).get("organizations", [])
        if not orgs:
            print("❌ 没有找到 Organization")
            return None

        print("📋 Organizations:")
        for org in orgs:
            print(f"   ID: {org['id']}  Name: {org['name']}")

        org_id = orgs[0]["id"]

        # 查询 Channels
        query_channels = """
        query GetChannels($orgId: String!) {
          channels(input: { organizationId: $orgId }) {
            id
            name
            service
          }
        }
        """
        result = graphql_request(api_key, query_channels, {"orgId": org_id})
        channels = result.get("data", {}).get("channels", []) or []

        print(f"\n📺 Channels (Organization: {orgs[0]['name']}):")
        for ch in channels:
            print(f"   ID: {ch['id']}  Name: {ch['name']}  Service: {ch['service']}")

        # 找 Pinterest channel
        pinterest_channels = [ch for ch in channels if ch["service"] == "pinterest"]
        if pinterest_channels:
            print(f"\n✅ 找到 Pinterest Channel: {pinterest_channels[0]['id']}")
            return {
                "organization_id": org_id,
                "pinterest_channel_id": pinterest_channels[0]["id"],
                "all_channels": channels,
            }
        else:
            print("\n⚠️ 没有找到 Pinterest channel，请确认已在 Buffer 中授权 Pinterest")
            print("可用的 channels:")
            for ch in channels:
                print(f"   - {ch['service']}: {ch['id']}")
            return None

    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        return None


def create_buffer_post(
    api_key: str,
    channel_id: str,
    text: str,
    image_url: str = "",
    mode: str = "addToQueue",
) -> dict:
    """创建 Buffer 帖子 - 使用 GraphQL variables 避免转义问题"""
    # 构建 assets 变量
    assets = None
    if image_url:
        assets = [{"image": {"url": image_url}}]

    variables = {
        "text": text,
        "channelId": channel_id,
        "mode": mode,
        "meta": {
            "pinterest": {
                "boardServiceId": "1092474890799708177",
                "title": text.split('\n')[0],
                "url": ""
            }
        }
    }
    if assets:
        variables["assets"] = assets

    query = """
    mutation CreatePost($text: String!, $channelId: ChannelId!, $mode: ShareMode!, $assets: [AssetInput!]!) {
      createPost(input: {
        text: $text,
        channelId: $channelId,
        schedulingType: automatic,
        mode: $mode,
        assets: $assets
      }) {
        ... on PostActionSuccess {
          post { id text dueAt }
        }
        ... on MutationError {
          message
        }
      }
    }
    """
    return graphql_request(api_key, query, variables)


def load_posted_articles() -> set:
    """加载已发布的文章 URL 集合"""
    if POSTED_ARTICLES_FILE.exists():
        return set(json.loads(POSTED_ARTICLES_FILE.read_text(encoding="utf-8")))
    return set()


def save_posted_articles(urls: set):
    """保存已发布的文章 URL"""
    POSTED_ARTICLES_FILE.write_text(
        json.dumps(sorted(urls), indent=2), encoding="utf-8"
    )


def load_config() -> dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}


def save_config(config: dict):
    """保存配置"""
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


# ============================================================
# 主逻辑
# ============================================================

def fetch_all_articles() -> list[dict]:
    """获取所有文章"""
    print("📥 正在抓取 RizzWigs 文章列表...")
    all_articles = []
    for page_url in BLOG_LIST_PAGES:
        try:
            html = fetch_url(page_url)
            articles = extract_articles_from_page(html)
            print(f"   {page_url}: 找到 {len(articles)} 篇文章")
            all_articles.extend(articles)
        except Exception as e:
            print(f"   ⚠️ {page_url}: {e}")

    # 去重
    seen = set()
    unique = []
    for a in all_articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    print(f"📊 共发现 {len(unique)} 篇唯一文章\n")
    return unique


def enrich_articles(articles: list[dict], limit: int = 0) -> list[dict]:
    """为文章获取详细信息（标题、描述、图片）"""
    enriched = []
    targets = articles[:limit] if limit > 0 else articles

    for i, article in enumerate(targets):
        url = article["url"]
        print(f"  [{i+1}/{len(targets)}] {url}")
        detail = extract_article_detail(url)
        if detail and detail["title"]:
            enriched.append(detail)
        else:
            # 用原始数据
            enriched.append({
                "url": url,
                "title": article.get("title_raw", "Wig Article"),
                "description": "",
                "image_url": "",
            })
        time.sleep(0.5)  # 礼貌爬取

    return enriched


def generate_pin_text(article: dict, template_index: int = 0) -> str:
    """生成 Pinterest pin 文案"""
    import random
    template = PIN_TEMPLATES[template_index % len(PIN_TEMPLATES)]

    description = article.get("description", "")
    # 截断描述到 200 字符
    if len(description) > 200:
        description = description[:197] + "..."

    return template.format(
        title=article["title"],
        description_short=description,
        url=article["url"],
    )


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="RizzWigs → Buffer → Pinterest 自动发布")
    parser.add_argument("--api-key", help="Buffer API Key")
    parser.add_argument("--discover", action="store_true", help="发现账号和频道信息")
    parser.add_argument("--list", action="store_true", help="列出所有文章（不发布）")
    parser.add_argument("--publish-one", action="store_true", help="发布一篇文章（测试）")
    parser.add_argument("--publish", type=int, help="发布 N 篇文章到队列")
    parser.add_argument("--publish-all", action="store_true", help="发布所有未发布的文章")
    parser.add_argument("--dry-run", action="store_true", help="仅模拟，不真正发布")
    args = parser.parse_args()

    # 加载 API Key
    api_key = args.api_key or os.environ.get("BUFFER_API_KEY")
    config = load_config()
    if not api_key and config.get("api_key"):
        api_key = config["api_key"]

    # --list 不需要 API Key
    if args.list:
        articles = fetch_all_articles()
        print(f"\n📋 文章列表 ({len(articles)} 篇):\n")
        for i, a in enumerate(articles):
            print(f"  {i+1}. {a['title_raw'][:80]}")
            print(f"     {a['url']}")
        print()
        return

    if not api_key and not args.list:
        print("❌ 请提供 Buffer API Key:")
        print("   1. 打开 https://developers.buffer.com/")
        print("   2. 登录并点击 'Get API Key'")
        print("   3. 运行: python buffer_rizzwigs_auto.py --api-key YOUR_KEY --discover")
        sys.exit(1)

    # 保存 API Key
    if api_key and api_key != config.get("api_key"):
        config["api_key"] = api_key
        save_config(config)

    # --discover
    if args.discover:
        result = discover_account(api_key)
        if result:
            config["organization_id"] = result["organization_id"]
            config["pinterest_channel_id"] = result["pinterest_channel_id"]
            save_config(config)
            print("\n✅ 配置已保存到 .buffer_config.json")
        return

    # 需要发布，先确认配置
    channel_id = config.get("pinterest_channel_id")
    if not channel_id:
        print("❌ 未找到 Pinterest Channel ID")
        print("   请先运行: python buffer_rizzwigs_auto.py --api-key YOUR_KEY --discover")
        sys.exit(1)

    posted = load_posted_articles()
    articles = fetch_all_articles()

    # 过滤未发布的
    unpublished = [a for a in articles if a["url"] not in posted]
    print(f"📊 总文章: {len(articles)} | 已发布: {len(posted)} | 待发布: {len(unpublished)}")

    # --publish-one
    if args.publish_one:
        if not unpublished:
            print("✅ 所有文章都已发布!")
            return
        target = unpublished[0]
        print(f"\n📌 发布测试: {target['title_raw'][:80]}")
        detail = extract_article_detail(target["url"])
        if not detail:
            print("❌ 获取文章详情失败")
            return

        pin_text = generate_pin_text(detail)
        print(f"\n--- Pin 内容预览 ---")
        print(pin_text)
        print(f"--- 图片: {detail.get('image_url', '(无)')} ---")

        if args.dry_run:
            print("\n🔍 [DRY RUN] 未实际发布")
        else:
            print("\n🚀 正在发布到 Buffer...")
            result = create_buffer_post(
                api_key, channel_id, pin_text, detail.get("image_url", "")
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))

            if "PostActionSuccess" in str(result):
                posted.add(target["url"])
                save_posted_articles(posted)
                print("✅ 发布成功!")
            else:
                print("❌ 发布失败，请检查上面的错误信息")
        return

    # --publish N
    count = args.publish or (9999 if args.publish_all else 0)
    if count > 0:
        targets = unpublished[:count]
        if not targets:
            print("✅ 所有文章都已发布!")
            return

        print(f"\n📥 正在获取 {len(targets)} 篇文章的详细信息...")
        enriched = enrich_articles(targets)

        print(f"\n🚀 准备发布 {len(enriched)} 篇到 Buffer 队列...")
        success = 0
        for i, article in enumerate(enriched):
            pin_text = generate_pin_text(article, i)
            print(f"\n  [{i+1}/{len(enriched)}] {article['title'][:60]}")

            if args.dry_run:
                print(f"     🔍 [DRY RUN] 跳过")
                success += 1
                continue

            result = create_buffer_post(
                api_key, channel_id, pin_text, article.get("image_url", "")
            )

            if "PostActionSuccess" in str(result):
                posted.add(article["url"])
                save_posted_articles(posted)
                print(f"     ✅ 已加入 Queue")
                success += 1
            else:
                error_msg = str(result)
                print(f"     ❌ 失败: {error_msg[:100]}")

            time.sleep(2)  # API rate limit

        print(f"\n📊 完成: {success}/{len(enriched)} 篇发布成功")

        # 清理记录 (如果已发布数量太大)
        if len(posted) > 500:
            # 只保留最新的 300 条记录
            recent = sorted(posted)[-300:]
            save_posted_articles(set(recent))
            print(f"📝 已清理发布记录（保留最近300条）")


if __name__ == "__main__":
    main()
