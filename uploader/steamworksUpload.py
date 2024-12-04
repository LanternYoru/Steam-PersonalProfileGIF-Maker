import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def load_cookies(driver, cookies_file):
    """从文件加载 cookies 并添加到浏览器。"""
    with open(cookies_file, 'r') as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    return cookies


def save_cookies(driver, cookies_file):
    """保存 cookies 到文件。"""
    cookies = driver.get_cookies()
    with open(cookies_file, 'w') as file:
        json.dump(cookies, file)


def setup_driver(headless=False):
    """初始化 WebDriver。"""
    options = Options()
    if headless:
        options.add_argument('--headless')
    return webdriver.Chrome(options=options)


def upload_files(driver, files, titles):
    """上传文件到目标页面。"""
    for index, file in enumerate(files):
        driver.execute_script(
            "$J('#ConsumerAppID').val(480);$J('[name=visibility]').val(0);$J('[name=file_type]').val(0);")
        title_input = driver.find_element(By.NAME, "title")
        title_input.send_keys(titles[index])
        file_input = driver.find_element(By.NAME, "file")
        file_input.send_keys(file)
        agree_terms = driver.find_element(By.NAME, "agree_terms")
        agree_terms.click()
        submit_button = driver.find_element(By.XPATH, "//a[@onclick='SubmitItem( false );']")
        submit_button.click()
        print(f"{titles[index]}上传成功")
        driver.get('https://steamcommunity.com/sharedfiles/edititem/767/3/')


def get_files_and_titles(uploading_folder, use_filenames):
    """获取文件路径和对应标题。"""
    files = [os.path.join(uploading_folder, f) for f in os.listdir(uploading_folder) if not f.startswith('.')][:-1]
    if use_filenames:
        titles = [os.path.splitext(os.path.basename(f))[0] for f in files]
    else:
        titles = [str(i + 1) for i in range(len(files))]
    return files, titles


def main():
    cookies_file = "./cookies.json"
    try:
        driver = setup_driver(headless=True)
        driver.get("https://steamcommunity.com/login/home/?goto=login")

        # 加载 cookies
        cookies = load_cookies(driver, cookies_file)
        print("已找到 cookies，按照 cookies 登录。")

        # 验证登录
        driver.refresh()
        steam_name = driver.find_element(By.CLASS_NAME, "actual_persona_name").text
        print(f"登录的 Steam 账号为 {steam_name}。输入 Y 继续，N 重新登录：")
        checking = input().strip().lower()
        if checking != 'y':
            raise FileNotFoundError

        # 转到上传页面
        driver = setup_driver()
        driver.get("https://steamcommunity.com/sharedfiles/edititem/767/3/")
        load_cookies(driver, cookies_file)
        print("进入 Steam 艺术作品上传页。")

        # 获取文件和标题
        uploading_folder = input("输入想要上传的文件夹路径：").strip()
        print("上传标题可以选择：\n(1) 用文件名命名\n(2) 按序号命名")
        title_choice = input("选择输入 1 或 2：").strip()
        use_filenames = title_choice == "1"
        files, titles = get_files_and_titles(uploading_folder, use_filenames)
        print(f"正在上传的文件是：{titles}")
        input("按下回车确认")
        # 上传文件
        upload_files(driver, files, titles)
        print("文件上传完成！")

    except FileNotFoundError:
        # 手动登录
        print("没有找到 cookies 文件，请自行登录。")
        driver = setup_driver()
        driver.get("https://steamcommunity.com/login/home/?goto=login")
        input("等待登录完成后按回车继续...")
        save_cookies(driver, cookies_file)
        print("Cookies 已保存，请重新运行程序。")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
