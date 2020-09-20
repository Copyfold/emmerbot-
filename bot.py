import random
import re
from collections import defaultdict
from os import environ
from typing import Any, Dict, List, Optional

import discord
from discord.ext import commands

TOKEN = environ["token"]

bot = commands.Bot(command_prefix="!")


class LString:
    def __init__(self) -> None:
        self._total = 0
        self._successors: Dict[str, int] = defaultdict(int)

    def put(self, word: str) -> None:
        self._successors[word] += 1
        self._total += 1

    def get_random(self) -> Optional[str]:
        ran = random.randint(0, self._total - 1)
        for key, value in self._successors.items():
            if ran < value:
                return key
            else:
                ran -= value
        return None


couple_words: Dict[Any, Any] = defaultdict(LString)


def load(phrases: str) -> None:
    with open(phrases, "r") as f:
        for line in f:
            add_message(line)


def add_message(message: str) -> None:
    message = re.sub(r"[^\w\s\']", "", message).lower().strip()
    words = message.split()
    for i in range(2, len(words)):
        couple_words[(words[i - 2], words[i - 1])].put(words[i])
    couple_words[(words[-2], words[-1])].put("")


def generate() -> str:
    result: List[Any] = []
    while len(result) < 10 or len(result) > 20:
        result = []
        s = random.choice(list(couple_words.keys()))
        result.extend(s)
        while result[-1]:
            w = couple_words[(result[-2], result[-1])].get_random()
            result.append(w)

    return " ".join(result)


@bot.event
async def on_ready() -> None:
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("Eating Bacon")
    )


@bot.event
async def on_message(message: Any) -> None:
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    channel = message.channel
    print(
        f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    )

    if message.content.startswith("!markov"):
        resp = generate()
        await channel.send(resp)
        return

    if message.content.startswith("hello"):
        response = random.choice(
            [
                "Hello " + str(message.author) + "!",
                "Henlo!",
                "Greetings human o/",
                "Bemlo!",
            ]
        )
        await channel.send(response)

    elif message.content.startswith("i love you"):
        await channel.send("i love you too " + str(message.author) + "!")

    elif message.content.startswith("i love emmerbot"):
        await channel.send("emmerbot loves you!")

    elif message.content.startswith("how are you"):
        await channel.send("I'm fat, I've had too much bacon")

    elif message.content.startswith("i need slee"):
        await channel.send("do a snoozy woozy!")

    elif message.content.startswith("sorry emmerbot"):
        await channel.send("It's okay, I forgive you!")

    bad_words = ["big bad", "nonono", "bad slur", "etc."]

    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            print(
                f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
            )
            await message.delete()

    await bot.process_commands(message)


load("training.txt")

bot.run(TOKEN)
