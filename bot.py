from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from colorama import *
from datetime import datetime
from fake_useragent import FakeUserAgent
import asyncio, json, random, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Unich:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://unich.com",
            "Referer": "https://unich.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }

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
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Unich - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def mask_account(self, account):
        if '@' in account:
            local, domain = account.split('@', 1)
            hide_local = local[:3] + '*' * 3 + local[-3:]
            return f"{hide_local}@{domain}"
        
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account
    
    def generate_random_username(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        username = []
        for _ in range(8 // 2):
            username.append(random.choice(consonants))
            username.append(random.choice(vowels))
        return '@' + ''.join(username)
    
    def print_message(self, action, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}{action}{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
        )
    
    async def get_proxy_ip(self, proxy: str):
        """Fetches the public IP (as seen by ip-api.com) when using the given proxy."""
        url = "http://ip-api.com/json"
        try:
            async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                async with session.get(url=url, proxy=proxy) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("query", "Unknown")
        except Exception:
            return "Unknown"
    
    async def user_info(self, token: str, proxy: str, retries=5):
        url = "https://api.unich.com/airdrop/user/v1/info/my-info"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy) as response:
                        if response.status == 401:
                            return self.print_message("Account   :", Fore.WHITE, 
                                f"{self.mask_account(token)}"
                                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Access Token Expired{Style.RESET_ALL}"
                            )
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError):
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message("Account   :", Fore.WHITE, 
                    f"{self.mask_account(token)}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Data Is None{Style.RESET_ALL}"
                )
    
    async def user_confirm(self, token: str, proxy: str):
        url = "https://api.unich.com/airdrop/user/v1/ref/refer-sign-up"
        data = json.dumps({"code":"2CQMZB"})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                async with session.post(url=url, headers=headers, data=data, proxy=proxy) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError):
            return None
    
    async def mining_recent(self, token: str, proxy: str, retries=5):
        url = "https://api.unich.com/airdrop/user/v1/mining/recent"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy) as response:
                        if response.status == 401:
                            return self.print_message("Mining    :", Fore.RED, "Access Token Expired")
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError):
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def start_mining(self, token: str, proxy: str, retries=5):
        url = "https://api.unich.com/airdrop/user/v1/mining/start"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "0",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.post(url=url, headers=headers, proxy=proxy) as response:
                        if response.status == 401:
                            return self.print_message("Mining    :", Fore.RED, "Not Started"
                                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Access Token Expired{Style.RESET_ALL}"
                            )
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError):
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message("Mining    :", Fore.RED, "Not Started")
            
    async def task_lists(self, token: str, proxy: str, retries=5):
        url = "https://api.unich.com/airdrop/user/v1/social/list-by-user"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy) as response:
                        if response.status == 401:
                            return self.print_message("Task Lists:", Fore.RED, "Access Token Expired")
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['items']
            except (Exception, ClientResponseError):
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
    
    async def claim_tasks(self, token: str, quest_id: str, title: str, proxy: str, retries=5):
        url = f"https://api.unich.com/airdrop/user/v1/social/claim/{quest_id}"
        data = json.dumps({"evidence": self.generate_random_username()})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy) as response:
                        if response.status == 401:
                            return self.print_message("     > ", Fore.WHITE, f"{title}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Access Token Expired {Style.RESET_ALL}"
                            )
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError):
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message("     > ", Fore.WHITE, f"{title}"
                    f"{Fore.RED + Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                )
    
    async def process_accounts(self, token: str, proxy: str):
        user = await self.user_info(token, proxy)
        if not user:
            return

        # Fetch and display the proxy IP
        if proxy:
            proxy_ip = await self.get_proxy_ip(proxy)
        else:
            proxy_ip = "No Proxy"
        self.print_message("Ip used   :", Fore.WHITE, f"{proxy_ip}")

        await self.user_confirm(token, proxy)
        
        name = user['email']
        balance = user['mUn']

        self.print_message("Account   :", Fore.WHITE, f"{self.mask_account(name)}")
        self.print_message("Balance   :", Fore.WHITE, f"{balance} FD Points")

        mining = await self.mining_recent(token, proxy)
        if mining:
            reward = mining['miningDailyReward']
            is_mining = mining['isMining']

            if not is_mining:
                start = await self.start_mining(token, proxy)
                if start and start.get("code") == "OK":
                    self.print_message("Mining    :", Fore.GREEN, "Is Started"
                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {reward} FD Points {Style.RESET_ALL}"
                    )
            else:
                self.print_message("Mining    :", Fore.YELLOW, "Already Started")
        else:
            self.print_message("Mining    :", Fore.RED, "Data Is None")

        tasks = await self.task_lists(token, proxy)
        if tasks:
            self.print_message("Task Lists:", Fore.GREEN, f"Available {len(tasks)} Tasks")
            for task in tasks:
                if task:
                    task_id = task['id']
                    title = task['title']
                    reward = task['pointReward']
                    is_claimed = task['claimed']

                    if is_claimed:
                        self.print_message("     > ", Fore.WHITE, f"{title}"
                            f"{Fore.YELLOW + Style.BRIGHT} Already Claimed {Style.RESET_ALL}"
                        )
                        continue

                    claim = await self.claim_tasks(token, task_id, title, proxy)
                    if claim and claim.get("code") == "OK":
                        self.print_message("     > ", Fore.WHITE, f"{title}"
                            f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT} Reward {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{reward} FD Points{Style.RESET_ALL}"
                        )

    async def main(self):
        try:
            with open('tokens.txt', 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
            
            with open('proxy.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}=" * 60)
                
                for i, token in enumerate(tokens):
                    if token:
                        # Use corresponding proxy for each account (cycle if needed)
                        proxy = proxies[i % len(proxies)] if proxies else None
                        await self.process_accounts(token, proxy)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}=" * 60)
                        await asyncio.sleep(3)

                seconds = 12 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError as e:
            if 'tokens.txt' in str(e):
                self.log(f"{Fore.RED}File 'tokens.txt' Not Found.{Style.RESET_ALL}")
            elif 'proxy.txt' in str(e):
                self.log(f"{Fore.RED}File 'proxy.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

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
