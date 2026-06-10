import { getCollection } from 'astro:content';
import { POST_CATEGORIES } from '../data/categories';
import { toPostSlug } from '../lib/slug';

const SITE_URL = 'https://seogeo.cc';

const STATIC_ROUTES = [
  { path: '/', priority: '1.0', changefreq: 'weekly' },
  { path: '/about', priority: '0.5', changefreq: 'monthly' },
  { path: '/contact', priority: '0.5', changefreq: 'monthly' },
  { path: '/rss.xml', priority: '0.3', changefreq: 'weekly' },
];

export async function GET() {
  const posts = await getCollection('posts');
  const categoryRoutes = POST_CATEGORIES.map((category) => ({
    path: `/${category.slug}`,
    priority: '0.8',
    changefreq: 'weekly',
  }));

  const postRoutes = posts
    .map((post) => ({
      path: `/${toPostSlug(post.id)}`,
      lastmod: post.data.updatedDate.toISOString(),
      priority: '0.7',
      changefreq: 'monthly',
    }))
    .sort((a, b) => a.path.localeCompare(b.path));

  const entries = [...STATIC_ROUTES, ...categoryRoutes, ...postRoutes]
    .map((route) => {
      const url = new URL(route.path, SITE_URL).toString();
      return [
        '  <url>',
        `    <loc>${escapeXml(url)}</loc>`,
        route.lastmod ? `    <lastmod>${route.lastmod}</lastmod>` : '',
        `    <changefreq>${route.changefreq}</changefreq>`,
        `    <priority>${route.priority}</priority>`,
        '  </url>',
      ]
        .filter(Boolean)
        .join('\n');
    })
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}\n</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
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
