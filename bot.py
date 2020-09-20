from os import environ
from os.path import join, realpath
from random import choice, choices, randint
from string import whitespace
from typing import Any, Dict, Iterator, List, Sequence, cast

import discord
from discord.ext import commands

TOKEN = environ["token"]

bot = commands.Bot(command_prefix="!")
TRAINING = join(realpath(__file__), "training.txt")

M_LO, M_HI = 10, 20

WS = {*whitespace}
store: Dict[str, Dict[str, int]] = {}


def load(src: str) -> Iterator[str]:
    acc: List[str] = []
    with open(src) as fd:
        for line in fd:
            for char in line:
                if char not in WS:
                    acc.append(char)
                else:
                    if acc:
                        yield "".join(acc)
                        acc.clear()


def populate(it: Iterator[str]) -> None:
    prev: str = ""
    for word in it:
        sub_store = store.setdefault(prev, {})
        sub_store[word] = sub_store.get(word, 0) + 1
        prev = word


def generate() -> str:
    acc: List[str] = []
    acc.append(choice(tuple(store)))
    for _ in range(0, randint(M_LO, M_HI)):
        candidates = store[acc[-1]]
        pop, weights = zip(*candidates.items())
        nxt, *_ = choices(
            cast(Sequence[str], pop), weights=cast(Sequence[int], weights)
        )
        acc.append(nxt)

    return " ".join(acc)


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
        response = choice(
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


it = load(TRAINING)
populate(it)


bot.run(TOKEN)