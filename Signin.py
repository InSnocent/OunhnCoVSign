# coding=utf=8
from selenium import webdriver
import random
import smtplib 
from email.mime.text import MIMEText
from time import sleep
import time
import json

StuIds=[]
phoneNunbers=[]
addresses=[]
Emails=[]

def main(): 
    f = open('./data.json',encoding='utf-8')
    data = json.load(f)
    info = data['info']
    for i in range(len(info)):
        StuIds.append(info[i]['StuId'])
        phoneNunbers.append(info[i]['phoneNumber'])
        addresses.append(info[i]['address'])
        Emails.append(info[i]['Email'])
        print(StuIds[i])
        print(phoneNunbers[i])
        print(addresses[i])
        print(Emails[i])
        # Start servive
        sleep(random.randint(2, 5)) 
        driver = webdriver.Chrome()
        driver.get("http://kq.ounh.org:92/login") 
        time.sleep(2) 
        now_handle = driver.current_window_handle
        driver.find_element_by_css_selector("[type=text]").click()
        driver.find_element_by_css_selector("[type=text]").send_keys(StuIds[i])
        driver.find_element_by_css_selector('.login').click()
        time.sleep(2)
        driver.find_element_by_xpath(".//*[@id='root']/div/div[2]/div/div[1]/div/div[2]/div[2]/img").click()
        time.sleep(2)
        pn = driver.find_element_by_css_selector("[type=tel]")
        pn.click()
        driver.execute_script("arguments[0].value = '';", pn)
        pn.send_keys(phoneNunbers[i])
        driver.find_element_by_css_selector("[type=text]").send_keys(addresses[i])
        driver.find_element_by_css_selector("[type=radio]").click()
        driver.find_element_by_xpath("//*[@id='root']/div/form/div/div/div[14]/div[1]/div/a[1]").click()
        # sentemail
        host = 'smtp.163.com' #设置发件服务器地址
        port = 465 #设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
        sender ='' #设置发件邮箱，一定要自己注册的邮箱
        pwd = ''# 设置发件邮箱的密码，登陆用
        receiver = Emails[i] #设置邮件接收人，可以是扣扣
        body ='<h1>今日打卡已完成</h1><p></p>'#设置邮件正文，支持HTML

        msg = MIMEText(body,'html')#设置正文为符合邮件格式的HTML内容
        msg['subject'] = '打卡通知'#设置邮件标题
        msg['from'] = sender#设置发送人
        msg['to'] = receiver #设置接收人

        try:
            s = smtplib.SMTP_SSL(host,port) #注意！如果是使用SSL端口，这里就要改为SMTP_SSL
            s.login(sender,pwd)#登陆邮箱
            s.sendmail(sender,receiver,msg.as_string())#发送邮件！
            print('Done.sent email success')
        except smtplib.SMTPException:
            print('Error.sent email fail')
            
main()