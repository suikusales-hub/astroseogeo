import re
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
targets = [f.stem for f in posts_dir.glob("2026-ai-*.md")]
targets += [f.stem for f in posts_dir.glob("2026-article-*.md")]
targets += [f.stem for f in posts_dir.glob("2026-seo-*.md")]

# List of div IDs that are WeChat UI overlay junk
wechat_dialog_ids = [
    "js_tags_preview_toast",
    "content_bottom_area",
    "font_pannel_area",
    "js_temp_bottom_area",
    "js_claim_source_content",
    "sg_tj",
    "page_bottom_area",
    "js_pc_qr_code",
    "js_related_news_flow_area",
    "js_network_msg_wrp",
    "js_ad_control",
    "audio_panel_area",
    "js_profile_card_modal",
    "js_emotion_panel_pc",
    "js_alert_panel",
    "js_pc_weapp_code",
    "js_minipro_dialog",
    "js_link_dialog",
    "js_product_dialog",
    "js_analyze_btn",
    "js_jump_wx_qrcode_dialog",
    "js_alert_content",
]

for slug in targets:
    p = posts_dir / f"{slug}.md"
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    old = len(text)

    # Remove <div id="xxx">...</div> blocks for known WeChat IDs
    for div_id in wechat_dialog_ids:
        # Match <div id="div_id" ...> up to matching </div>
        pattern = r'<div\s[^>]*\bid\s*=\s*["\']' + re.escape(div_id) + r'["\'][^>]*>'
        for div_start in re.finditer(pattern, text):
            pos = div_start.start()
            depth = 0
            i = pos
            while i < len(text):
                if text[i:i+4] == '<div':
                    depth += 1
                    i += 4
                elif text[i:i+5] == '</div':
                    depth -= 1
                    if depth == 0:
                        # Found closing tag
                        text = text[:pos] + text[i+6:]
                        break
                    i += 6
                else:
                    i += 1
            else:
                continue  # no match found, skip

    # Remove <ul id="js_emotion_list_pc">...</ul>
    text = re.sub(r'<ul\s[^>]*\bid\s*=\s*["\']js_emotion_list_pc["\'][^>]*>.*?</ul>', '', text, flags=re.DOTALL)

    # Remove <style>.weui-dialog_link...</style> blocks
    text = re.sub(r'<style>.*?weui-dialog_link.*?</style>', '', text, flags=re.DOTALL)

    # Remove orphaned WeChat text lines
    wechat_texts = [
        '预览时标签不可点',
        '微信扫一扫 关注该公众号',
        '知道了',
        '微信扫一扫',
        '取消',
        '允许',
    ]
    lines = text.split('\n')
    kept = []
    for line in lines:
        s = line.strip()
        skip = False
        for wt in wechat_texts:
            if s == wt or s == f'<span>{wt}</span>' or s == f'<a [^>]*>{wt}</a>' or wt in s and len(s) < 30:
                skip = True
                break
        if not skip:
            kept.append(line)
    text = '\n'.join(kept)

    # Remove empty div chains at the end
    text = re.sub(r'(</div>\s*){4,}$', '', text)
    text = re.sub(r'\n{4,}', '\n\n', text)
    text = text.rstrip() + '\n'

    if len(text) != old:
        p.write_text(text, encoding='utf-8')
        print(f"Cleaned: {slug} ({old - len(text)} chars removed)")
    else:
        print(f"Skip: {slug} (nothing found)")
