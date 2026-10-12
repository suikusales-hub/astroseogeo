import { getCollection } from 'astro:content';
import { toPostSlug } from '../lib/slug';

export async function GET() {
  const posts = await getCollection('posts');
  const categories = await getCollection('categories');
  const pages = await getCollection('pages');
  const routes = new Set<string>([
    '/',
    '/about',
    '/blog',
    '/contact',
    '/admin',
    '/llms.txt',
    '/robots.txt',
    '/rss.xml',
    '/sitemap.xml',
    '/site-routes.json',
  ]);

  for (const category of categories) {
    if (category.id) {
      routes.add(`/${category.id}`);
    }
  }

  for (const page of pages) {
    if (page.id) {
      routes.add(`/p/${page.id}`);
    }
  }

  const tagNames = new Set<string>();

  for (const post of posts) {
    for (const tag of post.data.tags) {
      tagNames.add(tag);
    }
    const slug = toPostSlug(post.id);
    if (slug) {
      routes.add(`/${slug}`);
    }
  }

  for (const tag of tagNames) {
    routes.add(`/tag/${encodeURIComponent(tag)}`);
  }

  return new Response(JSON.stringify({ routes: Array.from(routes).sort() }), {
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'public, max-age=300',
    },
  });
}