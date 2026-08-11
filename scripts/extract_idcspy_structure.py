import re, json

with open('/tmp/idcspy_94799.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find the article content area
m = re.search(r'<article[^>]*>(.*?)</ar...[truncated]