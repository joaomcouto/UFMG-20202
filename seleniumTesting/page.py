from locator import *
from element import BasePageElement
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.action_chains import ActionChains

class SearchTextElement(BasePageElement):
    locator = "q"

class BasePage(object):
    def __init__(self,driver):
        self.driver = driver

class MainPage(BasePage):
    search_text_element = SearchTextElement()

    def is_title_matches(self):
        return "Python" in self.driver.title
        #return "MyRecipes" in self.driver.title

    def click_go_button(self):
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()

class SearchResultPage(BasePage):
    def is_results_found(self):
        return "No results found." not in self.driver.page_source

class IndexPage(BasePage):
    def click_refresher(self):
        element = self.driver.find_element(*indexPageLocators.REFRESHER)
        element.click()

    def assert_titles_matches(self):
        element = self.driver.title
        return "MyRecipes" in element

    def registerFromIndex(self):
       #cadastrar = driver.find_element_by_xpath('//a[@href="/register"]')
        cadastrar = self.driver.find_element(*indexPageLocators.REGISTER)
        #self.driver.implicitly_wait(6000) 
        time.sleep(0.3)
        ActionChains(self.driver).click(cadastrar).perform()

        name = self.driver.find_element(*registerPageLocators.NAME)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        name.send_keys("Marco Tulio")

        email = self.driver.find_element(*registerPageLocators.EMAIL)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        email.send_keys("marcotulio2@pds.teste")

        password = self.driver.find_element(*registerPageLocators.PASSWORD)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        password.send_keys("12345678")

        passwordConfirmation = self.driver.find_element(*registerPageLocators.PASSWORDCONFIRMATION)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        passwordConfirmation.send_keys("12345678")

        submit = self.driver.find_element(*registerPageLocators.SUBMIT)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        ActionChains(self.driver).click(submit).perform()


    def assert_sucessfully_logged(self):
        profileName = self.driver.find_element(*indexPageLocators.PROFILE)
        return "Marco Tulio" in profileName.text

    def logInFromIndex(self):
        login = self.driver.find_element(*indexPageLocators.LOGIN)
        time.sleep(0.3)
        ActionChains(self.driver).click(login).perform()

        email = self.driver.find_element(*loginPageLocators.EMAIL)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        email.send_keys("marcotulio2@pds.teste")

        password = self.driver.find_element(*loginPageLocators.PASSWORD)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        password.send_keys("12345678")

        submit = self.driver.find_element(*loginPageLocators.SUBMIT)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        ActionChains(self.driver).click(submit).perform()

    def createRecipe(self):
        receitasDropdown = self.driver.find_element(*indexPageLocators.RECEITAS)
        time.sleep(0.3)
        ActionChains(self.driver).click(receitasDropdown).perform()

        receitasNew = self.driver.find_element(*indexPageLocators.RECEITASNEW)
        time.sleep(0.3)
        ActionChains(self.driver).click(receitasNew).perform()

        name = self.driver.find_element(*recipeCreationPageLocators.NAME)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        name.send_keys("Ovos fritos")

        tempo = self.driver.find_element(*recipeCreationPageLocators.TIME)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        tempo.send_keys("5")

        porcao = self.driver.find_element(*recipeCreationPageLocators.PORTION)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        porcao.send_keys("3")

        porcao = self.driver.find_element(*recipeCreationPageLocators.INGREDIENTS)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        porcao.send_keys("3 ovos")

        preparo = self.driver.find_element(*recipeCreationPageLocators.PREPARO)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        preparo.send_keys("Frita os ovos")

        submit = self.driver.find_element(*recipeCreationPageLocators.SUBMIT)
        #self.driver.implicitly_wait(1) 
        time.sleep(0.3)
        ActionChains(self.driver).click(submit).perform()

    def assert_recipe_creation(self):
        receitasDropdown = self.driver.find_element(*indexPageLocators.RECEITAS)
        time.sleep(0.3)
        ActionChains(self.driver).click(receitasDropdown).perform()

        receitasAll = self.driver.find_element(*indexPageLocators.VIEWALLRECIPES)
        time.sleep(0.3)
        ActionChains(self.driver).click(receitasAll).perform()

        time.sleep(2)
        try:
            firstRecipe = self.driver.find_element(*recipesPageLocators.FIRSTRECIPE)
            print("Achou")
            return True
        except:
            print("Não achou")
            return False
        #time.sleep(0.3)
        #ActionChains(self.driver).click(firstRecipe).perform()
        






