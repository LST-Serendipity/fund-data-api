import akshare as ak
import json
import gzip
import os
from datetime import datetime
import pandas as pd

def safe_float(value):
    """安全转换为float，处理所有异常情况"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return None
    try:
        return float(value)
    except:
        return None

def get_all_funds_basic():
    """获取所有公募基金基本信息（2026年5月最稳定接口）"""
    print("正在获取所有公募基金基本信息...")
    try:
        # 这个接口是akshare最稳定的基金列表接口，几乎不会变
        fund_name_df = ak.fund_name_em()
        print(f"✅ 成功获取基金基本信息，共 {len(fund_name_df)} 只基金")
        
        funds = []
        for _, row in fund_name_df.iterrows():
            fund = {
                "code": str(row["基金代码"]).strip(),
                "name": str(row["基金简称"]).strip(),
                "type": str(row["基金类型"]).strip() if "基金类型" in row and not pd.isna(row["基金类型"]) else "未知",
                "pinyin": str(row["拼音缩写"]).strip() if "拼音缩写" in row and not pd.isna(row["拼音缩写"]) else ""
            }
            funds.append(fund)
        return funds
    except Exception as e:
        print(f"❌ 获取基金基本信息失败: {e}")
        return []

def save_json_gzip(data, filepath):
    """保存为gzip压缩的JSON文件，减小传输体积"""
    with gzip.open(filepath, 'wt', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    start_time = datetime.now()
    print(f"数据更新开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建docs目录（如果不存在）
    os.makedirs('docs', exist_ok=True)
    
    # 获取核心数据
    funds = get_all_funds_basic()
    
    # 生成结果
    result = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_funds": len(funds),
        "funds": funds
    }
    
    # 保存完整版数据（压缩格式）
    save_json_gzip(result, 'docs/funds_full.json.gz')
    print(f"✅ 完整数据已保存到 docs/funds_full.json.gz")
    
    # 保存精简版基金列表（专门用于搜索，体积小加载快）
    simple_funds = [{"code": f["code"], "name": f["name"], "type": f["type"]} for f in funds]
    simple_result = {
        "update_time": result["update_time"],
        "total": len(simple_funds),
        "funds": simple_funds
    }
    
    with open('docs/funds_simple.json', 'w', encoding='utf-8') as f:
        json.dump(simple_result, f, ensure_ascii=False, indent=2)
    print(f"✅ 精简版基金列表已保存到 docs/funds_simple.json")
    
    # 删除空的排名文件
    if os.path.exists('docs/fund_ranks.json'):
        os.remove('docs/fund_ranks.json')
        print("ℹ️ 已删除旧的排名数据文件")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n🎉 数据更新全部完成！")
    print(f"⏱️  总耗时: {duration:.2f}秒")
    print(f"📊 共获取 {len(funds)} 只公募基金数据")
    print(f"🌐 API地址: https://LST-Serendipity.github.io/fund-data-api/funds_simple.json")

if __name__ == "__main__":
    main()