import telebot
import configure
import sqlite3
from telebot import types
import time
from xlsxwriter.workbook import Workbook

client = telebot.TeleBot(configure.config['token'])
db = sqlite3.connect('baza.db', check_same_thread=False)
sql = db.cursor()
markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """

# database

sql.execute(
    """CREATE TABLE IF NOT EXISTS users (id BIGINT, nick TEXT, access INT)""")
sql.execute(
    """CREATE TABLE IF NOT EXISTS tasks (id BIGINT, nick TEXT, number INT, time TEXT, message TEXT)""")
db.commit()

# Первый запуск и авторизация или Проверка доступов и вывод меню


@client.message_handler(commands=['start'])
def start(message):
    try:
        getname = message.from_user.first_name
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT id FROM users WHERE id = {uid}")
        if sql.fetchone() is None:
            sql.execute(
                f"INSERT INTO users VALUES ({uid}, '{getname}', 0)")
            msg = client.send_message(cid, f"Добро пожаловать, {getname}!\n"
                                      "Я бот Информационно-технической службы\n"
                                      "Моя цель помочь в решении Вашей проблемы")
            db.commit()
            sql.execute(f"SELECT * FROM users WHERE id = {uid}")
            getaccess = sql.fetchone()[2]
            if getaccess == 0:
                client.send_message(cid, "Добро пожаловать Пользователь")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать работу")
                markup.add(btn1)
                client.send_message(message.from_user.id,
                                    "Чтобы продолжить нажмите: Начать работу", reply_markup=markup)
            elif getaccess == 777:
                client.send_message(cid, "Добро пожаловать Администратор")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать работу Администратора")
                markup.add(btn1)
                client.send_message(message.from_user.id,
                                    "Чтобы продолжить нажмите: Начать работу", reply_markup=markup)
            elif getaccess == 1:
                client.send_message(cid, "Добро пожаловать Инженер")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать работу Инженера")
                markup.add(btn1)
                client.send_message(message.from_user.id,
                                    "Чтобы продолжить нажмите: Начать работу", reply_markup=markup)
        else:
            msg = client.send_message(cid, f"Добро пожаловать, {getname}!\n"
                                      "Я бот Информационно-технической службы\n"
                                      "Моя цель помочь в решении Вашей проблемы")
            sql.execute(f"SELECT * FROM users WHERE id = {uid}")
            getaccess = sql.fetchone()[2]
            if getaccess == 0:
                client.send_message(cid, "Добро пожаловать Пользователь")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать работу")
                markup.add(btn1)
                client.send_message(message.from_user.id,
                                    "Чтобы продолжить нажмите: Начать работу", reply_markup=markup)
            elif getaccess == 777:
                client.send_message(cid, "Добро пожаловать Администратор")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать работу Администратора")
                markup.add(btn1)
                client.send_message(message.from_user.id,
                                    "Чтобы продолжить нажмите: Начать работу", reply_markup=markup)
            elif getaccess == 1:
                client.send_message(cid, "Добро пожаловать Инженер")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать работу Инженера")
                markup.add(btn1)
                client.send_message(message.from_user.id,
                                    "Чтобы продолжить нажмите: Начать работу", reply_markup=markup)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команд')


# Список всех пользователей в БД
@client.message_handler(commands=['users'])
def allusers(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 777
        if getaccess < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            text = '*🗃 | Список всех пользователей:*\n\n'
            idusernumber = 0
            for info in sql.execute(f"SELECT * FROM users"):
                if info[2] == 0:
                    accessname = 'Пользователь'
                elif info[2] == 777:
                    accessname = 'Администратор'
                elif info[2] == 1:
                    accessname = 'Инженер'
                idusernumber += 1
                text += f"*{idusernumber}. {info[0]} ({info[1]})*\n* | Уровень доступа:* {accessname}\n*✉️ | Профиль:*" + \
                    f" [{info[1]}](tg://user?id="+str(info[0])+")\n\n"
            client.send_message(cid, f"{text}", parse_mode='Markdown')
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')


# Список Задач в БД
@client.message_handler(commands=['tasks'])
def alltasks(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 1
        if getaccess < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            text = '*🗃 | Список заявок в работе:*\n\n'
            idtasknumber = 0
            for info in sql.execute(f"SELECT * FROM tasks"):
                text += f"*Номер заявки {info[2]}*\n*Время отправки {info[3]}*\n*Текст заявки:*{info[4]}*\n*\n*✉️ | Отправитель Профиль:*" + \
                    f" [{info[1]}](tg://user?id="+str(info[0])+")\n\n"
            client.send_message(cid, f"{text}", parse_mode='Markdown')
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Заявка выполнена


@client.message_handler(commands=['taskcomplt'])
def taskcomplt(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 1
        if getaccess < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            msg = client.send_message(
                cid, f"*Введите номер выполненой заявки:*", parse_mode='Markdown')
            client.register_next_step_handler(msg, taskcomplt_next)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')


def taskcomplt_next(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global numbertask
            numbertask = int(message.text)
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                for infotask in sql.execute(f"SELECT * FROM tasks WHERE number = {numbertask}"):
                    rmk = types.InlineKeyboardMarkup()
                    item_yes = types.InlineKeyboardButton(
                        text='✅', callback_data='taskcompltyes')
                    item_no = types.InlineKeyboardButton(
                        text='❌', callback_data='taskcompltno')
                    rmk.add(item_yes, item_no)
                    msg = client.send_message(
                        cid, f"Данные о заявке:\n\nНомер заяки: {infotask[2]}\nID отправителя: {infotask[0]}\nИмя отправителя: {infotask[1]}\nВремя отправки: {infotask[3]}\nТекст заявки: {infotask[4]}\n\nВы выполнили заявку? Отменить действие будет НЕВОЗМОЖНО.", reply_markup=rmk)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')


@client.callback_query_handler(lambda call: call.data == 'taskcompltyes' or call.data == 'taskcompltno')
def taskcomplt_callback(call):
    try:
        if call.data == 'taskcompltyes':
            sql.execute(f"SELECT * FROM tasks")
            sql.execute(f"DELETE FROM tasks WHERE number = {numbertask}")
            client.delete_message(call.message.chat.id,
                                  call.message.message_id-0)
            client.send_message(call.message.chat.id, f"✅ | Заявка выполнена")
            db.commit()
        elif call.data == 'taskcompltno':
            client.delete_message(call.message.chat.id,
                                  call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(call.message.chat.id,
                            f'🚫 | Ошибка при выполнении команды')

# Экспорт заявок из БД в XML


@client.message_handler(commands=['exportexcel'])
def exportexcel(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 777
        if getaccess < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            workbook = Workbook('DataBase.xlsx')
            worksheet = workbook.add_worksheet()
            sql.execute("SELECT * FROM tasks")
            mysel = sql.execute("SELECT * FROM tasks")
            for i, row in enumerate(mysel):
                for j, value in enumerate(row):
                    worksheet.write(i, j, value)
            workbook.close()
            client.send_message(message.from_user.id,
                                'База данных выгружена')
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Получение информации о профиле пользователя по ID


@client.message_handler(commands=['getprofile', 'info'])
def getprofile(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 777
        if getaccess < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                msg = client.send_message(
                    cid, f'Введите ID пользователя:\n Пример: {info[0]}')
                client.register_next_step_handler(msg, getprofile_next)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Присвоение имён по ячейке access


def getprofile_next(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            getprofileid = message.text
            for info in sql.execute(f"SELECT * FROM users WHERE id = {getprofileid}"):
                if info[2] == 0:
                    accessname = 'Пользователь'
                elif info[2] == 777:
                    accessname = 'Администратор'
                elif info[2] == 1:
                    accessname = 'Инженер'
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Выбор кому выдать права


@client.message_handler(commands=['access', 'setaccess', 'dostup'])
def setaccess(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 777
        if getaccess < accessquery:
            client.send_message(cid, f"⚠️ | У вас нет доступа!")
        else:
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                msg = client.send_message(
                    cid, 'Введите ID пользователя:\n Пример: 7561592', parse_mode="Markdown")
                client.register_next_step_handler(msg, access_user_id_answer)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Выбор выдаваемых прав


def access_user_id_answer(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global usridaccess
            usridaccess = message.text
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton('Пользователь'), types.KeyboardButton(
                'Администратор'), types.KeyboardButton('Инженер'))
            msg = client.send_message(
                cid, 'Какой уровень доступа Вы хотите выдать?:', reply_markup=rmk, parse_mode="Markdown")
            client.register_next_step_handler(msg, access_user_access_answer)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Выбор выдаваемых прав


def access_user_access_answer(message):
    try:
        global accessgaved
        global accessgavedname
        cid = message.chat.id
        uid = message.from_user.id
        rmk = types.InlineKeyboardMarkup()
        access_yes = types.InlineKeyboardButton(
            text='✅', callback_data='setaccessyes')
        access_no = types.InlineKeyboardButton(
            text='❌', callback_data='setaccessno')
        rmk.add(access_yes, access_no)
        for info in sql.execute(f"SELECT * FROM users WHERE id = {usridaccess}"):
            if message.text == "Пользователь":
                accessgavedname = "Пользователь"
                accessgaved = 0
            elif message.text == "Администратор":
                accessgavedname = "Администратор"
                accessgaved = 777
            elif message.text == "Инженер":
                accessgavedname = "Инженер"
                accessgaved = 1

            client.send_message(
                cid, f'Данные для выдачи:\nID пользователя: {usridaccess} ({info[1]})\n Уровень доступа: {message.text}\n\n Верно?', reply_markup=rmk)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Обработка Подтверждения\отказа выдачи прав


@client.callback_query_handler(lambda call: call.data == 'setaccessyes' or call.data == 'setaccessno')
def access_user_gave_access(call):
    try:
        removekeyboard = types.ReplyKeyboardRemove()
        if call.data == 'setaccessyes':
            for info in sql.execute(f"SELECT * FROM users WHERE id = {usridaccess}"):
                sql.execute(
                    f"UPDATE users SET access = {accessgaved} WHERE id = {usridaccess}")
                db.commit()
                client.delete_message(
                    call.message.chat.id, call.message.message_id-0)
                client.send_message(
                    call.message.chat.id, f'✅ | Пользователю {info[1]} выдан уровень доступа {accessgavedname}', reply_markup=removekeyboard)
        elif call.data == 'setaccessno':
            for info in sql.execute(f"SELECT * FROM users WHERE id = {usridaccess}"):
                client.delete_message(
                    call.message.chat.id, call.message.message_id-0)
                client.send_message(
                    call.message.chat.id, f'🚫 | Вы отменили выдачу уровня доступа {accessgavedname} пользователю {info[1]}', reply_markup=removekeyboard)
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(f'🚫 | Ошибка при выполнении команды')

# Выдача прав Админа


@client.message_handler(commands=['getadminZN'])
def getadminclientchik(message):
    if message.from_user.id == 1: # Тут необходимо указать id 1го админа
        sql.execute(f"UPDATE users SET access = 777 WHERE id = 1") # Тут необходимо указать id 1го админа
        client.send_message(
            message.chat.id, f"✅ | Вы выдали права Администратора")
        db.commit()
    else:
        client.send_message(message.chat.id, f"⛔️ | Отказано в доступе!")

# Сообщить о проблеме в техподдержку


@client.message_handler(commands=['messageIT'])
def teh(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        msg = client.send_message(
            cid, f"*📨 | Введите текст который хотите отправить тех.поддержке*", parse_mode='Markdown')
        client.register_next_step_handler(msg, teh_next)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Подтверждение\отказ отправки сообщения


def teh_next(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global tehtextbyuser
            global tehnamebyuser
            global tehidbyuser
            tehidbyuser = int(message.from_user.id)
            tehnamebyuser = str(message.from_user.first_name)
            tehtextbyuser = str(message.text)
            rmk = types.InlineKeyboardMarkup()
            item_yes = types.InlineKeyboardButton(
                text='✉️', callback_data='tehsend')
            item_no = types.InlineKeyboardButton(
                text='❌', callback_data='tehno')
            rmk.add(item_yes, item_no)
            msg = client.send_message(
                cid, f"✉️ | Данные об отправке:\n\n Текст для отправки: {tehtextbyuser}\n\n Вы действительно хотите отправить это тех.поддержке?", parse_mode='Markdown', reply_markup=rmk)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Обработка Подтверждения\отказа отправки сообщения
# В случае подтверждения формирование сторки в БД


@client.callback_query_handler(func=lambda call: call.data == 'tehsend' or call.data == 'tehno')
def teh_callback(call):
    try:
        if call.data == 'tehsend':
            for info in sql.execute(f"SELECT * FROM users WHERE id = {call.from_user.id}"):
                client.delete_message(
                    call.message.chat.id, call.message.message_id-0)
                client.send_message(
                    call.message.chat.id, f"✉️ | Ваше сообщение отправлено тех.поддержке, ожидайте ответа.")
                named_tuple = time.localtime()  # получить struct_time
                time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
                sql.execute(f"SELECT * FROM tasks")
                number_task = sql.fetchone()[2]
                number_tasks = number_task
                sql.execute(
                    f"INSERT INTO tasks VALUES ({tehidbyuser}, '{tehnamebyuser}', {number_tasks}, '{time_string}', '{tehtextbyuser}')")
                db.commit()
                sql.execute(f"UPDATE tasks SET number = rowid ")
                db.commit()
                client.send_message(
                    1665883795, f"✉️ | Пользователь {tehnamebyuser} отправил сообщение в тех.поддержку\n\nID пользователя: {tehidbyuser}\nТекст: {tehtextbyuser}\n\nЧтобы ответить пользователю напишите /otvet")
        elif call.data == 'tehno':
            client.delete_message(call.message.chat.id,
                                  call.message.message_id-0)
            client.send_message(
                call.message.chat.id, f"🚫 | Вы отменили отправку сообщения тех.поддержке")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(f'🚫 | Ошибка при выполнении команды')

# Ответ пользователю


@client.message_handler(commands=['otvet'])
def sendmsgtouser(message):
    try:
        cid = message.chat.id
        msg = client.send_message(
            cid, f"👤 | Введите ID пользователя которому хотите отправить сообщение:")
        client.register_next_step_handler(msg, sendmsgtouser_next)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Набор сообщения пользователю


def sendmsgtouser_next(message):
    try:
        cid = message.chat.id

        if message.text == message.text:
            global getsendmsgtouserid
            getsendmsgtouserid = int(message.text)
            msg = client.send_message(
                cid, f"📨 | Введите текст который хотите отправить пользователю:")
            client.register_next_step_handler(msg, sendmsgtouser_next_text)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Подтверждение отправки сообщения пользователю


def sendmsgtouser_next_text(message):
    try:
        cid = message.chat.id

        if message.text == message.text:
            global getsendmsgtousertext
            getsendmsgtousertext = str(message.text)
            rmk = types.InlineKeyboardMarkup()
            item_yes = types.InlineKeyboardButton(
                text='✅', callback_data='sendmsgtouseryes')
            item_no = types.InlineKeyboardButton(
                text='❌', callback_data='sendmsgtouserno')
            rmk.add(item_yes, item_no)
            msg = client.send_message(
                cid, f"Данные об отправке сообщения:\n\nID пользователя: {getsendmsgtouserid}\n Текст для отправки: {getsendmsgtousertext}\n\n Отправить сообщение?", reply_markup=rmk)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Обработки отправки и отмены сообщения


@client.callback_query_handler(func=lambda call: call.data == 'sendmsgtouseryes' or call.data == 'sendmsgtouserno')
def sendmsgtouser_callback(call):
    try:
        if call.data == 'sendmsgtouseryes':
            client.delete_message(call.message.chat.id,
                                  call.message.message_id-0)
            client.send_message(call.message.chat.id,
                                f"✉️ | Сообщение отправлено!")
            client.send_message(
                getsendmsgtouserid, f"✉️ | Администратор прислал вам сообщение:\n\n{getsendmsgtousertext}")
        elif call.data == 'sendmsgtouserno':
            client.delete_message(call.message.chat.id,
                                  call.message.message_id-0)
            client.send_message(
                call.message.chat.id, f"🚫 | Вы отменили отправку сообщения пользователю")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(call.message.chat.id,
                            f'🚫 | Ошибка при выполнении команды')

# Получить ID пользователя по нику


@client.message_handler(commands=['getid'])
def getiduser(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
        accessquery = 777
        if getaccess < accessquery:
            client.send_message(cid, f"⚠️ | У вас нет доступа!")
        else:
            msg = client.send_message(cid, 'Введите никнейм пользователя:')
            client.register_next_step_handler(msg, next_getiduser_name)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')


def next_getiduser_name(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            getusername = message.text
            sql.execute(f"SELECT * FROM users WHERE nick = '{getusername}'")
            result = sql.fetchone()[0]
            client.send_message(cid, f'👤 | ID пользователя: {result}')
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды')

# Различные меню


@client.message_handler(content_types=['text'])
def menu(message):
    try:
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[2]
# Меню Администратора
        if message.text == "Начать работу Администратора" and getaccess == 777:
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True)
            btn1 = types.KeyboardButton('📰 Сообщить о проблеме')
            btn2 = types.KeyboardButton('📁 Телефоны отделов')
            btn3 = types.KeyboardButton('📚 Настройки бота')
            markup.add(btn1, btn2, btn3)
            client.send_message(
                message.from_user.id, "Вас приветствует бот ZN ITS", reply_markup=markup)
            client.send_message(message.from_user.id,
                                'Выберите интересующий вас раздел')

        elif message.text == '🔙 Главное меню' and getaccess == 777:
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True)
            btn1 = types.KeyboardButton('📰 Сообщить о проблеме')
            btn2 = types.KeyboardButton('📁 Телефоны отделов')
            btn3 = types.KeyboardButton('📚 Настройки бота')
            markup.add(btn1, btn2, btn3)
            client.send_message(
                message.from_user.id, "Вас приветствует бот ZN ITS", reply_markup=markup)
            client.send_message(message.from_user.id,
                                'Выберите интересующий вас раздел')

        elif message.text == '📚 Настройки бота' and getaccess == 777:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            btn2 = types.KeyboardButton("/users")
            btn3 = types.KeyboardButton("/getprofile")
            btn4 = types.KeyboardButton("/setaccess")
            btn5 = types.KeyboardButton("/getid")
            btn6 = types.KeyboardButton("/tasks")
            btn7 = types.KeyboardButton("/exportexcel")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
            client.send_message(message.from_user.id, 'Твой раздел: 📚 Настройки бота\n'
                                '/users - Список всех пользователей в БД\n'
                                '/getprofile - Получение информации о профиле пользователя по ID\n'
                                '/setaccess - Выдать права\n'
                                '/getid - Получить ID пользователя по нику\n'
                                '/tasks - Получить заявки в работе\n'
                                '/exportexcel - Выгрузить заявки из БД в Excel\n',
                                reply_markup=markup, parse_mode='Markdown')

# Меню стандартного пользователя
        elif message.text == "Начать работу" and getaccess == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('📰 Сообщить о проблеме')
            btn2 = types.KeyboardButton('📁 Телефоны отделов')
            btn3 = types.KeyboardButton('📚 Частые проблемы')
            markup.add(btn1, btn2, btn3)
            client.send_message(
                message.from_user.id, "Вас приветствует бот ZN ITS", reply_markup=markup)
            client.send_message(message.from_user.id,
                                'Выберите интересующий вас раздел')

        elif message.text == '🔙 Главное меню' and getaccess == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('📰 Сообщить о проблеме')
            btn2 = types.KeyboardButton('📁 Телефоны отделов')
            btn3 = types.KeyboardButton('📚 Частые проблемы')
            markup.add(btn1, btn2, btn3)
            client.send_message(
                message.from_user.id, "Вас приветствует бот ZN ITS", reply_markup=markup)
            client.send_message(message.from_user.id,
                                'Выберите интересующий вас раздел')

# Меню Инженера
        elif message.text == "Начать работу Инженера" and getaccess == 1:
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True)
            btn1 = types.KeyboardButton('📰 Сообщить о проблеме')
            btn2 = types.KeyboardButton('📁 Телефоны отделов')
            btn3 = types.KeyboardButton('📚 Частые проблемы')
            btn4 = types.KeyboardButton('💻 Заявки в работе')
            markup.add(btn1, btn2, btn3, btn4)
            client.send_message(
                message.from_user.id, "Вас приветствует бот ZN ITS", reply_markup=markup)
            client.send_message(message.from_user.id,
                                'Выберите интересующий вас раздел')
        elif message.text == '🔙 Главное меню' and getaccess == 1:
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True)
            btn1 = types.KeyboardButton('📰 Сообщить о проблеме')
            btn2 = types.KeyboardButton('📁 Телефоны отделов')
            btn3 = types.KeyboardButton('📚 Частые проблемы')
            btn4 = types.KeyboardButton('💻 Заявки в работе')
            markup.add(btn1, btn2, btn3, btn4)
            client.send_message(
                message.from_user.id, "Вас приветствует бот ZN ITS", reply_markup=markup)
            client.send_message(message.from_user.id,
                                'Выберите интересующий вас раздел')

        elif message.text == '💻 Заявки в работе' and getaccess == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            btn2 = types.KeyboardButton("/tasks")
            btn3 = types.KeyboardButton("/taskcomplt")
            markup.add(btn1, btn2, btn3)
            client.send_message(message.from_user.id, 'Твой раздел: 💻 Заявки в работе\n'
                                '/tasks - Получить заявки в работе\n'
                                '/taskcomplt - Отметить выполненую заявку\n',
                                reply_markup=markup, parse_mode='Markdown')
# Общие пункты и подпункты меню
        elif message.text == '📰 Сообщить о проблеме':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            btn2 = types.KeyboardButton("/messageIT")
            markup.add(btn1, btn2)
            client.send_message(message.from_user.id, 'Твой раздел: 📰 Сообщить о проблеме\n',
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '📁 Телефоны отделов':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn01 = types.KeyboardButton('🔙 Главное меню')
            btn1 = types.KeyboardButton('🔎 Приёмная')
            btn2 = types.KeyboardButton('🔎 Агроотдел')
            btn3 = types.KeyboardButton('🔎 IT служба')
            btn4 = types.KeyboardButton('🔎 Техподдержка Тесса')
            btn5 = types.KeyboardButton('🔎 Бухгалтерия')

            markup.add(btn01, btn1, btn2, btn3, btn4, btn5)
            client.send_message(message.from_user.id,
                                '⬇ Выберите отдел', reply_markup=markup)

        elif message.text == '🔎 Приёмная':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 🔎 Приёмная\n \nВот какие номера доступны:\n'
                                '18111 - Иванова Стефания Давидовна\n'
                                '18112 - Алексеева Ульяна Александровна\n'
                                '18113 - Алексеева Дарья Михайловна',
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '🔎 IT служба':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 🔎 IT служба\n \nВот какие номера доступны:\n'
                                "18114 - Кочетов Фёдор Михайлович\n"
                                "18115 - Кузнецов Никита Германович\n"
                                "18116 - Петрова Анна Александровна",
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '🔎 Агроотдел':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 🔎 Агроотдел\n \n Вот какие номера доступны:\n'
                                "18124 - Родионов Василий Антонович\n"
                                "18125 - Головин Артемий Даниилович\n"
                                "18126 - Рябова Анастасия Александровна",
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '🔎 Техподдержка Тессы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 🔎 Техподдержка Тессы\n \n Вот какие номера доступны:\n'
                                "18117 - Волкова Анастасия Марковна\n"
                                "18119 - Быкова Полина Михайловна\n"
                                "18120 - Масленников Давид Борисович\n",
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '🔎 Бухгалтерия':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 🔎 Бухгалтерия\n \n Вот какие номера доступны:\n'
                                "18121 -Дегтярева Вероника Глебовна\n"
                                "18122 - Баженова Оливия Егоровна\n"
                                "18123 - Петрова Алиса Андреевна\n",
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '📚 Частые проблемы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn01 = types.KeyboardButton('🔙 Главное меню')
            btn1 = types.KeyboardButton('📚 Почта')
            btn2 = types.KeyboardButton('📚 Тесса')
            btn3 = types.KeyboardButton('📚 1С Предприятие')
            markup.add(btn01, btn1, btn2, btn3)
            client.send_message(message.from_user.id,
                                '⬇ Выберите подраздел', reply_markup=markup)

        elif message.text == '📚 Почта':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 📚 Почта\n \n Вот что есть в доступе:\n'
                                "Вопрос: \nВсем привет! У меня на компе не работает ни одна почта.\n"
                                "В настройках стоит принимать все письма, но они не приходят. А когда захожу на ящик, то он закрыт. И не открывается. Что делать? Спасибо.\n"
                                "Ответ: \nМожет быть, стоит сменить пароль на почтовом ящике.",
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '📚 Тесса':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 📚 Тесса\n \n Вот что есть в доступе:\n'
                                "Вопрос: \n Перестала открываться Тесса, в чём может быть проблема?\n"
                                "Ответ: \n Как правило, такое случается когда зависает сессия, необходимо сделать полный выход из приложения.\n"
                                "В скрытых значках найти иконку Тессы и через клик правой кнопкой мыши сделать выход.",
                                reply_markup=markup, parse_mode='Markdown')

        elif message.text == '📚 1С Предприятие':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('🔙 Главное меню')
            markup.add(btn1)
            client.send_message(message.from_user.id, 'Твой раздел: 📚 1С Предприятие\n \n Вот что есть в доступе:\n'
                                "Вопрос: \n На экране высвечивается сообщение о невозможности подключения к БД, что делать?\n"
                                "Ответ: \n Напишите заявку в IT-отдел, с вами свяжутся и помогут решить проблему",
                                reply_markup=markup, parse_mode='Markdown')
    except:
        client.send_message('🚫 | Ошибка при выполнении')


client.polling(none_stop=True)
