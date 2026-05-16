#!/usr/bin/env python3
"""08:30 每日早报脚本 - 读取followup_data_悠悠.json，生成待跟进清单"""

import json
import sys
from datetime import datetime, timedelta

DATA_FILE = "/root/.hermes/followup_data_悠悠.json"


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"customers": []}


def get_customers_by_level(data, level):
    return [c for c in data.get("customers", []) if c.get("level") == level]


def format_customer(c):
    name = c.get("name", "未知")
    phone = c.get("phone", "无")
    last_follow = c.get("lastFollowUp", "未跟进")
    next_visit = c.get("nextFollowUp", "未填写")
    note = c.get("note", "")
    return f"- {name}（{phone}）上次跟进：{last_follow} | 下次回访：{next_visit}"


def generate_report():
    data = load_data()
    customers = data.get("customers", [])

    if not customers:
        return """📋 今日待跟进清单

暂无客户数据，请老板录入新客户～"""

    today = datetime.now().date()
    s_customers = get_customers_by_level(data, "S")
    a_customers = get_customers_by_level(data, "A")
    b_customers = get_customers_by_level(data, "B")

    # S级：2天内必须跟进
    s_overdue = []
    s_pending = []
    for c in s_customers:
        next_visit = c.get("nextFollowUp", "")
        if next_visit:
            try:
                nd = datetime.strptime(next_visit, "%Y-%m-%d").date()
                if nd <= today:
                    s_overdue.append(c)
                else:
                    s_pending.append(c)
            except:
                s_pending.append(c)
        else:
            s_pending.append(c)

    # A级：5天内跟进
    a_pending = []
    for c in a_customers:
        next_visit = c.get("nextFollowUp", "")
        if next_visit:
            try:
                nd = datetime.strptime(next_visit, "%Y-%m-%d").date()
                if nd <= today + timedelta(days=5):
                    a_pending.append(c)
            except:
                a_pending.append(c)
        else:
            a_pending.append(c)

    # 统计今日预约带看（从viewings字段）
    viewings_today = data.get("viewings", [])
    viewing_lines = []
    for v in viewings_today:
        v_date = v.get("date", "")
        if v_date == str(today):
            viewing_lines.append(f"- {v.get('customer', '未知')}：{v.get('time', '')} {v.get('property', '')}")

    report = "📋 今日待跟进清单\n\n"

    # S级
    report += "【S级客户】（2天内必须跟进）\n"
    if s_overdue:
        for c in s_overdue:
            report += format_customer(c) + " ⚠️已逾期\n"
    if s_pending:
        for c in s_pending:
            report += format_customer(c) + "\n"
    if not s_overdue and not s_pending:
        report += "无\n"

    # A级
    report += "\n【A级客户】（5天内跟进）\n"
    if a_pending:
        for c in a_pending[:5]:
            report += format_customer(c) + "\n"
        if len(a_pending) > 5:
            report += f"...还有{len(a_pending) - 5}位\n"
    else:
        report += "无\n"

    # 今日预约带看
    report += "\n【今日预约带看】\n"
    if viewing_lines:
        report += "\n".join(viewing_lines) + "\n"
    else:
        report += "无\n"

    report += "\n请老板确认或补充"

    return report


if __name__ == "__main__":
    print(generate_report())