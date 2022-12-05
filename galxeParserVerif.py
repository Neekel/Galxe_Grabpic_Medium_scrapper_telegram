from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
from aiogram import Bot, types
import asyncio

config = json.load(open('config.json','r'))
API_TOKEN = config['bot_token']
CHANNEL_ID = config['channel_id']

# useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument("--headless")

try:
    url = "https://galxe.com/campaigns"
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url=url)
    time.sleep(3)

    button = driver.find_element(By.CLASS_NAME, "sort-button").click()
    time.sleep(2)
    newest_button = driver.find_element(By.CLASS_NAME, "v-list-item__title").click()
    time.sleep(2)

    with open("galxe.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open("galxe.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    project_cards = soup.find_all(class_="card clickable")
    print(len(project_cards))

    project_link = []

    with open("galxe_link.txt", "r", encoding="utf-8") as file:
        all_links = file.read()

    for item in project_cards:
        link = "https://galxe.com" + item.find("a").get("href")

        if link in all_links:
            print("Already exist> " + link)
            break
        else:
            print("New" + link)
            project_link.append(link)

    new_project_dict = {}

    for item in project_link:

        url = item
        s = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=s, options=options)
        driver.get(url=url)
        time.sleep(3)

        with open("galxe.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open("galxe.html", "r", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        print("check >>  " + url)
        # check_icon = src.find(class_="check-icon")
        # print(check_icon)

        if src.find("defs") != -1:
            print(src.find("defs"))
            print('find data')
            title = soup.find(class_="flex-box flex-justify-between word-break-word").text
            title = title.replace("\n  ", "")
            print("Title " + title)
            #content = soup.find(class_="content").text
            minted = soup.find(class_="mr-6").text
            print("Minted " + minted)
            try:
                deadline = soup.find(class_="flex-fixed mr-15 mb-8 width-max-100").find(class_="text-16-bold").text
                deadline = deadline.replace("\n", "")
                deadline = deadline.strip()
                print("Deadline " + deadline)
                new_project_dict[url] = title, minted, deadline
                print(new_project_dict[url])

                with open('projects.json', 'w', encoding="utf-8") as file:
                    json.dump(new_project_dict, file, indent=4, ensure_ascii=False)

                with open("project_link.txt", "a", encoding="utf-8") as file:
                    file.write(url + '\n')

                print('start posting telegram')

                text_message_GAL = (f'#GALXE\n🔸<b>{title}</b>▪️{item}\n▪️{deadline}\n▪️{minted}')

            except Exception as ex:
                print(ex)
                new_project_dict[url] = title, minted
                print(new_project_dict[url])

                with open("galxe_link.txt", "a", encoding="utf-8") as file:
                    file.write(url + '\n')

                print('start posting telegram')

                text_message_GAL = (f'#GALXE\n🔸<b>{title}</b>▪️{item}\n▪️{minted}')

            bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

            async def send_message(channel_id: int, text: str):
                await bot.send_message(channel_id, text)

            async def main():
                await send_message(CHANNEL_ID, text_message_GAL)

            if __name__ == '__main__':
                asyncio.run(main())

        else:
            print("Not Verified, next")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

