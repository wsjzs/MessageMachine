# encoding="utf-8"
from selenium import webdriver
import json
import sys


class MessageMachine():
    BY = {'ID': "id",
          'XPATH': "xpath",
          'LINK_TEXT': "link text",
          'PARTIAL_LINK_TEXT': "partial link text",
          'NAME': "name",
          'TAG_NAME': "tag name",
          'CLASS_NAME': "class name",
          'CSS_SELECTOR': "css selector"}

    # commandList = {'get': openPage}

    def __init__(self, driver, phone: str):
        '''
        初始化数据(webdriver,phone)
        '''
        self.driver = driver
        self.phone = phone
        # interval间隔时间默认0秒
        self.interval = 0
        print('init success')

    def setInterval(self, time: int):
        '''
        time:每次发送间隔时间(秒)默认是3秒
        '''
        self.interval = time

    def openPage(self, url):
        self.driver.get(url)

    def findEmelent(self, by, value):
        '''
        by:'ID','XPATH','LINK_TEXT','PARTIAL_LINK_TEXT','NAME','TAG_NAME','CLASS_NAME','CSS_SELECTOR'
        '''

        return self.driver.find_element(MessageMachine.BY[by], value)

    def addCommands(self, commands: dict):
        self.commands = commands

    def quit(self):
        self.driver.quit()

    def executeOne(self, one: dict):
        '''
        one dict 一次完整的发送短信命令列表
        '''
        try:
            tmp = {}
            for i in one:
                head = i[0]
                if head == 'get':
                    self.openPage(i[1])
                    continue

                if head == 'find':
                    tmp[i[3]] = self.findEmelent(i[1], i[2])
                    continue
                if head == 'input':
                    value = i[2]
                    if(value == 'phone'):
                        # place phone
                        value = self.phone
                    tmp[i[1]].send_keys(value)
                    continue

                if head == 'click':
                    tmp[i[1]].click()
                    continue

                if head == 'execute_script':
                    self.driver.execute_script(i[1])
                    continue
                if head == 'wait':
                    import time
                    time.sleep(i[1])
                    continue
                if head=='implicitly_wait':
                    self.driver.implicitly_wait(i[1])
            self.driver.implicitly_wait(10)
            import time
            time.sleep(self.interval)
        except:
            print('error:'+one[0][1])
            return False
        print('send success:'+one[0][1])
        return True

    def executeAll(self):
        for i in self.commands:
            self.executeOne(i)
            # self.driver.switch_to.alert.accept()


def start():
    phone='******' #短信接收号码
    send_rounds=20 #发送几轮短信(循环json文件的次数)
    root = sys.path[0]
    d_path = root+r'\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=d_path,options=options)
    a = MessageMachine(driver, phone)
    # a.setInterval(4) #设置每次发送间隔
    with open(root+r'\data.json','r') as f:
        data =json.load(f)
        a.addCommands(data)
        for i in range(send_rounds):
            a.executeAll()

start()
