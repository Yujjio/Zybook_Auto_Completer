from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


def login(browser):
    user_id = browser.find_element(By.ID, "ember9")
    user_id.clear()
    user = input("input your username(mail address): ").strip()
    user_id.send_keys(user)
    password_id = browser.find_element(By.ID, "ember11")
    password_id.clear()
    password = input("input your password: ").strip()
    password_id.send_keys(password)
    browser.find_element(By.CLASS_NAME, "signin-button").click()


def get_class(browser):
    classes = browser.find_elements(By.CLASS_NAME, "heading")
    print("----------")
    for x, y in enumerate(classes):
        if x == len(classes)-1:
            break
        print(str(x), ": ", y.text)
    print("----------")
    choose = int(input("input(0-" + str(len(classes)-2) + ") to choose the course: "))
    while choose < 0 or choose > len(classes)-2:
        print("invalid number")
        choose = int(input("input(0-" + str(len(classes) - 2) + ") to choose the course: "))
    browser.find_element(By.XPATH, "//div[@class='zybooks-container large']/a[" + str(choose+1) + "]").click()


def get_week(browser, action):
    xpath = "//ul[@class='table-of-contents-list fixed-header header-absent']/li"
    week = browser.find_elements(By.XPATH, xpath)
    choose = int(input("input week number(1-" + str(len(week)) + ") or -1 to quit: "))
    if choose == -1:
        return True
    while choose < 1 or choose > len(week):
        print("invalid number")
        choose = int(input("input week number(1-" + str(len(week)) + "): "))
    action.move_to_element(week[choose-1]).perform()
    week[choose-1].click()
    return False


def multiple_choice(browser, action):
    multi_choice = browser.find_elements(By.CLASS_NAME, "zb-radio-button")
    for x, y in enumerate(multi_choice):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()


def filling(browser, action):
    show_answer_list = browser.find_elements(By.CLASS_NAME, "show-answer-button")
    for x, y in enumerate(show_answer_list):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()
        time.sleep(0.1)
        y.click()
        time.sleep(0.1)
        # get answer
        answer = browser.find_elements(By.CLASS_NAME, "forfeit-answer")[x].text
        textarea = browser.find_elements(By.CLASS_NAME, "ember-text-area")[x]
        textarea.send_keys(answer)
        time.sleep(0.1)
        browser.find_elements(By.CLASS_NAME, "check-button")[x].click()
        time.sleep(0.5)


def video(browser, action):
    video_list = browser.find_elements(By.CLASS_NAME, "start-graphic")
    for x, y in enumerate(video_list):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()
        time.sleep(1)
        play_button = browser.find_elements(By.CLASS_NAME, "normalize-controls")[x]
        # judge whether this animation is finished or not
        while True:
            time.sleep(3)
            play_button_img = browser.find_elements(By.CLASS_NAME, "play-button")
            if len(play_button_img) <= x:  # animation is still processing
                continue
            else:
                play_button_img = play_button_img[x]
            judge_end = play_button_img.get_attribute("class").find("rotate-180")
            judge = play_button_img.get_attribute("class").find("bounce")
            if judge_end != -1:  # the animation has finished
                break
            if judge != -1:  # step finished
                play_button_img.click()


if __name__ == "__main__":
    browser = webdriver.Chrome()
    action = ActionChains(browser)
    browser.get('https://learn.zybooks.com/library')
    # log
    login(browser)
    time.sleep(3)
    # choose class
    get_class(browser)
    time.sleep(3)
    while True:
        # choose week
        quit_judge = get_week(browser, action)
        if quit_judge:
            break
        time.sleep(1)
        # get sections inside the week
        sections = browser.find_elements(By.CLASS_NAME, "section-title-link")
        for i, j in enumerate(sections):
            # get into each section
            action.move_to_element(j).perform()
            j.click()
            time.sleep(5)
            # multiple choice
            multiple_choice(browser, action)
            print("finished section " + str(i) + "'s multiple choice problem")
            # filling
            filling(browser, action)
            print("finished section " + str(i) + "'s filling problem")
            # video
            video(browser, action)
            print("finished section " + str(i) + "'s video problem")
            # back to the week page
            browser.back()
            print("finished section " + str(i) + "'s. Progress: " + str(i+1) + "/" + str(len(sections)))
            time.sleep(5)
