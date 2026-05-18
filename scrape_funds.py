import akshare as ak
import json
import gzip
import os
from datetime import datetime
import pandas as pd

def get_all_funds_basic():
    """获取所有开放式基金基本信息（使用最新稳定接口）"""
    print("正在获取所有开放式基金基本信息...")
    try:
        # 2026年5月最新接口：fund_name_em 获取所有基金基本信息
        fund_name_df = ak.fund_name_em()
        
        # 2026年5月最新接口：fund_open_fund_daily_em 获取最新净值数据
        print("正在获取最新基金净值数据...")
        fund_daily_df = ak.fund_open_fund_daily_em()
        
        # 合并两个数据集
        fund_df = pd.merge(
            fund_name_df, 
            fund_daily_df, 
            on=["基金代码", "基金简称"], 
            how="left"
        )
        
        funds = []
        for _, row in fund_df.iterrows():
            fund = {
                "code": str(row["基金代码"]),
                "name": str(row["基金简称"]),
                "type": str(row["基金类型"]) if "基金类型" in row and not pd.isna(row["基金类型"]) else "未知",
                "net_value": float(row["单位净值"]) if "单位净值" in row and not pd.isna(row["单位净值"]) else None,
                "daily_growth": float(row["日增长率"]) if "日增长率" in row and not pd.isna(row["日增长率"]) else None,
                "pinyin": str(row["拼音缩写"]) if "拼音缩写" in row and not pd.isna(row["拼音缩写"]) else ""
            }
            funds.append(fund)
        return funds
    except Exception as e:
        print(f"获取基金基本信息失败: {e}")
        # 备用方案：只使用fund_name_em
        try:
            print("尝试使用备用方案获取基金列表...")
            fund_name_df = ak.fund_name_em()
            funds = []
            for _, row in fund_name_df.iterrows():
                funds.append({
                    "code": str(row["基金代码"]),
                    "name": str(row["基金简称"]),
                    "type": str(row["基金类型"]) if "基金类型" in row and not pd.isna(row["基金类型"]) else "未知",
                    "net_value": None,
                    "daily_growth": None,
                    "pinyin": str(row["拼音缩写"]) if "拼音缩写" in row and not pd.isna(row["拼音缩写"]) else ""
                })
            return funds
        except Exception as e2:
            print(f"备用方案也失败: {e2}")
            return []

def get_fund_ranks():
    """获取各类基金排名（使用最新接口）"""
    print("正在获取基金排名数据...")
    ranks = {}
    fund_types = ["股票型", "混合型", "债券型", "指数型", "QDII", "FOF"]
    periods = ["近1周", "近1月", "近3月", "近6月", "近1年", "近3年", "近5年"]
    
    for fund_type in fund_types:
        ranks[fund_type] = {}
        for period in periods:
            try:
                # 2026年5月最新接口：fund_open_fund_rank_em 参数改为indicator
                rank_df = ak.fund_open_fund_rank_em(symbol=fund_type, indicator=period)
                ranks[fund_type][period] = []
                for _, row in rank_df.head(50).iterrows():
                    ranks[fund_type][period].append({
                        "code": str(row["基金代码"]),
                        "name": str(row["基金简称"]),
                        "return_rate": float(row["收益率"]) if not pd.isna(row["收益率"]) else None,
                        "rank": int(row["排名"]) if not pd.isna(row["排名"]) else None
                    })
            except Exception as e:
                print(f"获取{fund_type}基金{period}排名失败: {e}")
                ranks[fund_type][period] = []
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
    ranks = get_fund_ranks()
    
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
    print(f"数据更新完成，耗时: {duration:.2f}秒")
    print(f"共获取 {len(funds)} 只基金数据")

if __name__ == "__main__":
    main()