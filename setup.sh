#!/bin/bash
set -e

REPO="https://github.com/liyuheng200408-pixel/real-estate-agent.git"
TARGET_DIR="$HOME/.hermes/real-estate-agent"

echo "开始安装悠悠房产机器人..."

# 1. 判断 Hermes Agent 是否已安装
if [ ! -d "$HOME/.hermes" ]; then
    echo "错误：请先安装 Hermes Agent"
    echo "安装命令：curl -LsSf https://setup.hermesagent.ai | sh"
    exit 1
fi

# 2. 克隆或更新仓库
if [ -d "$TARGET_DIR" ]; then
    echo "已存在仓库，正在更新..."
    cd "$TARGET_DIR" && git pull
else
    echo "正在克隆仓库..."
    git clone "$REPO" "$TARGET_DIR"
fi

# 3. 复制脚本
echo "复制脚本文件..."
cp "$TARGET_DIR/scripts/delayed_reminder_悠悠.py" "$HOME/.hermes/scripts/"
cp "$TARGET_DIR/scripts/match_houses.py" "$HOME/.hermes/scripts/"
chmod +x "$HOME/.hermes/scripts/delayed_reminder_悠悠.py"
chmod +x "$HOME/.hermes/scripts/match_houses.py"

# 4. 复制配置文件（使用新文件名避免覆盖原有配置）
cp "$TARGET_DIR/configs/HEARTBEAT.md" "$HOME/.hermes/cache/documents/doc_悠悠_HEARTBEAT.md"
cp "$TARGET_DIR/configs/AGENTS.md" "$HOME/.hermes/cache/documents/doc_悠悠_AGENTS.md"
cp "$TARGET_DIR/configs/IDENTITY.md" "$HOME/.hermes/cache/documents/doc_悠悠_IDENTITY.md"
cp "$TARGET_DIR/configs/SOUL.md" "$HOME/.hermes/cache/documents/doc_悠悠_SOUL.md"

# 5. 复制技能包
echo "复制技能包..."
mkdir -p "$HOME/.hermes/skills/domain/real-estate-sales"
cp "$TARGET_DIR/skills/domain/real-estate-sales/SKILL.md" "$HOME/.hermes/skills/domain/real-estate-sales/"

# 6. 初始化示例数据（如果用户还没有真实数据）
if [ ! -f "$HOME/.hermes/followup_data_悠悠.json" ]; then
    cp "$TARGET_DIR/examples/followup_data_悠悠.json" "$HOME/.hermes/followup_data_悠悠.json"
fi

if [ ! -f "$HOME/.hermes/data/悠悠房源库.db" ]; then
    mkdir -p "$HOME/.hermes/data"
    cp "$TARGET_DIR/examples/悠悠房源库.db" "$HOME/.hermes/data/悠悠房源库.db"
fi

# 7. 提示用户配置飞书频道
echo ""
echo "=========================================="
echo "安装完成！请检查以下配置："
echo ""
echo "1. 配置飞书频道："
echo "   编辑 ~/.hermes/cache/documents/doc_悠悠_HEARTBEAT.md"
echo "   将其中的飞书频道 ID 替换为您自己的"
echo ""
echo "2. 重启 Hermes Agent："
echo "   pkill -f hermes && sleep 2 && hermes run &"
echo ""
echo "3. 验证安装："
echo "   hermes doctor"
echo "=========================================="