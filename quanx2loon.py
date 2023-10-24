import re

import requests
from jinja2 import Template


text = '''
// ==UserScript==
// @ScriptName        Keep 净化
// @Author            @ddgksf2013
// @ForHelp           若有屏蔽广告的需求，可公众号后台回复APP名称
// @WechatID          公众号墨鱼手记
// @TgChannel         https://t.me/ddgksf2021
// @Contribute        https://t.me/ddgksf2013_bot
// @Feedback          📮 ddgksf2013@163.com 📮
// @UpdateTime        2023-09-09
// @Function          应用净化去广告
// @Suitable          自行观看“# > ”注释内容
// @Attention         如需引用请注明出处，谢谢合作！
// @Version           V1.0.5
// @ScriptURL         https://github.com/ddgksf2013/Rewrite/raw/master/AdBlock/KeepStyle.conf
// ==/UserScript==


hostname=api.gotokeep.com, kad.gotokeep.com

# > 屏蔽应用内弹窗
^https?:\/\/api\.gotokeep\.com\/guide-webapp\/v\d\/popup\/getPopUp url reject
# > 屏蔽部分启动弹窗
^https?:\/\/api\.gotokeep\.com\/kprime\/v\d\/popups\/primeGuide url reject
# > 屏蔽开屏广告请求
^https?:\/\/kad\.gotokeep\.com\/op-engine-webapp\/v\d\/ad url reject
# > 屏蔽青少年弹窗
^https?:\/\/api.gotokeep.com/cauchy/growth/init url reject
# > 屏蔽搜索栏自动填充词
^https?:\/\/api\.gotokeep\.com\/search\/v\d\/default\/keyword\/list url reject
# > 屏蔽热词
^https?:\/\/api\.gotokeep\.com\/search\/v\d\/hotword\/list url reject
# > 屏蔽hotCourse
^https?:\/\/api\.gotokeep\.com\/search\/v\d\/hotCourse\/list url reject
# > 屏蔽adwebapp
^https?:\/\/api\.gotokeep\.com\/op-engine-webapp\/v\d\/ad url reject
# > 屏蔽广告预加载
^https?:\/\/api\.gotokeep\.com\/ads\/v\d\/ads\/preload url reject
# > 屏蔽adbox
^https?:\/\/api\.gotokeep\.com\/training\/box\/config url reject
# > 屏蔽更新
^https?:\/\/api\.gotokeep\.com\/anno\/v\d\/upgrade\/check url reject
# > 我的页面去推广
^https?:\/\/api\.gotokeep\.com\/athena\/v\d\/people\/my$ url script-response-body https://github.com/ddgksf2013/Scripts/raw/master/keepStyle.js
# > 应用底部栏净化
^https?:\/\/api\.gotokeep\.com\/config\/v\d\/basic url script-response-body https://github.com/ddgksf2013/Scripts/raw/master/keepStyle.js
# > 发现页处理
https://api.gotokeep.com/homepage/v\d/tab url script-response-body https://github.com/ddgksf2013/Scripts/raw/master/keepStyle.js
# > 课程预览页广告
https://api.gotokeep.com/nuocha/course/v2/\w+/preview url script-response-body https://github.com/ddgksf2013/Scripts/raw/master/keepStyle.js
# > 我的运动页面去除下方推荐
https://api.gotokeep.com/sportpage/sport/v3/mysport url script-response-body https://github.com/ddgksf2013/Scripts/raw/master/keepStyle.js

'''


class QuanxConfig:
    def __init__(self, file_content):
        self.hostname = ''
        self.rule_list = []
        self.header = {
            key: value for key, value in self.parse_header(file_content)
        }

        for item in self.parse_rule(file_content):
            self.rule_list.append({
                'url': item[0],
                'operation': item[1],
                'script': item[2],
                'tag': item[3] if len(item) > 3 else '',
            })

    def parse_header(self, file_content: str):
        lines = filter(lambda l: l.strip() != "", file_content.split("\n"))
        header_flag = False
        header = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.find("UserScript") != -1 and line.find('/UserScript') == -1:
                header_flag = True
                continue
            if line.find("/UserScript") != -1:
                header_flag = False
                break
            if header_flag:
                res = re.findall(r'@(\w+)(\s+.*)', line)
                for item in res:
                    key = item[0]
                    value = item[1]
                    header.append([key, value.strip()])
        return header

    def parse_rule(self, file_content: str):
        lines = filter(lambda l: l.strip() != "" and not l.startswith("//"), file_content.split("\n"))
        res = []
        last_tag = ''
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("hostname"):
                self.hostname = (line.split('=')[1]).strip()
                continue
            if line.startswith("#"):
                last_tag = re.sub(r"[#> ]", "", line)
                continue
            split_line = re.split(r' ', line)
            res.append([split_line[0], split_line[2], split_line[3] if len(split_line) > 3 else '', last_tag])
            last_tag = ''
        return res

    def __repr__(self) -> str:
        return f'hostname: {self.hostname} \n' \
               f'header:{self.header} \n' \
               f'rule_list:{self.rule_list} \n'

loon_template=Template('''
#!name={{quanx.header['ScriptName']}}
#!desc={{quanx.header['MainFunction']}}
#!author=mm


[Script]
{%  for rule in quanx.rule_list  -%}
{%  if rule.operation.find('script-response-body') != -1  -%}
# > {{rule.tag}}
http-response {{rule.url}} script-path={{rule.script}},requires-body=true,timeout=10,enabled=true,tag={{rule.tag}}
{% endif -%}
{% endfor -%}

[Rewrite]
{%  for rule in quanx.rule_list  -%}
{%  if rule.operation.find('reject') != -1  -%}
{{rule.url}} {{rule.operation}}
{% endif -%}
{% endfor -%}



[MITM]
hostname = {{quanx.hostname}}
''')




import json

def lambda_handler(event, context):
    parameters = event['queryStringParameters']
    if not parameters:
        return {
        'statusCode': 200,
        'body': "请填入要转换的文件路径"
        }
    url = parameters.get('url')
    url_content = ''
    if not url :
        return {
        'statusCode': 200,
        'body': "请填入要转换的文件路径"
        }
    response = requests.get(url)
    url_content = response.text
    quanx = QuanxConfig(url_content)
    content = loon_template.render(quanx=quanx)
    return {
        'statusCode': 200,
        'body': content
    }

