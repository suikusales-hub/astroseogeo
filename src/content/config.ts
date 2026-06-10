import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { POST_CATEGORY_SLUGS } from '../data/categories';

const posts = defineCollection({
  loader: glob({
    base: './src/content/posts',
    pattern: '**/*.{md,mdx}',
  }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date(),
    heroImage: z
      .string()
      .regex(
        /^\/images\/(?:[a-z0-9-]+\/)*[a-z0-9-]+\.(avif|webp|png|jpg|jpeg)$/,
        'heroImage must use /images/file-name.ext',
      ),
    category: z.enum(POST_CATEGORY_SLUGS),
    tags: z.array(z.string().min(1)),
  }),
});

export const collections = { posts };
