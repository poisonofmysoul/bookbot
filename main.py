import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from config_data.config import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)

router = Router()
# routers = [default_router]


# def register_handlers(main_router: Router):
#     for router in routers:
#         main_router.include_router(router)


async def main():
    logging.basicConfig(level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger.info('starting bot')
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    await set_main_menu(bot)
    # register_handlers(dp)
    dp.include_router(user_handlers.router)
    # dp.include_router(other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())