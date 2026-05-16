# 悠悠房产机器人 (Real Estate Agent - Yoyo)

基于 Hermes Agent 的房产销售AI助手，支持客户跟进、房源匹配、延迟提醒等功能。

## 功能特性

- 客户分级管理（S/A/B级）
- 房源智能匹配（预算/户型/面积/装修等条件）
- 定时跟进提醒（每日早报、午间检查等）
- 飞书消息推送
- 支持三亚、海口、陵水、儋州等海南主要区域

## 系统要求

- 已安装 Hermes Agent v0.14.0+
- Node.js 22+
- Python 3.12+
- 飞书机器人（可选，用于消息推送）

## 快速开始

### 1. 安装 Hermes Agent

```bash
curl -LsSf https://setup.hermesagent.ai | sh
```

### 2. 安装悠悠房产机器人

```bash
bash <(curl -LsSf https://raw.githubusercontent.com/liyuheng200408-pixel/real-estate-agent/main/setup.sh)
```

### 3. 配置飞书频道（可选）

编辑配置文件，替换为您自己的飞书频道ID：
```bash
nano /opt/hermes-agent/HEARTBEAT.md
```

### 4. 重启并验证

```bash
pkill -f hermes && sleep 2 && hermes run &
hermes doctor
```

## 脚本说明

### 房源匹配

```bash
# 按预算和户型匹配
python3 ~/.hermes/scripts/match_houses.py --budget 80 --layout "3室2厅2卫"

# 按预算和面积范围匹配
python3 ~/.hermes/scripts/match_houses.py --budget 100 --area-min 90 --area-max 130

# 精装修 + 预算限制
python3 ~/.hermes/scripts/match_houses.py --budget 80 --decoration "精装修"
```

### 延迟跟进提醒

```bash
# 看房完成后创建30分钟后提醒
python3 ~/.hermes/scripts/delayed_reminder_悠悠.py create 张三 2026-05-17 14:00 0.5

# 查看所有提醒
python3 ~/.hermes/scripts/delayed_reminder_悠悠.py list

# 删除提醒
python3 ~/.hermes/scripts/delayed_reminder_悠悠.py delete 张三
```

## 目录结构

```
~/.hermes/
├── scripts/
│   ├── delayed_reminder_悠悠.py   # 延迟跟进提醒脚本
│   └── match_houses.py            # 房源匹配脚本
├── skills/domain/real-estate-sales/
│   └── SKILL.md                   # 房产销售技能包
├── data/
│   └── 悠悠房源库.db              # 房源数据库
├── followup_data_悠悠.json        # 客户跟进数据
└── /opt/hermes-agent/
    ├── HEARTBEAT.md               # 定时任务配置
    ├── AGENTS.md                  # 销售跟单规范
    ├── IDENTITY.md                # 身份设定
    └── SOUL.md                    # 人格配置
```

## 客户分级标准

| 级别 | 客户特征 | 跟进周期 |
|------|---------|---------|
| S级 | 已带看、主动问价、1-3个月购房计划 | 2天内 |
| A级 | 有需求未带看、3-6个月购房计划 | 5天内 |
| B级 | 刚咨询、6个月以上计划 | 节假日维护 |

## 自定义数据

示例数据位于 `examples/` 目录，可以替换为真实数据：

- `followup_data_悠悠.json` — 客户跟进数据
- `悠悠房源库.db` — 房源数据库

## 开源协议

MIT License

Copyright (c) 2026 liyuheng200408-pixel

本项目基于 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 开发。