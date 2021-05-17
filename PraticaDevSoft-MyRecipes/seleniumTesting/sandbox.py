from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.action_chains import ActionChains

PATH = "/home/joaomcouto/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("http://localhost:3000/recipes")
driver.maximize_window()

#print(driver.title) #Printa o titulo da pagina

#Com o get na pagina de recipes encontrar a caixa de filtro e escreve test e clica enter
#search = driver.find_element_by_id("filter") 
#search.send_keys("test")
#search.send_keys(Keys.RETURN)

#Encontra o MyRecipes no navbag e clica nele, dando refresh na pagina TRANSFERIDO
#search = driver.find_element_by_class_name("navbar-brand") 
#time.sleep(2)
#ActionChains(driver).click(search).perform()


#Clica em cadastro, preenche o form e submita #TRANSFERINDO
cadastrar = driver.find_element_by_xpath('//a[@href="/register"]')
time.sleep(2)
ActionChains(driver).click(cadastrar).perform()

name = driver.find_element_by_id("name") 
time.sleep(1)
name.send_keys("Marco Tulio")

email = driver.find_element_by_id("email") 
time.sleep(1)
email.send_keys("marcotulio@pds.teste")

password = driver.find_element_by_id("password") 
time.sleep(1)
password.send_keys("12345678")

passwordConfirmation = driver.find_element_by_id("passwordConfirmation") 
time.sleep(1)
passwordConfirmation.send_keys("12345678")

submit = driver.find_element_by_xpath('//button[text()="Cadastrar"]')
time.sleep(1)
ActionChains(driver).click(submit).perform()


#driver.implicity_wait(5) #Espera 5 segundos




#driver.back() #Volta pra pagina anterior
#driver.forward() #Volta pra pagina a frente

#driver.close()#Fecha aba

#element.clear() # Limpa o texto ja presente no elemento como em search bars


#time.sleep(5)
#driver.quit()  #Fecha browser todo

