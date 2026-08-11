from pathlib import Path
import re

BASE = Path(r'C:\Users\Administrator\Documents\SEOGEO\src\content\posts')

updates = {
    '2025-05-10-sitemap-seo-html-xml-txt': {
        'description': '系统拆解 HTML、XML、TXT 三类站点地图的作用、适用场景与提交方式，帮助独立站避免收录入口混乱，提升谷歌抓取效率。',
        'tags': ['HTML站点地图', 'XML Sitemap', 'TXT站点地图', '技术SEO', '谷歌收录', '独立站地图'],
    },
    '2025-05-07-independent-site-traffic-case-study-coaching': {
        'description': '复盘陪跑学员独立站流量暴涨 20 倍的真实路径，重点拆解关键词捕鱼模式、内容执行节奏与低成本 SEO 增长方法。',
        'tags': ['SEO流量案例', '陪跑学员案例', '独立站增长', '关键词捕鱼模式', '自然流量提升', 'SEO实战复盘'],
    },
    '2025-11-23-foreign-trade-coaching-seo-geo': {
        'description': '记录第八期外贸 SEO+GEO 陪跑课的核心内容，涵盖外贸独立站、AI 搜索优化、实操训练与一年陪跑赋能安排。',
        'tags': ['外贸SEO陪跑', 'GEO培训', 'AI搜索优化', '深圳SEO课程', '跨境独立站', 'SEO实战训练'],
    },
    '2025-11-20-multilingual-native-gemini-3-ai-seo': {
        'description': '结合 Gemini 3 能力升级，分析 AI 原生写作对纯血小语种 SEO 的影响，以及外贸独立站如何提升本地化内容质量。',
        'tags': ['Gemini 3', 'AI小语种SEO', '纯血小语种', '本地化内容', 'AI原生写作', '外贸SEO'],
    },
    '2025-10-04-guide-ai-2025-geo': {
        'description': '面向 2025 年 AI 搜索趋势，讲清 GEO 的价值、适用行业、执行步骤与投入判断，帮助独立站提前布局生成式流量。',
        'tags': ['2025 GEO指南', '生成式引擎优化', 'AI搜索流量', 'ChatGPT SEO', 'Gemini优化', '品牌曝光'],
    },
    '2025-10-14-foreign-trade-multilingual-seo': {
        'description': '从外贸市场竞争和关税变化出发，分析小语种 SEO 为什么是新蓝海，以及企业如何用独立站避开英语红海。',
        'tags': ['外贸小语种SEO', '小语种蓝海', '非英语市场', '本地化独立站', '跨境流量', '外贸增长'],
    },
    '2025-04-12-gsc-webp': {
        'description': '针对 GSC 中 WebP 图片显示“已抓取未索引”的问题，解释原因、是否需要屏蔽，以及图片 SEO 的正确处理方式。',
        'tags': ['GSC WebP', '图片未索引', 'WebP SEO', '谷歌搜索控制台', '图片抓取', '技术SEO排查'],
    },
    '2025-04-14-google-seo': {
        'description': '盘点新手和老手都容易犯的 Google SEO 错误，包括关键词调研、页面布局、收录判断和执行节奏，帮你少走弯路。',
        'tags': ['Google SEO错误', 'SEO避坑', '关键词调研误区', '独立站优化', '新手SEO', 'SEO经验复盘'],
    },
    '2025-04-30-google-link-building-seo': {
        'description': '围绕 Google 外链建设讲清白帽链接、资源选择、风险识别和权重提升逻辑，适合外贸独立站制定安全外链策略。',
        'tags': ['Google外链', '白帽外链', '外链建设策略', '独立站权重', 'SEO链接资源', '外贸SEO'],
    },
    '2025-05-05-strategy-seo': {
        'description': '阐述长尾词为什么是 SEO 最稳的策略，并用 SEO 小平的捕鱼模式解释如何广撒网、多布局、低成本获取精准流量。',
        'tags': ['长尾词策略', 'SEO捕鱼模式', '关键词布局', '低竞争关键词', '自然搜索流量', '独立站SEO策略'],
    },
    '2025-05-04-keyword-tools-ai-seo-semrush-ahrefs': {
        'description': '比较 Semrush、Ahrefs 与 Gemini 在关键词调研中的优缺点，帮助独立站团队判断哪些数据可信、如何组合使用。',
        'tags': ['Semrush关键词', 'Ahrefs关键词', 'Gemini关键词调研', 'AI SEO工具', '关键词数据判断', 'SEO工具对比'],
    },
    '2025-04-18-independent-site-seo': {
        'description': '从用户洞察、关键词调研和页面内容出发，说明独立站 SEO 的底层逻辑，适合外贸老板理解白帽 SEO 怎么真正见效。',
        'tags': ['独立站SEO逻辑', '白帽SEO', '用户搜索意图', '外贸网站优化', '关键词洞察', 'SEO基础方法'],
    },
    '2025-04-20-multilingual-google-seo': {
        'description': '讲解多语言 Google SEO 的核心难点，包括翻译、本地关键词、页面结构和国家市场选择，避免只做机器翻译站。',
        'tags': ['多语言Google SEO', '小语种独立站', '本地关键词', '多语种页面结构', '外贸多语言', '国际SEO'],
    },
    '2025-05-03-independent-site-hosting': {
        'description': '面向外贸独立站新手，拆解 SiteGround、Hostinger 等主机选择逻辑，说明速度、稳定性、预算与 SEO 的关系。',
        'tags': ['独立站主机', '外贸网站服务器', 'SiteGround', 'Hostinger', '网站速度SEO', '建站托管'],
    },
    '2025-06-10-independent-site-inquiry-107-7': {
        'description': '复盘独立站拿到 107 个询盘的增长案例，分析页面、关键词、内容和小语种布局如何共同推动外贸询盘转化。',
        'tags': ['独立站询盘', '107个询盘案例', '外贸转化', 'SEO询盘增长', '小语种布局', 'B2B独立站'],
    },
    '2025-07-11-inquiry-writing-content-guide-100-seo': {
        'description': '围绕“如何写出带询盘的 SEO 内容”，拆解 100 分内容标准、用户问题覆盖、转化引导和外贸文章写作细节。',
        'tags': ['询盘型内容', 'SEO文章写作', '外贸内容营销', '100分内容', '转化文案', '谷歌内容优化'],
    },
    '2025-07-16-google-seo-sem': {
        'description': '对比 Google SEO 与 SEM 的获客逻辑、成本结构和适用阶段，帮助外贸企业判断自然流量与广告投放如何配合。',
        'tags': ['Google SEO vs SEM', '谷歌广告', '自然流量', '付费获客', '外贸推广', 'SEO SEM组合'],
    },
    '2025-09-18-seo-c': {
        'description': '从 C 端独立站视角讲解 SEO 增长方法，覆盖选品内容、长尾词、页面体验和转化链路，适合跨境电商卖家参考。',
        'tags': ['C端SEO', '跨境电商SEO', 'C端独立站', '选品内容', '长尾流量', '电商转化'],
    },
    '2025-08-15-google-independent-site-content-seo-freshness': {
        'description': '解释 Google 为什么重视内容新鲜度，独立站文章如何更新、补充案例和维护旧页面，避免内容长期不动影响排名。',
        'tags': ['内容新鲜度', 'Google内容更新', '旧文章维护', '独立站内容SEO', 'Freshness算法', '页面更新策略'],
    },
    '2025-07-14-independent-site-guide': {
        'description': '给外贸独立站新手的一份建站与 SEO 入门指南，梳理域名、主机、内容、关键词、收录和长期运营的关键步骤。',
        'tags': ['独立站指南', '外贸建站入门', 'SEO入门流程', '域名主机', '网站收录', '长期运营'],
    },
    '2025-06-11-google-ranking-6-14-15-seo': {
        'description': '记录 6 月 14-15 日 SEO 实战分享重点，围绕 Google 排名、小语种避红海和关键词捕鱼模式展开具体方法。',
        'tags': ['Google排名', 'SEO实战分享', '小语种避红海', '关键词捕鱼', '线下课程', '独立站排名'],
    },
    '2025-06-05-indexing-website-google-90': {
        'description': '围绕网站 90 天收录与排名观察，分析 Google 索引节奏、内容质量、站点结构和新站冷启动的实际表现。',
        'tags': ['Google收录90天', '新站索引', '网站冷启动', '收录观察', 'SEO周期', '独立站排名'],
    },
    '2025-05-21-robots-txt': {
        'description': '讲清 robots.txt 的正确写法、常见误区和 SEO 影响，帮助独立站避免误屏蔽重要页面或浪费谷歌抓取预算。',
        'tags': ['robots.txt', '抓取预算', '谷歌爬虫', '技术SEO配置', '页面屏蔽', '独立站robots'],
    },
    '2025-05-26-google-ai-mode-seo-vip': {
        'description': '解读 Google AI Mode 对 SEO 的影响，重点分析查询扇出、长尾内容覆盖和 GEO 布局如何改变独立站流量入口。',
        'tags': ['Google AI Mode', '查询扇出', 'AI搜索SEO', 'GEO布局', '长尾内容覆盖', 'AI时代流量'],
    },
    '2025-05-22-google-ai-mode-serp': {
        'description': '从 SERP 变化角度分析 Google AI Mode，说明 AI 摘要、引用机会和内容结构如何影响未来自然搜索点击。',
        'tags': ['AI Mode SERP', '谷歌AI搜索结果', 'AI摘要', 'SERP变化', '内容引用', '搜索点击率'],
    },
    '2025-06-25-code-theme-wordpress': {
        'description': '围绕 WordPress 主题代码和 SEO 结构优化，说明模板、速度、代码干净度与搜索表现之间的关系。',
        'tags': ['WordPress主题代码', 'WordPress SEO', '主题优化', '代码结构', '网站速度', '模板SEO'],
    },
    '2025-06-04-independent-site-website-building': {
        'description': '分享独立站建站的实战思路，从工具选择、页面结构、SEO 基础到后续运营，帮助新手避免只建不推广。',
        'tags': ['独立站建站', '外贸网站建设', '建站实战', 'SEO基础配置', '页面结构', '网站运营'],
    },
    '2025-07-01-google-algorithm-ranking-seo-15': {
        'description': '结合 Google 算法和排名波动，分析 15 个影响独立站 SEO 的关键因素，帮助站长判断问题出在哪里。',
        'tags': ['Google算法', '排名波动', 'SEO排名因素', '算法更新', '独立站诊断', '搜索排名'],
    },
    '2025-05-19-coaching-seo-3-2-1': {
        'description': '总结 3 天 2 夜 SEO 陪跑课程的训练内容，包括关键词实操、AI 写作、外贸案例和纯血小语种 SEO SOP。',
        'tags': ['SEO陪跑课程', '3天2夜培训', '关键词实操', 'AI写作训练', '小语种SOP', '外贸SEO学习'],
    },
    '2025-04-29-foreign-trade-coaching-multilingual-2-1': {
        'description': '介绍外贸小语种 SEO 陪跑 2.1 版本思路，聚焦团队配置、AI 使用、本地化内容和多语言独立站执行流程。',
        'tags': ['外贸陪跑', '小语种SEO培训', '多语言独立站', 'AI内容流程', '团队配置', '本地化执行'],
    },
    '2025-09-30-seo-700-350': {
        'description': '围绕 700 与 350 等流量或页面数据展开 SEO 复盘，分析小站如何通过内容矩阵和关键词策略提高产出效率。',
        'tags': ['SEO数据复盘', '内容矩阵', '页面效率', '关键词策略', '流量增长', '独立站案例'],
    },
    '2025-10-03-seo-2025': {
        'description': '面向 2025 年 SEO 趋势，梳理 AI 搜索、内容质量、品牌信任和小语种市场对独立站运营的影响。',
        'tags': ['2025 SEO趋势', 'AI搜索趋势', '内容质量', '品牌信任', '小语种市场', '独立站运营'],
    },
    '2025-03-23-indexing-mistakes-website-seo': {
        'description': '总结网站收录常见错误，包括页面质量、内链、robots、sitemap 和重复内容问题，帮助独立站提高索引率。',
        'tags': ['网站收录错误', '索引率提升', 'sitemap问题', '内链优化', '重复内容', '收录诊断'],
    },
    '2025-03-24-deepseek': {
        'description': '分析 DeepSeek 对独立站 SEO 和内容生产的实际价值，讨论 AI 写作、关键词扩展和低成本建站运营机会。',
        'tags': ['DeepSeek SEO', 'AI内容生产', '关键词扩展', '低成本运营', 'AI建站', '独立站工具'],
    },
    '2025-03-20-google-algorithm-seo': {
        'description': '从谷歌算法更新带来的流量波动出发，讲解独立站如何通过多站布局、小语种市场和白帽策略降低风险。',
        'tags': ['谷歌算法更新', '流量波动', '白帽SEO策略', '多站布局', '风险分散', '小语种SEO'],
    },
    '2025-03-19-google-algorithm-traffic-multilingual-3-seo': {
        'description': '结合 3 月谷歌算法与小语种流量变化，分析多语言独立站如何应对排名波动并维持稳定自然流量。',
        'tags': ['3月算法更新', '多语言流量', '排名波动应对', '小语种独立站', '自然流量稳定', 'Google SEO'],
    },
    '2025-03-31-google-seo': {
        'description': '围绕 Google SEO 实战经验，梳理关键词、内容、收录和排名之间的关系，帮助新手建立正确优化顺序。',
        'tags': ['Google SEO实战', '优化顺序', '关键词内容', '收录排名', 'SEO新手', '独立站优化'],
    },
    '2025-03-29-website-screaming-frog-seo-spider': {
        'description': '介绍 Screaming Frog SEO Spider 在网站诊断中的用法，覆盖抓取、死链、标题描述、内链和技术问题排查。',
        'tags': ['Screaming Frog', 'SEO Spider', '网站诊断', '死链检查', '标题描述检查', '技术SEO工具'],
    },
    '2025-03-06-ai': {
        'description': '讨论 AI 对独立站 SEO 的改变，包括内容生产、关键词研究、建站效率和普通外贸人使用 AI 的实际路径。',
        'tags': ['AI与SEO', 'AI内容工具', 'AI建站效率', '外贸AI应用', '关键词研究AI', '独立站自动化'],
    },
    '2025-02-10-independent-site-multilingual-seo-ai': {
        'description': '讲解 AI 如何辅助外贸独立站做多语言 SEO，从小语种市场选择、内容生成到本地化校验，形成可执行流程。',
        'tags': ['AI多语言SEO', '外贸小语种', '多语言内容生成', '本地化校验', '独立站AI流程', '海外市场'],
    },
    '2025-02-11-independent-site-case-study-multilingual-50': {
        'description': '复盘 50.2 万曝光量的小语种独立站案例，分析 AI+多语言 SEO 如何降低执行成本并带来真实搜索增长。',
        'tags': ['50万曝光案例', '小语种案例', 'AI多语言站', 'GSC曝光', '独立站增长案例', '多语言SEO实战'],
    },
    '2025-02-26-independent-site-case-study-multilingual-seo': {
        'description': '继续拆解小语种独立站成功案例，重点说明关键词捕鱼、AI 内容、团队 SOP 与外贸询盘之间的协同关系。',
        'tags': ['小语种成功案例', '关键词捕鱼实操', 'AI内容SOP', '外贸询盘', '多语言增长', '独立站案例'],
    },
    '2025-03-01-case-study-multilingual-native-b2b': {
        'description': '从 B2B 视角分析纯血小语种独立站案例，关注关键词难度、市场空白、内容本地化和企业询盘机会。',
        'tags': ['B2B小语种案例', '纯血小语种B2B', '关键词难度', '市场空白', '内容本地化', 'B2B询盘'],
    },
    '2026-02-02-traffic-website-seo-moltbot': {
        'description': '分析 Moltbot、Clawdbot 等 AI 爬虫带来的网站流量变化，讨论独立站如何识别机器人访问与真实 SEO 增长。',
        'tags': ['Moltbot流量', 'AI爬虫', 'Clawdbot', '机器人访问', 'SEO流量判断', '网站日志'],
    },
    '2026-02-03-traffic-seo': {
        'description': '围绕网站流量与 SEO 结果判断，讲解如何区分有效自然流量、异常访问和真正能带来询盘的关键词增长。',
        'tags': ['SEO流量判断', '自然流量质量', '异常访问', '询盘关键词', '流量分析', '独立站数据'],
    },
    '2026-01-09-google-b-seo-c': {
        'description': '对比 Google B 端与 C 端 SEO 的差异，说明关键词、内容深度、转化路径和独立站页面结构应该如何调整。',
        'tags': ['B端SEO', 'C端SEO', 'B2B关键词', 'C端转化', '页面结构', 'Google优化'],
    },
    '2026-01-06-google-traffic-reddit': {
        'description': '分析 Reddit 在 Google 搜索流量中的曝光变化，讨论独立站内容如何借鉴社区问答，提高真实用户需求覆盖。',
        'tags': ['Reddit搜索流量', 'Google社区内容', '用户需求覆盖', '问答内容SEO', '社区SEO', '内容策略'],
    },
    '2025-12-02-traffic-118-2025-geo': {
        'description': '复盘 2025 年 GEO 与 SEO 带来的 118 个流量或询盘节点，分析 AI 搜索时代独立站获客路径的变化。',
        'tags': ['118流量复盘', '2025 GEO', 'AI搜索获客', 'SEO询盘', '独立站增长', 'GEO案例'],
    },
    '2025-11-26-multilingual-native-seo': {
        'description': '系统说明纯血版小语种 SEO 的核心标准，强调一站一语言、本地关键词、文化适配和 AI 原生内容生产。',
        'tags': ['纯血版小语种SEO', '一站一语言', '本地关键词研究', '文化适配', 'AI原生内容', '多语言独立站'],
    },
    '2025-04-09-google-tariff-104': {
        'description': '从 104% 关税话题切入，分析外贸企业为什么要尽早布局 Google SEO、小语种市场和低成本自然流量渠道。',
        'tags': ['104关税', '外贸SEO应对', '低成本流量', '小语种市场', 'Google自然流量', '外贸风险'],
    },
    '2025-04-07-independent-site-multilingual-native': {
        'description': '结合权威媒体与实操案例，说明为什么纯血版小语种独立站是长期趋势，以及企业应如何提前布局海外市场。',
        'tags': ['纯血小语种独立站', '海外市场布局', '多语言趋势', '外贸本地化', '小语种机会', '独立站战略'],
    },
    '2025-10-09-independent-site-foreign-trade-training-seo': {
        'description': '介绍外贸独立站 SEO 培训的实战内容，涵盖关键词调研、网站诊断、内容布局和学员陪跑执行重点。',
        'tags': ['外贸SEO培训', '独立站培训', '关键词实操', '网站诊断课程', '内容布局', 'SEO陪跑'],
    },
    '2025-09-09-traffic-0-seo': {
        'description': '针对独立站流量为 0 的情况，拆解常见原因与排查顺序，包括收录、关键词、内容质量、内链和执行周期。',
        'tags': ['流量为0', '独立站没流量', 'SEO排查', '收录问题', '关键词缺失', '新站优化'],
    },
    '2025-09-13-ranking-inquiry-seo': {
        'description': '从排名到询盘的转化链路出发，分析 SEO 不只是冲排名，还要让关键词、页面内容和表单设计共同带来客户。',
        'tags': ['排名到询盘', 'SEO转化链路', '询盘优化', '关键词转化', '外贸页面', '自然流量变现'],
    },
}

def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'

for slug, data in updates.items():
    path = BASE / f'{slug}.md'
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        raise SystemExit(f'No frontmatter: {path}')
    parts = text.split('---', 2)
    fm = parts[1]
    body = parts[2]
    fm = re.sub(r'^description:\s*".*"\s*$', f'description: {yaml_quote(data["description"])}', fm, flags=re.M)
    fm = re.sub(r'^tags:\n(?:  - ".*"\n?)+', 'tags:\n' + ''.join(f'  - {yaml_quote(tag)}\n' for tag in data['tags']), fm, flags=re.M)
    path.write_text('---' + fm + '---' + body, encoding='utf-8')

seen_desc = {}
seen_tags = {}
for slug, data in updates.items():
    desc = data['description']
    tags_key = tuple(data['tags'])
    if desc in seen_desc:
        raise SystemExit(f'Duplicate description: {slug} and {seen_desc[desc]}')
    if tags_key in seen_tags:
        raise SystemExit(f'Duplicate tags: {slug} and {seen_tags[tags_key]}')
    seen_desc[desc] = slug
    seen_tags[tags_key] = slug
print(f'Updated {len(updates)} posts with unique descriptions and tags.')
