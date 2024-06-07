import telebot

TOKEN = '' 

bot = telebot.TeleBot(TOKEN)

roles = {'admin': 0, 'moderator': 1, 'user': 2}

chat_id = None
current_user = None

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Привет! Я - бот-блокировщик рекламы.')

@bot.message_handler(commands=['assign_role'])
def assign_role(message):
    current_user = message.from_user
    role_name = message.text.split()[1]
    if role_name in roles.keys():
        role_id = roles[role_name]
        for member in message.chat.get_members():
            if member.id == current_user.id:
                member.role = role_id
        bot.send_message(message.chat.id, f'Роль назначена пользователю {current_user.first_name}: {role_name}')
    else:
        bot.send_message(message.chat.id, 'Неверное название роли')

@bot.message_handler(content_types=['text'])
def text_handler_url(message):
    if "https://" and not("https://www.youtube.com/") and not("https://store.steampowered.com/") and not("https://store.epicgames.com/")in message.text:
        bot.reply_to(message, "Ссылки в этом чате запрещены")
        bot.delete_message(message.chat.id, message.message_id)
bot.infinity_polling()

@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    bot.send_message(chat_id, f'Новый пользователь присоединился: {message.new_chat_member.mention()}')

@bot.message_handler(content_types=['left_chat_member'])
def left_member(message):
    bot.send_message(chat_id, f'Пользователь {message.left_chat_member.mention()} покинул чат')

bot.infinity_polling()