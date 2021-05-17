from selenium.webdriver.common.by import By


class MainPageLocators(object):
    GO_BUTTON = (By.ID, "submit")


class SearchResultPageLocators(object):
    pass

class indexPageLocators(object):
    REFRESHER = (By.CLASS_NAME, "navbar-brand")
    REGISTER = (By.XPATH, '//a[@href="/register"]')
    PROFILE = (By.XPATH, '//a[@href="/profile"]')
    LOGIN = (By.XPATH, '//a[@href="/login"]')
    RECEITAS = (By.ID,"recipes-dropdown")
    RECEITASNEW = (By.XPATH, '//a[@href="/recipes/new"]')
    VIEWALLRECIPES = (By.XPATH, '//a[@href="/recipes"]')
class registerPageLocators(object):
    NAME = (By.ID,"name")
    EMAIL =  (By.ID,"email")
    PASSWORD = (By.ID,"password")
    PASSWORDCONFIRMATION = (By.ID,"passwordConfirmation")
    SUBMIT = (By.XPATH, '//button[text()="Cadastrar"]')

class loginPageLocators(object):
    EMAIL =  (By.ID,"email")
    PASSWORD = (By.ID,"password")
    SUBMIT = (By.XPATH, '//button[text()="Entrar"]')

class recipeCreationPageLocators(object):
    NAME = (By.ID,"title")
    TIME = (By.ID,"time")
    PORTION = (By.ID,"servings")
    INGREDIENTS = (By.ID,"ingredients")
    PREPARO = (By.ID,"howTo")
    SUBMIT = (By.ID,"submit")

class recipesPageLocators(object):
    FIRSTRECIPE = (By.XPATH, '//a[@href="/recipe/1"]')
