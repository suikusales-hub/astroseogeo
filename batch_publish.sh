#!/bin/bash
# 批量发布 RizzWigs 文章到 Buffer Pinterest
# Usage: bash batch_publish.sh [count]

API_KEY="HhSHpRTBmZ7GOYeDGRsmOjeFqj3Sjq4aB1nZuXpZNU0"
CHANNEL_ID="6a6c52e24b2d03035f73d0d6"
API_URL="https://api.buffer.com/graphql"
COUNT="${1:-5}"
POSTED_FILE="$(dirname "$0")/.buffer_posted_articles.json"

# 获取文章列表
echo "📥 正在抓取文章列表..."
ARTICLES_RAW=$(curl -s "https://rizzwigs.com/blog-list-1.html" "https://rizzwigs.com/blog-list-2.html" "https://rizzwigs.com/blog-list-3.html" "https://rizzwigs.com/blog-list-4.html" "https://rizzwigs.com/blog-list-5.html" | grep -oP 'href="(/[a-z0-9][^"]*\.html)"' | sed 's/href="//;s/"//' | grep -v 'product-category\|blog-list\|categories\|blog-categories\|hot-wigs\|wig-article-index' | sort -u)

# 加载已发布列表
POSTED="[]"
[ -f "$POSTED_FILE" ] && POSTED=$(cat "$POSTED_FILE")

SUCCESS=0
CURRENT=0

while IFS= read -r path; do
  URL="https://rizzwigs.com$path"
  
  # 检查是否已发布
  if echo "$POSTED" | grep -qF "$URL"; then
    continue
  fi
  
  CURRENT=$((CURRENT + 1))
  if [ $CURRENT -gt $COUNT ]; then
    break
  fi
  
  echo ""
  echo "  [$CURRENT/$COUNT] Fetching $URL..."
  
  # 获取文章详情
  HTML=$(curl -sL "$URL" 2>/dev/null)
  TITLE=$(echo "$HTML" | grep -oP '<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>\K[^<]+' | head -1)
  [ -z "$TITLE" ] && TITLE=$(echo "$HTML" | grep -oP '<h1[^>]*>\K[^<]+' | head -1)
  DESC=$(echo "$HTML" | grep -oP '<meta\s+name="description"\s+content="\K[^"]+' | head -1)
  
  # 找图片
  IMG=$(echo "$HTML" | grep -oP 'src="(/uploads/[^"]+)"' | grep -v 'Jesica\|height="70"' | head -1 | sed 's/src="//;s/"//')
  [ -n "$IMG" ] && IMG="https://rizzwigs.com$IMG"
  
  # 截断描述
  DESC_SHORT="${DESC:0:180}"
  [ ${#DESC} -gt 180 ] && DESC_SHORT="${DESC_SHORT}..."
  
  # 生成 Pin 文案
  TEXT="$TITLE

${DESC_SHORT}

Read more 👇
$URL

#wigs #hairtips #wigguide"
  
  echo "     Title: ${TITLE:0:60}"
  echo "     Image: ${IMG:-none}"
  
  # 构建 JSON
  PAYLOAD=$(jq -n --arg text "$TEXT" --arg ch "$CHANNEL_ID" --arg img "$IMG" '{
    query: "mutation($text:String!,$channelId:ChannelId!,$mode:ShareMode!,$assets:[AssetInput!]!){createPost(input:{text:$text,channelId:$channelId,schedulingType:automatic,mode:$mode,assets:$assets}){...on PostActionSuccess{post{id text dueAt}}...on MutationError{message}}}",
    variables: {
      text: $text,
      channelId: $ch,
      mode: "addToQueue",
      assets: [ { image: { url: $img } } ]
    }
  }')
  
  # 发布
  RESULT=$(curl -s -X POST "$API_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" 2>&1)
  
  if echo "$RESULT" | grep -q '"post"'; then
    POST_ID=$(echo "$RESULT" | grep -oP '"id":"[^"]+"' | head -1 | cut -d'"' -f4)
    echo "     ✅ Queued! ID: $POST_ID"
    SUCCESS=$((SUCCESS + 1))
    # 记录已发布
    echo "$URL" >> "${POSTED_FILE}.tmp"
  else
    ERR=$(echo "$RESULT" | grep -oP '"message":"[^"]+"' | head -1)
    echo "     ❌ Failed: $ERR"
  fi
  
  sleep 2
done <<< "$ARTICLES_RAW"

# 更新已发布列表
if [ -f "${POSTED_FILE}.tmp" ]; then
  cat "${POSTED_FILE}.tmp" >> "$POSTED_FILE" 2>/dev/null
  rm "${POSTED_FILE}.tmp"
fi

echo ""
echo "📊 Done: $SUCCESS/$COUNT published successfully"
