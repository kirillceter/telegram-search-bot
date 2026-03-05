import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from bs4 import BeautifulSoup

TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"

bot = Bot(TOKEN)
dp = Dispatcher()



async def search(query):

    url = f"https://www.google.com/search?q=site:t.me+{query}&num=10"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with aiohttp.ClientSession(headers=headers) as session:

        async with session.get(url) as resp:

            html = await resp.text()

    links = []

    for part in html.split("https://t.me/"):

        if "/" in part:

            link = "https://t.me/" + part.split('"')[0]

            if link not in links:

                links.append(link)

        if len(links) >= 5:
            break

    return links


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer("Отправь слово и я найду посты Telegram")


@dp.message()
async def search_posts(message: Message):

    word = message.text

    wait = await message.answer("Ищу...")

    links = await search(word)

    if not links:

        await wait.edit_text("Ничего не найдено")
        return

    text = ""

    for i, link in enumerate(links, 1):

        text += f"{i}. {link}\n"

    await wait.edit_text(text)


async def main():

    await dp.start_polling(bot)


asyncio.run(main())
