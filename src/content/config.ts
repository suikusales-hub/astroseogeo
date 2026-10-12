import { defineCollection } from 'astro:content';
import { file, glob } from 'astro/loaders';
import { load as loadYaml } from 'js-yaml';
import { z } from 'astro/zod';

const imageSchema = z
  .string()
  .regex(
    /^\/images\/.+\.(avif|webp|png|jpe?g|gif|svg)$/i,
    'heroImage must use /images/file-name.ext',
  );

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
    heroImage: imageSchema,
    // Slugs reference the file name of an entry in src/content/categories.
    category: z.string().min(1),
    tags: z.array(z.string().min(1)),
  }),
});

const pages = defineCollection({
  loader: glob({
    base: './src/content/pages',
    pattern: '**/*.{md,mdx}',
  }),
  schema: z.object({
    title: z.string().min(1),
    description: z.string().min(1),
    heroImage: imageSchema.optional(),
  }),
});

const categories = defineCollection({
  loader: glob({
    base: './src/content/categories',
    pattern: '**/*.{yml,yaml}',
  }),
  schema: z.object({
    name: z.string().min(1),
    description: z.string().min(1),
  }),
});

const tags = defineCollection({
  loader: glob({
    base: './src/content/tags',
    pattern: '**/*.{yml,yaml}',
  }),
  schema: z.object({
    name: z.string().min(1),
    description: z.string().optional(),
  }),
});

// Sveltia CMS singletons are flat YAML files (one object of fields).
// The file() loader treats each top-level key as an entry, so we wrap the
// parsed document to expose the fields as a single collection entry.
const singletonYamlLoader = (path: string) =>
  file(path, {
    parser: (text: string) => ({ main: loadYaml(text) }),
  });

const nav = defineCollection({
  loader: singletonYamlLoader('src/data/nav.yml'),
  schema: z.object({
    items: z.array(z.object({ label: z.string(), href: z.string() })),
    ctaLabel: z.string(),
    ctaHref: z.string(),
  }),
});

const footer = defineCollection({
  loader: singletonYamlLoader('src/data/footer.yml'),
  schema: z.object({
    navLinks: z.array(z.object({ label: z.string(), href: z.string() })),
    socialLinks: z.array(
      z.object({ label: z.string(), href: z.string(), icon: z.string() }),
    ),
  }),
});

const sidebar = defineCollection({
  loader: singletonYamlLoader('src/data/sidebar.yml'),
  schema: z.object({
    categoriesTitle: z.string(),
    recommendedTitle: z.string(),
    cta: z
      .object({
        enabled: z.boolean(),
        title: z.string().optional(),
        text: z.string().optional(),
        buttonLabel: z.string().optional(),
        buttonHref: z.string().optional(),
      })
      .optional(),
  }),
});

const blogIndex = defineCollection({
  loader: singletonYamlLoader('src/data/blog-index.yml'),
  schema: z.object({
    title: z.string(),
    description: z.string(),
  }),
});

export const collections = {
  posts,
  pages,
  categories,
  tags,
  nav,
  footer,
  sidebar,
  blog_index: blogIndex,
};