# xhs-api-cli

小红书命令行工具：通过逆向 API 搜索笔记、阅读内容、互动操作。使用浏览器 Cookie 认证，无需 API Key，纯 HTTP 请求。

## Install

```bash
cd ~/code/xhs-api-cli
uv sync
uv pip install -e .
```

## Usage

```bash
# Check connection
xhs status

# Search notes
xhs search "AI编程" --sort popular

# Read a note
xhs read <note_id_or_url>

# Get comments
xhs comments <note_id_or_url>

# User profile
xhs user <user_id>
xhs user-posts <user_id>

# Browse feed
xhs feed

# Search topics
xhs topics "Claude Code"
```

All commands support `--json` for raw JSON output.

## How It Works

Uses browser cookies from Chrome/Safari/Firefox and signs API requests with the XHS signing algorithm. No browser automation — pure HTTP requests.

## License

Apache-2.0
