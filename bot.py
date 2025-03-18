import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "7270373741:AAGmJ6m_KDMfNiNIdRC198L91S_SkTHLeBg"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


class CareerTest(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    question_12 = State()


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔄 Начать заново")]], resize_keyboard=True
)

keyboard_q2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="До 18")], [KeyboardButton(text="18–25")],
        [KeyboardButton(text="26–35")], [KeyboardButton(text="36+")],
    ], resize_keyboard=True
)

keyboard_q3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Высокие зарплаты")], [KeyboardButton(text="Интерес к технологиям")],
        [KeyboardButton(text="Удалённая работа")], [KeyboardButton(text="Перспективы роста")],
    ], resize_keyboard=True
)

keyboard_q4 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Программирование")], [KeyboardButton(text="Разработка интерфейсов (UI)")],
        [KeyboardButton(text="Аналитика данных")], [KeyboardButton(text="Администрирование и DevOps")],
        [KeyboardButton(text="Мобильная разработка")], [KeyboardButton(text="Кибербезопасность")],
    ], resize_keyboard=True
)

keyboard_q5 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Docker, Kubernetes")], [KeyboardButton(text="React, Vue.js")],
        [KeyboardButton(text="Python, Django")], [KeyboardButton(text="SQL, MongoDB")],
        [KeyboardButton(text="Flutter, Swift")],
    ], resize_keyboard=True
)

keyboard_q6 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Python")], [KeyboardButton(text="JavaScript")],
        [KeyboardButton(text="Java")], [KeyboardButton(text="C++")],
        [KeyboardButton(text="Go")],
    ], resize_keyboard=True
)

keyboard_q7 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Менее 1 часа")], [KeyboardButton(text="1–3 часа")],
        [KeyboardButton(text="3–5 часов")], [KeyboardButton(text="Больше 5 часов")],
    ], resize_keyboard=True
)

keyboard_q8 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нет, я новичок")], [KeyboardButton(text="Базовые знания (курсы)")],
        [KeyboardButton(text="Есть опыт программирования")], [KeyboardButton(text="Работал в IT")],
    ], resize_keyboard=True
)

keyboard_q9 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начальный (A1–A2)")], [KeyboardButton(text="Средний (B1–B2)")],
        [KeyboardButton(text="Продвинутый (C1–C2)")], [KeyboardButton(text="Не знаю английский")],
    ], resize_keyboard=True
)

keyboard_q10 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="В команде разработки")], [KeyboardButton(text="В аналитической компании")],
        [KeyboardButton(text="В сфере безопасности")], [KeyboardButton(text="В стартапе")],
        [KeyboardButton(text="В крупной IT-компании")],
    ], resize_keyboard=True
)

keyboard_q11 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оптимизация систем")], [KeyboardButton(text="Разработка UI")],
        [KeyboardButton(text="Анализ данных")], [KeyboardButton(text="Обеспечение безопасности")],
    ], resize_keyboard=True
)

keyboard_q12 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Работать в команде над большими проектами")],
        [KeyboardButton(text="Самостоятельно решать задачи")],
        [KeyboardButton(text="Экспериментировать и создавать новое")],
        [KeyboardButton(text="Анализировать и улучшать готовое")],
    ], resize_keyboard=True
)


resources = {
    'q4': {
        "Программирование": "https://www.codecademy.com/catalog/subject/all",
        "Разработка интерфейсов (UI)": "https://www.freecodecamp.org/news/learn-responsive-web-design/",
        "Аналитика данных": "https://www.datacamp.com/courses/intro-to-python-for-data-science",
        "Администрирование и DevOps": "https://www.edx.org/learn/devops",
        "Мобильная разработка": "https://developer.android.com/courses",
        "Кибербезопасность": "https://www.coursera.org/learn/intro-to-cyber-security",
    },
    'q5': {
        "Docker, Kubernetes": "https://www.udemy.com/course/docker-mastery/",
        "React, Vue.js": "https://reactjs.org/docs/getting-started.html",
        "Python, Django": "https://www.djangoproject.com/start/",
        "SQL, MongoDB": "https://www.codecademy.com/learn/learn-sql",
        "Flutter, Swift": "https://flutter.dev/docs",
    },
    'q6': {
        "Python": "https://www.learnpython.org/",
        "JavaScript": "https://www.javascript.com/learn",
        "Java": "https://www.codecademy.com/learn/learn-java",
        "C++": "https://www.learncpp.com/",
        "Go": "https://golang.org/doc/",
    },
}


