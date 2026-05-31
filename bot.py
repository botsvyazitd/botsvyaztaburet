import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ── НАСТРОЙКИ ──────────────────────────────────────
TOKEN = "8999909620:AAG6VJDEnTfzBcNo_zx6P4ND7MAIDNFJMDc"   # токен от BotFather
MY_ID = 5740984955   # твой Telegram ID — узнай у @userinfobot
# ───────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)

# Словарь: chat_id пользователя → его имя
users = {}

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪐 Привет! Это бот taburet725.\n\nНапиши своё сообщение — я передам его."
    )

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    text = update.message.text

    # Если пишет сам владелец — это ответ пользователю
    if user.id == MY_ID:
        # Формат ответа: reply на пересланное сообщение
        if update.message.reply_to_message:
            # Достаём chat_id из текста пересланного сообщения
            fwd_text = update.message.reply_to_message.text or ""
            for uid, name in users.items():
                if name in fwd_text:
                    await ctx.bot.send_message(chat_id=uid, text=f"💬 {text}")
                    await update.message.reply_text("✅ Отправлено")
                    return
        await update.message.reply_text("⚠️ Сделай reply на сообщение пользователя чтобы ответить")
        return

    # Обычный пользователь — пересылаем тебе
    name = f"@{user.username}" if user.username else user.first_name
    users[chat_id] = name

    await ctx.bot.send_message(
        chat_id=MY_ID,
        text=(
            f"📩 Новое сообщение\n"
            f"От: {name} (id: {chat_id})\n"
            f"{'─'*25}\n"
            f"{text}\n"
            f"{'─'*25}\n"
            f"↩️ Сделай reply на это сообщение чтобы ответить"
        )
    )
    await update.message.reply_text("✅ Сообщение отправлено! Ожидай ответа.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен ✅")
app.run_polling()
