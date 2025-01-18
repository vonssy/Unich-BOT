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
    
    def hide_account(self, account):
        if '@' in account:
            local, domain = account.split('@', 1)
            hide_local = local[:3] + '*' * 3 + local[-3:]
            return f"{hide_local}@{domain}"
        
        hide_account = account[:3] + '*' * 3 + account[-3:]
        return hide_account
    
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
    
    async def user_info(self, token: str):
        url = "https://api.unich.com/airdrop/user/v1/info/my-info"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['data']
        except (Exception, ClientResponseError) as e:
            return None
    
    async def user_confirm(self, token: str):
        url = "https://api.unich.com/airdrop/user/v1/ref/refer-sign-up"
        data = json.dumps({"code":"2CQMZB"})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            return None
    
    async def task_lists(self, token: str):
        url = "https://api.unich.com/airdrop/user/v1/social/list-by-user"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['data']['items']
        except (Exception, ClientResponseError) as e:
            return None
    
    async def claim_tasks(self, token: str, quest_id: str):
        url = f"https://api.unich.com/airdrop/user/v1/social/claim/{quest_id}"
        data = json.dumps({"evidence":self.generate_random_username()})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            return None
    
    async def mining_recent(self, token: str):
        url = "https://api.unich.com/airdrop/user/v1/mining/recent"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['data']
        except (Exception, ClientResponseError) as e:
            return None
    
    async def start_mining(self, token: str):
        url = "https://api.unich.com/airdrop/user/v1/mining/start"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "0",
            "Content-Type": "application/json"
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                async with session.post(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            return None
    
    async def process_accounts(self, token: str):
        user = await self.user_info(token)
        if not user:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {self.hide_account(token)} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}Data Is None{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            return

        email = user['email']
        self.log(
            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.hide_account(email)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {user['mUn']} FD Points {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
        )
        await asyncio.sleep(1)

        await self.user_confirm(token)

        tasks = await self.task_lists(token)
        if tasks:
            completed = False
            for task in tasks:
                task_id = task['id']
                is_claimed = task['claimed']

                if task and not is_claimed:
                    claim = await self.claim_tasks(token, task_id)
                    if claim and claim.get("code") == "OK":
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {task['pointReward']} FD Points {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )

                else:
                    completed = True

            if completed:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
        else:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Task{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
            )

        mining = await self.mining_recent(token)
        if mining:
            is_mining = mining['isMining']
            if not is_mining:
                start = await self.start_mining(token)
                if start and start.get("code") == "OK":
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {task['pointReward']} FD Points {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Is Already Started {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
        else:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )

    async def main(self):
        try:
            with open('tokens.txt', 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
            
            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                
                for token in tokens:
                    token = token.strip()
                    if token:
                        await self.process_accounts(token)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        await asyncio.sleep(3)

                seconds = 86400
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

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'tokens.txt' Not Found.{Style.RESET_ALL}")
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