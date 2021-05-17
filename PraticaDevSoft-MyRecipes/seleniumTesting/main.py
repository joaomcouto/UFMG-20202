import unittest
unittest.TestLoader.sortTestMethodsUsing = None
from selenium import webdriver
import page
import time


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("/home/joaomcouto/chromedriver") 
        #self.driver.get("http://localhost:3000/recipes")
        self.driver.get("http://www.python.org")

    # def test_title(self):
    #     mainPage = page.MainPage(self.driver)
    #     assert mainPage.is_title_matches()
    #     mainPage.search_text_element = "pycon"
    #     mainPage.click_go_button()
    #     search_result_page = page.SearchResultPage(self.driver)
    #     assert search_result_page.is_results_found()


    def tearDown(self):
        self.driver.close()


#Testes Sprint 3 - João

class IndexPageRefresher(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("/home/joaomcouto/chromedriver") 
        self.driver.get("http://localhost:3000/")
        self.driver.maximize_window()

    def test_refreshing(self):
        indexPage = page.IndexPage(self.driver)
        #time.sleep(2)
        indexPage.click_refresher()

    def tearDown(self):
        self.driver.close()


class IndexPageTitle(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("/home/joaomcouto/chromedriver") 
        self.driver.get("http://localhost:3000/")
        self.driver.maximize_window()

    def test_title(self):
        indexPage = page.IndexPage(self.driver)
        #time.sleep(2)
        assert indexPage.assert_titles_matches()

    def tearDown(self):
        self.driver.close()



class registeringAndLoggingIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("/home/joaomcouto/chromedriver") 
        self.driver.get("http://localhost:3000/")
        self.driver.maximize_window()
    
    def test_1registering(self):
        indexPage = page.IndexPage(self.driver)
        indexPage.registerFromIndex()
        time.sleep(2)
        assert indexPage.assert_sucessfully_logged()


    def test_2login(self):
        indexPage = page.IndexPage(self.driver)
        indexPage.logInFromIndex()
        time.sleep(2)
        assert indexPage.assert_sucessfully_logged()

    def test_3recipe_creation(self):
        indexPage = page.IndexPage(self.driver)
        indexPage.logInFromIndex()
        indexPage.createRecipe()
        #time.sleep(2)
        assert indexPage.assert_recipe_creation()




    def tearDown(self):
        self.driver.close()

class loggingIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("/home/joaomcouto/chromedriver") 
        self.driver.get("http://localhost:3000/")
        self.driver.maximize_window()
    

    def tearDown(self):
        self.driver.close()






if __name__ == "__main__":
    unittest.main()