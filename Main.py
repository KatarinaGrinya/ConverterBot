import telebot
from configur import keys, TOKEN
from exceptions import APIExeption, CryptoConverter, DeclinasionByCases


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате:\n <имя валюты,. цену которой хотите узнать> ' \
        '<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> \n' \
        'Увидеть все доступные валюты /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 4:
            raise APIExeption('Слишком много параметров.')
        elif len(values) < 3:
            raise APIExeption('Слишком мало параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount,)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        inclined_quote = DeclinasionByCases(quote, float(amount))
        inclined_base = DeclinasionByCases(base, float(total_base))
        quote = inclined_quote.incline()
        base = inclined_base.incline()
        text = f'{amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
