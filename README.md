# astroseogeo

SEO小平（https://seogeo.cc）—— Astro 纯静态站点，部署在 Cloudflare Pages。

## 网站后台（Sveltia CMS）使用指南

本站内置了 [Sveltia CMS](https://sveltiacms.app/) 后台，界面类似 WordPress，非技术同学也可以直接在网页上写文章、传图片、改菜单，保存后会自动提交到 Git 并触发 Cloudflare Pages 重新构建发布。

### 一、准备工作：Fork 仓库

1. 在 GitHub 上 Fork 本仓库（`astroseogeo`）到自己的账号。
2. 打开仓库里的 `public/admin/config.yml`，把 `backend.repo` 改成你自己的仓库：

   ```yaml
   backend:
     name: github
     repo: 你的GitHub用户名/astroseogeo   # 原来是 suikusales-hub/astroseogeo
     branch: main
   ```

3. 提交这个修改。

### 二、连接 Cloudflare Pages

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)，进入 **Workers 和 Pages → 创建 → Pages → 连接到 Git**，选择你 Fork 的仓库。
2. 构建设置：
   - **框架预设**：`Astro`（没有就选 None）
   - **构建命令**：`npm run build`
   - **构建输出目录**：`dist`
3. 点击保存并部署。等待构建完成后，网站就上线了（建议绑定自己的域名）。

### 三、登录后台

1. 打开 `https://你的域名/admin/`（本地开发时访问 `http://127.0.0.1:4321/admin/index.html`）。
2. 点击登录界面的 **Sign In with Token**（使用访问令牌登录）。
3. 按提示打开 GitHub 令牌页面生成令牌并粘贴即可登录（令牌需要勾选 `repo` 权限）。
4. 如果想给多人使用、免去粘贴令牌，可以自行部署 [Sveltia CMS Authenticator](https://github.com/sveltia/sveltia-cms-auth) 到 Cloudflare Workers，然后在 `config.yml` 的 `backend` 里加一行 `base_url: 你的认证服务地址`。

### 四、后台里能做什么

| 栏目 | 说明 | 对应前台页面 |
| --- | --- | --- |
| **博客文章** | 写文章：标题、摘要、日期、封面图、分类、标签、正文 | `/<文章别名>` |
| **博客分类** | 管理文章分类（名称 + 描述） | `/<分类别名>`（如 `/seo-tutorial`） |
| **博客标签** | 管理标签 | `/tag/<标签名>` |
| **页面** | 自由排版页面，不绑定博客模板 | `/p/<页面别名>` |
| **媒体库** | 上传/选择图片和文件 | 存放在 `public/images/` |
| **博客列表页** | `/blog` 的标题和描述 | `/blog` |
| **主导航菜单** | 顶部导航的菜单项和咨询按钮 | 全站顶部 |
| **页脚菜单** | 页脚的导航链接和社交链接 | 全站底部 |
| **侧边栏小部件** | 文章页侧边栏的栏目标题和咨询按钮（CTA） | 文章页右侧 |

### 五、注意事项（重要）

- **网址别名（slug）只能用小写英文字母、数字和连字符**，例如 `my-first-post`。文章别名就是文章的网址，已发布的文章改别名会改变网址。
- 现有的 8 个分类（SEO教程、谷歌算法更新等）**不要删除或修改别名**，否则已有文章和分类页会受影响。
- 新建文章时，如果分类或标签还不存在，先去「博客分类」「博客标签」里创建，再回到文章里选择。
- 保存内容后 Cloudflare Pages 会自动重新构建，大约 1-2 分钟后前台更新。
- 媒体库里的图片会保存到仓库的 `public/images/` 目录，请尽量上传压缩过的 WebP/JPG 图片。

### 本地开发

```bash
npm install
npm run dev      # 开发预览 http://127.0.0.1:4321
npm run build    # 构建到 dist/（含 Pagefind 搜索索引）
npm run preview  # 本地预览构建结果
```

### 技术栈

- [Astro 6](https://astro.build/)（`output: 'static'`，纯静态输出）
- [Sveltia CMS](https://sveltiacms.app/)（CDN 引入，位于 `public/admin/`）
- Tailwind CSS 4
- [Pagefind](https://pagefind.app/) 静态搜索
- Cloudflare Pages + `_worker.js` 路由规则