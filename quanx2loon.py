import re

text='''
// ==UserScript==
// @ScriptName        Bing首页简化[墨鱼版]
// @Author            @ddgksf2013
// @ForHelp           若有屏蔽广告的需求，可公众号后台回复APP名称
// @WechatID          公众号墨鱼手记
// @TgChannel         https://t.me/ddgksf2021
// @Contribute        https://t.me/ddgksf2013_bot
// @Feedback          📮 ddgksf2013@163.com 📮
// @UpdateTime        2023-03-30
// @Suitable          自行观看“# > ”注释内容[请卸载重装]
// @Attention         如需引用请注明出处，谢谢合作！
// @Version           V1.0.3
// @ScriptURL         https://github.com/ddgksf2013/Rewrite/raw/master/AdBlock/BingSimplify.conf
// ==/UserScript==



hostname = sapphire.api.microsoftapp.net, assets.msn.com, api.msn.com

# > bing_首页优化
^https?:\/\/sapphire\.api\.microsoftapp\.net\/config\/api\/v1\/get url script-response-body https://raw.githubusercontent.com/ddgksf2013/Scripts/master/bing.js
# > bing_位置请求
^https?:\/\/assets\.msn\.com\/service\/weather\/locations\/search url reject-dict
# > bing_信息流
^https?:\/\/assets\.msn\.com\/service\/news\/feed\/pages\/superapp url reject-dict
# > bing_天气请求
^https?:\/\/api\.msn\.com\/weather url reject-dict


'''

split = text.split("\n")

header_flag = False

header = {}
hostname=''

body_flag = False
config_list = []


for line in split:
    line = line.strip()
    if not line:
        continue

    if line.find("UserScript") != -1 and line.find('/UserScript') == -1 :
        header_flag = True
        continue
    if line.find("/UserScript") != -1:
        header_flag = False
        continue
    if header_flag:
        res = re.findall(r'@(\w+)(\s+.*)', line)
        for item in res:
            key = item[0]
            value = item[1]
            header[key] = value.strip()
    if not header_flag:
        if line.startswith("hostname"):
            hostname = line.split('=')[1]
            continue
        if line.startswith("#"):
            continue

        split_line = re.split(r' ', line)
        config_list.append({
            'url': split_line[0],
            # '': split_line[1],
            'operation': split_line[2],
            'script': split_line[3] if len(split_line) > 3 else ''
        })




print(header)
print(hostname)
print(config_list)