---
name: astrbot-plugin-generator
description: Generate a complete AstrBot plugin project scaffold with metadata.yaml, main.py, and requirements.txt. Use when creating new AstrBot plugins or extensions.
---

# AstrBot Plugin Generator

This skill helps you create a complete AstrBot plugin project that conforms to the AstrBot plugin specification.

## When to Use

Use this skill when the user wants to:
- Create a new AstrBot plugin project
- Generate an AstrBot plugin scaffold/template
- Start developing an AstrBot extension
- Build a custom AstrBot skill

## Instructions

When this skill is activated, follow these steps to generate a complete AstrBot plugin project:

### Step 1: Gather Information

Ask the user for the following information:

1. **Plugin name**: The plugin identifier (must start with `astrbot_plugin_`, lowercase, underscores only, no spaces)
   - Example: `astrbot_plugin_weather`, `astrbot_plugin_music`
   
2. **Display name**: A human-readable name for the plugin
   - Example: "Weather Query", "Music Player"

3. **Description**: A brief description of what the plugin does
   - Example: "A plugin that provides weather query functionality"

4. **Author**: The author's name or GitHub username

5. **Version**: Initial version (default: "0.1.0")

6. **Repository URL**: The GitHub/Gitee repository URL (optional)

7. **Plugin functionality**: What commands or features should the plugin have?
   - Describe the main functionality so appropriate command handlers can be generated

8. **Supported platforms** (optional): Which platforms does the plugin support?
   - Valid values: `telegram`, `aiocqhttp`, `discord`, `qq_official`, `wecom`, `dingtalk`, `lark`
   - Default: all platforms

### Step 2: Generate Project Files

Create the following directory structure:

```
astrbot_plugin_<name>/
  metadata.yaml
  main.py
  requirements.txt
```

#### 2.1 Generate `metadata.yaml`

```yaml
name: astrbot_plugin_<name>
display_name: <display_name>
desc: <description>
author: <author>
version: "<version>"
repo: <repo_url or empty string>

# Optional: add if user specified platforms
support_platforms:
  - telegram
  - aiocqhttp
  - discord
  - qq_official
  - wecom
  - dingtalk
  - lark

# Optional: add if user needs version constraint
astrbot_version: ">=4.16,<5"
```

#### 2.2 Generate `main.py`

Use this template and customize based on user's functionality requirements:

```python
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star
from astrbot.api import logger


class Main(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("<command_name>")
    async def <command_name>(self, event: AstrMessageEvent):
        '''<command description>'''
        user_name = event.get_sender_name()
        message_str = event.message_str
        logger.info(f"<command_name> triggered by {user_name}: {message_str}")
        
        # TODO: Implement your logic here
        yield event.plain_result(f"Hello, {user_name}!")

    async def terminate(self):
        '''Cleanup resources when plugin is unloaded.'''
        pass
```

**Key Rules for `main.py`:**

1. **Class naming**: The class MUST be named `Main` and inherit from `Star`
2. **Constructor**: Takes `Context` parameter, calls `super().__init__(context)`
3. **Command registration**: Use `@filter.command("name")` decorator
4. **Message reply**: Use `yield event.plain_result(text)` for text replies
5. **Logging**: Import and use `logger` from `astrbot.api`, NOT `print()`
6. **Async only**: All network requests must use `aiohttp` or `httpx`, NEVER `requests`

**Advanced decorators:**

```python
# Admin-only command
from astrbot.api.event.filter import permission_type, PermissionType

@filter.permission_type(PermissionType.ADMIN)
@filter.command("admin_cmd")
async def admin_cmd(self, event: AstrMessageEvent):
    yield event.plain_result("Admin command executed!")

# Regex pattern matching
@filter.regex(r"hello|hi|hey")
async def greet(self, event: AstrMessageEvent):
    yield event.plain_result("Hello there!")

# Platform-specific handler
@filter.platform("telegram")
@filter.command("tg_only")
async def telegram_only(self, event: AstrMessageEvent):
    yield event.plain_result("This only works on Telegram!")
```

**Useful event methods:**

| Method | Description |
|--------|-------------|
| `event.get_sender_name()` | Get sender's display name |
| `event.get_sender_id()` | Get sender's unique ID |
| `event.message_str` | Get message text content |
| `event.is_private_chat()` | Check if private chat |
| `event.get_session_id()` | Get session ID |
| `event.plain_result(text)` | Create text reply |
| `event.image_result(url)` | Create image reply |

#### 2.3 Generate `requirements.txt`

Only include third-party dependencies the plugin actually needs:

```
aiohttp>=3.8.0
```

Do NOT include `astrbot` itself as a dependency.

### Step 3: Provide Usage Summary

After generating all files, inform the user:

1. **Generated files list** with their purposes
2. **Available commands** the plugin registers
3. **Installation instructions**:
   - Copy the plugin folder to `AstrBot/data/plugins/`
   - Restart AstrBot or use hot-reload from WebUI (Plugin Management > `...` > Reload)
   - Test commands in a chat

4. **Development tips**:
   - Use WebUI for hot-reload during development
   - Check logs in WebUI or console for debugging
   - Store persistent data in global `data/` directory, not plugin folder

## Templates

The following templates are provided in the `templates/` directory:

- `metadata.yaml` - Basic metadata template
- `main.py` - Minimal plugin code template

## Important Guidelines

- **Async patterns**: All I/O operations must be async
- **Error handling**: Wrap risky operations in try/except to prevent bot crashes
- **Code quality**: Follow ruff formatting standards
- **Documentation**: Add docstrings to command handlers
- **Data persistence**: Use global `data/` directory for persistent storage
- **Class name**: MUST be `Main` - this is an AstrBot requirement

## Example Usage

User: "Create an AstrBot plugin that can query weather"

Response:
1. Ask for plugin name → `astrbot_plugin_weather`
2. Ask for description → "Weather query plugin"
3. Ask for author → "DeveloperName"
4. Ask for functionality → "Commands: /weather <city> to query current weather"

Generated files:
- `astrbot_plugin_weather/metadata.yaml`
- `astrbot_plugin_weather/main.py` with `/weather` command
- `astrbot_plugin_weather/requirements.txt` with `aiohttp`
