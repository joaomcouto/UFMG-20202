from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


PATH = "/home/joaomcouto/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://orteil.dashnet.org/cookieclicker/")
#driver.maximize_window()

driver.implicitly_wait(15)

cookie = driver.find_element_by_id('bigCookie')
cookie_count = driver.find_element_by_id("cookies")
items = [driver.find_element_by_id("productPrice" + str(i)) for i in range(1,0,-1)]

tooltip = driver.find_element_by_id('tooltip')

actions = ActionChains(driver)
actions.click(cookie)

upperLimit = 0
for i in range (5000):
    actions.perform()
    count = int(cookie_count.text.split(" ")[0])
    #largestItem = items[0]
    maxRatio = 10000
    #print("limit antes", upperLimit)
    #try:
    
    #except:
        #continue
    #try:
        #driver.find_element_by_id("productPrice" + str(upperLimit+1))
        #print("Achou")
        #upperLimit = upperLimit + 1 
    #except:
        #print("N Achou")
        #pass
    items = [driver.find_element_by_id("productPrice" + str(j)) for j in range(10,-1,-1)]
    #print("limit depois", upperLimit)
    #print("len depois", len(items))
    for item in items:
        if(item.text != ''):
            value = int(item.text.replace(",",""))
            #print(value)
            if value <= count:
                upgrade_actions =ActionChains(driver)
                upgrade_actions.move_to_element(item)
                upgrade_actions.perform()

                try:
                    data = tooltip.find_element_by_class_name("data")
                    perMin = int(data.find_element_by_xpath("/b[0]").text)
                    print(perMin)
                    #time.sleep(0.5)
                except:
                    ActionChains(driver).click().perform()
                    


                
