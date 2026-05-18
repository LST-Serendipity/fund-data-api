公募基金数据 API - 最终稳定版
基于 GitHub Pages 和 GitHub Actions 构建的免费、稳定、零维护公募基金数据 API，使用 akshare 获取全量基金基本信息，每日自动更新。
✨ 功能特点
🆓 完全免费：无需服务器、无需域名、无任何费用
🔄 每日自动更新：北京时间 18:30 自动同步最新基金列表
📊 全量数据：包含国内所有 26700 + 只公募基金
🚀 全球访问：GitHub Pages CDN 加速，加载速度快
📦 双版本数据：提供精简版（搜索专用）和完整版（详细信息）
🛡️ 稳定可靠：使用 akshare 最稳定的核心接口，避免频繁变更
📡 API 端点
表格
端点	说明	文件大小	更新频率
/funds_simple.json	精简版基金列表（代码、名称、类型）	~2MB	每日
/funds_full.json.gz	完整版基金数据（含拼音缩写）	~3MB（压缩后）	每日
API 根地址：https://LST-Serendipity.github.io/fund-data-api/
🚀 快速使用
JavaScript 前端调用
```
运行
// 获取所有基金列表（用于搜索功能）
fetch('https://LST-Serendipity.github.io/fund-data-api/funds_simple.json')
  .then(response => response.json())
  .then(data => {
    console.log(`更新时间: ${data.update_time}`);
    console.log(`基金总数: ${data.total}`);
    
    // 基金搜索示例
    const searchKeyword = '华夏';
    const results = data.funds.filter(fund => 
      fund.name.includes(searchKeyword) || fund.code.includes(searchKeyword)
    );
    
    console.log(`搜索"${searchKeyword}"找到${results.length}只基金`);
    console.log(results.slice(0, 10));
  });
```
Python 调用
```
import requests
import json
import gzip

# 获取精简版基金列表
url = 'https://LST-Serendipity.github.io/fund-data-api/funds_simple.json'
response = requests.get(url)
data = response.json()
print(f"基金总数: {data['total']}")

# 获取完整版压缩数据
url_full = 'https://LST-Serendipity.github.io/fund-data-api/funds_full.json.gz'
response_full = requests.get(url_full)
data_full = json.loads(gzip.decompress(response_full.content))
print(f"更新时间: {data_full['update_time']}")
```
📋 数据字段说明
精简版 (funds_simple.json)
表格
字段名	类型	说明
code	string	6 位基金代码
name	string	基金简称
type	string	基金类型（混合型、股票型、债券型等）
完整版 (funds_full.json.gz)
表格
字段名	类型	说明
code	string	6 位基金代码
name	string	基金简称
type	string	基金类型
pinyin	string	基金名称拼音缩写
🛠️ 部署说明（已完成）
本 API 已成功部署并正常运行，每日自动更新数据。
已完成步骤
✅ GitHub 仓库创建与代码上传
✅ GitHub Pages 启用（分支：main，目录：/docs）
✅ GitHub Actions 权限配置
✅ 首次数据生成成功
✅ 每日自动更新任务配置
手动更新数据
如需立即更新数据：
进入 Actions 页面
点击左侧 "更新公募基金数据" 工作流
点击右侧 "Run workflow" 按钮
等待 2-3 分钟完成更新
⚠️ 注意事项
数据来源：数据来源于东方财富网，仅供学习和研究使用
更新时间：每个交易日北京时间 18:30 自动更新
免费额度：GitHub Actions 每月 2000 分钟免费运行时间，完全满足每日更新需求
数据准确性：基金基本信息仅供参考，投资决策请以基金公司官方数据为准
合规性：请勿用于商业用途或大规模爬取
📝 项目结构
plaintext
fund-data-api/
├── .github/
│   └── workflows/
│       └── update_funds.yml    # 自动更新工作流
├── docs/
│   ├── .nojekyll               # 禁用Jekyll处理
│   ├── index.html              # API文档页面
│   ├── funds_simple.json       # 精简版基金列表（自动生成）
│   └── funds_full.json.gz      # 完整版基金数据（自动生成）
├── scrape_funds.py             # 数据获取脚本
├── requirements.txt            # Python依赖
└── README.md                   # 本说明文档
🔧 扩展功能
如需添加以下功能，可以随时告诉我：
单只基金实时估值查询
基金历史净值数据
基金持仓明细查询
基金收益率排名
基金搜索演示页面
API 状态：🟢 正常运行最后更新：2026-05-18基金总数：26730 只
