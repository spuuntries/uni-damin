from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as webdriver
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
from uuid import uuid4
import json
import time
import os

load_dotenv()


def logger(str: str, processed_count: int):
    print(f"[{datetime.now()}] [{processed_count} processed] {str}")


yturl = "https://youtube.com"
logger("Scraping Youtube", 0)

res = {}
processed_count = 0
max_depth = 2

options = Options()
options.binary_location = (
    os.environ["BINARY"]
)
options.add_argument("-headless")
if "DATADIR" in os.environ:
    options.add_argument(f"--user-data-dir={os.environ["DATADIR"]}")  # Get this from chrome://version
options.add_argument("--profile-directory=Default")


def explore_videos(driver, video_urls, depth, max_depth):
    global processed_count

    if depth > max_depth:
        return

    for video_url in video_urls:
        driver.get(video_url)

        try:
            wait = WebDriverWait(driver, timeout=30)
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "yt-formatted-string.ytd-watch-metadata"))
            )

            logger(f"Extracting metadata for {video_url}", processed_count)
            parsed = BeautifulSoup(driver.page_source, features="html.parser")
            title = parsed.select_one("yt-formatted-string.ytd-watch-metadata").text  # So linter doesn't scream # type: ignore

            if title not in res:
                res[title] = {"title": title, "href": video_url}

                # Grab description
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
                    logger(f"({title}) description located.", processed_count)
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    res[title]["desc"] = parsed.select_one(
                        "#description-inline-expander span.yt-core-attributed-string"  # So linter doesn't scream # type: ignore
                    ).text  # So linter doesn't scream # type: ignore
                    logger(f"({title}) description extracted: {res[title]['desc'][:20]}...", processed_count)
                except:
                    logger(
                        f"({title}) failed to locate description, assuming empty or non-standard tagging, skipping.",
                        processed_count
                    )

                # Grab likes
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                ".YtLikeButtonViewModelHost .yt-spec-button-shape-next__button-text-content",
                            )
                        )
                    )
                    logger(f"({title}) likes located.", processed_count)
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    res[title]["likes"] = parsed.select_one(
                        ".YtLikeButtonViewModelHost .yt-spec-button-shape-next__button-text-content"  # So linter doesn't scream # type: ignore
                    ).text  # So linter doesn't scream # type: ignore
                    logger(f"({title}) likes extracted: : {res[title]['likes']}", processed_count)
                except:
                    logger(
                        f"({title}) failed to locate likes, assuming empty or non-standard tagging, skipping.",
                        processed_count
                    )

                # Grab duration
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                ".ytp-time-duration",
                            )
                        )
                    )
                    logger(f"({title}) duration located.", processed_count)
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    res[title]["duration"] = parsed.select_one(
                        ".ytp-time-duration"
                    ).text  # type: ignore
                    logger(f"({title}) duration extracted: {res[title]['duration']}", processed_count)
                except:
                    logger(
                        f"({title}) failed to locate duration, assuming empty or non-standard tagging, skipping.",
                        processed_count,
                    )

                # Grab channel
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                ".ytd-channel-name a",
                            )
                        )
                    )
                    logger(f"({title}) channel located.", processed_count)
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    res[title]["channelName"] = parsed.select_one(
                        ".ytd-channel-name a",
                    ).text  # type: ignore
                    logger(f"({title}) channel extracted: {res[title]['channelName']}", processed_count)
                except:
                    logger(
                        f"({title}) failed to locate channel, assuming empty or non-standard tagging, skipping.",
                        processed_count,
                    )

                # Grab sub count
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "#owner-sub-count",
                            )
                        )
                    )
                    logger(f"({title}) sub count located.", processed_count)
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    res[title]["subCount"] = parsed.select_one(
                        "#owner-sub-count"
                    ).text  # type: ignore
                    logger(f"({title}) sub count extracted: {res[title]['subCount']}", processed_count)
                except:
                    logger(
                        f"({title}) failed to locate sub count, assuming empty or non-standard tagging, skipping.",
                        processed_count,
                    )

                # Grab views and date
                try:
                    wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                ".ytd-watch-info-text #info",
                            )
                        )
                    )
                    logger(f"({title}) date & views located.", processed_count)
                    parsed = BeautifulSoup(driver.page_source, features="html.parser")

                    res[title]["dateAndViews"]  = parsed.select_one(".ytd-watch-info-text #info").text  # type: ignore
                    logger(f"({title}) date & views extracted: {res[title]['dateAndViews']}", processed_count)
                except:
                    logger(
                        f"({title}) failed to locate date & views count, assuming empty or non-standard tagging, skipping.",
                        processed_count,
                    )

                processed_count += 1

                # Extract related video URLs
                related_videos = parsed.select("a.ytd-compact-video-renderer")
                related_video_urls = [yturl + video["href"] for video in related_videos]  # So linter doesn't scream # type: ignore

                # Recursively explore related videos
                explore_videos(driver, related_video_urls, depth + 1, max_depth)

        except:
            logger(f"Failed to extract metadata for {video_url}", processed_count)
            driver.get_screenshot_as_file(f"fail_{len(list(filter(lambda x: 'fail' in x, os.listdir(os.getcwd())))) + 1}.png")


with webdriver.Chrome(options=options, version_main=127) as driver:
    try:
        driver.switch_to.new_window("windus")
        driver.get(yturl)
        logger("Opened YT", processed_count)

        try:
            wait = WebDriverWait(driver, timeout=30)
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a#video-title-link"))
            )

            logger("Titles rendered on page, parsing...", processed_count)
            parsed = BeautifulSoup(driver.page_source, features="html.parser")
            all_titles = parsed.select("a#video-title-link")

            initial_video_urls = [yturl + str(title["href"]) for title in all_titles]

            explore_videos(driver, initial_video_urls, 0, max_depth)

        except:
            driver.get_screenshot_as_file(f"fail_{len(list(filter(lambda x: 'fail' in x, os.listdir(os.getcwd())))) + 1}.png")
            raise LookupError("Element not found")

        with open(f"ytResults_{len(list(filter(lambda x: 'ytResults' in x, os.listdir(os.getcwd())))) + 1}_{uuid4()}.json", "w") as f:
            f.write(json.dumps(res))
            logger(f"In total, we extracted {len(res.keys())} video metadatas.", processed_count)

    except Exception as e:
        print(e)
