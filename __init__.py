import datetime
from hoshino import Service,R
from .Ashare import *
from .MyTT import *  
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from matplotlib.ticker import MultipleLocator
import hoshino
import re
import base64
import os
import io

helpText= '''
()中表示根据情况替换,+表示空格，[]表示里面为指令
指令1:
[股票查询 + 股票代码 + (1d|1w|1M|1m|5m|15m) + (数字) + (XXXX-XX-XX)]
备注:
1.股票代码支持sh,.XSHG,.XSHE格式
2.第一个()为设置1d日线|1w周线|1M月线，不填默认日线
以及分钟线'1m','5m','15m','30m','60m'(月线是大写M)
3.第二个()为设置总数，不填默认为5个
4.第三个()为设置日期，不填默认今天(格式要正确，严格按照示例)
5.顺序可以打乱
指令2:
[股票图像 + 股票代码]
显示布林带指标图像
'''
sv = Service('股票查询', enable_on_default=True, help_=helpText)

orginal_frequency = '1d'
orginal_count = 5
frequency = ['1m','5m','15m','30m','60m','1d','1w','1M']
minute = ['1m','5m','15m','30m','60m']

@sv.on_prefix('股票查询')
async def check_stock(bot, ev):
    f = orginal_frequency
    c = orginal_count
    now = datetime.datetime.now() 
    d = now.strftime("%Y-%m-%d")
    date = "日"
    info = ev.raw_message
    content = info.split()
    lenC = len(content)
    if lenC == 1:
        await bot.send(ev,helpText, at_sender=True)
        return
    elif 1 < lenC < 6:
        for value in content:
            if re.match(r'(sz|sh)\d{6}', value) or re.match(r'\d{6}.(XSHG|XSHE)', value):
                stockID = str(value)
            if value in frequency:
                f = str(value)
                if f == "1d" :
                    date = "日"
                elif f == '1w':
                    date = '周'
                elif f == '1M':
                    date = '月'
                elif f in minute :
                    date = "分钟"
            if re.match(r'\d$', value):
                c = int(value)
            if re.match(r'\d{2}-\d{2}-\d{2}', value):
                d = str(value)
    else :
        await bot.send(ev,'你多输入了参数,爬爬', at_sender=True)
        return
    stock_info=get_price(stockID, frequency= f ,count= c ,end_date= d)
    stock_info_edit = str(stock_info).replace('open','开盘').replace('close','收盘').replace('high','最高价').replace('low','最低价').replace('volume','成交量')
    pic = image_draw(stock_info_edit)
    await bot.send(ev,f'上证指数{date}线行情\n'+ f'[CQ:image,file={pic}]', at_sender=True)

@sv.on_prefix('股票图像')
async def img_stock(bot, ev):
    info = ev.raw_message
    content = info.split()
    lenC = len(content)
    if lenC == 1:
        await bot.send(ev,helpText, at_sender=True)
        return
    elif lenC == 2:
        stockID = str(content[1])
    else :
        await bot.send(ev,'你多输入了参数,爬爬', at_sender=True)
        return
    stock_info=get_price(stockID,frequency='1d',count=120)

    CLOSE=stock_info.close.values
    MA10=MA(CLOSE,10)                              #获取10日均线序列
    up,mid,lower=BOLL(CLOSE)                       #获取布林带指标数据

    plt.figure(figsize=(15,8))  
    plt.plot(CLOSE,label='SHZS')
    plt.plot(up,label='UP');           #画图显示 
    plt.plot(mid,label='MID')
    plt.plot(lower,label='LOW')
    plt.plot(MA10,label='MA10',linewidth=0.5,alpha=0.7)
    plt.legend()
    plt.grid(linewidth=0.5,alpha=0.7)
    plt.gcf().autofmt_xdate(rotation=45)
    plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
    plt.title('SH-INDEX   &   BOLL SHOW',fontsize=20)
    plt.savefig(hoshino.config.RES_DIR + '\\img\\stock.png')
    
    await bot.send(ev,R.img('stock.png').cqcode, at_sender=True)

def image_draw(msg):
    fontpath = font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')
    font1 = ImageFont.truetype(fontpath, 16)
    width, height = font1.getsize_multiline(msg)
    img = Image.new("RGB", (width + 20, height + 20), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), msg, fill=(0, 0, 0), font=font1)
    b_io = io.BytesIO()
    img.save(b_io, format="JPEG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str




  