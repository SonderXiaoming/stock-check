from hoshino import Service, R
from .sina import get_stock_image, get_stock_info, name_dict
from .create_img import image_draw

helpText = '''
[股票查询 + 【股市代码】+ 【股票代码】]
sh：沪市，sz：深市，hk：港市,usr_：美股
例：股票查询usr_aapl，股票查询hk00001
[(日k|分时|周k|月k)线图像 + 【股市代码】+【股票代码】]
例：日k线图像sh000001
(深成指|上证指|道琼斯|纳斯达克|恒生指|日经指数|台湾加权|新加坡)查询
例：深成指查询
'''
sv = Service('股票查询', enable_on_default=True, help_=helpText)

@sv.on_prefix('股票查询帮助')
async def stock_help(bot, ev):
    await bot.send(ev, helpText, at_sender=True)

@sv.on_prefix('股票查询')
async def check_stock(bot, ev):
    stockID = ev.message.extract_plain_text()
    stock_info = get_stock_info(stockID)
    if stock_info:
        msg = f'''
股票名称：  {stock_info["name"]}
今日开盘价：{stock_info["open"]}元
昨日收盘价：{stock_info["close"]}元
最近成交价：{stock_info["recent_deal"]}元
最高成交价：{stock_info["high_deal"]}元
最低成交价：{stock_info["low_deal"]}元
成交数量：  {stock_info["deal_num"]}股
成交金额：  {stock_info["deal_money"]}元
'''.strip()
        pic = image_draw(msg)
        await bot.send(ev, f'[CQ:image,file={pic}]', at_sender=True)
    else:
        await bot.send(ev, "股票代码错误", at_sender=True)


@sv.on_rex(r'(深成指|上证指|道琼斯|纳斯达克|恒生指|日经指数|台湾加权|新加坡)查询')
async def check_stock(bot, ev):
    stockname = ev['match'].group(1)
    stockID = name_dict[stockname]
    stock_info = get_stock_info(stockID, True)
    if stock_info:
        msg = f'''
股票名称：{stockname}
当前点数：{stock_info["point"]}点
点数变动：{stock_info["price"]}点
涨跌率：  {stock_info["rate"]}%
'''.strip()
        pic = image_draw(msg)
        await bot.send(ev, f'[CQ:image,file={pic}]', at_sender=True)
    else:
        await bot.send(ev, "股票代码错误", at_sender=True)


@sv.on_rex(r'(日k|分时|周k|月k)线图像(.+)')
async def img_stock(bot, ev):
    time = ev['match'].group(1)
    stockID = ev['match'].group(2)
    image = get_stock_image(time, stockID)
    if image:
        await bot.send(ev, f'[CQ:image,file={image}]', at_sender=True)
    else:
        await bot.send(ev, "股票代码错误", at_sender=True)
