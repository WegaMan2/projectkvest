import telebot
import json
from game import Game
API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Загрузка данных из JSON-файла
with open('locations.json', 'r', encoding='utf-8') as f:
    locations = json.load(f)

# Загрузка данных пользователей из user.json
try:
    with open('user.json', 'r', encoding='utf-8') as f:
        user_data = json.load(f)
except FileNotFoundError:
    user_data = {}

# Функция для получения данных пользователя
def get_user_data(chat_id):
    if str(chat_id) not in user_data:
        user_data[str(chat_id)] = {'current_location': 'start'}
        save_user_data()
    return user_data[str(chat_id)]

# Функция для сохранения данных пользователя
def save_user_data():
    with open('user.json', 'w') as f:
        json.dump(user_data, f, indent=4)

# Функция для обновления текущей локации пользователя
def update_current_location(chat_id, new_location):
    user = get_user_data(chat_id)
    user['current_location'] = new_location
    save_user_data()

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    start_button = telebot.types.KeyboardButton('Начать игру')
    markup.add(start_button)
    bot.send_message(message.chat.id, "Добро пожаловать в игру! Начнем игру?", reply_markup=markup)
    bot.send_message(message.chat.id, 'Предыстория:'
                                      '\nВы - отважный искатель приключений, отправившийся на поиски древнего артефакта,'
                                       'способного спасти ваш родной город от неминуемого разрушения.'
                                      '\nВаше путешествие начинается в маленькой деревне,'
                                      'откуда вам предстоит исследовать различные локации,'
                                      'встретить опасности и принять решения, влияющие на развитие сюжета.')

# Обработка сообщений с текстом
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    game = Game(chat_id)

    if message.text.lower() == '/command1':
        game.reset_game()
        send_location(chat_id, locations['start'])
    elif message.text.lower() == 'начать игру':
        game.start_game()
        send_location(chat_id, locations['start'])
    else:
        response = game.handle_action(message.text)
        if response:
            bot.send_message(chat_id, response)
            current_location = game.current_location
            send_location(chat_id, locations[current_location])

# Функция отправки локации
def send_location(chat_id, location):
    # Отправка описания локации
    bot.send_photo(chat_id, location['illustration'])
    bot.send_message(chat_id, location['description'])
    # Отправка кнопок действий
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for action in location['actions']:
        markup.add(telebot.types.KeyboardButton(action))
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

# Запуск бота
bot.polling()