import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! Я бот... Меня зовут Jonny!!!👻\n' \
           'Я умею конвертировать валюту по актуальному курсу!\n' '\n' \
            'Чтобы начать работу введите валюту в следующем порядке:\n' \
           '<название валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
           'Пример:   доллар рубль 10\n' '\n' \
           'Увидеть список всех доступных валют: /values  💵\n' \
            'Напомнить, что здесь вообще происходит /help  🧐'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты  💵:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверный формат ввода...  /help  🧐')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'УПС-И-И-И! 😱 \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}!')
    else:
        text = f'Ахалай-Маххалай🕺🕺🕺\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()

