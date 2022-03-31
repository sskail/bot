from telethon import TelegramClient
import logging
import asyncio
import re
from bestchange_api import BestChange
import pandas as pd
import datetime

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


# Parse @BTC_CHANGE_BOT buy price 
async def get_1_buy_price():
    await client.send_message('BTC_CHANGE_BOT', '\U0001f4ca Обмен BTC/RUB')
    await asyncio.sleep(1)
    message = await client.get_messages('BTC_CHANGE_BOT',limit=1)
    await message[0].click(text='\U0001f4c8 Купить')
    await asyncio.sleep(1)
    message = await client.get_messages('BTC_CHANGE_BOT',limit=1)
    # for button in message[0].buttons:
    #     print(button[0].text)
        
    # Convert HTML or XML to int
    #print(message[0].text)
    text = message[0].buttons[0][0].text
    res = text.split(' ')[3].replace(u'\xa0','').replace(u'\u2009', '')
    #print(int(res))
    res = int(res)
    return(res)


async def get_1_sell_price():
    await client.send_message('BTC_CHANGE_BOT', '\U0001f4ca Обмен BTC/RUB')
    await asyncio.sleep(1)
    message = await client.get_messages('BTC_CHANGE_BOT',limit=1)
    await message[0].click(text='📉 Продать')
    await asyncio.sleep(1)
    message = await client.get_messages('BTC_CHANGE_BOT',limit=1)
    # for button in message[0].buttons:
    #     print(button[0].text)
        
    # Convert HTML or XML to int
    #print(message[0].text)
    text = message[0].buttons[0][0].text
    res = text.split(' ')[3].replace(u'\xa0','').replace(u'\u2009', '')
    #print(int(res))
    res = int(res)
    return(res)


# Parse @CryptoBot buy price 
async def get_2_buy_price():
    await client.send_message('CryptoBot', '/market')
    await asyncio.sleep(0.3)
    message = await client.get_messages('CryptoBot',limit=1)
    await message[0].click(text='\U0001f4c8 Купить')
    await asyncio.sleep(0.3)
    message = await client.get_messages('CryptoBot',limit=1)
    # for button in message[0].buttons:
    #     print(button[0].text)
        
    # Convert str to int
    text = message[0].buttons[0][0].text
    res_list = text.split(' ')[3:6]
    res =''
    for it in res_list:
        res+=re.sub(r'\.\d+.','',it)
    res = int(re.sub(r'\D','',res))
    #print(res)
    return(res)


# Parse @CryptoBot buy price 
async def get_2_sell_price():
    await client.send_message('CryptoBot', '/market')
    await asyncio.sleep(0.7)
    message = await client.get_messages('CryptoBot',limit=1)
    await message[0].click(text='📉 Продать')
    await asyncio.sleep(0.7)
    message = await client.get_messages('CryptoBot',limit=1)
    # for button in message[0].buttons:
    #     print(button[0].text)
        
    # Convert str to int
    text = message[0].buttons[0][0].text
    res_list = text.split(' ')[3:6]
    res =''
    for it in res_list:
        res+=re.sub(r'\.\d+.','',it)
    res = int(re.sub(r'\D','',res))
    #print(res)
    return(res)



async def check_site_buy():
    api = BestChange()
    exchangers = api.exchangers().get()
    dir_from = 42
    dir_to = 93
    rows = api.rates().filter(dir_from, dir_to)
    res=[]
    for val in rows:
        #print('{} {}'.format(exchangers[val['exchange_id']]['name'], round(val['get'])))
        res.append(exchangers[val['exchange_id']]['name']+' '+ str(round(val['give'])))
    return(res)
  
    
async def check_site_sell():
    api = BestChange()
    exchangers = api.exchangers().get()
    dir_from = 93
    dir_to = 42
    rows = api.rates().filter(dir_from, dir_to)
    res=[]
    for val in rows:
        #print('{} {}'.format(exchangers[val['exchange_id']]['name'], round(val['get'])))
        res.append(exchangers[val['exchange_id']]['name']+' '+ str(round(val['get'])))
    return(res)

# Remember to use your own values from my.telegram.org!
api_id = 'id'
api_hash = 'hash'

client = TelegramClient('name', api_id, api_hash)


DB_SELL = pd.read_csv(r'db_sell.csv')
DB_BUY = pd.read_csv(r'db_buy.csv')

async def sbor_buy():
    slovar = {}
    slovar['@BTC_CHANGE_BOT'] = await get_1_buy_price()
    slovar['@CryptoBot'] = await get_2_buy_price()
    price_site_list = await check_site_buy()
    for item in price_site_list:
        slovar[item.split(' ')[0]]=item.split(' ')[1]

    now = datetime.datetime.now()
    df = pd.DataFrame(slovar, index=[now.strftime("%d-%m-%Y %H:%M")])
    df.to_csv('tmp.csv',index_label = 'Date')
    df = pd.read_csv(r'tmp.csv')
    global DB_BUY
    DB_BUY = pd.concat([DB_BUY,df])
    print(DB_BUY)
    DB_BUY.to_csv('db_buy.csv',index = False)
    
async def sbor_sell():
    slovar = {}
    slovar['@BTC_CHANGE_BOT'] = await get_1_sell_price()
    slovar['@CryptoBot'] = await get_2_sell_price()
    price_site_list = await check_site_sell()
    for item in price_site_list:
        slovar[item.split(' ')[0]]=item.split(' ')[1]

    now = datetime.datetime.now()
    df = pd.DataFrame(slovar, index=[now.strftime("%d-%m-%Y %H:%M")])
    df.to_csv('tmp2.csv',index_label = 'Date')
    df = pd.read_csv(r'tmp2.csv')
    global DB_SELL
    DB_SELL = pd.concat([DB_SELL,df])
    print(DB_SELL)
    DB_SELL.to_csv('db_sell.csv',index = False)
    
    
async def main():
    while True:
        try:
            print('start sbor')
            await sbor_buy()
            await sbor_sell()
            await asyncio.sleep(60)
            print('stop sbor')
        except Exception as ex:
            print(ex)


with client:
    client.loop.run_until_complete(main())


