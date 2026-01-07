import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

# --- TOKEN ---
TOKEN = os.environ.get("TOKEN")  # добавь через Replit Secrets 🔑

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Главная клавиатура ---
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Здесь может быть ваш каталог", callback_data="show_products")],
        [InlineKeyboardButton(text="❓ Как это помогает магазину", callback_data="how_it_helps")]
    ]
)

# --- Демокаталог с URL картинок ---
products = [
    {"name": "🍎 Яблоки", "price": "100 ₽/кг", "photo": "https://i.imgur.com/1bX5QH6.jpg"},
    {"name": "🍌 Бананы", "price": "80 ₽/кг", "photo": "https://i.imgur.com/4AiXzf8.jpg"},
    {"name": "🥕 Морковь", "price": "50 ₽/кг", "photo": "https://i.imgur.com/0DElr0H.jpg"}
]

# --- /start ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет!\nЯ — DemoSellBot, пример Telegram-бота для магазина.\n"
        "Нажмите кнопку ниже и посмотрите, как это работает 👇",
        reply_markup=main_menu
    )

# --- Обработка кнопок ---
@dp.callback_query()
async def handle_buttons(callback: types.CallbackQuery):
    data = callback.data

    # Показ товаров
    if data == "show_products":
        for product in products:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Заказать", callback_data=f"order_{product['name']}")]]
            )
            await callback.message.answer_photo(
                product["photo"], caption=f"{product['name']}\nЦена: {product['price']}", reply_markup=keyboard
            )

    # Заказ товара
    elif data.startswith("order_"):
        await callback.message.answer(
            "✅ Заказ принят!\nХотите такого бота для своего магазина?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="👍 Да, хочу такого бота", callback_data="lead")],
                    [InlineKeyboardButton(text="👀 Просто смотрю", callback_data="just_looking")]
                ]
            )
        )

    # Захват лида
    elif data == "lead":
        await callback.message.answer(
            "Отлично!\nНапишите ссылку на ваш магазин и что вы продаёте.\n"
            "Мы свяжемся с вами для пилотного запуска.\n\n"
            "📩 Контакт для связи: @bannybub"
        )
        # Возврат к каталогу
        await asyncio.sleep(1)
        await callback.message.answer("Между тем, вот наш демонстрационный каталог товаров:", reply_markup=main_menu)

    elif data == "just_looking":
        await callback.message.answer("Хорошо, смотрите товары и возвращайтесь, когда будет интересно!", reply_markup=main_menu)

    # Польза бота
    elif data == "how_it_helps":
        await callback.message.answer(
            "Наш бот помогает владельцам магазинов:\n"
            "• Автоматизировать ответы на вопросы клиентов\n"
            "• Принимать заказы 24/7\n"
            "• Экономить время и не терять продажи\n\n"
            "Хотите протестировать бота на вашем магазине?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Да, хочу попробовать", callback_data="lead")],
                    [InlineKeyboardButton(text="Пока просто смотрю", callback_data="just_looking")]
                ]
            )
        )

# --- Веб-сервер для UptimeRobot ---
async def handle(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.add_routes([web.get("/", handle)])

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

# --- Запуск бота ---
async def main():
    print("🚀 DemoSellBot запущен...")
    await start_web()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
