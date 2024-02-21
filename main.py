import telebot
from telebot import types
import sqlite3

login = ''
bot = telebot.TeleBot('6605651085:AAEA0og4FEEx1IXupa1rDb0OcrggXlHUijk')


@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key,'
                ' name varchar(50),'
                ' infoStore varchar(50),'
                ' infoPlot varchar(50),'
                ' infoEnd varchar(10))')
    conn.commit()
    cur.close()
    conn.close()
    start(message)


def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Начнем наше приключение!'))
    #markup.add(types.KeyboardButton('Продолжим с того момента, где остановились)'))
    markup.add(types.KeyboardButton('Проверка корректности'))
    bot.send_message(message.chat.id,
                     f'Добрый день, соискатель приключений! Давай же поскорее отправимся в путь, выбери в меню нужное действие',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    global login
    print('Боту отправили обычный текст')
    if message.text == 'Начнем наше приключение!':
        print('зашел1')
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         f'Пожалуйста, введите имя', reply_markup=markup)
        bot.register_next_step_handler(message, txt)
    elif message.text == 'Продолжим с того момента, где остановились)':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         f'Пожалуйста, введите имя', reply_markup=markup)
        bot.register_next_step_handler(message, txt_min)

    elif message.text == 'Проверка корректности':
        callback(message)
        start(message)
        return

    elif ((message.text == 'Веревки') or message.text == 'Подводный аппарат'
          or message.text == 'Компас' or message.text == 'Книга о морских приключениях' or message.text == 'Провизия'):
        name = message.text.strip()
        print('зашел2', name)
        func = record(2, name, message)
        if func:
            on_click2(message)
    elif (message.text == 'Яхта: роскошный вариант с комфортом и скоростью' or
          message.text == 'Парусник: более медленный, но экологичный выбор' or
          message.text == 'Корабль: универсальное средство, которое обеспечит безопасность и комфорт в длительном '
                          'плавании'):
        name = message.text.strip()
        print('зашел3 ', name)
        func = record(3, name, message)
        print('значение func ', func)
        if func:
            print('func == True')
            on_click3(message)
    elif (message.text == 'Осмотреть риф и рискнуть судном'):
        var = fromTable(message, 'infoStore')
        print('var ', var)
        if var == 'Веревки':
            on_click4(message)
        if var == 'Подводный аппарат':
            on_click8(message)
        # else:
    elif (message.text == 'Исследовать риф'):
        on_click9(message)
    elif (message.text == 'Выходить скорее из опасного участка моря' or message.text == 'Обогнуть риф и продолжить путешествие'):
        on_end1(message)
    elif (message.text == 'Помочь потерпевшим крушение'):
        on_click5(message)
    elif (message.text == 'Вау, пираты! Всегда мечтал стать одним из них'):
        on_end2(message)
    elif (message.text == 'Нужно скорее делать ноги отсюда'):
        on_click6(message)
    elif (message.text == 'Обыскать шлюпку на возможные предметы помощи'):
        on_click7(message)
    elif (message.text == 'Мальчик справа' or message.text == 'Мальчик слева'):
        on_end3(message)
    elif (message.text == 'Равное количество воды'):
        on_end4(message)
    elif (message.text == 'Проплыть мимо'):
        on_end1(message)
    elif (message.text == '322 560' or message.text == '104 044 953 600'):
        bot.send_message(message.chat.id, 'Белые пешки можно расположить 40 320 способами, белые ладьи - 2 способами, '
                                          'белых коней - 2 способами и белых слонов - 2 способами. Перемножая эти '
                                          'числа,'
                                          'мы обнаружим, что белые фигуры можно  расположить 322 560 различными '
                                          'способами.\nЧерные фигуры можно, разумеется, расположить таким же числом '
                                          'способов. Следовательно, общее число различных расположений равно 322 '
                                          '560^2 ='
                                          '104 044 953 600. Саму доску можно расположить 2 способами. Следовательно, '
                                          'ответ нужно удвоить, что даст 208 089 907 200 различных способов.')
        on_end5(message)
    elif (message.text == '208 089 907 200'):
        on_click10(message)
    elif (message.text == 'Поднять черный ящик'):
        on_click11(message)
    elif (message.text == 'Завершить обследование'):
        on_end6(message)
    elif (message.text == '228'):
        on_end7(message)
    elif (message.text == '200' or message.text == '216'):
        on_end8(message)
    else:
        print('Ничего не нашел')


