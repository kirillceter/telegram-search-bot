import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def search_tg(query):
    url = f"https://searx.tiekoetter.com/search?q=site:t.me+{query}&format=json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    links = []

    for result in data.get("results", []):
        link = result.get("url")

        if "t.me/" in link:
            links.append(link)

    return links[:3]


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Отправь слово, я найду Telegram посты 🔎")


@dp.message()
async def search(message: types.Message):
    query = message.text

    await message.answer("Ищу...")

    links = await search_tg(query)

    if not links:
        await message.answer("Ничего не найдено")
        return

    text = "\n\n".join(links)

    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())