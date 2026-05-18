# 公募基金数据API

基于GitHub Pages和GitHub Actions构建的免费公募基金数据API，使用akshare获取数据，每日自动更新。

## 功能特点

- 🆓 完全免费，无需服务器
- 🔄 每日自动更新数据
- 📊 包含全面的基金基本信息
- 🏆 各类基金收益率排名
- 🚀 GitHub Pages托管，全球访问
- 📦 提供精简版和完整版数据

## API端点

| 端点 | 说明 | 文件大小 | 更新频率 |
|------|------|----------|----------|
| `/funds_simple.json` | 精简版基金列表（代码、名称、类型） | ~1.5MB | 每日 |
| `/funds_full.json.gz` | 完整版基金数据（详细信息） | ~2MB（压缩后） | 每日 |
| `/fund_ranks.json` | 各类基金收益率排名 | ~500KB | 每日 |

## 部署步骤

### 1. 创建仓库

点击右上角的"Use this template"按钮，创建一个新的仓库。

### 2. 启用GitHub Pages

1. 进入仓库的`Settings` → `Pages`
2. 在`Build and deployment`部分，选择`Deploy from a branch`
3. 分支选择`main`，文件夹选择`/docs`
4. 点击`Save`

### 3. 手动触发第一次更新

1. 进入仓库的`Actions`页面
2. 点击左侧的"更新公募基金数据"工作流
3. 点击右侧的"Run workflow"按钮
4. 等待工作流运行完成（大约需要2-3分钟）

### 4. 访问API

几分钟后，你就可以通过以下URL访问API了：