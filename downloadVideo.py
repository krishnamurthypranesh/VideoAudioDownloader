# import modules================================================================
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
# get the links of the videos that need to be downloaded========================

# get input html file from the user
html_file_directory = input("Enter the path to the html file: ")
# parse page
contentSoup = bs4.BeautifulSoup(open(html_file_directory), "html.parser")

# getting the links of the videos from the playlist
videos = contentSoup.find_all(
            "a",
            class_= "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
            )

# extracting the links from the videos
links = [i.get("href") for i in videos]

# download the required files===================================================
browser = webdriver.Chrome(executable_path = "./chromedriver")

# function to download the file-------------------------------------------------
def downloadVideo(url): # function to download videos

    # site to download audio from
    browser.get("https://www.onlinevideoconverter.com/mp3-converter")
    browser.set_window_size(900, 900) # setting the browser window size
    browser.set_window_position(0, 0) # setting the browser position window
    # pasting url to convert
    browser.find_element_by_id("texturl").send_keys(url)
    time.sleep(5)
    # initiating conversion
    browser.find_element_by_id("texturl").send_keys(Keys.RETURN)
    time.sleep(20)
    # initiating download
    browser.find_element_by_id("downloadq").click()
    # closing any opened tabs
    if len(browser.window_handles) > 1:
        browser.switch_to_window(browser.window_handles[1])
        browser.close()
        # switching focus back to original window
        browser.switch_to_window(browser.window_handles[0])
    time.sleep(90)

# downloading videos in links---------------------------------------------------
try:
    for i in range(len(links)):
        print("Downloaded video " + str(i + 1)) # message to indicate video download
        downloadVideo(links[i])
except Exception as err: # catching errors
    print("An error occured! Error Code: \n" + str(err))
    print("Closing the browser! and terminating all operations")
    try: # writing errors raised to file
        # appending to file
        with open("errors.txt", "a") as errors:
            current_time = str(datetime.datetime.now())
            print("The following error occured while downloading video " +
            str(i + 1) + "\n" + "Error Code: " + str(err) + "at: " +
            current_time, file = errors)
    except Exception as tryErr:
        print(str(tryErr))
finally:
    browser.close()
