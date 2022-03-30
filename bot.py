import telebot
from telebot import types
import pandas as pd

API_TOKEN = '5292481096:AAFUJER3qnV3v0moNUPUchyvA6p9eSWiKAU'

link={
    'Coco-Pay':'https://coco-pay.com/',
    'Шахта':'https://mine.exchange/',
    'МультиВал':'https://multival.is/',
    'CryptoMax':'https://cryptomax.ru/',
    'ChangeProject':'https://changeproject.bz/',
    'Adb':'https://adb.bz/',
    'GlobalBits':'https://globalbits.org/',
    'Excoin':'https://excoin.in/',
    'FastEx':'https://fastex.su/',
    'Bitcoin24Pro':'https://bitcoin-24.pro/',
    'AllMoney':'https://allmoney.market/',
    'HASchange':'https://haschange.com/',
    'Belqi':'https://belqi.net/',
    
}

bot=telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("➕ Купить")
    item2=types.KeyboardButton("➖ Продать")
    markup.add(item1,item2)
    
    
    msg = bot.reply_to(message, """\
Привет!
Данный бот поможет тебе обменять биткоин по самому выгодному курсу.
Для начала работы выбери нужную команду в выпадающем меню.
""",  reply_markup=markup)

   
@bot.message_handler(content_types='text')
def message_reply(message):
    
    if message.text=="➕ Купить":
        DB_BUY = pd.read_csv(r'db_buy.csv')
        stroka = 'Держи список самых выгоднных обменников для покупки биткоина за рубли\n\
Если перед названием обменника стоит @ - то это телеграмм бот.\n\
Обычный текст - найди этот обменник самостоятельно через гугл.\n\n'

        for i in range(5):
            change_name = DB_BUY.iloc[-1][1:].sort_values().index[i]
            if link.get(change_name):
                stroka += f'<a href="{link.get(change_name)}">{change_name}</a>' + " - "
            else:
                stroka += change_name + " - "
            stroka+= str(DB_BUY.iloc[-1][1:].sort_values()[i]) + "₽\n"
            
        bot.send_message(message.chat.id,stroka,parse_mode = 'HTML',    disable_web_page_preview = True)
        
    elif message.text=="➖ Продать":
        DB_SELL = pd.read_csv(r'db_sell.csv')
        stroka = 'Держи список самых выгоднных обменников для продажи биткоинов за рубли\n\
Если перед названием обменника стоит @ - то это телеграмм бот.\n\
Обычный текст - найди этот обменник самостоятельно через гугл.\n\n'

        for i in range(5):
            change_name = DB_SELL.iloc[-1][1:].sort_values(ascending=False).index[i]
            if link.get(change_name):
                stroka += f'<a href="{link.get(change_name)}">{change_name}</a>' + " - "
            else:
                stroka += change_name + " - "
            stroka+= str(DB_SELL.iloc[-1][1:].sort_values(ascending=False)[i]) + "₽\n"
            
        bot.send_message(message.chat.id,stroka,parse_mode = 'HTML',disable_web_page_preview = True)
bot.infinity_polling()