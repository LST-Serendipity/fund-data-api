import akshare as ak
import json
import gzip
import os
from datetime import datetime
import pandas as pd

def safe_float(value):
    """安全转换为float，处理空字符串、空格和异常值"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return None
    try:
        return float(value)
    except:
        return None

def get_all_funds_basic():
    """获取所有开放式基金基本信息（最稳定版本）"""
    print("正在获取所有开放式基金基本信息...")
    try:
        # 2026年5月最稳定的基金列表接口
        fund_name_df = ak.fund_name_em()
        print(f"成功获取基金基本信息，共 {len(fund_name_df)} 只基金")
        
        funds = []
        for _, row in fund_name_df.iterrows():
            fund = {
                "code": str(row["基金代码"]).strip(),
                "name": str(row["基金简称"]).strip(),
                "type": str(row["基金类型"]).strip() if "基金类型" in row and not pd.isna(row["基金类型"]) else "未知",
                "net_value": None,
                "daily_growth": None,
                "pinyin": str(row["拼音缩写"]).strip() if "拼音缩写" in row and not pd.isna(row["拼音缩写"]) else ""
            }
            funds.append(fund)
        return funds
    except Exception as e:
        print(f"获取基金基本信息失败: {e}")
        return []

def get_fund_ranks_simple():
    """简化版基金排名，使用最稳定的接口"""
    print("正在获取基金排名数据...")
    ranks = {}
    # 只获取最常用的混合型和股票型基金近1月排名
    fund_types = ["混合型", "股票型"]
    
    for fund_type in fund_types:
        try:
            # 使用最稳定的默认参数获取排名
            rank_df = ak.fund_open_fund_rank_em(symbol=fund_type)
            ranks[fund_type] = []
            for _, row in rank_df.head(50).iterrows():
                ranks[fund_type].append({
                    "code": str(row["基金代码"]).strip(),
                    "name": str(row["基金简称"]).strip(),
                    "return_rate": safe_float(row["收益率"]),
                    "rank": int(row["排名"]) if not pd.isna(row["排名"]) else None
                })
            print(f"成功获取{fund_type}基金排名，共 {len(ranks[fund_type])} 只")
        except Exception as e:
            print(f"获取{fund_type}基金排名失败: {e}")
            ranks[fund_type] = []
    return ranks

def save_json_gzip(data, filepath):
    """保存为gzip压缩的JSON文件"""
    with gzip.open(filepath, 'wt', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    start_time = datetime.now()
    print(f"数据更新开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建docs目录
    os.makedirs('docs', exist_ok=True)
    
    # 获取数据
    funds = get_all_funds_basic()
    ranks = get_fund_ranks_simple()
    
    # 生成结果
    result = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_funds": len(funds),
        "funds": funds,
        "ranks": ranks
    }
    
    # 保存完整数据（压缩版）
    save_json_gzip(result, 'docs/funds_full.json.gz')
    print(f"完整数据已保存到 docs/funds_full.json.gz")
    
    # 保存精简版基金列表（只包含代码和名称，用于搜索）
    simple_funds = [{"code": f["code"], "name": f["name"], "type": f["type"]} for f in funds]
    simple_result = {
        "update_time": result["update_time"],
        "total": len(simple_funds),
        "funds": simple_funds
    }
    
    with open('docs/funds_simple.json', 'w', encoding='utf-8') as f:
        json.dump(simple_result, f, ensure_ascii=False, indent=2)
    print(f"精简版基金列表已保存到 docs/funds_simple.json")
    
    # 保存排名数据
    with open('docs/fund_ranks.json', 'w', encoding='utf-8') as f:
        json.dump({
            "update_time": result["update_time"],
            "ranks": ranks
        }, f, ensure_ascii=False, indent=2)
    print(f"基金排名数据已保存到 docs/fund_ranks.json")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n✅ 数据更新完成，耗时: {duration:.2f}秒")
    print(f"✅ 共获取 {len(funds)} 只基金数据")
    print(f"✅ API已准备就绪")

if __name__ == "__main__":
    main()