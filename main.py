from telebot import types
from random import randint, choice
from class8 import *
from class9 import *
from class10 import class10_get_question
from models import Quiz, Result, Question
from bot_ini import bot, remove_buttons


@bot.message_handler(commands=['start'])
def hi(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Это бот <b>MxWell</b> - ваш помощник по подготовке к физике. '
                     'Я могу проверить твои знания, чтобы ты смог лучше подготовиться к работе.', parse_mode='html')
    bot.send_message(message.chat.id, 'Нужна помощь? Напиши в чат команду <u>/help</u>', parse_mode='html')
    bot.send_message(message.chat.id, 'Давай выберем твой класс, чтобы я мог ориентироваться на твой уровень знаний.'
                                      'Напиши в чат команду <u>/class</u>', parse_mode='html')


@bot.message_handler(commands=['class'])
def chose_class1(message):
    class_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    class_8 = types.KeyboardButton('8 класс')
    class_9 = types.KeyboardButton('9 класс')
    class_10 = types.KeyboardButton('10 класс')
    class_btn.add(class_8, class_9, class_10)

    bot.send_message(message.chat.id, 'В каком классе ты учишься?', reply_markup=class_btn)
    global user_class
    user_class = 0

    def choose_class2(message):
        if (message.text[0:2] not in ['8 ', '9 ', '10']):
            bot.send_message(message.chat.id, 'Ошибка! Указано некорректное значение. '
                                              'Этот бот предназначен только для <b>8-10 классов</b>. Напиши в чат <u>/class</u> ещё раз.',
                             parse_mode='html')
        else:
            user_class = int(message.text[0:2])
            bot.send_message(message.chat.id, f'Отлично, ты учишься в {user_class} классе.',
                             reply_markup=remove_buttons)

    bot.register_next_step_handler(message, choose_class2)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вот что я умею делать:\n'
                                      '<u>/start</u> - начать диалог сначала\n'
                                      '<u>/help</u> - помощь, список команд (то, что ты сейчас видишь)\n'
                                      '<u>/class</u> - выбрать класс, в котором ты сейчас учишься\n'
                                      '<u>/test</u> - начать тест\n'
                                      '<u>/marks</u> - посмотреть оценки, поставленные ботом.', parse_mode='html')


#### Ниже начинаются мои изменения.
## Постараюсь добавить коменты к каждому пункту
# Наша проблема заключалась в том, что "register_next_step_handler" ожидает ВВОДА от юзера и пока юзер на отправит сообщение переданная функция не будет вызвана
@bot.message_handler(commands=['beta_test'])
def beta_test(message):
    # Создаю кнопки для начла теста
    btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    r_ans = types.KeyboardButton('Готов!')
    w_ans1 = types.KeyboardButton('Выбрать другой класс')
    btn.add(r_ans, w_ans1)
    bot.send_message(message.chat.id, 'Это бета-версия теста, Вы готовы?', reply_markup=btn)
    
    # Определяю два объекта класса, и при каждом новом вызове "beta_test" данные обнулятся
    # TO-DO: обЪединить два этих класса в один класс Quiz
    right_ans = Result()
    # Параметр i - кол-во вопросов
    quiz = Quiz(i=3)
    
    # На этом этапе программа будет ждать пока юзер не ткнет на кнопку "Готово!" или "Выбрать другой класс"
    # На самом деле, чтобы юзер не отправил "get_questions" будет вызван.
    # Остальные параметры после "get_questions", в нашем случае "right_ans, quiz", будут переданы в "get_questions", как аргументы
    bot.register_next_step_handler(message, get_questions, right_ans, quiz)


