#!/usr/bin/env python3
"""
批量发布 RizzWigs 文章到 Buffer Pinterest (使用 curl 避免 Python 网络问题)
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

API_KEY = "HhSHpRTBmZ7GOYeDGRsmOjeFqj3Sjq4aB1nZuXpZNU0"
CHANNEL_ID = "6a6c52e24b2d03035f73d0d6"
PINTEREST_BOARD_ID = "1092474890799708177"  # Lace Front Wigs board
API_URL = "https://api.buffer.com/graphql"
POSTED_FILE = Path(__file__).parent / ".buffer_posted_articles.json"

QUERY = """
mutation($text:String!,$channelId:ChannelId!,$mode:ShareMode!,$assets:[AssetInput!]!,$meta:PostInputMetaData!) {
  createPost(input:{text:$text,channelId:$channelId,schedulingType:automatic,mode:$mode,assets:$assets,metadata:$meta}) {
    ... on PostActionSuccess { post { id text dueAt } }
    ... on MutationError { message }
  }
}
"""


def curl_fetch(url: str) -> str:
    """使用 curl 获取 URL 内容"""
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "20", url],
        capture_output=True, text=True
    )
    return result.stdout


def curl_post(payload: str) -> str:
    """使用 curl 发送 POST 请求"""
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", API_URL,
         "-H", f"Authorization: Bearer {API_KEY}",
         "-H", "Content-Type: application/json",
         "-d", payload,
         "--max-time", "20"],
        capture_output=True, text=True
    )
    return result.stdout


def get_all_article_urls():
    """获取所有文章 URL"""
    blog_pages = [
        "https://rizzwigs.com/blog-list-1.html",
        "https://rizzwigs.com/blog-list-2.html",
        "https://rizzwigs.com/blog-list-3.html",
        "https://rizzwigs.com/blog-list-4.html",
        "https://rizzwigs.com/blog-list-5.html",
    ]
    urls = set()
    for page in blog_pages:
        try:
            html = curl_fetch(page)
            matches = re.findall(r'href="(/[a-z0-9][^"]*\.html)"', html)
            for m in matches:
                skip = ["product-category", "blog-list", "categories",
                        "blog-categories", "hot-wigs", "wig-article-index"]
                if not any(s in m for s in skip):
                    urls.add(f"https://rizzwigs.com{m}")
        except Exception as e:
            print(f"  ⚠️ {page}: {e}")
    return sorted(urls)


def extract_article(html: str) -> dict:
    """从 HTML 提取文章信息"""
    # 标题
    title_m = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not title_m:
        title_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ""

    # 描述
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    desc = desc_m.group(1) if desc_m else ""

    # 图片
    img_url = ""
    og_m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    if og_m and og_m.group(1):
        img_url = og_m.group(1)
    else:
        imgs = re.findall(r'<img[^>]*src="(/uploads/[^"]+)"[^>]*>', html)
        for img_tag in imgs:
            full_src = f"https://rizzwigs.com{img_tag}"
            if "Jesica" in full_src:
                continue
            img_url = full_src
            break

    return {"title": title, "description": desc, "image_url": img_url}


def load_posted() -> set:
    if POSTED_FILE.exists():
        return set(json.loads(POSTED_FILE.read_text(encoding="utf-8")))
    return set()


def save_posted(urls: set):
    POSTED_FILE.write_text(json.dumps(sorted(urls), indent=2), encoding="utf-8")


def publish_articles(count: int):
    """发布 count 篇文章"""
    all_urls = get_all_article_urls()
    posted = load_posted()
    unpublished = [u for u in all_urls if u not in posted]

    print(f"📊 Total: {len(all_urls)} | Posted: {len(posted)} | Remaining: {len(unpublished)}")

    targets = unpublished[:count]
    if not targets:
        print("✅ All articles published!")
        return

    success = 0
    for i, url in enumerate(targets):
        slug = url.split("/")[-1].replace(".html", "").replace("-", " ")[:50]
        print(f"\n[{i+1}/{count}] {slug}")

        # 获取文章
        html = curl_fetch(url)
        if not html:
            print("  ⚠️ Failed to fetch")
            continue

        article = extract_article(html)
        if not article["title"]:
            print("  ⚠️ No title found")
            continue

        # 生成 Pin 文案
        desc = article["description"]
        desc_short = desc[:180] + ("..." if len(desc) > 180 else "")
        text = f"{article['title']}\n\n{desc_short}\n\nRead more 👇\n{url}\n\n#wigs #hairtips #wigguide"

        print(f"  📝 {article['title'][:60]}")
        print(f"  🖼️  {article['image_url'][:60] or '(no image)'}")

        # 构建请求
        payload = json.dumps({
            "query": QUERY,
            "variables": {
                "text": text,
                "channelId": CHANNEL_ID,
                "mode": "addToQueue",
                "assets": [{"image": {"url": article["image_url"]}}] if article["image_url"] else [],
                "meta": {
                    "pinterest": {
                        "boardServiceId": PINTEREST_BOARD_ID,
                        "title": article["title"],
                        "url": url
                    }
                }
            }
        })

        # 发布
        result = curl_post(payload)
        try:
            data = json.loads(result)
        except:
            print(f"  ❌ Parse error: {result[:100]}")
            continue

        create_result = data.get("data", {}).get("createPost", {})
        if "errors" in data:
            err_msg = data["errors"][0].get("message", str(data["errors"]))
            print(f"  ❌ {err_msg[:120]}")
        elif create_result.get("post"):
            post_id = create_result["post"]["id"]
            due = create_result["post"].get("dueAt", "unknown")
            print(f"  ✅ Queued! ID: {post_id} @ {due}")
            posted.add(url)
            save_posted(posted)
            success += 1
        elif create_result.get("message"):
            print(f"  ❌ {create_result['message'][:120]}")
        else:
            print(f"  ❌ Unexpected: {str(data)[:120]}")

        time.sleep(2)

    print(f"\n📊 Done: {success}/{count} published")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    publish_articles(count)
