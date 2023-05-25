from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get('https://blogdosvinhos.com.br/category/harmonizacao/')

# Encontre todos os links para os posts
link_elements = driver.find_elements(By.CLASS_NAME, "grid-title")
links = [elem.find_element(By.TAG_NAME, 'a').get_attribute("href") for elem in link_elements]

# Para cada link, navegue até a página e imprima o conteúdo do post
content = []
for link in links:
    driver.get(link)

    # Aguarde um pouco para garantir que a página seja carregada completamente
    time.sleep(3)

    post_content = driver.find_element(By.CLASS_NAME, 'inner-post-entry')
    content.append(post_content.text)

driver.quit()

# Salvando o conteúdo em um arquivo
with open('blogdosvinhos.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(content))