# запись данных в базу данных id - столбец, name что вносим в столбец
def record(id, name, message):
    global login
    if login == '':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Кажется сервер вылетел, введите имя ещё раз ૮₍ ´• ˕ •` ₎ა'
                                          'после чего в меню выберите нужный вариант ответа)')
        bot.register_next_step_handler(message, txt_find)
        return False
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
    el = 'name'
    if id == 1:
        el = 'name'
    if id == 2:
        el = 'infoStore'
    if id == 3:
        el = 'infoPlot'
    if id == 4:
        el = 'infoEnd'
    cur.execute(f"UPDATE users SET ({el}) = '{name}' WHERE name = '{login}'")
    conn.commit()
    cur.close()
    conn.close()
    return True


def callback(message):
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += F'Имя: {el[1]}, предмет: {el[2]}, средство передвижения: {el[3]}, концовка №{el[4]}\n'
    bot.send_message(message.chat.id, info)
    cur.close()
    conn.close()


def txt_find(message):
    global login
    name = message.text.strip()
    print('name: ', name)
    login = name


def txt_min(message):
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
    global login
    name = message.text.strip()
    print('name:', name)
    login = name
    cur.execute(f'SELECT name FROM users WHERE name = "{login}"')
    if cur.fetchone() is None:
        bot.send_message(message.chat.id, 'Такого героя в игре ещё не бывало, давайте вернемся назад')
        print('Такого героя в игре ещё не бывало, давайте вернемся назад')
        cur.close()
        conn.close()
        start(message)
        return
    else:
        print('герой есть!')
    # и вот тут если будет не лень дописать перемещение по уровням


def txt(message):
    global login
    name = message.text.strip()
    print('name:', name)
    login = name
    print('никого не жлу')
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM users WHERE name = '{name}'")
    if cur.fetchone() is None:
        cur.execute(f"INSERT INTO users (name) VALUES ('%s')" % (name))
        conn.commit()
    else:
        bot.send_message(message.chat.id, 'Такой герой уже бывал в наших рядах, давай вернемся на шаг назад')
        start(message)
        return
    cur.close()
    conn.close()
    on_click(message)


def fromTable(message, column):
    global login
    print('column ', column)
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
    cur.execute(f"SELECT {column} FROM users WHERE name = '{login}'")
    result = cur.fetchone()
    info = result[0]
    print('info% ', info)
    assert isinstance(info, object)
    return info


def on_click(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Веревки'))
    markup.add(types.KeyboardButton('Подводный аппарат'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/xwIuKqvLmZX_GA',
                   caption='Пора начать подготовку к путешествию и выбрать необходимое оборудование для плавания. Что '
                           'ты возьмешь с собой?',
                   reply_markup=markup)


def on_click2(message):
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Яхта: роскошный вариант с комфортом и скоростью'))
    markup2.add(types.KeyboardButton('Парусник: более медленный, но экологичный выбор'))
    markup2.add(types.KeyboardButton(
        'Корабль: универсальное средство, которое обеспечит безопасность и комфорт в длительном плавании'))
   # markup2.add(types.KeyboardButton('Плот: экстремальный выбор для тех, кто ищет приключения'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/f6Fp_wc83WSBlQ',
                   caption='Ты подходишь к порту и перед тобой становится задача выбрать, на чём ты отправишься в '
                           'плаванье?',
                   reply_markup=markup2)
    # bot.register_next_step_handler(message, on_click3)


def on_click3(message):
    print('захожу в on_click3')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Осмотреть риф и рискнуть судном'))
    markup2.add(types.KeyboardButton('Обогнуть риф и продолжить путешествие'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/PbgLX_JWk8Yggw',
                   caption='Пришло время отправиться в море. Перед вами лежит океан возможностей и открытий. '
                           'После многих часов плавания вы замечаете нечто странное вдали. '
                           'Постепенно приближаясь, вы осознаете, что это опасный коралловый риф. '
                           'Возникает вопрос: решите ли вы исследовать его?',
                   reply_markup=markup2)


def on_click4(message):
    print('захожу в on_click4')
    var = fromTable(message, 'infoStore')
    if var == 'Веревки':
        markup2 = types.ReplyKeyboardMarkup()
        markup2.add(types.KeyboardButton('Помочь потерпевшим крушение'))
        markup2.add(types.KeyboardButton('Выходить скорее из опасного участка моря'))
        bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/OKBSNDYclemBeA',
                       caption='Ты включаешь мощь двигателя, чтобы преодолеть риф, ощущая, '
                               'как яхта медленно, но верно преодолевает волнующие воды. '
                               'По мере того как ты продвигаешься вперед, твой взгляд улавливает '
                               'обломки корабля, а на их фоне - люди, потерпевшие кораблекрушение. '
                               'Их крики о помощи разносятся по ветру, напоминая о беспокойстве '
                               'и опасностях этого морского путешествия. Твоё сердце наполняется '
                               'решимостью помочь, и ты решаешь реагировать на этот вызов. '
                               'Помня о веревках на яхте, ты готовишься к спасательной операции, '
                               'подготавливаясь бросить им спасительный канат и вытащить их к себе на борт.',
                       reply_markup=markup2)


def on_click5(message):
    print('захожу в on_click5')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Вау, пираты! Всегда мечтал стать одним из них'))
    markup2.add(types.KeyboardButton('Нужно скорее делать ноги отсюда'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/vXneYWerqSBFnw',
                   caption='Когда они поднимаются на твою яхту, ты замечаешь нечто странное в их поведении. Они выглядят не так, как обычные моряки. Их одежда, их манеры, даже их взгляд - все это наводит на мысль, что они необычные. И вот, когда они находятся на твоей яхте, они разворачиваются и обращаются к тебе с угрожающим видом. '
                           '\n - Добро пожаловать на борт, моряк,- один из них произносит смеющимся тоном, который вызывает у тебя ощущение дискомфорта. - Ты сделал большую ошибку, остановившись здесь. Теперь ты наш заложник! \n Ты осознаешь, что попал в ловушку. Люди, которых ты пытался спасти, оказались пиратами! Твое сердце начинает биться сильнее, когда ты осознаешь, что они не собираются отпускать тебя так просто. Теперь ты оказался в серьезной опасности.',
                   reply_markup=markup2)


def on_click6(message):
    print('захожу в on_click6')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Обыскать шлюпку на возможные предметы помощи'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/TUJUa8Q6FaTRwQ',
                   caption='Вместо того чтобы погружаться в панику, ты начинаешь действовать быстро и сообразительно. С тихими шагами ты подкрадываешься к борту яхты, обнаруживая один из спасательных шлюпок. Стремительно ты прыгаешь в шлюпку, высвобождая ее от веревок и спасательного снаряжения.'
                           '\nКогда пираты замечают твоё исчезновение, уже слишком поздно. Ты уже далеко от них, гребя в глубины моря на своей спасательной шлюпке. С каждым взмахом весла ты чувствуешь, как свобода возвращается к тебе, и ты осознаешь, что ничто не может удержать тебя в плену.'
                           'Но что же делать дальше?',
                   reply_markup=markup2)


def on_click7(message):
    print('захожу в on_click7')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Мальчик справа'))
    markup2.add(types.KeyboardButton('Мальчик слева'))
    markup2.add(types.KeyboardButton('Равное количество воды'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/YTH38bZqElp_ug',
                   caption='Для успешного обыска шлюпки необходимо разгадать загадку: какой из мальчиков на картинке '
                           'принесет больше воды?',
                   reply_markup=markup2)


def on_click8(message):
    print('захожу в on_click8')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Исследовать риф'))
    markup2.add(types.KeyboardButton('Проплыть мимо'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/ybep7uFHVCWLkg',
                   caption='Когда ты пытаешься преодолеть риф, вдруг твое внимание привлекает странный объект в '
                           'глубине моря. При ближайшем рассмотрении ты осознаешь, что это обломки самолета, '
                           'затонувшего в этом районе. ',
                   reply_markup=markup2)


def on_click9(message):
    print('захожу в on_click9')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('322 560'))
    markup2.add(types.KeyboardButton('104 044 953 600'))
    markup2.add(types.KeyboardButton('208 089 907 200'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/hZJLzyOtSTtuHQ',
                   caption='Чтобы успешно исследовать обломки, необходимо правильно решить задачку)'
                           '\nЕсть единственная шахматная доска и единственный набор шахматных фигур. Сколькими '
                           'различными способами можно правильно расставить фигуры перед началом игры?',
                   reply_markup=markup2)


def on_click10(message):
    print('захожу в on_click10')
    bot.send_message(message.chat.id, 'Белые пешки можно расположить 40 320 способами, белые ладьи - 2 способами, '
                                      'белых коней - 2 способами и белых слонов - 2 способами. Перемножая эти числа, '
                                      'мы обнаружим, что белые фигуры можно  расположить 322 560 различными '
                                      'способами.\nЧерные фигуры можно, разумеется, расположить таким же числом '
                                      'способов. Следовательно, общее число различных расположений равно 322 560^2 = '
                                      '104 044 953 600. Саму доску можно расположить 2 способами. Следовательно, '
                                      'ответ нужно удвоить, что даст 208 089 907 200 различных способов.')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('Поднять черный ящик'))
    markup2.add(types.KeyboardButton('Завершить обследование'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/OdsHWpowDEM3Qw',
                   caption='Подводный аппарат медленно опускается на дно океана, освещая темные глубины своими яркими '
                           'фарами. Приблизившись к обломкам самолета, ты начинаешь внимательно обследовать '
                           'окружающую обстановку. Вдруг твой взгляд зацепляет черный ящик - ключевой элемент, '
                           'который может содержать ценные данные о произошедшем инциденте. /nТы стоишь перед '
                           'решением: пытаться ли поднять черный ящик, рискуя раскрыть секреты этого загадочного '
                           'происшествия? Решение в твоих руках, и оно может повлиять на ход всего твоего '
                           'приключения. Внутренний конфликт между жаждой знаний и страхом неожиданных открытий '
                           'требует от тебя взвешенного решения.',
                   reply_markup=markup2)


def on_click11(message):
    print('захожу в on_click11')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton('216'))
    markup2.add(types.KeyboardButton('228'))
    markup2.add(types.KeyboardButton('200'))
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/SvBseTtUE0tnRg',
                   caption='Ну что, пора разомнуть мозг, хехе'
                           '\nПароход, отойдя от пристани, прошел за первый час 25 км. Но так как ветер был попутный, '
                           'пароход ускорял свой ход каждый час на километр. На восьмом часу пути он шел уже со '
                           'скоростью 32 км/ч. Какое расстояние прошел пароход за 8 часов?',
                   reply_markup=markup2)


def on_click12(message):
    print('захожу в on_click12')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click13(message):
    print('захожу в on_click13')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click14(message):
    print('захожу в on_click14')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click15(message):
    print('захожу в on_click15')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click16(message):
    print('захожу в on_click16')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click17(message):
    print('захожу в on_click17')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click18(message):
    print('захожу в on_click18')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click19(message):
    print('захожу в on_click19')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_click20(message):
    print('захожу в on_click20')
    markup2 = types.ReplyKeyboardMarkup()
    markup2.add(types.KeyboardButton(''))
    markup2.add(types.KeyboardButton(''))
    bot.send_photo(message.chat.id, '',
                   caption='',
                   reply_markup=markup2)


def on_end2(message):
    print('захожу в on_end2')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/yR5kg8O-EQWsag',
                   caption='Внутри тебя '
                           'пробуждается что-то новое - чувство романтики приключений, которые ждут тебя '
                           'впереди. Ты видишь себя, стоящим на палубе пиратского корабля, ветер волшебно ласкающий '
                           'твои волосы, а море приглашающе манящее тебя в свои объятия. \n "Я остаюсь,'
                           '" - ты решительно заявляешь, чувствуя, как твое сердце наполняется азартом и свободой, '
                           'которые ты никогда раньше не испытывал. "Я хочу прочувствовать эту романтику, '
                           'стать частью вашей команды и вместе с вами покорять моря!"'
                           '\nТы видишь удивление в глазах пиратов, затем они улыбаются, одобряя твоё решение. И ты '
                           'понимаешь, что теперь ты вступил на новый путь - путь пиратства, полный опасностей, '
                           'приключений и свободы. \nВы успешно дошли до финала №2',
                   reply_markup=markup)
    func = record(4, '2', message)


def on_end1(message):
    print('захожу в on_end1')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/dHaFyGbwjiRqdQ',
                   caption='Когда море поднимается перед тобой во всей своей величии, оно кажется океаном загадок, '
                           'приглашающим тебя на свой бескрайний танец. Ты подходишь ближе, с горящим желанием '
                           'раскрыть его тайны, погрузиться в его глубины и почувствовать его живую сущность. Но '
                           'когда приходит момент смелости, чтобы исследовать, море кажется неотступно беспощадным, '
                           'отводящим тебя назад на берег с горьким осознанием своей собственной трусости. Тайны моря '
                           'остаются недоступными, оно сохраняет свои загадки под замком, подобно сокровищам, '
                           'защищенным древними проклятиями. Ты возвращаешься домой, обессиленный и разочарованный, '
                           'оставив за спиной лишь тени невыполненных приключений. Но даже в этом поражении есть '
                           'урок: море учит тебя уважать его силу и непредсказуемость, напоминая о том, что не все '
                           'тайны готовы раскрываться на твой запрос. \nТы успешно дошёл до финала №1',
                   reply_markup=markup)
    func = record(4, '1', message)


def on_end3(message):
    print('захожу в on_end3')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/yhsR_GXxX9cPNQ',
                   caption='Пока ты обыскиваешь шлюпку в поисках полезных предметов, твои надежды начинают угасать. '
                           'Каждый уголок ты внимательно изучаешь, но, к сожалению, ничего полезного не находишь. '
                           '\n Твоё сердце сжимается от отчаяния. Ты чувствуешь, что надежда на '
                           'спасение начинает ускользать от тебя.',
                   reply_markup=markup)
    bot.send_message(message.chat.id, 'Без колебаний, ты берёшься за весла и начинаешь направлять шлюпку к '
                                      'ближайшему берегу. Ты не имеешь карты, компаса или других средств навигации, '
                                      'но все же решаешься на это рискованное предприятие.'
                                      '\n Наконец, после упорного плавания, ты видишь контуры берега вдали. Твои '
                                      'силы '
                                      'почти'
                                      'иссякли, но взгляд на берег наполняет тебя новой энергией и решимостью. Ты '
                                      'продолжаешь'
                                      'грести, пока наконец не добираешься до берега.'
                                      '\n Ты выходишь на сушу, изнурённый, но с чувством облегчения.'
                                      '\n Ты успешно (ну или не совсем) дошёл до финала №3')
    func = record(4, '3', message)


def on_end4(message):
    print('захожу в on_end4')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/fl5kP0yM4IB85w',
                   caption='Пока ты обыскиваешь шлюпку в поисках полезных предметов, твой взгляд упирается в маленький '
                           'ящик, прикрепленный к стойке. В нем ты обнаруживаешь карту и компас. Радость овладевает тобой: '
                           'в этих простых предметах ты видишь шанс на спасение.'
                           '\nСжав карту и компас в руках, ты ставишь перед собой цель - добраться до ближайшего '
                           'берега. Ты приступаешь к плаванию, следуя указаниям компаса и ориентируясь на карту. Когда '
                           'ты наконец увидишь контуры берега, твоё сердце забьётся сильнее от волнения. Ты продолжаешь '
                           'грести с упорством и, наконец, добираешься до берега.'
                           '\nТы выходишь на сушу с огромным облегчением и радостью. Ты благодаришь свою находчивость '
                           'и решимость, которые помогли тебе выжить в этой непростой ситуации. Так начинается новое '
                           'приключение - исследование неизведанных просторов загадочного берега.'
                           '\nВы успешно дошли до финала №4', reply_markup=markup)
    func = record(4, '4', message)


def on_end5(message):
    print('захожу в on_end5')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id,'https://disk.yandex.ru/i/nKFSh0wI5x2lNw',
                   caption='Ты начинаешь погружение подводного аппарата в глубины океана, '
                           'напряженно смотря на морские глубины, ожидая открытий. Но, '
                           'к несчастью, в процессе погружения кабель подводного аппарата '
                           'зацепился за острые скалы рифа и оборвался. С тяжелым сердцем ты '
                           'осознаешь, что твой подводный аппарат навсегда останется на дне '
                           'океана, в том же месте, где находятся обломки таинственного '
                           'самолета.'
                           '\nВы успешно дошли до финала №5', reply_markup=markup)
    func = record(4, '5', message)


def on_end6(message):
    print('захожу в on_end6')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/0Q6OP0dsCDfzYw',
                   caption='Приняв решение не рисковать оборудованием, ты продолжаешь свое путешествие с '
                           'осторожностью, но не упускаешь из виду возможности для исследований. Твой путь проходит '
                           'спокойно, но при этом ты остаешься открытым для новых впечатлений. Возвращаясь домой, '
                           'ты чувствуешь себя умиротворенным и удовлетворенным, зная, что сделал правильный выбор, '
                           'сохраняя баланс между безопасностью и жаждой приключений.'
                           '\nВы успешно дошли до финала №6', reply_markup=markup)
    func = record(4, '6', message)


def on_end7(message):
    print('захожу в on_end7')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/nfeX91sMd7n5Cg',
                   caption='Подняв черный ящик, ты осознаешь, что это самолет принадлежал Амелии '
                                                'Эрхарт - известной американской пилотке, чье исчезновение стало '
                                                'загадкой мирового масштаба. Амелия Эрхарт была первой '
                                                'женщиной-пилотом, которая совершила соло-перелет через Атлантический '
                                                'океан. Она стала иконой авиации и символом женской смелости и '
                                                'решительности.'
                                                '\nВы успешно дошли до финала №7', reply_markup=markup)
    bot.send_message(message.chat.id, 'Исчезновение Амелии Эрхарт в 1937 году, '
                                                'когда она пыталась совершить кругосветный полет, до сих пор остается '
                                                'одной из самых загадочных тайн в истории. Ее последний радиосигнал '
                                                'был принят недалеко от острова Никумба в Тихом океане, после чего '
                                                'она и ее самолет пропали без вести. /nОткрытие ее самолета в этом '
                                                'районе моря приносит новые надежды на разгадку загадки ее '
                                                'исчезновения. Твое открытие может стать ключом к раскрытию этой '
                                                'таинственной истории и пролить свет на судьбу этой отважной женщины '
                                                'и ее экипажа.')
    func = record(4, '7', message)


def on_end8(message):
    print('захожу в on_end8')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/-pCn5j8v-WvYUA', caption='Ты с напряжением следишь, как аппарат пытается достать черный ящик '
                                                'из глубины океана, но несмотря на все усилия, ничего не получается. '
                                                'Сердце бьется быстрее от разочарования, когда осознаешь, что это не '
                                                'судьба привезти с собой этот важный артефакт. В итоге ты уходишь ни '
                                                'с чем, но внутри тебя горит огонь решимости. Ты понимаешь, '
                                                'что этот опыт лишь подогрел твое желание вернуться сюда с большой '
                                                'командой, чтобы справиться с этим вызовом и раскрыть тайны, '
                                                'которые скрывает океан.'
                                                '\nВы успешно дошли до финала №8', reply_markup=markup)
    func = record(4, '8', message)


def on_end9(message):
    print('захожу в on_end9')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, '', caption=''
                                                '\nВы успешно дошли до финала №9', reply_markup=markup)
    func = record(4, '9', message)


def on_end10(message):
    print('захожу в on_end10')
    markup = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, '', caption=''
                                                '\nВы успешно дошли до финала №10', reply_markup=markup)
    func = record(4, '10', message)


bot.polling(none_stop=True)
