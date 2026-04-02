"""
AstrBot Plugin Template
Replace <placeholders> with your actual values
"""

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star
from astrbot.api import logger


class Main(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("hello")
    async def hello(self, event: AstrMessageEvent):
        '''Say hello to the user'''
        user_name = event.get_sender_name()
        logger.info(f"hello command triggered by {user_name}")
        yield event.plain_result(f"Hello, {user_name}!")

    @filter.command("help")
    async def help_cmd(self, event: AstrMessageEvent):
        '''Show help message'''
        help_text = """Available commands:
/hello - Say hello
/help - Show this help message
"""
        yield event.plain_result(help_text)

    async def terminate(self):
        '''Cleanup resources when plugin is unloaded.'''
        logger.info("Plugin is being unloaded")
        pass
