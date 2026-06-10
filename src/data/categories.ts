export const POST_CATEGORY_SLUGS = [
  'seo-tutorial',
  'google-algorithm',
  'ai-geo',
  'multilingual-seo',
  'website-building',
  'keyword-content',
  'technical-seo',
  'case-study',
] as const;

export type PostCategorySlug = (typeof POST_CATEGORY_SLUGS)[number];

export const POST_CATEGORIES: Array<{
  slug: PostCategorySlug;
  name: string;
  description: string;
}> = [
  {
    slug: 'seo-tutorial',
    name: 'SEO基础教程',
    description: '谷歌 SEO、独立站 SEO、B2B/B2C 出海流量的基础方法与实操框架。',
  },
  {
    slug: 'google-algorithm',
    name: '谷歌算法更新',
    description: 'Google 核心算法、排名机制、SERP 变化与应对策略。',
  },
  {
    slug: 'ai-geo',
    name: 'AI与GEO',
    description: 'AI 搜索、GEO、ChatGPT、Gemini、Codex 与生成式流量机会。',
  },
  {
    slug: 'multilingual-seo',
    name: '小语种SEO',
    description: '纯血版小语种独立站、海外蓝海市场与多语言 SEO 实战。',
  },
  {
    slug: 'website-building',
    name: '独立站建站',
    description: 'WordPress、Shopify、服务器、主题、建站流程与站点架构。',
  },
  {
    slug: 'keyword-content',
    name: '关键词与内容',
    description: '关键词研究、内容策略、SEO 文章写作与内容工程 SOP。',
  },
  {
    slug: 'technical-seo',
    name: '技术SEO工具',
    description: 'GSC、Screaming Frog、robots.txt、站点地图、收录与技术诊断。',
  },
  {
    slug: 'case-study',
    name: '案例与陪跑',
    description: '学员案例、培训复盘、线下活动、真实询盘与订单增长故事。',
  },
];

export function getPostCategory(slug: string) {
  return POST_CATEGORIES.find((category) => category.slug === slug);
}
