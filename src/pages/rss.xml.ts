import { getCollection } from 'astro:content';
import { toPostSlug } from '../lib/slug';

const SITE_URL = 'https://seogeo.cc';

export async function GET() {
  const posts = (await getCollection('posts'))
    .sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime())
    .slice(0, 50);

  const items = posts
    .map((post) => {
      const url = `${SITE_URL}/${toPostSlug(post.id)}`;
      return [
        '<item>',
        `<title>${escapeXml(post.data.title)}</title>`,
        `<link>${url}</link>`,
        `<guid>${url}</guid>`,
        `<description>${escapeXml(post.data.description)}</description>`,
        `<pubDate>${post.data.pubDate.toUTCString()}</pubDate>`,
        '</item>',
      ].join('');
    })
    .join('');

  const xml = `<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel><title>SEO小平</title><link>${SITE_URL}</link><description>SEO小平的谷歌 SEO、AI 搜索与内容工程文章。</description>${items}</channel></rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
    },
  });
}

function escapeXml(value: string) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
