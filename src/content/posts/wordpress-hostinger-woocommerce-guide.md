---
title: "WordPress + Hostinger主机独立站建站教程"
description: "手把手教你用 Hostinger 主机搭建 WordPress + WooCommerce 外贸独立站。从购买主机、注册域名、安装 SSL、配置主题插件到发布产品，全流程实操演示，零代码基础也能完成独立站上线。"
pubDate: 2026-08-01
updatedDate: 2026-08-01
heroImage: "/images/default-post.png"
category: "website-building"
tags:
  - "WordPress建站"
  - "Hostinger"
  - "WooCommerce"
  - "外贸独立站"
  - "建站教程"
  - "跨境电商"
---

跨境电商独立站已经进入低门槛时代。WordPress 这样成熟的 CMS 系统，加上 Hostinger 这类性价比极高的主机服务商，让任何一个没有编程背景的外贸卖家都能在半天内搭建出一个功能完整、面向全球的在线商城。

本文是写给零起点用户的实操指南——不讲概念，只走流程。每一步都配了真实后台的截图，跟着点就行。

## 一、为什么用 WordPress 做独立站

在进入具体操作之前，简单说明一下选择 WordPress 的逻辑：

- **零版权成本：** WordPress 是完全开源的内容管理系统，不需要购买授权，也不存在年度订阅费。你用它建出来的网站，代码和数据 100% 归你自己。
- **后台操作直觉化：** 所有内容管理——写文章、上传产品、更新页面——都在一个可视化后台完成。不需要触碰代码，也不用理解什么叫 FTP。
- **生态壁垒：** 全球超过 40% 的网站跑在 WordPress 上。这意味着任何你遇到的问题，网上都有现成的中文/英文解决方案。主题、插件、教程的丰富程度是任何商业 SaaS 建站工具无法比拟的。
- **维护成本极低：** 只要主机服务商靠谱（比如本文用的 Hostinger），日常维护就是登录后台点一下"更新"按钮。

## 二、购买 Hostinger 主机

Hostinger 有两类产品线：虚拟主机和 WordPress 专属主机。如果目标是建外贸商城，**无脑选 WordPress 专属主机**——它针对 WP 做了运行环境优化，内置了一键安装 WordPress、自动备份、WP-CLI 等专有工具，稳定性和加载速度明显优于普通虚拟机。

目前 Hostinger WordPress 主机有三个方案：

| 方案 | 建站数量 | 存储空间 | 月度流量 | 域名 | 优惠价/月 | 额外赠送 |
|------|---------|---------|---------|------|----------|---------|
| Premium | 3 个 | 20GB SSD | 不限 | 首年免费 | $2.69 | +3 个月 |
| Business | 50 个 | 50GB NVMe | 不限 | 首年免费 | $3.59 | +3 个月 |
| Cloud Startup | 100 个 | 100GB NVMe | 不限 | 首年免费 | $7.19 | +3 个月 |

新手从 **Business** 起步是最合理的——50 个建站名额足够做多站点矩阵，NVMe 存储比 SSD 快一个量级，按月折算不到 30 元人民币。预算充裕可以直接上 Cloud Startup。

选好方案后进入购买页面：

