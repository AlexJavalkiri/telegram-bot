# Импортируем нужные модули
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters
import random, os
import re

# Читаем токен из переменной окружения (настраивается в Render)
TOKEN = os.getenv("TOKEN")  # Пример: читает токен, например, "1234567890:NEW_TOKEN_HERE" из Render

# Слова, на которые бот реагирует
TRIGGER_WORDS = [
    "привет", "да", "бля", "хуй", "похуй",
    "первый", "циркулярная", "хахаха", "хпхпхп",
    "матроскин", "туплю", "приказ", "командир", "постираться",
    "хуйня", "похуй", "каракоба", "ваня", "игла2", "старшина", "Дембель",
    "виноват", "баня", "власов сказал", "бпла"
]

# Специфические ответы на слова
SPECIFIC_RESPONSES = {
    "да": "Пизда",
    "первый": "Пидорас",
    "привет": "Здарова, заебал! ~(˘▾˘~)",
    "циркулярная": "О, пиздец ヽ(∀° )人( °∀)ノ",
    "хахаха": "Не смешно (╯°□°)╯",
    "хпхпхп": "Дохуя смешно тебе (o_O)?",
    "матроскин": "Ты тоже такой медленный)?",
    "туплю": "Ты чё ебало в блиндаже топил, когда мозги всем раздавали?",
    "приказ": "Приказ на бумаге",
    "командир": "Слюнявого не называй, толчок наш больше командир чем он)",
    "постираться": "Ага, размечтался, в вонючем ходи",
    "хуйня": "Хуйня в строевой или, за белой дверью в роте, а это не хуйня",
    "похуй": "3 дня до дома будет, будет похуй, а сейчас ебошка",
    "каракоба": "Долина в Крыму в окрестностях Севастополя, вливается в Инкерманскую с востока у пос. Сахарная головка. Пространственно сопряжена с одноименной 280 м горой",
    "ваня": "Его пердеж настолько громкий, что ИГЛА-2 путает его с детонацией ᕦ(ò_óˇ)ᕤ",
    "игла2": "Медведь и стая пидорасов",
    "старшина": "Начало мне уже не нравится!",
    "морсков": "После многих и многих научных исследований,учеными было решено, что это самый медленный человек не то что в России, даже не в мире, в целом, нет существ более медленных чем он",
    "дембель": "Не существует его",
    "виноват": "Виноват военкомат, что призвал тебя",
    "баня": "Не называй горячий душ баней, это же просто горячая вода",
    "власов сказал": "Ебать, боец , ты чё приказы из жопы выдумал?",
    "бпла": "Беспилотный летательный аппарат, если что!)"
}

# Команда /start
async def start(update, context):
    await update.message.reply_text(
        f"Привет! Добавь меня в группу, будет весело! и упомяни @{context.bot.username}"
    )

# Команда /who (Кто сегодня пиздализ?)
async def who(update, context):
    if update.message.chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Эта команда работает только в группах!")
        return

    # Проверяем, была ли команда уже вызвана в этой группе
    if context.chat_data.get("pizdaliz_called"):
        await update.message.reply_text("я же блять сказал, кто сегодня пиздализ :)")
        return

    try:
        # Получаем список участников группы
        members = await context.bot.get_chat_members(update.effective_chat.id)
        # Фильтруем только пользователей (не ботов)
        users = [member.user for member in members if not member.user.is_bot]
        
        if len(users) < 2:
            await update.message.reply_text("В группе слишком мало людей, чтобы выбрать пиздализов!")
            return

        # Выбираем двух случайных участников
        pizdalizs = random.sample(users, 2)
        pizdaliz1 = pizdalizs[0]
        pizdaliz2 = pizdalizs[1]

        # Формируем ссылки на пользователей
        pizdaliz1_link = f"@{pizdaliz1.username}" if pizdaliz1.username else pizdaliz1.first_name
        pizdaliz2_link = f"@{pizdaliz2.username}" if pizdaliz2.username else pizdaliz2.first_name

        # Отправляем ответ
        await update.message.reply_text(
            f"Сегодня пиздализы: {pizdaliz1_link} и {pizdaliz2_link}!"
        )

        # Помечаем, что команда была вызвана
        context.chat_data["pizdaliz_called"] = True

    except Exception as e:
        await update.message.reply_text(f"Ошибка, блять: {str(e)}")

# Реакция на триггерные слова в группах (без ROASTS!)
async def handle_triggers(update, context):
    try:
        if update.message.chat.type in ["group", "supergroup"]:
            text = update.message.text.lower()
            # Проверяем, есть ли триггерное слово (точное совпадение)
            for word in TRIGGER_WORDS:
                if re.search(r'\b' + re.escape(word) + r'\b', text):
                    response = SPECIFIC_RESPONSES.get(word)
                    if response:  # Отвечаем только если есть специфический ответ
                        await update.message.reply_text(response)
                    return
    except Exception as e:
        print(f"Error in handle_triggers: {str(e)}")  # Лог для отладки

# Приветствие новичков и реакция на выход из группы (исправлено для v21)
async def handle_chat_member(update, context):
    try:
        # В v21+ используем update.chat_member (ChatMemberUpdated)
        chat_member_update = update.chat_member
        old_status = chat_member_update.old_chat_member.status if chat_member_update.old_chat_member else None
        new_status = chat_member_update.new_chat_member.status
        user = chat_member_update.from_user  # Пользователь, чей статус изменился
        first_name = user.first_name if user else "Неизвестный"

        # Вход в группу (стал member/admin/creator)
        if new_status in ["member", "administrator", "creator"] and old_status != new_status:
            await update.effective_chat.send_message(
                f"Добро пожаловать, пидор, в наш гей-клуб, {first_name}!"
            )
        # Выход из группы (стал left/kicked)
        elif new_status in ["left", "kicked"] and old_status not in ["left", "kicked"]:
            await update.effective_chat.send_message(
                f"Пошёл нахуй, ебанный натурал, {first_name}!"
            )
    except Exception as e:
        print(f"Error in handle_chat_member: {str(e)}")  # Лог для отладки

# Запуск бота (polling для тестов)
def main():
    if not TOKEN:
        print("Ошибка: TOKEN не задан в environment variables!")
        return

    # Создаём бота с токеном
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем handlers
    app.add_handler(CommandHandler("start", start))  # Для /start
    app.add_handler(CommandHandler("who", who))  # Для /who
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_triggers))  # Для триггерных слов
    app.add_handler(ChatMemberHandler(handle_chat_member, ChatMemberHandler.CHAT_MEMBER))  # Для новичков и ухода (v21+)
    
    # Запускаем бота (polling)
    print("Бот запущен в режиме polling...")
    app.run_polling(drop_pending_updates=True)

# Старт программы
if __name__ == "__main__":
    main()
