from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup


USER = "본인 아이디"
PASS = "본인 비번"

browser = webdriver.Chrome()
browser.implicitly_wait(3)

# 로그인 페이지에 접근하기. 
url_login = "https://www.yes24.com/Templates/FTLogin.aspx?ReturnURL=http://ticket.yes24.com/Pages/Perf/Detail/Detail.aspx&&ReturnParams=IdPerf=30862"
browser.get(url_login)
print("로그인 페이지에 접근합니다.")

# 아이디와 비밀번호 입력하기.
e = browser.find_element_by_id("SMemberID")
e.clear()
e.send_keys(USER)
e = browser.find_element_by_id("SMemberPassword")
e.clear()
e.send_keys(PASS)

# 입력 양식 전송해서 로그인하기.
form = browser.find_element_by_css_selector("button#btnLogin").submit()
print("로그인 버튼을 클릭합니다.")

# 예매버튼 클릭.
reserve_bt = browser.find_element_by_class_name("rbt_reserve").click()
print("예매 버튼을 클릭합니다.")

# 팝업 창으로 전환.
browser.switch_to.window(browser.window_handles[1])

# 날짜 선택하기(26일)
date_sel = browser.find_element_by_id("2019-01-17").click()
sleep(1)

# '좌석선택' 버튼 클릭.
res = browser.find_element_by_css_selector("div.fr img").click()

#좌석 선택하기

browser.switch_to.frame(browser.find_element_by_name("ifrmSeatFrame"))


browser.find_element_by_id('t800012').click()

browser.find_element_by_class_name('booking').click()

print("좌석선택완료")

browser.switch_to_default_content()

print("다시원래창으로 돌아옴")

browser.find_element_by_xpath('//*[@id="StepCtrlBtn03"]/a[2]/img').click()

print("할인쿠폰 다음버튼")

sleep(3)
browser.find_element_by_xpath('//*[@id="StepCtrlBtn04"]/a[2]/img').click()

browser.find_element_by_id('rdoPays22').click()

browser.find_element_by_xpath('//*[@id="selBank"]/option[5]').click()



browser.find_element_by_xpath('//*[@id="cbxCancelFeeAgree"]').click()
browser.find_element_by_xpath('//*[@id="chkinfoAgree"]').click()

pic = browser.save_screenshot("pic.png")

browser.find_element_by_xpath('//*[@id="imgPayEnd"]').click()

# for i in seat:
#     a = i.text
#     print(i)


# print(seat)
# # for s in seat:
# #     print("-", s.text)





# 브라우저 닫음
# browser.close()
