#!/bin/bash
set -e

REPO="https://gitee.com/liyuheng888/real-estate-agent.git"
TARGET_DIR="$HOME/.hermes/real-estate-agent"

echo "开始安装悠悠房产机器人..."

# 1. 判断 Hermes Agent 是否已安装
if [ ! -d "$HOME/.hermes" ]; then
    echo "错误：请先安装 Hermes Agent"
    echo "安装命令：curl -LsSf https://setup.hermesagent.ai | sh"
    exit 1
fi

# 2. 判断 Hermes Agent 主目录是否存在
if [ ! -d "/opt/hermes-agent" ]; then
    echo "错误：未找到 /opt/hermes-agent，请确认 Hermes Agent 已正确安装"
    exit 1
fi

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
chmod +x "$HOME/.hermes/scripts/delayed_reminder_悠悠.py"
chmod +x "$HOME/.hermes/scripts/match_houses.py"

# 5. 复制配置文件到 /opt/hermes-agent/（覆盖原官方配置）
echo "复制配置文件到 /opt/hermes-agent/..."
cp "$TARGET_DIR/configs/HEARTBEAT.md" "/opt/hermes-agent/HEARTBEAT.md"
cp "$TARGET_DIR/configs/AGENTS.md" "/opt/hermes-agent/AGENTS.md"
cp "$TARGET_DIR/configs/IDENTITY.md" "/opt/hermes-agent/IDENTITY.md"
cp "$TARGET_DIR/configs/SOUL.md" "/opt/hermes-agent/SOUL.md"
cp "$TARGET_DIR/configs/USER.md" "/opt/hermes-agent/USER.md"
cp "$TARGET_DIR/configs/MEMORY.md" "/opt/hermes-agent/MEMORY.md"

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
echo "   nano /opt/hermes-agent/HEARTBEAT.md"
echo "   将其中的飞书频道 ID 替换为您自己的"
echo ""
echo "2. 重启 Hermes Agent："
echo "   pkill -f hermes && sleep 2 && hermes run &"
echo ""
echo "3. 验证安装："
echo "   hermes doctor"
echo "=========================================="