from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from base64 import urlsafe_b64decode
from datetime import datetime
from colorama import *
import asyncio, random, time, json, re, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Unich:
    def __init__(self) -> None:
        self.BASE_API = "https://api.unich.com/airdrop/user/v1"
        self.REF_CODE = "2CQMZB" # U can change it with yours.
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.sessions = {}
        self.ua_index = 0
        
        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/117.0.0.0"
        ]

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Unich {Fore.BLUE + Style.BRIGHT}Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_tokens(self):
        filename = "tokens.txt"
        try:
            with open(filename, 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
            return tokens
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Tokens: {e}{Style.RESET_ALL}")
            return None

    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"
    
    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
    
    def get_next_user_agent(self):
        ua = self.USER_AGENTS[self.ua_index]
        self.ua_index = (self.ua_index + 1) % len(self.USER_AGENTS)
        return ua
    
    def initialize_headers(self, token: str):
        if token not in self.HEADERS:
            self.HEADERS[token] = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                "Authorization": f"Bearer {token}",
                "Cache-Control": "no-cache",
                "Origin": "https://unich.com",
                "Pragma": "no-cache",
                "Referer": "https://unich.com",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": self.get_next_user_agent()
            }
        return self.HEADERS[token]
    
    async def get_session(self, token: str, proxy_url=None, timeout=60):
        if token not in self.sessions:
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            
            session = ClientSession(
                connector=connector,
                timeout=ClientTimeout(total=timeout)
            )
            
            self.sessions[token] = {
                'session': session,
                'proxy': proxy,
                'proxy_auth': proxy_auth
            }
        
        return self.sessions[token]
    
    async def close_session(self, token: str):
        if token in self.sessions:
            await self.sessions[token]['session'].close()
            del self.sessions[token]
    
    async def close_all_sessions(self):
        for token in list(self.sessions.keys()):
            await self.close_session(token)
        
    def decode_token(self, token: str):
        try:
            header, payload, signature = token.split(".")
            decoded_payload = urlsafe_b64decode(payload + "==").decode("utf-8")
            parsed_payload = json.loads(decoded_payload)
            signed_at = parsed_payload["signedAt"]
            
            return signed_at
        except Exception as e:
            return None
        
    def check_token_status(self, signed_time: int):
        try:
            exp_time = signed_time + 864000000

            current_time = int(time.time()) * 1000
            
            if current_time > exp_time:
                return False

            return True
        except Exception as e:
            return False
    
    def generate_random_username(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        
        username = []
        for _ in range(8 // 2):
            consonant = random.choice(consonants)
            vowel = random.choice(vowels)
            username.append(consonant)
            username.append(vowel)
        
        return '@' + ''.join(username)
    
    def mask_account(self, account):
        if '@' in account:
            local, domain = account.split('@', 1)
            hide_local = local[:3] + '*' * 3 + local[-3:]
            return f"{hide_local}@{domain}"

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate_proxy = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate_proxy in ["y", "n"]:
                    rotate_proxy = rotate_proxy == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return proxy_choice, rotate_proxy
    
    async def ensure_ok(self, response):
        if response.status >= 400:
            error_text = await response.text()
            raise Exception(f"HTTP {response.status}: {error_text}")
    
    async def check_connection(self, token: str, proxy_url=None):
        url = "https://api.ipify.org?format=json"

        try:
            session_info = await self.get_session(token, proxy_url, 15)
            session = session_info['session']
            proxy = session_info['proxy']
            proxy_auth = session_info['proxy_auth']
            
            async with session.get(
                url=url, proxy=proxy, proxy_auth=proxy_auth
            ) as response:
                await self.ensure_ok(response)
                return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
        
        return None
    
    async def my_info(self, token: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/info/my-info"
        
        for attempt in range(retries):
            try:
                session_info = await self.get_session(token, proxy_url)
                session = session_info['session']
                proxy = session_info['proxy']
                proxy_auth = session_info['proxy_auth']

                headers = self.initialize_headers(token)
                
                async with session.get(
                    url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth
                ) as response:
                    await self.ensure_ok(response)
                    result = await response.json()
                    return result
                    
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Account:{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed to Fetch Info {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def apply_ref(self, token: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/ref/refer-sign-up"
        payload = {"code": self.REF_CODE}
        
        for attempt in range(retries):
            try:
                session_info = await self.get_session(token, proxy_url)
                session = session_info['session']
                proxy = session_info['proxy']
                proxy_auth = session_info['proxy_auth']

                headers = self.initialize_headers(token)
                headers["Content-Type"] = "application/json"
                
                async with session.post(
                    url=url, headers=headers, json=payload, proxy=proxy, proxy_auth=proxy_auth
                ) as response:
                    if response.status == 400: return False
                    return True
                        
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Refer  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed to Apply Code {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def recent_mining(self, token: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/mining/recent"
        
        for attempt in range(retries):
            try:
                session_info = await self.get_session(token, proxy_url)
                session = session_info['session']
                proxy = session_info['proxy']
                proxy_auth = session_info['proxy_auth']

                headers = self.initialize_headers(token)
                
                async with session.get(
                    url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth
                ) as response:
                    await self.ensure_ok(response)
                    result = await response.json()
                    return result
                        
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed to Fetch Status {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def start_mining(self, token: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/mining/start"
        
        for attempt in range(retries):
            try:
                session_info = await self.get_session(token, proxy_url)
                session = session_info['session']
                proxy = session_info['proxy']
                proxy_auth = session_info['proxy_auth']

                headers = self.initialize_headers(token)
                
                async with session.post(
                    url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth
                ) as response:
                    await self.ensure_ok(response)
                    result = await response.json()
                    return result
                        
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed to Start {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def task_lists(self, token: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/social/list-by-user"
        
        for attempt in range(retries):
            try:
                session_info = await self.get_session(token, proxy_url)
                session = session_info['session']
                proxy = session_info['proxy']
                proxy_auth = session_info['proxy_auth']

                headers = self.initialize_headers(token)
                
                async with session.get(
                    url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth
                ) as response:
                    await self.ensure_ok(response)
                    result = await response.json()
                    return result
                        
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Tasks  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Failed to Fetch Available Tasks {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def complete_task(self, token: str, task_id: str, title: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/social/claim/{task_id}"
        payload = {"evidence": self.generate_random_username()}
        
        for attempt in range(retries):
            try:
                session_info = await self.get_session(token, proxy_url)
                session = session_info['session']
                proxy = session_info['proxy']
                proxy_auth = session_info['proxy_auth']

                headers = self.initialize_headers(token)
                headers["Content-Type"] = "application/json"
                
                async with session.post(
                    url=url, headers=headers, json=payload, proxy=proxy, proxy_auth=proxy_auth
                ) as response:
                    await self.ensure_ok(response)
                    result = await response.json()
                    return result
                        
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.GREEN+Style.BRIGHT}   {Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Not Completed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None

    async def process_check_connection(self, token: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(token) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(token, proxy)
            if is_valid: return True

            if rotate_proxy:
                await self.close_session(token)
                proxy = self.rotate_proxy_for_account(token)
                await asyncio.sleep(1)
                continue

            return False

    async def process_accounts(self, token: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(token, use_proxy, rotate_proxy)
        if is_valid:
            proxy = self.get_next_proxy_for_account(token) if use_proxy else None

            account = await self.my_info(token, proxy)
            if account:

                if account.get("code") == "OK":
                    email = account.get("data", {}).get("email")
                    balance = account.get("data", {}).get("mUn")

                    await self.apply_ref(token, proxy)

                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Account:{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {self.mask_account(email)} {Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Balance:{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {balance} FD Points {Style.RESET_ALL}"
                    )
                
                else:
                    err_msg = account.get("message")
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Account:{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Failed to Fetch Info {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )

            mining = await self.recent_mining(token, proxy)
            if mining:

                if mining.get("code") == "OK":
                    is_mining = mining.get("data", {}).get("isMining")

                    if not is_mining:
                        start = await self.start_mining(token, proxy)
                        if start:

                            if start.get("code") == "OK":
                                self.log(
                                    f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Started Successfully {Style.RESET_ALL}"
                                )

                            else:
                                err_msg = start.get("message")
                                self.log(
                                    f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Failed to Start {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                                )

                    else:
                        self.log(
                            f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Already Started {Style.RESET_ALL}"
                        )
                
                else:
                    err_msg = mining.get("message")
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Mining :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Failed to Fetch Status {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )

            task_lists = await self.task_lists(token, proxy)
            if task_lists:

                if task_lists.get("code") == "OK":
                    self.log(f"{Fore.CYAN+Style.BRIGHT}Tasks  :{Style.RESET_ALL}")

                    tasks = task_lists.get("data", {}).get("items", [])
                    for task in tasks:
                        task_id = task.get("id")
                        title = task.get("title")
                        reward = task.get("pointReward")
                        is_claimed = task.get("claimed")

                        if is_claimed:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}   {Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Already Completed {Style.RESET_ALL}"
                            )
                            continue

                        complete = await self.complete_task(token, task_id, title, proxy)
                        if complete:

                            if complete.get("code") == "OK":
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}   {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{reward} FD Points{Style.RESET_ALL}"
                                )
                            else:
                                err_msg = complete.get("message")
                                self.log(
                                    f"{Fore.GREEN+Style.BRIGHT}   {Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT}{title}{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Not Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                                )
                else:
                    err_msg = task_lists.get("message")
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Tasks  :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Failed to Fetch Available Tasks {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} {err_msg} {Style.RESET_ALL}"
                    )
            
    async def main(self):
        try:
            tokens = self.load_tokens()
            if not tokens: return

            proxy_choice, rotate_proxy = self.print_question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
                )

                use_proxy = True if proxy_choice == 1 else False
                if use_proxy: self.load_proxies()

                separator = "=" * 25
                for idx, token in enumerate(tokens, start=1):
                    if token:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {len(tokens)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        signed_time = self.decode_token(token)
                        if not signed_time:
                            self.log(
                                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Invalid Token Data {Style.RESET_ALL}"
                            )
                            continue

                        is_valid = self.check_token_status(signed_time)
                        if not is_valid:
                            self.log(
                                f"{Fore.CYAN+Style.BRIGHT}Status :{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Token Already Expired {Style.RESET_ALL}"
                            )
                            continue
                        
                        await self.process_accounts(token, use_proxy, rotate_proxy)
                        await asyncio.sleep(random.uniform(2.0, 3.0))

                await self.close_all_sessions()

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                
                delay = 12 * 60 * 60
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e
        finally:
            await self.close_all_sessions()

if __name__ == "__main__":
    try:
        bot = Unich()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Unich - BOT{Style.RESET_ALL}                                       "                              
        )