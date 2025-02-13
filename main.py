import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot,Dispatcher
from app.hendlers import router
from app.SQLite import creation,newsletter
from datetime import datetime
import app.request as req
from app.SQLite import giv_data
from app.button import beck_keyboard
load_dotenv()
api_key = os.getenv('TG_API')

bot = Bot(token=api_key)
dp = Dispatcher()

async def send_daily_messages():
    pass
    while True:
        print("True")
        users,flag = await newsletter()
        if not users == "":
            for i in range(len(flag)):
                try:
                    if flag[i] == 1:
                        now = datetime.now()
                        today = str(now.date())
                        date = list(await giv_data(users[i]))[1]
                        result = req.validate(int(date[0:2]), int(date[3:5]), int(today[8:10]), int(today[5:7]),
                                              int(today[0:4]))
                        await bot.send_photo(int(users[i]), result[2],caption=f"Прогноз на {today}")
                        await bot.send_message(int(users[i]),f" Ваш Нумерологический код этого дня: {result[0]}\n{result[1]}",reply_markup=beck_keyboard)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения пользователю {users[i]}: {e}")

        await asyncio.sleep(86400)  # Ждем 24 часа


async def main():
    await creation()
    dp.include_router(router)
    await asyncio.gather(
        send_daily_messages(),
        dp.start_polling(bot))



if __name__ == "__main__":
    asyncio.run(main())
