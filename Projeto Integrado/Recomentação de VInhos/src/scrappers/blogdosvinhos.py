from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contextlib import closing


class BlogPostScraper:

    def __init__(self, base_url, num_pages):
        self.base_url = base_url
        self.num_pages = num_pages
        self.links = []
        self.contents = []
        self.driver = None

    def collect_post_links(self):
        for i in range(1, self.num_pages + 1):
            page_url = f"{self.base_url}/page/{i}/" if i > 1 else self.base_url
            self.driver.get(page_url)
            link_elements = self.driver.find_elements(By.CLASS_NAME, "grid-title")
            self.links.extend([elem.find_element(By.TAG_NAME, 'a').get_attribute("href") for elem in link_elements])

    def collect_post_contents(self):
        for link in self.links:
            self.driver.get(link)
            wait = WebDriverWait(self.driver, 10)
            post_content = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'inner-post-entry')))
            self.contents.append(post_content.text)

    def save_contents_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(self.contents))

    def scrape(self):
        with closing(webdriver.Chrome()) as self.driver:
            self.collect_post_links()
            self.collect_post_contents()

# Uso da classe
scraper = BlogPostScraper('https://blogdosvinhos.com.br/category/harmonizacao/', num_pages=5)
scraper.scrape()
scraper.save_contents_to_file('blogdosvinhos.txt')
