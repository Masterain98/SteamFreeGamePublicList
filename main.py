# -*-coding:UTF-8-*-
from urllib import request  # 导入request模块
import requests  # 导入requests模块
import json  # 导入JSON模块
import chardet  # 导入chardet编码识别模块
from bs4 import BeautifulSoup  # 导入BeautifulSoup
import MySQLdb  # 导入Mysql相关模块
import re

if __name__ == "__main__":
    # 定义header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    # 发起request
    req = request.Request("https://steamdb.info/upcoming/free/#upcoming-promotions", headers=headers)

    response = request.urlopen(req)  # 打开网站
    html = response.read()  # 读取内容

    charset = chardet.detect(html)  # 获取编码格式
    html = html.decode(charset["encoding"])  # 解码
    # print(html)

    freeGameList = []  # 初始化免费游戏sub列表
    soup = BeautifulSoup(html, features="lxml")
    freeGame_list_soup = soup.find('table', attrs={
        'class': 'table-products table-responsive-flex table-hover text-left table-sortable'})  # 找到免费游戏表格

    # 找到对应的每个游戏
    for game_sub in freeGame_list_soup.find_all('tr', attrs={'class': 'app sub'}):
        game_subid = str(game_sub["data-subid"])
        print("Sub id:", game_subid)  # 打印标签属性 game_sub.attrs会打印所有

        # 找到该游戏的Steam链接
        for game_logo in game_sub.find_all('td', attrs={'class': 'applogo'}):
            game_steamLink = game_logo.find('a')
            game_steamLink = game_steamLink["href"]
            # print("Steam link:", game_steamLink)

        # 找到该游戏的名字
        game_td = game_logo.find_next_sibling('td')
        game_sub_link = game_td.find('a')
        game_name = game_sub_link.find('b').string
        print(game_name)

        # 确定免费属性 (Keep or Weekend)
        game_type_menu = game_sub.find_all('td', attrs={'class': 'price-discount'})
        if "<b>Keep</b>" in str(game_type_menu):
            game_type_string = "Keep"
        else:
            game_type_menu = game_sub.find('td', attrs={'class': 'text-center'})
            # print(game_type_menu)
            game_type_string = game_type_menu.next_sibling.next_sibling.string
            # print(game_type_Weekend)
        print(game_type_string)

        # 生成免费入库游戏列表
        if game_type_string == "Keep":  # Not Weekend
            freeGame_Add = [game_subid, game_name, game_steamLink]
            freeGameList.append(freeGame_Add)
            # print(freeGameList)

    # 生成ASF入库命令
    ASFCommand = "addlicense ASF sub/"
    if (len(freeGameList) != 0):
        for i in range(len(freeGameList)):
            ASFCommand = ASFCommand + freeGameList[i][0]
            ASFCommand += ", sub/"
        ASFCommand = ASFCommand[:-6]  # 删除最后一组", sub/"
        print(ASFCommand)
    else:
        print("No Free Game Available!")

    # 连接数据库
    db = MySQLdb.connect(host="127.0.0.1",
                         user="root",
                         passwd="root",
                         db="steamdb",
                         charset="utf8")  # 建立MySQL连接

    # 检查是否存在asf和freeGame表
    cursor = db.cursor()
    cursor.execute("show tables")  # 发送查询库中所有表名的SQL
    table_list = [tuple[0] for tuple in cursor.fetchall()]  # 分离表名
    if "asf" not in table_list:
        # print("Build ASF")
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE `steamdb`.`asf` ( `display` INT NOT NULL , `command` TEXT NOT NULL ) ENGINE = InnoDB;")  # 发送创建asf表的SQL命令
        cursor.execute("INSERT INTO `asf` (`display`, `command`) VALUES ('1', 'empty')")  # 为asf表创建一个初始化值
        db.commit()
    if "freeGame" not in table_list:
        # print("Build freeGame")
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE `steamdb`.`freeGame` ( `game_name` TEXT NOT NULL , `sub_id` TEXT NOT NULL , `steam_link` TEXT NOT NULL ) ENGINE = InnoDB;")  # 发送创建freeGame表的SQL命令
        db.commit()

    # 更新ASF命令
    cursor = db.cursor()
    asf_update = "UPDATE asf SET command='" + ASFCommand + "' WHERE display=1"  # SQL更新命令
    # print(asf_update)
    cursor.execute(asf_update)
    db.commit()

    # 检查freeGame表数据是否过期
    cursor = db.cursor()  # 获取操作游标
    current_mysql_subid = "SELECT sub_id FROM freeGame"  # 读取freeGame表中的sub_id列
    cursor.execute(current_mysql_subid)  # 提交SQL
    current_mysql_subid_data = cursor.fetchall()  # 读取全部数据，生成一个列表
    for i in current_mysql_subid_data:  # 遍历MySQL数据列表
        i = str(i)  # 数据属性转换
        i = i[2:-3]  # 提取subid
        notExpired = any(i in sl for sl in freeGameList)  # 检查该subid是否在更新的subid列表中
        if notExpired == False:  # 如果更新列表中不存在该subid意为失效/过期
            cursor = db.cursor()  # 重置操作游标
            sql_delete_expSub = "DELETE FROM freeGame WHERE sub_id=" + i  # 生成SQL删除命令
            # print(sql_delete_expSub)
            cursor.execute(sql_delete_expSub)  # 提交SQL
            db.commit()  # 提交SQL

    # 写入数据库
    for i in range(len(freeGameList)):  # 遍历更新sub列表
        sub_id_db = freeGameList[i][0]  # 读取sub的数字
        game_name_db = freeGameList[i][1]  # 读取sub的名称
        sql_check = 'SELECT * FROM `freeGame` WHERE sub_id=' + sub_id_db  # 生成SQL查询命令
        cursor = db.cursor()  # 重置操作游标
        cursor.execute(sql_check)  # 提交SQL命令
        sql_check_result = cursor.fetchone()  # 获取SQL命令结果
        if sql_check_result is None:  # 如果收到None意味着该Sub不在MySQL数据库中
            sql_insert = 'INSERT INTO freeGame(game_name,sub_id,steam_link) VALUES("' + game_name_db + '","' + sub_id_db + '","' + game_steamLink + '")'  # 生成SQL添加命令
            print(sql_insert)
            cursor = db.cursor()  # 重置操作游标
            cursor.execute(sql_insert)  # 发送SQL添加命令
            db.commit()  # 提交
    db.close()  # 关闭MySQL连接

    # ASF API领取游戏
    # 定义header
    api_headers = {
        "accept": "application/json",
        "Authentication": "YourASFPasswd",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    # 定义Body
    api_POST_data = {
        "Command": ASFCommand
    }
    # print(api_POST_data)
    # 定义URL
    asf_url = "https://yourASFURL/Api/Command"
    # 发起POST request
    asf_req = requests.post(asf_url, headers=api_headers, data=json.dumps(api_POST_data))
    print(asf_req.text)
