import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from telethon import TelegramClient
from telethon.tl.functions.messages import SearchGlobalRequest

BOT_TOKEN = "PASTE_BOT_TOKEN"
API_ID = 123456
API_HASH = "PASTE_API_HASH"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = TelegramClient("session", API_ID, API_HASH)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🔎 Напиши слово для поиска постов Telegram")


async def search(query):

    result = await client(
        SearchGlobalRequest(
            q=query,
            filter=None,
            min_date=None,
            max_date=None,
            offset_rate=0,
            offset_peer=None,
            offset_id=0,
            limit=5
        )
    )

    posts = []

    for m in result.messages:
        try:
            cid = m.peer_id.channel_id
            link = f"https://t.me/c/{cid}/{m.id}"
            text = (m.text or "Без текста")[:100]

            posts.append(f"{text}\n{link}")
        except:
            pass

    return posts


@dp.message()
async def find(message: types.Message):

    await message.answer("🔎 Ищу...")

    posts = await search(message.text)

    if not posts:
        await message.answer("Ничего не найдено")
        return

    await message.answer("\n\n".join(posts))


async def main():

    await client.start()

    await dp.start_polling(bot)


asyncio.run(main())