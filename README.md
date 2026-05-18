# 公募基金数据API - 最终稳定版

基于GitHub Pages和GitHub Actions构建的**免费、稳定、零维护**公募基金数据API，使用akshare获取全量基金基本信息，每日自动更新。

## ✨ 功能特点

- 🆓 **完全免费**：无需服务器、无需域名、无任何费用
- 🔄 **每日自动更新**：北京时间18:30自动同步最新基金列表
- 📊 **全量数据**：包含国内所有26700+只公募基金
- 🚀 **全球访问**：GitHub Pages CDN加速，加载速度快
- 📦 **双版本数据**：提供精简版（搜索专用）和完整版（详细信息）
- 🛡️ **稳定可靠**：使用akshare最稳定的核心接口，避免频繁变更

## 📡 API端点

| 端点 | 说明 | 文件大小 | 更新频率 |
|------|------|----------|----------|
| `/funds_simple.json` | 精简版基金列表（代码、名称、类型） | ~2MB | 每日 |
| `/funds_full.json.gz` | 完整版基金数据（含拼音缩写） | ~3MB（压缩后） | 每日 |

**API根地址**：https://LST-Serendipity.github.io/fund-data-api/

## 🚀 快速使用

### JavaScript 前端调用
```javascript
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
### Python 调用
```python
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
### 📋 数据字段说明
精简版 (funds_simple.json)
| 字段名 | 类型   | 说明                     |
| ------ | ------ | ------------------------ |
| code   | string | 6 位基金代码             |
| name   | string | 基金简称                 |
| type   | string | 基金类型（混合型、股票型、债券型等） |

完整版 (funds_full.json.gz)
| 字段名 | 类型   | 说明           |
| ------ | ------ | -------------- |
| code   | string | 6 位基金代码   |
| name   | string | 基金简称       |
| type   | string | 基金类型       |
| pinyin | string | 基金名称拼音缩写 |


API 状态：🟢 正常
运行最后更新：2026-05-18
基金总数：26730 只



