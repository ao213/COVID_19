##ライブラリインポート領域##
import discord
import re
import os

##スクレイピング##
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.chrome.options import Options

##関数領域##

# params:
# return:

# params:都道府県名(末尾なし)
# return:都道府県名(末尾あり)
def add_tail(text):
    if text == '東京':
        text = text + '都'

    elif text == '北海':
        text = text + '道'

    elif text in ['京都','大阪']:
        text = text + '府'

    else:
        text = text + '県'
    return text

# params:message_text
# return:[True | False]
def search_tail(text):
    if '都' in text:
        return True
    elif '道' in text:
        return True
    elif '府' in text:
        return True
    elif '県' in text:
        return True
    else:
        return False
     
# params:message_text
# return:        
def regexp_for_message(text):
    if search_tail(text):
        #末尾あり
        matches = re.search('東京都|北海道|(?:京都|大阪)府|.{2,3}県',text)
        return matches.group()
    else:
        #末尾なし
        matches = re.search('東京|北海|京都|大阪|.{2,3}',text)
        add_tail(matches.group())
        return add_tail(matches.group())

# params:message_text
# return:[False,text | True,embed_message]
def create_message_for_covid_19_data(message):
        prefecture = regexp_for_message(message[10:])
        if ((data:=get_covid_19_data_from_web(prefecture)) is None):#ここの括弧のあり、なしの意味
            infected_count, dead_count = -1,-1
        else:
            infected_count, dead_count = data
        
        if infected_count == -1:
            return [False,'その県は対応してません']

        else:
            embed_message = discord.Embed(title=f'{prefecture}の感染者', description=f'{prefecture}の感染者と死亡者数を表示', color=0x9419e6)
            embed_message.set_author(name='COVID-19')
            embed_message.add_field(name='感染者数', value=infected_count, inline=True)
            embed_message.add_field(name='死亡者数', value=dead_count, inline=True)
            
        return [True,embed_message]
    
    
    
##スクレイピング用変数##
option = Options()
option.binary_location = '/app/.apt/usr/bin/google-chrome'
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)

# params: 都道府県名
# return: [infected_count,infected_count || None]
def get_covid_19_data_from_web(ken):
    browser.get('https://news.google.com/covid19/map?hl=ja&mid=%2Fm%2F03_3d&gl=JP&ceid=JP%3Aja')
    tbody = browser.find_elements_by_class_name('ppcUXd')
    trs = tbody[0].find_elements(By.TAG_NAME, 'tr')
    for i in range(2,len(trs)):
        if ken == trs[i].find_element_by_class_name('pcAJd').text:
            infected_count = trs[i].find_elements_by_xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div[4]/div/div/div[2]/div/div[1]/table/tbody/tr[{i + 1}]/td[1]')[0].text
            dead_count = trs[i].find_elements_by_xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div[4]/div/div/div[2]/div/div[1]/table/tbody/tr[{i + 1}]/td[5]')[0].text
            return infected_count,dead_count
        
###変数指定領域###
client = discord.Client()
prefix = '!!'    ##コマンドの頭
times = [1,60,3600,86400]
bot_token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_ready():
    activity = discord.Activity(name = '✧ʕ̢̣̣̣̣̩̩̩̩·͡˔·ོɁ̡̣̣̣̣̩̩̩̩✧',type = discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print('botはオンライン')
 
@client.event
#テキストに反応してメッセージを送信するbot
async def on_message(message):
    #API省略定義
    m_content = message.content
    m_channel = message.channel
    m_guild = message.guild

    if message.author.bot:
        return 
    
    if messagecont.startswith(prefix + 'COVID-19'):
        result,message = create_message_for_covid_19_data(messagecont)

        if result:
            await m_channel.send(embed = message)
        else:
            await m_channel.send(message)




client.run(bot_token)
