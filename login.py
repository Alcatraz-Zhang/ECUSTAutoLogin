import sys
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


def print_with_timestamp(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{timestamp}] : {message}")

class NetworkAutoReconnect:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.username = config['username']
        self.password = config['password']
        self.login_url = config['login_url']
        self.geckodriver_path = config['geckodriver_path']
        self.retry_time = config['retry_time']
        self.max_retry = config['max_retry']
        self.speed = config['speed']
        self.driver = None

    @staticmethod
    def check_connection():
        try:
            response = requests.get("http://www.baidu.com", timeout=5, allow_redirects=False)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def login(self):
        if self.driver is None:
            firefox_options = Options()
            firefox_options.add_argument("-headless")
            service = Service(self.geckodriver_path)
            self.driver = webdriver.Firefox(service=service, options=firefox_options)

        try:
            self.driver.get(self.login_url)

            # 输入用户名和密码
            username_input = WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, "username"))
            )
            username_input.send_keys(self.username)

            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(self.password)

            # 选择速度选项
            if self.speed == "25M":
                speed_option = self.driver.find_element(By.CSS_SELECTOR, "input[id='toll'][value='']")
                speed_option.click()
            else:
                speed_option = self.driver.find_element(By.CSS_SELECTOR, "input[id='toll'][value='@free']")
                speed_option.click()

            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[id='login'][class='btn-login']")
            login_button.click()

            time.sleep(5)

        except Exception as e:
            print_with_timestamp(f"登录过程中出现错误: {e}")
            if self.driver:
                self.driver.quit()
                self.driver = None

    def run(self):
        retry_count = 0
        print_with_timestamp("校园网自动重连脚本正在运行...")
        while True:
            if not self.check_connection():
                print_with_timestamp("检测到网络断开，尝试重新登录...")
                self.login()
                if self.check_connection():
                    print_with_timestamp("重新连接成功!")
                else:
                    if self.max_retry > 0:
                        if retry_count < self.max_retry:
                            retry_count += 1
                            print_with_timestamp(f"重新连接失败，30s后进行第{retry_count}次重试...")
                            time.sleep(30)
                        else:
                            print_with_timestamp(f"重试次数已达上限{self.max_retry}次，退出脚本...")
                            sys.exit(1)
                    else:
                        print_with_timestamp("重试次数未设置，将持续尝试重连...")
                        time.sleep(30)
            else:
                print_with_timestamp("网络连接正常...")
                time.sleep(self.retry_time)  # 每retry_time检查一次网络状态


if __name__ == "__main__":
    reconnector = NetworkAutoReconnect('config.json')
    reconnector.run()