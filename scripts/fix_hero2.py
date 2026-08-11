import re
from pathlib import Path

posts_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\src\content\posts")
public_dir = Path(r"E:\CodexChatGPTMigrated\SEOGEO\public")

for f in sorted(posts_dir.glob("2026-*.md")):
    text = f.read_text(encoding='utf-8')
    hero_m = re.search(r'^heroImage:\s*"([^"]+)"', text, re.M)
    if hero_m:
        hero = hero_m.group(1)
        needs_fix = False
        if hero.startswith('http'):
            needs_fix = True
        elif hero.startswith('/images/'):
            local_path = public_dir / hero.lstrip('/')
            if not local_path.exists():
                needs_fix = True
        if needs_fix:
            text = re.sub(r'^heroImage: ".*"', 'heroImage: "/images/default-post.png"', text, flags=re.M)
            f.write_text(text, encoding='utf-8')
            print(f"FIXED: {f.stem}")
        else:
            print(f"OK: {f.stem}")
