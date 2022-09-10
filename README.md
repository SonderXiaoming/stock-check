# 股票查询插件

这是一个适用hoshinobot的股票查询功能插件，数据来自新浪

由于本人水平有限，有能力的人如果有更好的想法直接pr，不用开issue

## 食用方法

1.下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

git clone https://github.com/SonderXiaoming/stock-check.git

2.装依赖：

到HoshinoBot\hoshino\modules\stock-check目录下，管理员方式打开powershell

pip install pandas

3.启用：

在 HoshinoBot\hoshino\config\ **bot**.py 文件的 MODULES_ON 加入 'stock-check'

然后重启 HoshinoBot

## 指令说明

[股票查询 + 【股市代码】+ 【股票代码】]

sh：沪市，sz：深市，hk：港市,usr_：美股

例：股票查询usr_aapl，股票查询hk00001

[(日k|分时|周k|月k)线图像 + 【股市代码】+【股票代码】]

例：日k线图像sh000001

(深成指|上证指|道琼斯|纳斯达克|恒生指|日经指数|台湾加权|新加坡)查询

例：深成指查询
