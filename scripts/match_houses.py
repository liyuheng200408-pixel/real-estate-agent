#!/usr/bin/env python3
"""
房源智能匹配脚本
根据客户需求从房源库中匹配符合条件的房源

用法：
    python3 match_houses.py --budget 60 --layout "3室2厅2卫"
    python3 match_houses.py --budget 80 --area-min 100 --area-max 130
    python3 match_houses.py --budget 100 --layout "4室2厅2卫" --decoration "精装修"
    python3 match_houses.py --budget 80 --layout "3室2厅2卫" --area-min 90 --decoration "精装修"
"""

import sqlite3
import argparse
import os
import sys

DB_PATH = os.path.expanduser("~/.hermes/data/悠悠房源库.db")


def parse_args():
    parser = argparse.ArgumentParser(description="房源智能匹配脚本")
    parser.add_argument("--budget", type=float, required=True, help="预算上限（万元），必须指定")
    parser.add_argument("--layout", type=str, default=None, help="户型，如：3室2厅2卫")
    parser.add_argument("--area-min", type=float, default=None, help="面积下限（平方米）")
    parser.add_argument("--area-max", type=float, default=None, help="面积上限（平方米）")
    parser.add_argument("--decoration", type=str, default=None, help="装修要求，如：精装修、毛坯")
    parser.add_argument("--floor", type=str, default=None, help="楼层偏好，如：低楼层、中楼层、高楼层")
    parser.add_argument("--district", type=str, default=None, help="区域，如：三亚、海口、陵水、儋州")
    parser.add_argument("--limit", type=int, default=10, help="返回结果数量限制，默认10")
    return parser.parse_args()


def build_query(args):
    """构建SQL查询语句"""
    sql = """
        SELECT 
            id, title, community, price, unit_price, area, layout,
            floor, direction, decoration, build_year, district,
            address, broker, score, listing_date, crawl_date, status, url
        FROM houses
        WHERE price <= ?
    """
    params = [args.budget]

    # 户型（必须满足）
    if args.layout:
        # 去掉空格后匹配，如 "3室2厅2卫" 匹配 "3室2厅2卫" 或 "3室2厅1卫"
        layout_clean = args.layout.replace(" ", "")
        sql += " AND REPLACE(layout, ' ', '') = ?"
        params.append(layout_clean)

    # 面积区间（可浮动10%）
    if args.area_min:
        area_min_adjusted = args.area_min * 0.9
        sql += " AND area >= ?"
        params.append(area_min_adjusted)

    if args.area_max:
        area_max_adjusted = args.area_max * 1.1
        sql += " AND area <= ?"
        params.append(area_max_adjusted)

    # 装修偏好（尽量满足）
    if args.decoration:
        sql += " AND decoration = ?"
        params.append(args.decoration)

    # 楼层偏好（尽量满足）
    if args.floor:
        sql += " AND floor LIKE ?"
        params.append(f"%{args.floor}%")

    # 区域
    if args.district:
        sql += " AND district = ?"
        params.append(args.district)

    # 按价格升序排列
    sql += " ORDER BY price ASC LIMIT ?"
    params.append(args.limit)

    return sql, tuple(params)


def format_result(row):
    """格式化单条房源信息"""
    if not row:
        return ""
    
    (id, title, community, price, unit_price, area, layout,
     floor, direction, decoration, build_year, district,
     address, broker, score, listing_date, crawl_date, status, url) = row

    result = []
    result.append(f"📍 {title}")
    result.append(f"小区：{community}")
    result.append(f"💰 价格：{price}万（单价 {unit_price}元/㎡）")
    result.append(f"📐 面积：{area}㎡ | 户型：{layout}")
    result.append(f"🏠 楼层：{floor} | 朝向：{direction} | 装修：{decoration}")
    result.append(f"📅 建成年份：{build_year}年 | 区域：{district}")
    result.append(f"🔗 {url}")
    return "\n".join(result)


def match_houses(args):
    """执行房源匹配"""
    # 检查数据库是否存在
    if not os.path.exists(DB_PATH):
        print(f"❌ 房源库不存在：{DB_PATH}")
        print("请先添加房源数据后再试。")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        sql, params = build_query(args)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()

        if not results:
            print("😔 未找到符合条件的房源，请尝试调整条件。")
            return True

        print(f"✅ 找到 {len(results)} 套符合条件的房源（预算 {args.budget}万以内）：")
        print("=" * 60)

        for i, row in enumerate(results, 1):
            print(f"\n【房源 {i}】")
            print(format_result(row))
            if i < len(results):
                print("-" * 60)

        return True

    except sqlite3.Error as e:
        print(f"❌ 数据库查询错误：{e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误：{e}")
        return False


def main():
    args = parse_args()
    success = match_houses(args)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()