@router.message(Command("test"))
@router.message(lambda message: message.text == "🔄 Начать заново")
async def start_test(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(CareerTest.question_1)
    await message.answer(
        "📟 **IT Тест**\n\n"
        "Я задам тебе несколько вопросов, чтобы подобрать подходящую IT-специальность.\n\n"
        "💡 Вопрос 1: Как тебя зовут?",
        reply_markup=None
    )


@router.message(CareerTest.question_1)
async def answer_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    await state.set_state(CareerTest.question_2)
    await message.answer("💡 Вопрос 2: Сколько тебе лет?", reply_markup=keyboard_q2)


@router.message(CareerTest.question_2)
async def answer_q2(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q2=message.text)
    await state.set_state(CareerTest.question_3)
    await message.answer("💡 Вопрос 3: Почему ты заинтересовался IT?", reply_markup=keyboard_q3)


@router.message(CareerTest.question_3)
async def answer_q3(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q3=message.text)
    await state.set_state(CareerTest.question_4)
    await message.answer("💡 Вопрос 4: Какую сферу IT тебе хотелось бы изучать?", reply_markup=keyboard_q4)


@router.message(CareerTest.question_4)
async def answer_q4(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q4=message.text)
    resource = resources['q4'].get(message.text, "Ресурс не найден")
    await state.set_state(CareerTest.question_5)
    await message.answer(
        f"🌐 Ресурс: {resource}\n\n💡 Вопрос 5: Какие технологии тебе интересны?",
        reply_markup=keyboard_q5
    )


@router.message(CareerTest.question_5)
async def answer_q5(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q5=message.text)
    resource = resources['q5'].get(message.text, "Ресурс не найден")
    await state.set_state(CareerTest.question_6)
    await message.answer(
        f"🌐 Ресурс: {resource}\n\n💡 Вопрос 6: Какие языки программирования тебе интересны?",
        reply_markup=keyboard_q6
    )


@router.message(CareerTest.question_6)
async def answer_q6(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q6=message.text)
    resource = resources['q6'].get(message.text, "Ресурс не найден")
    await state.set_state(CareerTest.question_7)
    await message.answer(
        f"🌐 Ресурс: {resource}\n\n💡 Вопрос 7: Сколько времени ты готов тратить на обучение в день?",
        reply_markup=keyboard_q7
    )


@router.message(CareerTest.question_7)
async def answer_q7(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q7=message.text)
    await state.set_state(CareerTest.question_8)
    await message.answer("💡 Вопрос 8: Есть ли у тебя опыт в IT?", reply_markup=keyboard_q8)


@router.message(CareerTest.question_8)
async def answer_q8(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q8=message.text)
    await state.set_state(CareerTest.question_9)
    await message.answer("💡 Вопрос 9: Какой у тебя уровень английского?", reply_markup=keyboard_q9)


@router.message(CareerTest.question_9)
async def answer_q9(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q9=message.text)
    await state.set_state(CareerTest.question_10)
    await message.answer("💡 Вопрос 10: Где бы ты хотел работать?", reply_markup=keyboard_q10)


@router.message(CareerTest.question_10)
async def answer_q10(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q10=message.text)
    await state.set_state(CareerTest.question_11)
    await message.answer("💡 Вопрос 11: С какими задачами тебе бы хотелось сталкиваться?", reply_markup=keyboard_q11)


@router.message(CareerTest.question_11)
async def answer_q11(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q11=message.text)
    await state.set_state(CareerTest.question_12)
    await message.answer("💡 Вопрос 12: Какой стиль работы тебе ближе?", reply_markup=keyboard_q12)


@router.message(CareerTest.question_12)
async def answer_q12(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново":
        await start_test(message, state)
        return
    await state.update_data(q12=message.text)
    user_data = await state.get_data()

    specialty = "Не определено"
    description = ""
    resource = "https://www.google.com"
    if user_data["q4"] == "Программирование" and user_data["q6"] == "JavaScript":
        specialty = "Frontend-разработчик"
        description = "Создаёшь интерфейсы сайтов с помощью HTML, CSS и JavaScript."
        resource = "https://www.freecodecamp.org/news/learn-responsive-web-design/"
    elif user_data["q4"] == "Аналитика данных" and user_data["q11"] == "Анализ данных":
        specialty = "Аналитик данных"
        description = "Работаешь с большими данными, анализируешь и визуализируешь их."
        resource = "https://www.datacamp.com/courses/intro-to-python-for-data-science"
    elif user_data["q4"] == "Кибербезопасность":
        specialty = "Специалист по кибербезопасности"
        description = "Защищаешь системы от угроз и атак."
        resource = "https://www.coursera.org/learn/intro-to-cyber-security"

    await message.answer(
        f"📊 **Результаты теста, {user_data['q1']}!**\n\n"
        f"1. Возраст: {user_data['q2']}\n"
        f"2. Мотивация: {user_data['q3']}\n"
        f"3. Сфера: {user_data['q4']}\n"
        f"4. Технологии: {user_data['q5']}\n"
        f"5. Языки: {user_data['q6']}\n"
        f"6. Время на обучение: {user_data['q7']}\n"
        f"7. Опыт: {user_data['q8']}\n"
        f"8. Английский: {user_data['q9']}\n"
        f"9. Где работать: {user_data['q10']}\n"
        f"10. Задачи: {user_data['q11']}\n"
        f"11. Стиль работы: {user_data['q12']}\n\n"
        f"🎯 **Рекомендуемая специальность:** {specialty}\n"
        f"ℹ️ {description}\n"
        f"🔗 Ресурс: {resource}",
        reply_markup=main_keyboard
    )
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())