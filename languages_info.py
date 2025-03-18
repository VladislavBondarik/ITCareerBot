import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

API_TOKEN = '7270373741:AAGmJ6m_KDMfNiNIdRC198L91S_SkTHLeBg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

languages = {
    'Python': {
        'description': 'Язык программирования высокого уровня с поддержкой различных парадигм.',
        'resources': [
            'https://docs.python.org/3/',
            'https://realpython.com/',
            'https://www.python.org/doc/'
        ],
    },
    'JavaScript': {
        'description': 'Язык программирования для создания динамичных веб-страниц.',
        'resources': [
            'https://developer.mozilla.org/ru/docs/Web/JavaScript',
            'https://javascript.info/',
            'https://www.ecma-international.org/publications-and-standards/standards/ecma-262/'
        ],
    },
    'Java': {
        'description': 'Объектно-ориентированный язык программирования, используется для создания приложений, от мобильных до серверных.',
        'resources': [
            'https://docs.oracle.com/en/java/',
            'https://www.javatpoint.com/java-tutorial',
            'https://www.java.com/en/docs/'
        ],
    },
    'C++': {
        'description': 'Язык программирования общего назначения, используемый для разработки ПО с высокими требованиями к производительности.',
        'resources': [
            'https://en.cppreference.com/w/',
            'https://www.learncpp.com/',
            'https://www.cplusplus.com/doc/tutorial/'
        ],
    },
    'Ruby': {
        'description': 'Язык программирования, ориентированный на простоту и продуктивность.',
        'resources': [
            'https://www.ruby-lang.org/en/documentation/',
            'https://www.learnrubythehardway.org/',
            'https://ruby-doc.org/'
        ],
    },
    'PHP': {
        'description': 'Скриптовый язык программирования для веб-разработки.',
        'resources': [
            'https://www.php.net/docs.php',
            'https://www.learn-php.org/',
            'https://www.phptherightway.com/'
        ],
    },
    'Go': {
        'description': 'Язык программирования с фокусом на производительность и удобство разработки.',
        'resources': [
            'https://golang.org/doc/',
            'https://www.learn-go.org/',
            'https://gobyexample.com/'
        ],
    },
    'Swift': {
        'description': 'Язык программирования от Apple, предназначенный для создания iOS и macOS приложений.',
        'resources': [
            'https://developer.apple.com/swift/',
            'https://www.raywenderlich.com/ios/paths/learn-swift',
            'https://www.hackingwithswift.com/'
        ],
    },
    'Kotlin': {
        'description': 'Современный язык программирования, совместимый с Java, используется для разработки Android-приложений.',
        'resources': [
            'https://kotlinlang.org/docs/home.html',
            'https://developer.android.com/kotlin',
            'https://www.baeldung.com/kotlin'
        ],
    },
    'Rust': {
        'description': 'Язык программирования с фокусом на безопасность, производительность и параллельность.',
        'resources': [
            'https://doc.rust-lang.org/book/',
            'https://www.rust-lang.org/learn',
            'https://www.rust-lang.org/learn/get-started'
        ],
    }
}

dp.message(Command("start"))


async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    for lang in languages.keys():
        keyboard.add(InlineKeyboardButton(text=lang, callback_data=lang))

    await message.answer("Выберите язык программирования:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in languages)
async def handle_language_choice(callback_query: types.CallbackQuery, user_data=None):
    language = callback_query.data
    user_data[callback_query.from_user.id] = language

    info = languages[language]
    description = info["description"]
    resources = "\n".join(info["resources"])

    message_text = f"📌 **{language}**\n\n📝 {description}\n🔗 Полезные ссылки:\n{resources}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Продолжить обучение", callback_data="continue"))
    keyboard.add(InlineKeyboardButton("Сменить язык", callback_data="change_language"))

    await callback_query.message.edit_text(message_text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "continue")
async def continue_learning(callback_query: types.CallbackQuery, user_data=None):
    user_id = callback_query.from_user.id
    language = user_data.get(user_id)

    if language:
        await callback_query.message.edit_text(f"Вы продолжаете обучение на языке **{language}**. 🚀")
    else:
        await callback_query.message.edit_text("Вы не выбрали язык. Пожалуйста, выберите язык.")


@dp.callback_query(lambda c: c.data == "change_language")
async def change_language(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    for lang in languages.keys():
        keyboard.add(InlineKeyboardButton(text=lang, callback_data=lang))

    await callback_query.message.edit_text("Выберите новый язык программирования:", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
