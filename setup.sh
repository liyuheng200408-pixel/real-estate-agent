#!/bin/bash
set -e

REPO="https://gitee.com/liyuheng200408/real-estate-agent.git"
TARGET_DIR="$HOME/.hermes/real-estate-agent"

echo "开始安装悠悠房产机器人..."

# 1. 判断 Hermes Agent 是否已安装
if [ ! -d "$HOME/.hermes" ]; then
    echo "错误：请先安装 Hermes Agent"
    echo "安装命令：curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
    exit 1
fi

# 2. 自动查找 Hermes Agent 安装目录
HERMES_DIR=""
if [ -d "/opt/hermes-agent" ]; then
    HERMES_DIR="/opt/hermes-agent"
elif [ -d "/usr/local/lib/hermes-agent" ]; then
    HERMES_DIR="/usr/local/lib/hermes-agent"
elif [ -d "$HOME/.hermes/hermes-agent" ]; then
    HERMES_DIR="$HOME/.hermes/hermes-agent"
else
    echo "错误：未找到 Hermes Agent 安装目录，请确认 Hermes Agent 已正确安装"
    exit 1
fi

echo "检测到 Hermes Agent 安装目录：$HERMES_DIR"

# 3. 克隆或更新仓库
if [ -d "$TARGET_DIR" ]; then
    echo "已存在仓库，正在更新..."
    cd "$TARGET_DIR" && git pull
else
    echo "正在克隆仓库..."
    git clone "$REPO" "$TARGET_DIR"
fi

# 4. 复制脚本到 ~/.hermes/scripts/
echo "复制脚本文件..."
cp "$TARGET_DIR/scripts/delayed_reminder_悠悠.py" "$HOME/.hermes/scripts/"
cp "$TARGET_DIR/scripts/match_houses.py" "$HOME/.hermes/scripts/"
cp "$TARGET_DIR/scripts/daily_report_悠悠.py" "$HOME/.hermes/scripts/"
cp "$TARGET_DIR/scripts/monthly_report_悠悠.py" "$HOME/.hermes/scripts/"
chmod +x "$HOME/.hermes/scripts/delayed_reminder_悠悠.py"
chmod +x "$HOME/.hermes/scripts/match_houses.py"
chmod +x "$HOME/.hermes/scripts/daily_report_悠悠.py"
chmod +x "$HOME/.hermes/scripts/monthly_report_悠悠.py"

# 5. 复制配置文件到 Hermes Agent 安装目录（覆盖原官方配置）
echo "复制配置文件到 $HERMES_DIR/..."
cp "$TARGET_DIR/configs/HEARTBEAT.md" "$HERMES_DIR/HEARTBEAT.md"
cp "$TARGET_DIR/configs/AGENTS.md" "$HERMES_DIR/AGENTS.md"
cp "$TARGET_DIR/configs/IDENTITY.md" "$HERMES_DIR/IDENTITY.md"
cp "$TARGET_DIR/configs/SOUL.md" "$HERMES_DIR/SOUL.md"
cp "$TARGET_DIR/configs/USER.md" "$HERMES_DIR/USER.md"
cp "$TARGET_DIR/configs/MEMORY.md" "$HERMES_DIR/MEMORY.md"

# 6. 复制技能包到 ~/.hermes/skills/domain/real-estate-sales/
echo "复制技能包..."
mkdir -p "$HOME/.hermes/skills/domain/real-estate-sales"
cp "$TARGET_DIR/skills/domain/real-estate-sales/SKILL.md" "$HOME/.hermes/skills/domain/real-estate-sales/"

# 7. 初始化示例数据（如果用户还没有真实数据）
if [ ! -f "$HOME/.hermes/followup_data_悠悠.json" ]; then
    cp "$TARGET_DIR/examples/followup_data_悠悠.json" "$HOME/.hermes/followup_data_悠悠.json"
fi

if [ ! -f "$HOME/.hermes/data/悠悠房源库.db" ]; then
    mkdir -p "$HOME/.hermes/data"
    cp "$TARGET_DIR/examples/悠悠房源库.db" "$HOME/.hermes/data/悠悠房源库.db"
fi

# 8. 提示用户配置飞书频道
echo ""
echo "=========================================="
echo "安装完成！请检查以下配置："
echo ""
echo "1. 配置飞书频道："
echo "   nano $HERMES_DIR/HEARTBEAT.md"
echo "   将其中的飞书频道 ID 替换为您自己的"
echo ""
echo "2. 重启 Hermes Agent："
echo "   pkill -f hermes && sleep 2 && hermes run &"
echo ""
echo "3. 验证安装："
echo "   hermes doctor"
echo "=========================================="