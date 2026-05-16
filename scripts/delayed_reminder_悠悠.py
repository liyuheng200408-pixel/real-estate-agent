#!/usr/bin/env python3
"""
延迟提醒脚本 - 悠悠专用
用于看房完成后30-60分钟跟进提醒

用法:
  python delayed_reminder_悠悠.py create <客户名> <看房时间> <延迟小时数>
  python delayed_reminder_悠悠.py update <客户名> <新看房时间> [新延迟小时数]
  python delayed_reminder_悠悠.py list
  python delayed_reminder_悠悠.py check
  python delayed_reminder_悠悠.py delete <客户名>

看房时间格式: YYYY-MM-DD HH:MM
延迟小时数: 数字，如 0.5 表示30分钟，1 表示1小时
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".hermes" / "delayed_reminders_悠悠.json"


def load_reminders():
    """加载提醒数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_reminders(reminders):
    """保存提醒数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)


def create_reminder(client_name, view_time_str, delay_hours):
    """创建提醒"""
    reminders = load_reminders()
    
    # 检查是否已存在
    for r in reminders:
        if r["client_name"] == client_name:
            print(f"⚠️ 客户 '{client_name}' 已存在提醒记录，使用 update 命令更新")
            return False
    
    view_time = datetime.strptime(view_time_str, "%Y-%m-%d %H:%M")
    trigger_time = view_time + timedelta(hours=float(delay_hours))
    
    reminder = {
        "client_name": client_name,
        "view_time": view_time_str,
        "delay_hours": float(delay_hours),
        "trigger_time": trigger_time.strftime("%Y-%m-%d %H:%M"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "pending"
    }
    
    reminders.append(reminder)
    save_reminders(reminders)
    
    print(f"✅ 提醒创建成功！")
    print(f"   客户: {client_name}")
    print(f"   看房时间: {view_time_str}")
    print(f"   延迟: {delay_hours} 小时")
    print(f"   触发时间: {trigger_time.strftime('%Y-%m-%d %H:%M')}")
    return True


def update_reminder(client_name, new_view_time_str, new_delay_hours=None):
    """更新提醒"""
    reminders = load_reminders()
    
    for r in reminders:
        if r["client_name"] == client_name:
            view_time = datetime.strptime(new_view_time_str, "%Y-%m-%d %H:%M")
            delay_hours = new_delay_hours if new_delay_hours else r["delay_hours"]
            trigger_time = view_time + timedelta(hours=float(delay_hours))
            
            r["view_time"] = new_view_time_str
            r["delay_hours"] = float(delay_hours)
            r["trigger_time"] = trigger_time.strftime("%Y-%m-%d %H:%M")
            r["status"] = "pending"
            
            save_reminders(reminders)
            
            print(f"✅ 提醒更新成功！")
            print(f"   客户: {client_name}")
            print(f"   新看房时间: {new_view_time_str}")
            print(f"   新延迟: {delay_hours} 小时")
            print(f"   新触发时间: {trigger_time.strftime('%Y-%m-%d %H:%M')}")
            return True
    
    print(f"❌ 未找到客户 '{client_name}' 的提醒记录")
    return False


def list_reminders():
    """列出所有提醒"""
    reminders = load_reminders()
    
    if not reminders:
        print("📭 暂无提醒记录")
        return
    
    print(f"\n{'='*60}")
    print(f"{'客户名':<12} {'看房时间':<16} {'延迟':<6} {'触发时间':<16} {'状态':<8}")
    print(f"{'-'*60}")
    
    for r in reminders:
        print(f"{r['client_name']:<12} {r['view_time']:<16} {r['delay_hours']:<6} {r['trigger_time']:<16} {r['status']:<8}")
    
    print(f"{'='*60}")
    print(f"共 {len(reminders)} 条记录\n")


def check_triggers():
    """检查并返回待触发的提醒"""
    now = datetime.now()
    reminders = load_reminders()
    triggered = []
    pending = []
    
    for r in reminders:
        if r["status"] == "triggered":
            continue
        
        trigger_time = datetime.strptime(r["trigger_time"], "%Y-%m-%d %H:%M")
        
        if now >= trigger_time:
            triggered.append(r)
        else:
            pending.append(r)
    
    return triggered, pending


def process_triggers():
    """处理已触发的提醒，返回待发送的消息列表"""
    triggered, pending = check_triggers()
    
    messages = []
    for t in triggered:
        messages.append({
            "client_name": t["client_name"],
            "view_time": t["view_time"],
            "delay_hours": t["delay_hours"],
            "message": f"🔔 看房跟进提醒\n客户: {t['client_name']}\n看房时间: {t['view_time']}\n已过 {t['delay_hours']} 小时，请及时跟进！"
        })
        t["status"] = "triggered"
    
    # 保存状态更新
    reminders = load_reminders()
    for t in triggered:
        for r in reminders:
            if r["client_name"] == t["client_name"]:
                r["status"] = "triggered"
                break
    save_reminders(reminders)
    
    return messages


def delete_reminder(client_name):
    """删除提醒"""
    reminders = load_reminders()
    original_len = len(reminders)
    
    reminders = [r for r in reminders if r["client_name"] != client_name]
    
    if len(reminders) < original_len:
        save_reminders(reminders)
        print(f"✅ 已删除客户 '{client_name}' 的提醒")
        return True
    else:
        print(f"❌ 未找到客户 '{client_name}' 的提醒记录")
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        if len(sys.argv) != 5:
            print("用法: create <客户名> <看房时间> <延迟小时数>")
            print("示例: create 张三 2026-05-17 14:00 0.5")
            return
        create_reminder(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("用法: update <客户名> <新看房时间> [新延迟小时数]")
            print("示例: update 张三 2026-05-17 15:00 1")
            return
        new_delay = sys.argv[4] if len(sys.argv) > 4 else None
        update_reminder(sys.argv[2], sys.argv[3], new_delay)
    
    elif command == "list":
        list_reminders()
    
    elif command == "check":
        messages = process_triggers()
        if messages:
            print(f"📤 待发送 {len(messages)} 条跟进提醒：\n")
            for m in messages:
                print(m["message"])
                print("-" * 40)
        else:
            print("✅ 暂无待触发的提醒")
    
    elif command == "delete":
        if len(sys.argv) != 3:
            print("用法: delete <客户名>")
            return
        delete_reminder(sys.argv[2])
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
