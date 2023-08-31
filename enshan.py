#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: enshan.py
Author: WFRobert
Date: 2023/9/1 1:09
cron: 0 50 6 * * ?
new Env('恩山论坛模拟登录脚本');
Description: 恩山论坛模拟登录,每日登录获得+1恩山币
Update: 2023/9/1 更新cron
"""
import os
import sys
import initialize
import requests
from bs4 import BeautifulSoup


def main():
    """
    主方法，开始模拟登录

    :return:
    """
    initialize.info_message("开始获取Cookie\n")
    if os.environ.get("ENSHAN_COOKIE"):
        cookies = os.environ.get("ENSHAN_COOKIE")
    else:
        initialize.error_message("请在环境变量填写ENSHAN_COOKIE的值")
        sys.exit()  # 未获取到cookie，退出系统

    for number, cookie in enumerate(cookies.split("&")):
        initialize.info_message(f"开始执行第{number + 1}个账号")
        url = 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&op=base'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
            'Referer': 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1',
            'Cookie': cookie
        }
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
            user_name = soup.find('a', attrs={'title': '访问我的空间'}).text  # 用户名
            points = soup.find('a', attrs={'id': 'extcreditmenu'}).text  # 目前积分
            user_group = soup.find('a', attrs={'id': 'g_upmine'}).text  # 用户组
            initialize.info_message(f"模拟登录成功---{user_name}---{points}---{user_group}")
        else:
            initialize.error_message(f"第{number + 1}个账号可能cookie过期了")


if __name__ == '__main__':
    initialize.init()  # 初始化日志
    main()  # 主方法
    initialize.send_notify("恩山论坛")  # 发送消息
