import sqlite3
import telebot
import config
from telebot import types
from random import randint
import datetime

bot = telebot.TeleBot(config.TOKEN)

def select_job(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton("π° Balance")
    item2 = types.KeyboardButton("π’ Work")
    item3 = types.KeyboardButton("πΌ Get a new job")

    markup1.add(item1, item2, item3)

    user_login = message.from_user.username.lower()
    job = message.text

    sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
    balance = sql.fetchall()[0][0]

    sql.execute(f"SELECT job FROM users WHERE login = '{user_login}'")
    current_job = sql.fetchall()[0][0]

    if job == 'πͺ Exit':
        bot.send_message(message.chat.id, "I will wait for you more", reply_markup=markup1)

    elif job == 'π£ Waiter' and balance >= 100 and current_job != 'π£ Waiter':
        new_balance = balance - 100

        sql.execute(f"""UPDATE users SET job = (?) WHERE login = (?)""", (job, user_login))
        db.commit()

        sql.execute(f"""UPDATE users SET cash = (?) WHERE login = (?)""", (new_balance, user_login))
        db.commit()

        bot.send_message(message.chat.id, "Now you Waiterπ£".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    elif job == 'π£ Waiter' and current_job == 'π£ Waiter':
        bot.send_message(message.chat.id, "You are already Waiterπ£".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)
    elif job == 'π£ Waiter' and balance < 100:
        bot.send_message(message.chat.id, "You don't have enough money".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    if job == 'π Manager' and balance >= 200 and current_job != 'π Manager':
        new_balance = balance - 200

        sql.execute(f"""UPDATE users SET job = (?) WHERE login = (?)""", (job, user_login))
        db.commit()

        sql.execute(f"""UPDATE users SET cash = (?) WHERE login = (?)""", (new_balance, user_login))
        db.commit()

        bot.send_message(message.chat.id, "Now you Managerπ".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    elif job == 'π Manager' and current_job == 'π Manager':
        bot.send_message(message.chat.id, "You are already π Manager".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    elif job == 'π Manager' and balance < 200:
        bot.send_message(message.chat.id, "You don't have enough money".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    if job == 'π» Programmer' and balance >= 400 and current_job != 'π» Programmer':
        new_balance = balance - 400

        sql.execute(f"""UPDATE users SET job = (?) WHERE login = (?)""", (job, user_login))
        db.commit()

        sql.execute(f"""UPDATE users SET cash = (?) WHERE login = (?)""", (new_balance, user_login))
        db.commit()

        bot.send_message(message.chat.id, "Now you π» Programmer".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    elif job == 'π» Programmer' and current_job == 'π» Programmer':
        bot.send_message(message.chat.id, "You are already π» Programmer".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    elif job == 'π» Programmer' and balance < 400:
        bot.send_message(message.chat.id, "You don't have enough money".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)


@bot.message_handler(commands=['start'])
def start(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton("π° Balance")
    item2 = types.KeyboardButton("π’ Work")
    item3 = types.KeyboardButton("πΌ Get a new job")
    item4 = types.KeyboardButton("π Top players")

    markup1.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, "Welcome, {0.first_name}!\n"
                                      "I - <b> {1.first_name} </b>\n"
                                      "With me you can play in financial game".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)

    user_login = message.from_user.username.lower()
    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (user_login, 0, 0, 'π§Ή Cleaner'))
        db.commit()

@bot.message_handler(content_types=['text'])
def commands(message):
    if message.chat.type == 'private':
        if message.text == 'π° Balance':
            user_login = message.from_user.username.lower()

            sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
            balance = sql.fetchall()[0][0]

            bot.send_message(message.chat.id, f'Your balance: {balance} π΅')

        elif message.text == 'π’ Work':
            user_login = message.from_user.username.lower()

            now_time = datetime.datetime.now()
            now_time = now_time.hour * 60 + now_time.minute

            sql.execute(f"SELECT timer FROM users WHERE login = '{user_login}'")
            last_time = sql.fetchall()[0][0]

            if now_time-last_time >= 60 or last_time-now_time >= 60:
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchall()[0][0]

                sql.execute(f"SELECT job FROM users WHERE login  = '{user_login}'")
                job = sql.fetchall()[0][0]

                if job == 'π§Ή Cleaner':
                    earning = randint(2, 10)
                elif job == 'π£ Waiter':
                    earning = randint(10, 20)
                elif job == 'π Manager':
                    earning = randint(30, 40)
                elif job == 'π» Programmer':
                    earning = randint(50, 70)

                new_balance = balance + earning
                sql.execute(f"""UPDATE users SET cash = (?) WHERE login = (?)""", (new_balance, user_login))
                db.commit()

                bot.send_message(message.chat.id, f'Your balance: {new_balance} π΅\n'
                                                  f'Your balance before work: {balance} π΅')

                sql.execute(f"""UPDATE users SET timer = (?) WHERE login = (?)""", (now_time, user_login))
                db.commit()
            else:
                bot.send_message(message.chat.id, 'You cant start working yet \n'
                                                  f'Theres more left {last_time+60-now_time} minutes')

        elif message.text == 'πΌ Get a new job':
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton("π£ Waiter")
            item2 = types.KeyboardButton("π Manager")
            item3 = types.KeyboardButton("π» Programmer")
            item4 = types.KeyboardButton("πͺ Exit")

            markup2.add(item1, item2, item3, item4)

            user_login = message.from_user.username.lower()

            sql.execute(f"SELECT job FROM users WHERE login = '{user_login}'")
            current_job = sql.fetchall()[0][0]

            bot.send_message(message.chat.id, f'At the moment your job is a {current_job}\n'
                                              f'You can become:\n'
                                              '\n'
                                              'π£ Waiter\n'
                                              'Earning: 10-20 π΅\n'
                                              'Cost to get a job: 100 π΅\n'
                                              '\n'
                                              'π Manager\n'
                                              'Earning: 30-40 π΅\n'
                                              'Cost to get a job: 200 π΅\n'
                                              '\n'
                                              'π» Programmer\n'
                                              'Earning: 50-70 π΅\n'
                                              'Cost to get a job: 400 π΅\n'
                                              '\n'
                                              'Choose who you want to be:'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup2)
            bot.register_next_step_handler(message, select_job)

        elif message.text == 'π Top players':

            string = 'π Top 5 players: \n'
            sql.execute("SELECT * FROM users ORDER BY cash DESC LIMIT 5")
            info = sql.fetchall()
            for value in info:
                string = string + f'{value[0]}      {value[1]}' + 'π΅\n'
            bot.send_message(message.chat.id, string.format(message.from_user, bot.get_me()))


if __name__ == '__main__':
    db = sqlite3.connect('server.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT,
        cash BIGINT,
        timer INT,
        job TEXT
    ) """)
    db.commit()

bot.polling(none_stop=True)
