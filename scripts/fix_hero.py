import re
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
public_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public")

for f in sorted(posts_dir.glob("2026-*.md")):
    text = f.read_text(encoding='utf-8')
    hero_m = re.search(r'^heroImage:\s*"(/images/[^"]+)"', text, re.M)
    if hero_m:
        hero = hero_m.group(1)
        local_path = public_dir / hero.lstrip('/')
        if not local_path.exists():
            text = re.sub(r'^heroImage: ".*"', 'heroImage: "/images/default-post.png"', text, flags=re.M)
            f.write_text(text, encoding='utf-8')
            print(f"FALLBACK: {f.stem}")
        else:
            print(f"OK: {f.stem} -> {hero}")
