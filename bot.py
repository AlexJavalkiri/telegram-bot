from telegram.ext import Updater, CommandHandler, MessageHandler, ChatMemberHandler, filters
import random, os

TOKEN = os.getenv("8445348429:AAFRx8nu-1JEM_SA3IKF32C3_e6QeaGKJ2Y")
ROASTS = ["Пиздец, ты чё, из морга сбежал?", "Блять, это как так жить умудрился?", "Сукин сын, твой текст мёртв, как мой кот!", "Нахуй, иди в гробике полежи!", "Ёпт, что за хуйня вместо мозгов?", "Ебать, ты в ударе, как катафалк!", "Хуйня полная, будто некролог писал!", "Похер, но это пиздец!", "Чё за хуйня, ты зомби?", "Бляха, это твой максимум или дохлый?", "Заебись, но в гробу лучше выглядишь!", "Похуй, твой текст — пиздец!", "Ебать, это что за хуй?", "Пиздец, ты как могильный камень!", "Хуёво дело, с кладбища пишешь?", "Блять, это призрак написал?", "Нахер, твой текст — как венок!", "Ёб твою мать, ты живой?", "Похуй, это хуйня уровня крематория!", "Заебал, пиши нормально или в ящик!", "Хуйло, твой текст — могила без креста!", "Ебать, ты из ада?"]
TRIGGER_WORDS = ["привет", "как дела", "бот", "бери", "давай", "похер", "норм", "го", "здаров", "пох", "похуй", "чё", "ну", "хуй", "заебись", "пиздец", "ебать", "хуета", "бля", "нах", "похерю", "ебаный", "хуйло", "похрен", "ёба"]

async def start(update, context):
    await update.message.reply_text(f"Бот с матом! Пиши слова ({', '.join(TRIGGER_WORDS)}) или упомяни @{context.bot.username}")

async def roast(update, context):
    if update.message.chat.type in ["group", "supergroup"] and (any(word in update.message.text.lower() for word in TRIGGER_WORDS) or f"@{context.bot.username}".lower() in update.message.text.lower()):
        await update.message.reply_text(random.choice(ROASTS))

async def welcome(update, context):
    for member in update.chat_member.new_chat_members:
        await update.message.reply_text(f"Добро пожаловать, {member.first_name}! Похер, с кладбища сбежал?")

def main():
    app = application().token("8445348429:AAFRx8nu-1JEM_SA3IKF32C3_e6QeaGKJ2Y").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roast))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.run_polling()

if __name__ == "__main__":
    main()
