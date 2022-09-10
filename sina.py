import requests
import base64

headers = {'referer': 'http://finance.sina.com.cn'}

word_dict = {
"日k":"daily",
"分时":"min",
"周k":"weekly",
"月k":"monthly"
}

name_dict = {
"深成指":"s_sz399001",
"上证指":"s_sh000001",
"道琼斯":"int_dji",
"纳斯达克":"int_nasdaq",
"恒生指": "int_hangseng",
"日经指数": "int_nikkei",
"台湾加权": "b_TWSE",
"新加坡":"b_FSSTI",
}

def get_stock_info(gudaima,special=False):
    resp = requests.get('http://hq.sinajs.cn/list=' + gudaima, headers=headers, timeout=6)
    data = resp.text.split(',')
    print(data)
    if len(data) < 3:
        return False
    stock_info = {}
    check = gudaima[:2]
    if not special:
        if check == 'sz' or check == 'sh':
            stock_info["name"] = data[0].replace(f'var hq_str_{gudaima}="','')
            stock_info["open"] = data[1]
            stock_info["close"] = data[2]
            stock_info["recent_deal"] = data[3]
            stock_info["high_deal"] = data[4]
            stock_info["low_deal"] = data[5]
            stock_info["deal_num"] = data[8]
            stock_info["deal_money"] = data[9]
        elif check == 'hk':
            stock_info["name"] = data[1]
            stock_info["open"] = data[2]
            stock_info["close"] = data[3]
            stock_info["recent_deal"] = data[6]
            stock_info["high_deal"] = data[4]
            stock_info["low_deal"] = data[5]
            stock_info["deal_num"] = data[12]
            stock_info["deal_money"] = data[11]
        else:
            stock_info["name"] = data[0].replace(f'var hq_str_{gudaima}="','')
            stock_info["open"] = data[5]
            stock_info["close"] = data[26]
            stock_info["recent_deal"] = data[1]
            stock_info["high_deal"] = data[6]
            stock_info["low_deal"] = data[7]
            stock_info["deal_num"] = data[10]
            stock_info["deal_money"] = data[30]
    else:
        stock_info["point"] = data[1]
        stock_info["price"] = data[2]
        stock_info["rate"] = data[3].replace("\";",'')
    return stock_info

def get_stock_image(time,id):
    time_edit = word_dict[time]
    url = f"http://image.sinajs.cn/newchart/{time_edit}/n/{id}.gif"
    resp = requests.get(url,timeout=6)
    pic_str = base64.b64encode(resp.content).decode()
    if pic_str:
        base64_str = 'base64://' + pic_str
        return base64_str
    else:
        return False
