import asyncio
import sqlite3
import json
import aiohttp
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7270373741:AAGmJ6m_KDMfNiNIdRC198L91S_SkTHLeBg"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


class Database:
    def __init__(self, db_name="career_test.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            answers TEXT,
            specialty TEXT,
            feedback INTEGER DEFAULT 0)''')
        self.conn.commit()

    def save_user(self, user_id, name, answers, specialty):
        self.cursor.execute("INSERT OR REPLACE INTO users (user_id, name, answers, specialty) VALUES (?, ?, ?, ?)",
                           (user_id, name, json.dumps(answers), specialty))
        self.conn.commit()

    def update_feedback(self, user_id, feedback):
        self.cursor.execute("UPDATE users SET feedback = ? WHERE user_id = ?", (feedback, user_id))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT name, answers, specialty FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_stats(self):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE feedback = 1")
        likes = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE feedback = -1")
        dislikes = self.cursor.fetchone()[0]
        return likes, dislikes

    def __del__(self):
        self.conn.close()


db = Database()


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


main_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔄 Начать заново")]], resize_keyboard=True)
keyboard_q2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="До 18")], [KeyboardButton(text="18–25")], [KeyboardButton(text="26–35")], [KeyboardButton(text="36+")]], resize_keyboard=True)
keyboard_q3 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Высокие зарплаты")], [KeyboardButton(text="Интерес к технологиям")], [KeyboardButton(text="Удалённая работа")], [KeyboardButton(text="Перспективы роста")]], resize_keyboard=True)
keyboard_q4 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Программирование")], [KeyboardButton(text="Разработка интерфейсов (UI)")], [KeyboardButton(text="Аналитика данных")], [KeyboardButton(text="Администрирование и DevOps")], [KeyboardButton(text="Мобильная разработка")], [KeyboardButton(text="Кибербезопасность")]], resize_keyboard=True)
keyboard_q5 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Docker, Kubernetes")], [KeyboardButton(text="React, Vue.js")], [KeyboardButton(text="Python, Django")], [KeyboardButton(text="SQL, MongoDB")], [KeyboardButton(text="Flutter, Swift")]], resize_keyboard=True)
keyboard_q6 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Python")], [KeyboardButton(text="JavaScript")], [KeyboardButton(text="Java")], [KeyboardButton(text="C++")], [KeyboardButton(text="Go")]], resize_keyboard=True)
keyboard_q7 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Менее 1 часа")], [KeyboardButton(text="1–3 часа")], [KeyboardButton(text="3–5 часов")], [KeyboardButton(text="Больше 5 часов")]], resize_keyboard=True)
keyboard_q8 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Нет, я новичок")], [KeyboardButton(text="Базовые знания (курсы)")], [KeyboardButton(text="Есть опыт программирования")], [KeyboardButton(text="Работал в IT")]], resize_keyboard=True)
keyboard_q9 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Начальный (A1–A2)")], [KeyboardButton(text="Средний (B1–B2)")], [KeyboardButton(text="Продвинутый (C1–C2)")], [KeyboardButton(text="Не знаю английский")]], resize_keyboard=True)
keyboard_q10 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="В команде разработки")], [KeyboardButton(text="В аналитической компании")], [KeyboardButton(text="В сфере безопасности")], [KeyboardButton(text="В стартапе")], [KeyboardButton(text="В крупной IT-компании")]], resize_keyboard=True)
keyboard_q11 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Оптимизация систем")], [KeyboardButton(text="Разработка UI")], [KeyboardButton(text="Анализ данных")], [KeyboardButton(text="Обеспечение безопасности")]], resize_keyboard=True)
keyboard_q12 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Работать в команде над большими проектами")], [KeyboardButton(text="Самостоятельно решать задачи")], [KeyboardButton(text="Экспериментировать и создавать новое")], [KeyboardButton(text="Анализировать и улучшать готовое")]], resize_keyboard=True)


async def get_course_resource(specialty):
    async with aiohttp.ClientSession() as session:
        keyword = specialty.split()[0]
        url = f"https://stepik.org/api/courses?search={keyword}&language=ru"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                courses = data.get("courses", [])
                if courses:
                    course = courses[0]
                    return f"https://stepik.org/course/{course['id']}"
            return "https://stepik.org/catalog"


@router.message(Command("test"))
@router.message(lambda message: message.text == "🔄 Начать заново")
async def start_test(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(CareerTest.question_1)
    await message.answer("📟 **IT Тест**\n\nЯ задам тебе несколько вопросов, чтобы подобрать подходящую IT-специальность.\n\n💡 Вопрос 1: Как тебя зовут?", reply_markup=None)


@router.message(CareerTest.question_1)
async def answer_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    await state.set_state(CareerTest.question_2)
    await message.answer("💡 Вопрос 2: Сколько тебе лет?", reply_markup=keyboard_q2)


@router.message(CareerTest.question_2)
async def answer_q2(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q2=message.text)
    await state.set_state(CareerTest.question_3)
    await message.answer("💡 Вопрос 3: Почему ты заинтересовался IT?", reply_markup=keyboard_q3)


@router.message(CareerTest.question_3)
async def answer_q3(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q3=message.text)
    await state.set_state(CareerTest.question_4)
    await message.answer("💡 Вопрос 4: Какую сферу IT тебе хотелось бы изучать?", reply_markup=keyboard_q4)


@router.message(CareerTest.question_4)
async def answer_q4(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q4=message.text)
    await state.set_state(CareerTest.question_5)
    await message.answer("💡 Вопрос 5: Какие технологии тебе интересны?", reply_markup=keyboard_q5)


@router.message(CareerTest.question_5)
async def answer_q5(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q5=message.text)
    await state.set_state(CareerTest.question_6)
    await message.answer("💡 Вопрос 6: Какие языки программирования тебе интересны?", reply_markup=keyboard_q6)


@router.message(CareerTest.question_6)
async def answer_q6(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q6=message.text)
    await state.set_state(CareerTest.question_7)
    await message.answer("💡 Вопрос 7: Сколько времени ты готов тратить на обучение в день?", reply_markup=keyboard_q7)


@router.message(CareerTest.question_7)
async def answer_q7(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q7=message.text)
    await state.set_state(CareerTest.question_8)
    await message.answer("💡 Вопрос 8: Есть ли у тебя опыт в IT?", reply_markup=keyboard_q8)


@router.message(CareerTest.question_8)
async def answer_q8(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q8=message.text)
    await state.set_state(CareerTest.question_9)
    await message.answer("💡 Вопрос 9: Какой у тебя уровень английского?", reply_markup=keyboard_q9)


@router.message(CareerTest.question_9)
async def answer_q9(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q9=message.text)
    await state.set_state(CareerTest.question_10)
    await message.answer("💡 Вопрос 10: Где бы ты хотел работать?", reply_markup=keyboard_q10)


@router.message(CareerTest.question_10)
async def answer_q10(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q10=message.text)
    await state.set_state(CareerTest.question_11)
    await message.answer("💡 Вопрос 11: С какими задачами тебе бы хотелось сталкиваться?", reply_markup=keyboard_q11)


@router.message(CareerTest.question_11)
async def answer_q11(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q11=message.text)
    await state.set_state(CareerTest.question_12)
    await message.answer("💡 Вопрос 12: Какой стиль работы тебе ближе?", reply_markup=keyboard_q12)


@router.message(CareerTest.question_12)
async def answer_q12(message: types.Message, state: FSMContext):
    if message.text == "🔄 Начать заново": await start_test(message, state); return
    await state.update_data(q12=message.text)
    user_data = await state.get_data()

    specialty, description = "Не определено", "Попробуй пройти тест ещё раз!"

    if user_data["q4"] == "Программирование":
        if user_data["q6"] == "JavaScript" and user_data["q5"] == "React, Vue.js":
            if user_data["q8"] in ["Нет, я новичок", "Базовые знания (курсы)"] and user_data["q3"] == "Удалённая работа":
                specialty = "Frontend-разработчик (Junior)"
                description = "Создаёшь интерфейсы сайтов, идеально для удалённой работы."
            elif user_data["q8"] in ["Есть опыт программирования", "Работал в IT"] and user_data["q2"] in ["26–35", "36+"]:
                specialty = "Frontend-разработчик (Middle)"
                description = "Разрабатываешь сложные веб-приложения с React или Vue.js."
        elif user_data["q6"] == "Python" and user_data["q5"] == "Python, Django":
            if user_data["q8"] == "Нет, я новичок" and user_data["q2"] == "18–25":
                specialty = "Python-разработчик (Junior)"
                description = "Молодой специалист, пишешь скрипты и учишься веб-разработке."
            elif user_data["q8"] == "Есть опыт программирования" and user_data["q3"] == "Высокие зарплаты":
                specialty = "Backend-разработчик (Middle)"
                description = "Создаёшь серверные приложения с высокой оплатой."
    elif user_data["q4"] == "Аналитика данных" and user_data["q11"] == "Анализ данных":
        if user_data["q6"] == "Python" and user_data["q7"] in ["3–5 часов", "Больше 5 часов"] and user_data["q2"] == "До 18":
            specialty = "Аналитик данных (Junior)"
            description = "Начинаешь карьеру в аналитике, работая с данными."
        elif user_data["q8"] == "Работал в IT" and user_data["q3"] == "Перспективы роста":
            specialty = "Data Scientist (Middle)"
            description = "Строишь модели ML с большими перспективами."
    elif user_data["q4"] == "Кибербезопасность" and user_data["q11"] == "Обеспечение безопасности":
        if user_data["q8"] == "Нет, я новичок" and user_data["q3"] == "Интерес к технологиям":
            specialty = "Специалист по кибербезопасности (Junior)"
            description = "Исследуешь технологии защиты данных."
        elif user_data["q8"] == "Есть опыт программирования" and user_data["q9"] != "Не знаю английский":
            specialty = "Специалист по кибербезопасности (Middle)"
            description = "Работаешь с сетями и сложными угрозами."
    elif user_data["q4"] == "Разработка интерфейсов (UI)" and user_data["q11"] == "Разработка UI":
        if user_data["q2"] in ["До 18", "18–25"] and user_data["q3"] == "Удалённая работа":
            specialty = "UX/UI-дизайнер (Junior)"
            description = "Создаёшь интерфейсы, работай удалённо!"
    elif user_data["q4"] == "Администрирование и DevOps" and user_data["q5"] == "Docker, Kubernetes":
        if user_data["q8"] in ["Нет, я новичок", "Базовые знания (курсы)"] and user_data["q7"] == "1–3 часа":
            specialty = "DevOps Engineer (Junior)"
            description = "Автоматизируешь процессы с Docker и Kubernetes."
        elif user_data["q8"] == "Работал в IT" and user_data["q3"] == "Перспективы роста":
            specialty = "DevOps Engineer (Middle)"
            description = "Управляешь инфраструктурой с большими перспективами."
    elif user_data["q4"] == "Мобильная разработка" and user_data["q5"] == "Flutter, Swift":
        if user_data["q6"] == "Java" and user_data["q8"] == "Нет, я новичок":
            specialty = "Mobile Developer (Junior)"
            description = "Создаёшь приложения для Android на Java."
        elif user_data["q8"] == "Есть опыт программирования" and user_data["q3"] == "Интерес к технологиям":
            specialty = "Mobile Developer (Middle)"
            description = "Разрабатываешь приложения на Flutter или Swift."

    resource = await get_course_resource(specialty)

    db.save_user(message.from_user.id, user_data["q1"], user_data, specialty)

    likes, dislikes = db.get_stats()

    feedback_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👍 Понравилось", callback_data="feedback_like")],
        [InlineKeyboardButton(text="👎 Не понравилось", callback_data="feedback_dislike")]
    ])

    await message.answer(
        f"📊 **Результаты теста, {user_data['q1']}!**\n\n"
        f"1. Возраст: {user_data['q2']}\n2. Мотивация: {user_data['q3']}\n3. Сфера: {user_data['q4']}\n"
        f"4. Технологии: {user_data['q5']}\n5. Языки: {user_data['q6']}\n6. Время на обучение: {user_data['q7']}\n"
        f"7. Опыт: {user_data['q8']}\n8. Английский: {user_data['q9']}\n9. Где работать: {user_data['q10']}\n"
        f"10. Задачи: {user_data['q11']}\n11. Стиль работы: {user_data['q12']}\n\n"
        f"🎯 **Рекомендуемая специальность:** {specialty}\n"
        f"ℹ️ {description}\n"
        f"🔗 Курс: {resource}\n\n"
        f"📈 Статистика: 👍: {likes} | 👎: {dislikes}\n\n"
        f"Оцени результат:",
        reply_markup=feedback_keyboard
    )
    await state.clear()


@router.callback_query(lambda c: c.data in ["feedback_like", "feedback_dislike"])
async def process_feedback(callback: types.CallbackQuery):
    feedback = 1 if callback.data == "feedback_like" else -1
    db.update_feedback(callback.from_user.id, feedback)
    likes, dislikes = db.get_stats()
    await callback.answer(
        "Спасибо за 👍! Рад, что тебе понравился тест!" if feedback == 1 else "Жаль, что 👎. Попробуй пройти тест ещё раз!",
        show_alert=True
    )
    await callback.message.edit_text(
        f"{callback.message.text.split('📈')[0]}"
        f"📈 Статистика: 👍: {likes} | 👎: {dislikes}",
        reply_markup=None
    )


@router.message(Command("my_results"))
async def show_results(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user:
        name, answers_json, specialty = user
        answers = json.loads(answers_json)
        await message.answer(
            f"📊 **Твои результаты, {name}!**\n\n"
            f"1. Возраст: {answers['q2']}\n2. Мотивация: {answers['q3']}\n3. Сфера: {answers['q4']}\n"
            f"4. Технологии: {answers['q5']}\n5. Языки: {answers['q6']}\n6. Время: {answers['q7']}\n"
            f"7. Опыт: {answers['q8']}\n8. Английский: {answers['q9']}\n9. Где работать: {answers['q10']}\n"
            f"10. Задачи: {answers['q11']}\n11. Стиль: {answers['q12']}\n\n"
            f"🎯 **Специальность:** {specialty}"
        )
    else:
        await message.answer("Ты ещё не проходил тест! Начни с /test")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())