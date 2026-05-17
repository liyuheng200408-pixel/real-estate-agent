# 悠悠房产机器人 (Real Estate Agent - Yoyo)

基于 Hermes Agent 的房产销售AI助手，支持客户跟进、房源匹配、延迟提醒等功能。

## 功能特性

- 客户分级管理（S/A/B级）
- 房源智能匹配（预算/户型/面积/装修等条件）
- 定时跟进提醒（每日早报、午间检查等）
- 飞书消息推送
- 支持三亚、海口、陵水、儋州等海南主要区域

## 系统要求

- Linux / macOS / WSL2 / Termux
- Node.js 22+
- Python 3.11+
- 飞书机器人（可选，用于消息推送）
- Git（用于克隆仓库）

---

## 快速开始

### 第一步：安装 Hermes Agent

**国内服务器推荐使用 GitHub 镜像或 Gitee 镜像：**

```bash
# 方法一：GitHub（部分服务器可能访问慢）
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 方法二：手动下载安装脚本（推荐网络不稳的国内服务器）
# 步骤：
# 1. 在电脑浏览器打开以下链接并全选复制全部内容：
https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh
# 2. 在服务器上运行：nano /tmp/install.sh（粘贴内容，Ctrl+O 保存，Ctrl+X 退出）
# 3. 运行：bash /tmp/install.sh
```

> 如果以上命令都失败，请在可以访问 GitHub 的机器上下载 install.sh，然后通过 U 盘或内网传到目标服务器。

安装完成后加载环境变量：

```bash
source ~/.bashrc    # 或 source ~/.zshrc
```

验证安装：

```bash
hermes --version
```

---

### 第二步：克隆悠悠房产机器人仓库

```bash
# 方法一：Gitee（推荐国内）
git clone https://gitee.com/liyuheng200408/real-estate-agent.git ~/.hermes/real-estate-agent

# 方法二：GitHub（部分服务器可能访问慢）
git clone https://github.com/liyuheng200408-pixel/real-estate-agent.git ~/.hermes/real-estate-agent
```

---

### 第三步：运行安装脚本

```bash
bash ~/.hermes/real-estate-agent/setup.sh
```

setup.sh 会自动完成以下操作：

1. 检查 Hermes Agent 是否已安装
2. 复制4个脚本到 `~/.hermes/scripts/`（房源匹配、看房提醒、早报、月报）
3. 复制6个配置文件到 `/opt/hermes-agent/`（覆盖官方默认配置）
4. 复制技能包到 `~/.hermes/skills/domain/real-estate-sales/`
5. 初始化示例数据（客户跟进表和房源库）

---

### 第四步：配置飞书机器人

定时提醒（早报、午间检查、晚间总结等）通过飞书推送。

1. 在飞书创建自定义机器人，拿到 Webhook 地址
2. 编辑 `/opt/hermes-agent/HEARTBEAT.md`，把里面的飞书配置替换为您自己的
3. 如果使用其他 IM 工具，修改对应 cron 任务的 prompt

---

### 第五步：重启并验证

```bash
pkill -f hermes && sleep 2 && hermes run &
hermes doctor
```

---

### 后续维护

更新到最新版本：

```bash
cd ~/.hermes/real-estate-agent && git pull
bash ~/.hermes/real-estate-agent/setup.sh
```

替换为自己的数据：

- 客户跟进数据：`~/.hermes/followup_data_悠悠.json`
- 房源数据库：`~/.hermes/data/悠悠房源库.db`

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
    ├── SOUL.md                    # 人格配置
    ├── USER.md                    # 用户偏好
    └── MEMORY.md                  # 记忆数据
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

悠悠房产机器人的核心配置文件（HEARTBEAT.md、AGENTS.md、IDENTITY.md、SOUL.md、USER.md、MEMORY.md）以及配套脚本（match_houses.py、delayed_reminder_悠悠.py 等）为房产机器人 AI 生成，版权归委托方（买家）所有，即本仓库所有者。