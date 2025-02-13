from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrap_book_info(url: str) -> dict:
    """
    Scrapes book information from the given Amazon product page URL.

    Parameters:
    url (str): The URL of the Amazon product page.

    Returns:
    dict: A dictionary containing the book's ASIN, title, and price.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)

        # Título
        try:
            title_element = driver.find_element(By.ID, 'productTitle')
            title = title_element.text
        except NoSuchElementException:
            title = 'Erro título'

        # Preço
        try:
            price_whole_element = driver.find_element(By.CLASS_NAME, 'a-price-whole')
            price_fraction_element = driver.find_element(By.CLASS_NAME, 'a-price-fraction')
            price = f"{price_whole_element.text},{price_fraction_element.text}"
        except NoSuchElementException:
            price = 'Erro preço'

        # Escritor
        try:
            writer_element = driver.find_element(By.XPATH, "//span[@class='author notFaded'][1]/a")
            writer = writer_element.text
        except NoSuchElementException:
            writer = 'Erro escritor'

        # Resumo
        try:
            leia_mais_element = driver.find_element(By.XPATH, "//*[@class='a-expander-prompt'][contains(text(), 'Leia mais')]")
            if leia_mais_element.is_displayed():
                leia_mais_element.click()
            resume_element = driver.find_element(By.ID, 'bookDescription_feature_div')
            resume = resume_element.text
        except NoSuchElementException:
            resume = 'Erro resumo'
        

        # ASIN ou ISBN-10 (número de identificação do produto)
        try:
            asin_element = driver.find_element(By.XPATH, "//span[@class='a-list-item' and contains (.,'ASIN')]//span[2]")
            asin = asin_element.text
        except NoSuchElementException:
            try:
                isbn_element = driver.find_element(By.XPATH, "//span[@class='a-list-item' and contains (.,'ISBN-10')]//span[2]")
                asin = isbn_element.text
            except NoSuchElementException:
                asin = 'Erro ASIN/ISBN-10'

    return {'asin': asin, 'title': title, 'price': price, 'writer': writer, 'resume': resume}

def get_book_info(url: str) -> dict:
    """
    Generates an Amazon affiliate link for the given product page URL.

    Parameters:
    url (str): The URL of the Amazon product page.

    Returns:
    str: The Amazon affiliate link.
    """
    info = scrap_book_info(url)
    clean_url = f"https://www.amazon.com.br/dp/{info['asin']}?tag=biancaperei0d-20"
    return {'asin': info['asin'], 'title': info['title'], 'price': info['price'], 'writer': info['writer'], 'resume': info['resume'], 'clean_url': clean_url}
