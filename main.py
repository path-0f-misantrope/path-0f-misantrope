import asyncio
from aiogram import Bot, Dispatcher, Router

import config  
import handlers
import utils
ALLOWED_UPDATES = ['message', 'edited_message']  #допускает только выбранные события

bot = Bot(token=config.token)  
dp = Dispatcher() 

dp.include_router(handlers.router) #регистрирует диспетчеры
dp.include_router(utils.utils_rt)  

async def main():
    await bot.delete_webhook(drop_pending_updates=True) #не учитывает запросы до включения бота
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    asyncio.run(main())
