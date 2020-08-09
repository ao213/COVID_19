##ライブラリインポート領域##
import discord
import random
import re
import time
import threading
import datetime
import asyncio
import fibonatti
import os
import subprocess


##スクレイピング##
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.chrome.options import Options


##関数領域##
def game1(x): #数当て用関数　エラーは値が入ってないエラーなのでコマンドを送れば問題はない
    
    game1_rand = random.randint(1,100)
    game1_hit = True
    if(game1_rand != x):
        game1_hit = False
    return game1_hit


##クラス定義領域##
##スクレイピング用変数##
option = Options()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)
def covid_19_deta_get():
    browser.get('https://news.google.com/covid19/map?hl=ja&mid=%2Fm%2F03_3d&gl=JP&ceid=JP%3Aja')
    tbody = browser.find_elements_by_class_name('ppcUXd')
    trs = tbody[0].find_elements(By.TAG_NAME, 'tr')
    for i in range(2,len(trs)):
        ths = trs[i].find_elements_by_css_selector('th')
        infe_num = trs[i].find_elements_by_xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div[4]/div/div/div[2]/div/div[1]/table/tbody/tr[{i + 1}]/td[1]')
        dead_num = trs[i].find_elements_by_xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div[4]/div/div/div[2]/div/div[1]/table/tbody/tr[{i + 1}]/td[5]')

        for j in range(0,len(ths)):
            ken_name = ths[j].find_elements_by_css_selector('div.pcAJd')
            COVID_19_jp[0][i] = ken_name[j].text
            COVID_19_jp[1][i] = infe_num[0].text
            COVID_19_jp[2][i] = dead_num[0].text

###変数指定領域###
client = discord.Client()##discordのオブジェクト生成
prefix = '!!'    ##コマンドの頭
member = [] ##メンバーリスト
notoinmess = 'CODMから逃げるな' ##メッセージ
COVID_19_jp = [[0 for i in range(47)] for j in range(3)]
times = [1,60,3600,86400]
#トークン設定#
bot_token = os.environ['DISCORD_BOT_TOKEN']
embed1 = discord.Embed(title="予定表の提出", description="予定を教えてください。", color=0xff7b7b)

@client.event
async def on_ready():
    ###オンライン時の処理##
    ##アクティビティ処理##
    activity = discord.Activity(name = '✧ʕ̢̣̣̣̣̩̩̩̩·͡˔·ོɁ̡̣̣̣̣̩̩̩̩✧',type = discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print('botはオンライン') ##ターミナル表示##
 
@client.event
#テキストに反応してメッセージを送信するbot
async def on_message(message):
    #API省略定義
    messagecont = message.content
    messagech = message.channel
    messageguil = message.guild
    BANchID = '633845736655814685' #BAN用チャンネルID

    if message.author.bot:
        return 

    if messagecont.startswith(prefix + 'test'):     #テストメッセージ
        print('test')
        await messagech.send('test')

    if messagecont.startswith(prefix + 'DM'):   #DMへメッセージ
        await message.author.send('HI DM')

    if messagecont.startswith(prefix + 'game'): #数当てゲームno1
        Num = int(messagecont[6:])
        game1_ans = game1(Num)
        if(game1_ans == True):
            await messagech.send('HIT!! おめでとう！')
        else:
            await messagech.send('NO HIT! 残念！')

    if messagecont.startswith(prefix + 'getch '): #チャンネルを指定
        global get_channel
        get_ch_id = int(messagecont[10:28])
        get_channel = client.get_channel(get_ch_id)
        await messagech.send('チャンネルを' + messagecont[8:] + 'に指定しました')

    if messagecont.startswith(prefix + 'timemess'): #一定期間メッセージを送る 未完
        
        time_interval = int(messagecont[10:])
        Now_time1 = datetime.datetime.today()
        Now_time2 = datetime.datetime.today()
        End_time = datetime.datetime.today()
        End_time = Now_time1 + datetime.timedelta(hours=time_interval)
        embed2 = discord.Embed(title="お知らせ", url="https://forms.gle/TgTs2kRdixnDYe49A", description="来週の予定を提出してください", color=0x008080)
        time_flag = True
        i = 0
        
        print(f'test;{End_time.minute}')
        while time_flag:
            i +=1
            print(f'{Now_time1}現在時間')
            print(f'{End_time}終了時間')
            print(f'現在{i}時間経過')
            print('////////////////')
            
            if Now_time1 >= End_time:
                print('終了')
                await get_channel.send(embed=embed1)
                break
            if Now_time1.minute >= Now_time2.minute:
                Now_time2 = Now_time1
                Now_time1 = datetime.datetime.today()
                await get_channel.send(f'このメッセージは{time_interval}分間続きます、{i}分間経過')
                await get_channel.send('!d bump')
            await asyncio.sleep(times[1])
    if messagecont.startswith(prefix + 'memcount'): ##にんずうかぞえてくれるけいだんじｄddddフェjふぃえあ音階ふぁんせあの得あvmあぁ⒡目亜lmふぇいあ⒡時あ⒡なフェア⒡場hfbhbヴぁ；枝折を：pfかpr化：フェ
        count_mem = message.guild.member_count
        await messagech.send(f'{count_mem}人が参加してます')
    if messagecont.startswith(prefix + 'COVID-19'):
        covid_19_deta_get()
        place_1 = (messagecont[10:])
        for i in range(2,len(COVID_19_jp[0])):
            if place_1 == COVID_19_jp[0][i]:
                embed_3 = embed=discord.Embed(title=f'{place_1}の感染者', description=f'{place_1}の感染者と死亡者数を表示', color=0x9419e6)
                embed.set_author(name='COVID-19')
                embed.add_field(name='感染者数', value=COVID_19_jp[1][i], inline=True)
                embed.add_field(name='死亡者数', value=COVID_19_jp[2][i], inline=True)
                await messagech.send(embed=embed_3)
            elif i == len(COVID_19_jp[0]):
                await messagech.send('その県は対応していないです')




client.run(bot_token)