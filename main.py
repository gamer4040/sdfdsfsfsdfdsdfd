import telebot 
import logging
from config import token

from logic import Pokemon, Wizard, Fighter

telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    user_key = message.from_user.id  # username может быть None; id всегда есть
    if user_key not in Pokemon.pokemons.keys():
        pokemon = Pokemon(user_key)
        bot.send_message(message.chat.id, pokemon.info())
        try:
            bot.send_photo(message.chat.id, pokemon.show_img())
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось отправить картинку, попробуй ещё раз позже.")
            telebot.logger.exception(e)
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Отправь /go, чтобы получить покемона ✨\nИли выбери тип:\n/wizard - волшебник\n/fighter - боец\n/battle - сразиться с врагом")

@bot.message_handler(commands=['wizard'])
def create_wizard(message):
    user_key = message.from_user.id
    if user_key not in Pokemon.pokemons.keys():
        pokemon = Wizard(user_key)
        bot.send_message(message.chat.id, pokemon.info() + "\nТип: Волшебник")
        try:
            bot.send_photo(message.chat.id, pokemon.show_img())
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось отправить картинку, попробуй ещё раз позже.")
            telebot.logger.exception(e)
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['fighter'])
def create_fighter(message):
    user_key = message.from_user.id
    if user_key not in Pokemon.pokemons.keys():
        pokemon = Fighter(user_key)
        bot.send_message(message.chat.id, pokemon.info() + "\nТип: Боец")
        try:
            bot.send_photo(message.chat.id, pokemon.show_img())
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось отправить картинку, попробуй ещё раз позже.")
            telebot.logger.exception(e)
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['battle'])
def battle(message):
    user_key = message.from_user.id
    if user_key in Pokemon.pokemons.keys():
        player_pokemon = Pokemon.pokemons[user_key]
        enemy_pokemon = Pokemon.create_enemy()
        
        # Определяем тип врага для отображения
        enemy_type = "Обычный покемон"
        if isinstance(enemy_pokemon, Wizard):
            enemy_type = "Волшебник"
        elif isinstance(enemy_pokemon, Fighter):
            enemy_type = "Боец"
        
        battle_info = f"⚔️ БИТВА НАЧАЛАСЬ! ⚔️\n\n"
        battle_info += f"Твой покемон:\n{player_pokemon.info()}\n\n"
        battle_info += f"Враг ({enemy_type}):\nИмя: {enemy_pokemon.name}\nЗдоровье: {enemy_pokemon.hp}\nСила: {enemy_pokemon.power}\n\n"
        
        # Проводим сражение
        result = player_pokemon.attack(enemy_pokemon)
        battle_info += f"Результат боя твоего и вражеского покемона:\n{result}\n\n"
        
        # Показываем финальное состояние
        battle_info += f"Твой покемон: HP={player_pokemon.hp}\n"
        battle_info += f"Враг: HP={enemy_pokemon.hp}"
        
        bot.send_message(message.chat.id, battle_info)
        
        # Отправляем картинку врага
        try:
            bot.send_photo(message.chat.id, enemy_pokemon.show_img())
        except Exception as e:
            telebot.logger.exception(e)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go, /wizard или /fighter")

# Фолбэк обработчик: подтверждаем, что бот получает сообщения
@bot.message_handler(func=lambda m: True)
def ping(message):
    bot.reply_to(message, "Я здесь! Напиши /go")

# На всякий случай отключаем/удаляем вебхук, чтобы polling получал апдейты
try:
    bot.delete_webhook(drop_pending_updates=True)
except Exception:
    try:
        bot.remove_webhook()
    except Exception:
        pass

bot.infinity_polling(skip_pending=True)

