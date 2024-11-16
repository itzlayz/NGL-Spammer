import aiohttp
import asyncio
import random

import uuid

from tqdm.asyncio import tqdm

URL = "https://ngl.link/api/submit"

try:
    with open("proxies.txt") as file:
        proxies = set(line.strip() for line in file.readlines())
except FileNotFoundError:
    proxies = set()

try:
    with open("questions.txt") as file:
        questions = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    questions = []


def get_proxy():
    if not proxies:
        return None
    return proxies.pop()


async def send_questions(username: str, question: str, amount: int):
    if not question and not questions:
        print("No questions found")
        exit()

    async with aiohttp.ClientSession() as session:
        for _ in tqdm(range(amount), desc="Sending questions"):
            proxy = get_proxy()
            if proxy:
                proxy_url = f"http://{proxy}"
            else:
                proxy_url = None

            try:
                async with session.post(
                    URL,
                    data={
                        "username": username,
                        "question": question or random.choice(questions),
                        "deviceId": str(uuid.uuid4()),
                        "gameSlug": "",
                        "referrer": "https://l.instagram.com/",
                    },
                    proxy=proxy_url,
                ) as response:
                    try:
                        await response.json()
                    except Exception:
                        await asyncio.sleep(1)

            except aiohttp.ClientError:
                print(f"Bad request ({proxy})")


async def main():
    print(
        r"""
  _   _  _____ _         _____ _____        __  __ __  __ ______ _____  
 | \ | |/ ____| |       / ____|  __ \ /\   |  \/  |  \/  |  ____|  __ \ 
 |  \| | |  __| |      | (___ | |__) /  \  | \  / | \  / | |__  | |__) |
 | . ` | | |_ | |       \___ \|  ___/ /\ \ | |\/| | |\/| |  __| |  _  / 
 | |\  | |__| | |____   ____) | |  / ____ \| |  | | |  | | |____| | \ \ 
 |_| \_|\_____|______| |_____/|_| /_/    \_\_|  |_|_|  |_|______|_|  \_\
                                                                        
        """
    )

    username = input("Enter username: ")
    question = input("Enter question (leave empty to send random questions): ")

    while True:
        try:
            amount = int(input("Enter amount of questions: "))
            if amount <= 0:
                raise ValueError("Amount must be higher than 0")
            break
        except ValueError as e:
            print(e)

    await send_questions(username, question, amount)
    print("Done!")


asyncio.run(main())