![购买Hostinger主机方案](https://www.idcspy.com/wp-content/uploads/2024/08/2.jpg)

接下来创建 Hostinger 账户，填邮箱即可，已有账户直接登录：

![创建Hostinger账号](https://www.idcspy.com/wp-content/uploads/2024/08/3.jpg)

登录后选择支付方式——Hostinger 支持支付宝、PayPal、信用卡等主流渠道，输入优惠码后确认付款：

![Hostinger支付页面](https://www.idcspy.com/wp-content/uploads/2024/08/4.jpg)

## 三、域名注册与 DNS 解析

付款成功后会进入新手引导界面。Hostinger 的后台设计对小白非常友好，每一步都标注得清清楚楚：

![开始建站导航](https://www.idcspy.com/wp-content/uploads/2024/08/5.jpg)

点击 "Start Now" 后，按实际情况回答三个问题：

- **I am creating a website for Myself**（为自己建站）
- **It will be an Online Store website**（电商/独立站）
- **I am creating my first website**（首次建站，选 Beginner）

![选择建站目标](https://www.idcspy.com/wp-content/uploads/2024/08/6.jpg)

下一个界面是选择建站工具。系统会问你要安装 WordPress 还是 WordPress + WooCommerce：

![选择建站方式](https://www.idcspy.com/wp-content/uploads/2024/08/7.jpg)

这里有个建站老手的经验之谈：**先选 WordPress 就够了，别在初始化阶段装 WooCommerce。** 等你把网站结构搭好、主题调好之后再手动安装 WooCommerce，能避免初始安装一大堆你用不上的插件，拖慢后台速度。

如果你是从别的服务商迁移过来的，Hostinger 免费提供一键搬家工具（migrate my website），用起来很方便。

继续往下，系统会让你为 WordPress 设置管理员邮箱和密码。这是你以后登录 `wp-admin` 后台的凭证，务必妥善保存。

> 系统会推荐你选一个主题模板。这里**直接跳过**——现在还不是选模板的时候。WordPress 后台的主题市场有几千个选择，等你把基础环境配置好、对网站风格有方向感了再来挑选更高效。

接下来进入域名设置环节。三个选项：

1. **申请免费域名：** 凡购买一年及以上 Hostinger 主机，赠送一个免费的 `.com` 域名（有效期第一年免费，续费约 $13.99/年）。起步阶段首选这个，因为主机商会自动帮你完成 DNS 解析，不需要你手动操作任何技术配置。
2. **购买新域名：** 如果需要注册多个域名就选这个。
3. **使用已购域名：** 如果你在 Gname、Namecheap 或 NameSilo 已经买过域名，选择此项后需要自己把域名的 DNS 指向 Hostinger 的服务器。

![域名注册选项](https://www.idcspy.com/wp-content/uploads/2024/08/8.jpg)

设置完域名后选机房位置。**机房离用户越近，网站打开越快。** 如果你的客户主要在欧美，选北美机房；做亚洲市场选新加坡或日本机房。

点击 "Finish setup" 后系统自动安装 WordPress，完成后会出现以下界面：

![WordPress安装完成页面](https://www.idcspy.com/wp-content/uploads/2024/08/9.jpg)

界面中的三个入口分别对应：

- **Manage WordPress：** 进入 WordPress 后台，之后直接访问 `https://你的域名.com/wp-admin` 即可，不需要每次都从 Hostinger 跳转
- **View Website：** 预览网站

![WordPress管理面板入口](https://www.idcspy.com/wp-content/uploads/2024/08/10.jpg)

- **Control Panel：** 主机控制面板，管理 SSL 证书、添加站点、查看服务器 IP 等都在这里操作

## 四、安装 SSL 证书

网站此时虽然可以访问，但地址栏还没有安全锁。SSL 证书就是给网站加 HTTPS 加密的那个"锁"——它不仅影响用户信任，还是谷歌排名因素之一。Hostinger 为所有用户提供**免费的 SSL 证书**。

要安装 SSL，首先要进 Hostinger 控制面板：点击顶部 "Websites"，选中你的域名，点旁边的 "Dashboard"：

![进入Hostinger控制面板](https://www.idcspy.com/wp-content/uploads/2024/08/11.jpg)

左侧菜单找到 **Security → SSL**：

![Security-SSL菜单](https://www.idcspy.com/wp-content/uploads/2024/08/12.jpg)

![选择要安装SSL的域名](https://www.idcspy.com/wp-content/uploads/2024/08/13.jpg)

选择你的域名，点击 **"Install SSL"**。几秒钟后对话框提示安装成功，刷新页面就能看到 SSL 状态变成绿色 "Active"：

![SSL安装成功](https://www.idcspy.com/wp-content/uploads/2024/08/14.jpg)

是否生效很容易验证——在浏览器地址栏输入域名，如果能看见**安全锁图标**就说明 SSL 已经正常工作：

![浏览器安全锁验证](/images/posts/wordpress-hostinger-woocommerce-guide/ssl.png)

SSL 搞定后，网站的基础环境就算配置完了。接下来进入真正的"建站"环节。

## 五、安装 WordPress 主题与插件

主题决定了网站长什么样，插件决定了网站能做什么。做电商独立站，核心插件就是 WooCommerce。

### 1. 安装主题模板

WordPress 安装后自带几套官方主题，比如 Twenty Twenty-One 系列，但这些是给博客设计的，不适合做商城展示。登陆后台后，进 **Appearance → Themes**：

![WordPress后台主题管理页面](https://www.idcspy.com/wp-content/uploads/2024/08/1-16.jpg)

系统内置了三套默认主题，先保留一个激活状态（WordPress 要求至少有一套活跃主题），等新主题装好后再删掉旧的。

点 "Add New" 进入主题市场。免费主题里有三款在全球建站圈被反复验证过的选择：

- **Astra：** 轻量化设计的代表，体积小、加载快，内置了数套电商 Starter Template
- **GeneratePress：** 极简主义路线，基础包不到 10KB，SEO 表现优异
- **Kadence：** 免费+付费混搭模式，内置的区块库功能比前两者更丰富

这三款由专业开发团队持续维护，代码质量和更新频率都远超 ThemeForest 市场上个人开发者的一次性付费主题。

本文全程使用 Kadence 来演示，它的特点：

![Kadence主题功能展示](https://www.idcspy.com/wp-content/uploads/2024/08/17.jpg)

- 免费版的功能已经足够一个外贸站日常使用
- 代码遵循 WordPress 核心规范，SEO 友好
- 基于 Gutenberg（古腾堡）区块编辑器，页面上任何区域都能拖拽式自定义

ThemeForest 上的绝大多数付费主题是由一到两个人开发的，代码风格和后续维护难以保障。新手阶段，优先从 Astra / GeneratePress / Kadence 三款里选一个即可。

下面以 Kadence 为例走一遍安装流程：在 "Add Themes" 搜索框输入 "Kadence"，找到最新版本，点 "Install" 再点 "Activate"。激活后系统会提示你安装配套的 "Kadence Starter Templates" 插件，按提示装上：

![安装Kadence主题](https://www.idcspy.com/wp-content/uploads/2024/08/18.jpg)

这个 Starter Templates 插件内置了二十多套整站模板，包含首页、关于我们、联系我们等页面。即便你不想直接用这些模板，安装它作为参考也是很值得的——Kadence 的模板数量在同类主题中并不算多，Astra 和 Blocksy 的模板库更大，但 Kadence 胜在模板质感更贴近商务场景。

安装完成后，左侧菜单 "Kadence" 下多了一个 "Starter Templates" 子菜单。进去后可以选择 AI 智能向导模式，让系统引导你一步步完成模板导入：

![Kadence AI向导](https://www.idcspy.com/wp-content/uploads/2024/08/19.jpg)

如果不想用 AI 向导，可以选择 "Classic Starter Templates" 手动模式。这里需要先确定建站工具——选项有两个：

- **Gutenberg Block Editor（古腾堡）：** WordPress 原生区块编辑器，免费且与系统深度整合
- **Elementor：** 目前最强大的第三方可视化建站插件，拖拽式设计，但部分高级功能收费

本文选择 Gutenberg，因为它完全免费且 Kadence 对它做了深度适配。选定建站工具后会进入模板库——Kadence 的 Gutenberg 方向提供约 9 套模板，其中 Print Shop 这一个是专门为电商独立站设计的：

![选择Print Shop模板](https://www.idcspy.com/wp-content/uploads/2024/08/20.jpg)

### 2. 导入模板

Gutenberg 的模板库中约有二十多种风格，其中针对电商的只有 Print Shop 等少数几个。Print Shop 虽然只是九套之一，但它涵盖的产品展示、购物车和结账页面的预设计都非常到位。

点击 Print Shop 模板后会弹出一个选项，问你是只导入首页还是导入整站。**务必选整站导入（Full Site）**，这样会连带安装 WooCommerce 和 Kadence Block 两个必备插件。你还可以在这一步选择网站的基础配色和字体方案：

![导入Print Shop整站模板](https://www.idcspy.com/wp-content/uploads/2024/08/21.jpg)

Kadence Block 是一个区块强化插件，在 Gutenberg 的基础上大大扩展了可用模块的数量和类型。如果你的主题没有自带这样的区块库，自己去插件市场也能搜到不少替代品。

选定配色和字体后点 "Full Site" 继续。系统会预览即将导入的内容概览，确认无误后开始导入。这个过程取决于网速，通常一到两分钟。

> 如果之后发现需要 WooCommerce 而当前模板没有包含，随时去 Plugins → Add New 搜索安装就行。对跨境电商来说 WooCommerce 是刚需，没有它就没法上架商品。

导入完成后，点 "Finished! View your site" 查看效果。此刻网站上的内容都是模板预设的示例数据，接下来就是替换成你自己的内容。

### 3. 安装必备插件

在导入模板的过程中，我们已经装好了 WooCommerce 和 Kadence Block。进 **Plugins** 菜单查看已安装列表。除此之外，以下几类插件建议在上线前一并装好：

- **子主题插件：** 在网站配置完成前，给当前激活的主题创建一个子主题（Child Theme），防止后续主题更新覆盖你的自定义代码。推荐 Child Theme Wizard 或 WP Child Theme Generator
- **缓存加速：** 优化页面加载速度。挂 Hostinger 主机的话推荐 LiteSpeed Cache
- **SEO 插件：** 是所有独立站的标配。三选一即可：Rank Math、Yoast SEO、All in One SEO
- **社交分享：** 让访问者一键分享产品到社交平台。推荐 Sassy Social Share 或 Super Socializer
- **表单插件：** 收集客户邮箱、接收询盘。推荐 Contact Form 7 或 WPForms（如果你用 Kadence，其区块内已内含表单功能，无需单独安装）
- **安全防护：** 额外增加防火墙和恶意软件扫描。推荐 Wordfence Security 或 All In One WP Security & Firewall
- **GDPR 合规：** 面向欧洲市场的网站需要展示 Cookie 同意弹窗。推荐 GDPR Cookie Consent 或 LuckyWP Cookie Notice

![安装必备插件](https://www.idcspy.com/wp-content/uploads/2024/08/22.jpg)

如果你在导入模板时跳过了 WooCommerce，现在记得补装。安装插件就三步：搜索→点 Install→点 Activate。

## 六、设置和自定义 WordPress 网站

从这一步开始，你不再是一路"Next"，而是要真正动手定制网站。本节能帮你搞清楚每个设置项在哪、做什么用，但具体填什么内容取决于你的行业和产品。

### 1. 基本设置

左侧菜单进 **Settings**：

- **General（常规）：** 填写网站标题（Site Title）和副标题（Tagline）。标题一旦确定就不要频繁改动，搜索引擎对频繁更改标题的网站会减分。WordPress 地址和站点地址保持一致：

![常规设置](https://www.idcspy.com/wp-content/uploads/2024/08/23.jpg)

- **Writing（撰写）：** 默认即可
- **Reading（阅读）：** 设置首页展示方式，底部 "Search Engine Visibility" 建议在建站期间勾选，避免搜索引擎抓取到没有完成的页面
- **Discussion（讨论）：** 默认
- **Media（媒体）：** 默认
- **Permalinks（固定链接）：** 这是 SEO 最核心的设置项之一。选 "Post name"（即 `域名.com/文章标题` 的格式），对搜索引擎最友好：

![固定链接设置](https://www.idcspy.com/wp-content/uploads/2024/08/24.jpg)

- **Privacy（隐私）：** 添加隐私政策页面，面向欧洲市场必须设置

### 2. 自定义网站外观和布局

进入 **Appearance → Customize**，开始可视化设置网站的前端外观。这是全站视觉风格的控制面板：

![外观自定义](https://www.idcspy.com/wp-content/uploads/2024/08/25.jpg)

以 Kadence 为例（不同主题的 Customize 界面大同小异）：

- **General（常规）：** 全局布局、配色、字体、按钮样式、侧边栏显示等。Breadcrumbs（面包屑导航）和 Performance 选项建议打开
- **Header & Footer（页眉与页脚）：** Kadence 将页眉和页脚各分成三行，每行都可以自由拖拽放置元素，比传统主题灵活太多。Footer 同样支持古腾堡区块，可以像编辑页面一样编辑页脚：

![页眉页脚设置](https://www.idcspy.com/wp-content/uploads/2024/08/26.jpg)

- **Page Layout / Blog Posts / Search Results：** 分别设置页面、文章和搜索结果的版式布局
- **Site Identity / Homepage Settings：** 上传 Logo 和 Favicon，设置首页
- **WooCommerce：** 控制产品目录、单个产品页、购物车、结账页面的布局
- **Additional CSS：** 面向有前端经验的用户，新手跳过
- **Import/Export：** 配置完成后导出设置备份

> 注意：Customize 只控制"框架"，不控制"内容"。要修改具体页面的文字和图片，需要去 Pages 菜单中逐页编辑。

### 3. 菜单和小工具

**Appearance → Menus** 管理网站的导航结构：

![菜单设置](https://www.idcspy.com/wp-content/uploads/2024/08/27.jpg)

导入 Kadence 后系统会预设几个菜单。你可以直接编辑它们：拖拽调整链接的排列顺序，或把某个链接拖入另一个链接下方变成二级导航。每个链接的显示名称都可以独立修改，比如页面标题是 "about" 但导航里显示 "About Us"。

**小工具（Widgets）** 是通过区块来管理侧边栏和页脚内容的功能模块：

![小工具管理](https://www.idcspy.com/wp-content/uploads/2024/08/28.jpg)

从 WordPress 5.8 开始，小工具编辑器全面采用古腾堡区块，操作逻辑和页面编辑完全统一。

此外，WooCommerce 的店铺基础设置也需要在这一步完成——包括商家信息、收款方式、物流运费模板等：

![WooCommerce设置](https://www.idcspy.com/wp-content/uploads/2024/08/29.jpg)

至此网站配置工作基本完成。

## 七、添加网站内容

如果前面六步是在盖房子和装修，这一步就是往里搬家具。网站到此已有框架，缺的是你的品牌内容。

### 1. 创建核心页面

导入模板时 Kadence 已经自动生成了部分页面，根据需求保留或删除。一个合格的外贸独立站至少需要以下页面：

![页面列表](https://www.idcspy.com/wp-content/uploads/2024/08/30.jpg)

新建一个页面（比如 "About Us"），你会看到古腾堡编辑器的界面：

![页面编辑器](https://www.idcspy.com/wp-content/uploads/2024/08/31.jpg)

页面编辑器的功能区对应关系：
1. 页面标题
2. 添加区块——点击 + 号插入段落、图片、标题、视频、按钮等模块
3. 文本格式设置（字体颜色、超链接、加粗等）
4. 发布状态、固定链接（Permalink）、评论开关
5. Kadence 主题的页面布局选项
6. Kadence Block 模块设置
7. Gutenberg 编辑器本身的偏好设置

页面的内容和布局完全取决于你的品牌定位。发布前先预览确认，无误后再点发布。

### 2. 上传产品

WooCommerce 的产品管理是独立站运营的核心。导入模板时 Kadence 附带了一些示例产品——**先不要删除它们**，参考它们的数据结构来填写自己的产品信息，等你自己的产品数据完整后，再清理这些示例。

![产品列表](https://www.idcspy.com/wp-content/uploads/2024/08/32.jpg)

添加产品的关键字段：

- **产品标题：** 建议用"品牌词 + 品类词 + 关键属性"的格式
- **产品数据（Product Data）：** 下拉选择产品类型——Simple（单一产品）、Grouped（组合产品）、External/Affiliate（外部/联盟产品）、Variable（变体产品，如不同颜色/尺寸）
- **价格和库存：** 正价、促销价、SKU 编号、库存数量
- **产品图片：** 上传主图（Product Image）和轮播图（Product Gallery）
- **分类与标签：** 建立清晰的产品分类层级

![产品编辑页面](https://www.idcspy.com/wp-content/uploads/2024/08/33.jpg)

WooCommerce 的产品描述编辑器默认是经典编辑器风格，对于习惯古腾堡的用户可能稍有不适应。但经典编辑器描述产品反倒更直接高效——你只需要写清楚产品参数、使用场景和规格就足够了。

除了产品和页面，WordPress 内置的博客功能也值得利用。围绕你的产品写使用指南和选购攻略，是独立站获取搜索流量的最佳方式之一。

## 八、发布 WordPress 独立站

当你有两到三个产品已上传、核心页面已完善后，就可以正式发布网站了。发布前有三步：

1. 去 **Settings → Reading**，取消 "Search Engine Visibility" 的勾选，允许搜索引擎收录
2. 将 `sitemap.xml` 提交到 Google Search Console，让谷歌主动来爬取你的页面
3. 安装一个 SEO 插件（如前面推荐的 Rank Math），它会自动优化你的标题、描述和结构化数据

**上线后务必注意：**

- 网站标题和核心描述发布后就不要频繁更改
- 不要三天两头换主题，每次换主题都可能导致布局崩塌
- 保持页面和产品链接（Permalink）简洁一致
- 每周至少更新 2-3 次内容，可以是新产品上架或行业相关的博客文章

以上就是通过 Hostinger 搭建 WordPress + WooCommerce 外贸独立站的完整流程。从购买主机到发布网站，总共八步，一路跟着操作下来，半天之内即可完成。

<style>
/* 约束表格、图片、代码块不超出文章底色区域 */
article table, main table { display: block; width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
article img, main img { max-width: 100% !important; height: auto !important; }
article pre, article code, main pre, main code { max-width: 100%; overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
article td, article th, main td, main th { word-break: break-word; overflow-wrap: break-word; }
</style>
