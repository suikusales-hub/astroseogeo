import { getCollection } from 'astro:content';
import { POST_CATEGORIES } from '../data/categories';
import { toPostSlug } from '../lib/slug';

export async function GET() {
  const posts = await getCollection('posts');
  const routes = new Set<string>([
    '/',
    '/about',
    '/contact',
    '/llms.txt',
    '/robots.txt',
    '/rss.xml',
    '/sitemap.xml',
    '/site-routes.json',
  ]);

  for (const category of POST_CATEGORIES) {
    routes.add(`/${category.slug}`);
  }

  for (const post of posts) {
    const slug = toPostSlug(post.id);
    if (slug) {
      routes.add(`/${slug}`);
    }
  }

  return new Response(JSON.stringify({ routes: Array.from(routes).sort() }), {
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'public, max-age=300',
    },
  });
}
