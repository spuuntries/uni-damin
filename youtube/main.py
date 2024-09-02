import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from uuid import uuid4
import undetected_chromedriver as webdriver

load_dotenv()


def logger(str: str):
    print(f"[{datetime.now()}] {str}")


yturl = "https://youtube.com"
logger("Scraping Youtube")

res = {}

options = Options()
options.binary_location = (
    os.environ["BINARY"]
)
options.add_argument("-headless")
if "DATADIR" in os.environ: 
    options.add_argument(f"--user-data-dir={os.environ["DATADIR"]}") # Get this from chrome://version
options.add_argument("--profile-directory=Default")

with webdriver.Chrome(options=options, version_main=127) as driver:
    try:
        driver.switch_to.new_window("windus")
        driver.get(yturl)
        logger("Opened YT")
        try:
            wait = WebDriverWait(driver, timeout=30)
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a#video-title-link"))
            )

            last_height = driver.execute_script("return document.body.scrollHeight")
            for _ in range(5):
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
                # Wait to load page
                time.sleep(2)
    
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height


            logger("Titles rendered on page, parsing...")
            parsed = BeautifulSoup(driver.page_source, features="html.parser")
            all_titles = parsed.select("a#video-title-link")

            for title in all_titles:
                if title.text not in res:
                    res[title.text] = {"title": title.text, "href": yturl + str(title["href"])}

            for video in res.values():
                to_visit = video["href"]
                logger(f"Visiting {to_visit} ({video["title"]})")
                driver.get(to_visit)

                # NOTE: Grabbing desc
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "#expand",
                            )
                        )
                    )
                    expand_button = driver.find_element(By.CSS_SELECTOR, "#expand")
                    expand_button.click()

                    wait.until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                "#description-inline-expander span.yt-core-attributed-string",
                            )
                        )
                    )
                    logger(f"({video["title"]}) description located.")
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    video["desc"] = parsed.select_one(
                        "#description-inline-expander span.yt-core-attributed-string"  # So linter doesn't scream # type: ignore
                    ).text  # So linter doesn't scream # type: ignore
                    logger(f"({video["title"]}) description extracted.")
                except:
                    logger(
                        f"({video["title"]}) failed to locate description, assuming empty or non-standard tagging, skipping."
                    )

                # NOTE: Grabbing likes
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                ".YtLikeButtonViewModelHost .yt-spec-button-shape-next__button-text-content",
                            )
                        )
                    )
                    logger(f"({video["title"]}) likes located.")
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    video["likes"] = parsed.select_one(
                        ".YtLikeButtonViewModelHost .yt-spec-button-shape-next__button-text-content"  # So linter doesn't scream # type: ignore
                    ).text  # So linter doesn't scream # type: ignore
                    logger(f"({video["title"]}) likes extracted.")
                except:
                    logger(
                        f"({video["title"]}) failed to locate likes, assuming empty or non-standard tagging, skipping."
                    )                              
        except:
            # NOTE: If fail, we grab a screenshot for debugging
            driver.get_screenshot_as_file(f"fail_{len(list(filter(lambda x: "fail" in x, os.listdir(os.getcwd())))) + 1}.png") 
            raise LookupError("Element not found")
            
        with open(f"ytResults_{len(list(filter(lambda x: "ytResults" in x, os.listdir(os.getcwd())))) + 1}_{uuid4()}.json", "w") as f:
                    f.write(json.dumps(res))
                    logger(f"In total, we extracted {len(res.keys())} video metadatas.")
    except Exception as e:
        print(e)