def get_questions(message: types.Message, right_ans: Result, quiz: Quiz):
    # Проверяем, что нам отправил юзер
    if message.text == "Выбрать другой класс":
        # Если он тыкнул кнопку "Выбрать другой класс", то мы пишем результат.
        bot.send_message(message.chat.id, f"Тест завершён!\nРезультат {right_ans.right_ans}/{right_ans.right_ans + right_ans.incorrect_ans}", reply_markup=remove_buttons)
        # И отправляем его менять свой класс.
        chose_class1(message)
        
    elif message.text in ['Готов!', 'Далее!']:
        # Тут мы уменьшаем кол-во оставшихся вопросов на 1
        quiz.minus_i()
        
        # Тут мы получаем рандомный вопрос из тестовой БД
        # Теперь каждый вопрос это объект класса "Question", можно обойтись и словарем, но с классами удобно делать типизацию,
        # чтобы всегда знать, что ты передаешь в функцию.
        # TO:DO: Доделать выбор вопросов для определенного класса, думаю можно воспользоваться твоей идеей {Ключ: функция}
        question = class10_get_question()
        
        # Получаем новые вопросы, пока он не будет уникальным
        while quiz.is_uniq_questions(question):
            question = class10_get_question()
        
        # Добавляем наш вопрос в уже полученные.
        quiz.add_questions(question)
        
        # Тут я вынес логику отправки вопроса в отдельную функцию для красоты, можно все в одном месте делать.
        send_question(message, question)
        
        # Ждем пока нам придет сообщение с ответом и вызываем "check_answer".
        bot.register_next_step_handler(message, check_answer, question, right_ans, quiz)
        

def send_question(message: types.Message, question: Question):
    # Создаем кнопки с вариантами ответов.
    btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Тут перебираем все варианты через for и сразу добавляем в btn.
    for option in question.options:
        btn.add(types.KeyboardButton(option))
    
    # Отправляем вопрос с вариантами ответов в кнопках
    # TO:DO: Сделай так, что-бы варианты ответов были отображены в тексте под своей 
    # буквой (A,B,C,D...), а в кнопках были только буквы, без тела ответа.
    bot.send_message(message.chat.id, text=f'Вопрос:\n{question.question}', reply_markup=btn)
    

def check_answer(message: types.Message, question: Question, right_ans: Result, quiz: Quiz):
    # Добавляем кнопки.
    btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next = types.KeyboardButton('Далее!')
    go_back = types.KeyboardButton('Выбрать другой класс')
    btn.add(next, go_back)
    
    # Если ответ верный.
    if message.text == question.answer:
        # Добавляем +1 очко к правильным ответам
        right_ans.add_right_ans()    
        bot.send_message(message.chat.id, f'Вопрос №{right_ans.right_ans + right_ans.incorrect_ans} Вероно!', reply_markup=btn)
    
    # Если ответ не верный но из нашего спика
    elif  message.text in question.options:
        # Добавляем +1 очко к НЕ правильным ответам
        right_ans.add_incorrect_ans()    
        bot.send_message(message.chat.id, f'Вопрос №{right_ans.right_ans + right_ans.incorrect_ans} Неверно!', reply_markup=btn)
    
    # Если юзер написал что-то непонятное) то добавляем еще один вопрос в тест, возможно была опечатка.
    else:
        quiz.plus_i()
        bot.send_message(message.chat.id, 'Ваш ответ мне непонятен', reply_markup=btn)
    
    # Если больше вопросов для теста нет, то завершаем тест
    # TO:DO: Отправить юзера на смену класса или заново пройти тест, в общем как хочешь. Можно дать выбор кнопками.
    if quiz.i <= 0:
        bot.send_message(message.chat.id, f"Поздравляю тест завершён!\nРезультат {right_ans.right_ans}/{right_ans.right_ans + right_ans.incorrect_ans}", reply_markup=remove_buttons)
        return
    
    # Ждем ответа от юзера и вызываем "get_questions" еще раз.
    bot.register_next_step_handler(message, get_questions, right_ans, quiz)


@bot.message_handler(commands=['test'])
def test_msg(message):
    bot.send_message(message.chat.id,
                     'Тест состоит из 10 вопросов по физике, каждый из которых будет соответствовать твоему'
                     ' уровню знаний. Тебе будут представлены четыре варианта ответа, верным из которых будет один.'
                     ' В конце будет выставлена оценка, которая зависимосит от количества правильных ответов.'
                     ' Твои оценки будут складываться в твой средний балл. Узнав результат, ты поймёшь, насколько хорошо подготовлен к настоящей работе.'
                     ' Готов?')


bot.polling(none_stop=True)
