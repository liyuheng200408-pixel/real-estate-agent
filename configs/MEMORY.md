- `~/.hermes/data/悠悠客户管理.xlsx` — 客户管理（含种类买房/租房）
- `~/.hermes/data/悠悠房源库.db` — 房源库（含种类出租/出售）
- `~/.hermes/悠悠知识库/` — 知识库
- `~/.hermes/data/悠悠房源资料/` — 房源文件
- `~/.hermes/data/悠悠客户资料/` — 客户文件
§
爬取房源时必须附带链接详情（58同城移动版URL），不能只提供小区/价格/户型信息。这是固定要求，每次发房源清单必须包含可点击链接。
§
飞书定时提醒去英文尾巴大法：用deliver=local + python3/curl直接调Bot API发送，消息只发飞书不回调聊天，绝无多余文字。具体方法：创建cron时deliver='local'，prompt里用python3发消息，发完只输出提醒内容本身，不要输出任何其他文字。
§
这台电脑的Chrome在Wayland模式运行，开启--remote-debugging-port后端口绑定到Unix socket而非TCP，外部无法连接。需要加--ozone-platform=x11参数才能用CDP协议远程控制。