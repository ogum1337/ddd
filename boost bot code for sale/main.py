from helpers.boost import *
from helpers.automated_boost import *
import httpx, random, time, datetime, json, os, hashlib, fade
import webbrowser
import datetime
import sys
from rgbprint import gradient_print, Color, rgbprint
import colorama
from colorama import Fore, Style
import discord
from discord import *
if os.name == 'nt':
    import ctypes

def cls(): #clears the terminal
    os.system('cls' if os.name =='nt' else 'clear')

    
config = json.load(open("config.json", encoding="utf-8"))

cls()


file1 = open('assets/1m_tokens.txt', 'r')

lines1 = file1.readlines()

num_lines1 = len(lines1)

file2 = open('assets/3m_tokens.txt', 'r')

lines2 = file2.readlines()

num_lines2 = len(lines2)


class Utils():
    @staticmethod
    async def isWhitelisted(ctx) -> bool:
        if (
            str(ctx.author.id) in open("assets/whitelist.txt", "r").read().splitlines()
            or str(ctx.author.id) == config["owner"]
        ):
            return True
        else:
            return False

activity1 = config['activity']

activity = discord.Activity(type=discord.ActivityType.playing, name=f"{activity1}")

bot = discord.Bot(command_prefix="*", activity=activity, status=discord.Status.online)
cls()
title = ("""
 █████╗ ███╗   ██╗██╗   ██╗██╗██╗         ██████╗  ██████╗  ██████╗ ███████╗████████╗███████╗
██╔══██╗████╗  ██║██║   ██║██║██║         ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝
███████║██╔██╗ ██║██║   ██║██║██║         ██████╔╝██║   ██║██║   ██║███████╗   ██║   ███████╗
██╔══██║██║╚██╗██║╚██╗ ██╔╝██║██║         ██╔══██╗██║   ██║██║   ██║╚════██║   ██║   ╚════██║
██║  ██║██║ ╚████║ ╚████╔╝ ██║███████╗    ██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ███████║
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚══════╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝                                                                                                                                                                                                                          
""")
gradient_print(title, start_color=(0x00C1FF), end_color=(0xfd00ff))
gradient_print(f"                                 ━━━━━━━━━━━━━━━━━━━━━━", start_color=(0x00C1FF), end_color=(0xfd00ff))
gradient_print(f"                                 >  1m Tokens | {num_lines1}     <", start_color=(0x00C1FF), end_color=(0xfd00ff))
gradient_print(f"                                 >  3m Tokens | {num_lines2}     <", start_color=(0x00C1FF), end_color=(0xfd00ff))
gradient_print(f"                                 ━━━━━━━━━━━━━━━━━━━━━━", start_color=(0x00C1FF), end_color=(0xfd00ff))

gradient_print(f"                             Boost bot is online and ready!", start_color=(0x00C1FF), end_color=(0xfd00ff))

@bot.slash_command(guild_ids=[config["guild_id"]],name="stock",description="Allows you to see the current token stock!",)
async def stock(ctx):
    embed = discord.Embed(title="Stock",description=f"```1 Month Token Stock: {len(open('assets/1m_tokens.txt', 'r').read().splitlines())}\n1 Month Boosts Stock: {len(open('assets/1m_tokens.txt', 'r').read().splitlines()) * 2}\n\n3 Month Token Stock: {len(open('assets/3m_tokens.txt', 'r').read().splitlines())} \n3 Month Boosts Stock: {len(open('assets/3m_tokens.txt', 'r').read().splitlines()) * 2}```",color=0x7982c9)
    gradient_print("                                /Stock used by",ctx.author,start_color=(0x00C1FF), end_color=(0xfd00ff))
    gradient_print("                                3 Months Token Stock:",num_lines2, start_color=(0x00C1FF), end_color=(0xfd00ff))
    gradient_print("                                1 Months Token Stock:",num_lines1, start_color=(0x00C1FF), end_color=(0xfd00ff))
    await ctx.respond(embed=embed)
   

@bot.slash_command(guild_ids=[config["guild_id"]], name="help", description="Shows all the commands the bot has!")
async def help(ctx: discord.ApplicationContext):
    return await ctx.respond(
        embed=discord.Embed(
        title="Help Menu",
        description="**/boost |** Boosts the provided server with nitro tokens\n**/stock |** Shows how many nitro tokens are in stock\n**/restock |** Restocks boosts with nitro tokens\n**/givetokens |** Sends tokens to the provided user\n**/whitelist |** Gives provided user access to the bot\n**/unwhitelist |** Removes the provided user access to the bot",
        color=0x7982c9
        )
    )



@bot.slash_command(guild_ids=[config["guild_id"]], name="restock", description="Restocks your tokens!")
async def restock(ctx,attachment: discord.Option(discord.Attachment, "Drag your file with tokens here.", required=True),months: discord.Option(int, "Uses 1m or 3m stock to boost servers", required=True)):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0x7982c9
            )
        )

    if months == 1:
        filename = "assets/1m_tokens.txt"
    if months == 3:
        filename = "assets/3m_tokens.txt"

    tokens = await attachment.read()
    tokens = tokens.decode()
    with open(filename, "a") as tokens_input:
        for token in tokens.splitlines():
            tokens_input.write(token + "\n")

    embed = discord.Embed(
        title="Successfully Restocked",
        description=f"*Restocked {len(tokens.splitlines())} tokens*",
        color=0x7982c9
    )

    await ctx.respond(embed=embed)    



@bot.slash_command(
    guild_ids=[config["guild_id"]],
    name="whitelist",
    description="Whitelist a user with ease.",
)
async def whitelist(
    ctx, user: discord.Option(discord.Member, "Member to whitelist", required=True)
):
    if str(ctx.author.id) != config["owner"]:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Contact {await bot.fetch_user(int(config['owner']))}",
                description="You need to be added as owner to run this command!",
                color=0x7982c9
            )
        )

    if (
        not (str(user.id) in open("assets/whitelist.txt", "r").read().splitlines())
        and str(user.id) != config["owner"]
    ):
        with open("assets/whitelist.txt", "a") as whitelist:
            whitelist.write(str(user.id) + "\n")

        embed = discord.Embed(
            title="Success",
            description=f"Successfully whitelisted {user}",
            color=0x7982c9
        )

        return await ctx.respond(embed=embed)

    elif str(user.id) == config["owner"]:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Already Owner!",
                description=f"You cant run this command you are owner on this bot!",
                color=0x7982c9
            )
        )

    else:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Already whitelisted!",
                description=f"{user} is already whitelisted!",
                color=0x7982c9
            )
        )


@bot.slash_command(
    guild_ids=[config["guild_id"]],
    name="unwhitelist",
    description="Unwhitelist a user with ease.",
)
async def unwhitelist(
    ctx, user: discord.Option(discord.Member, "Member to unwhitelist", required=True)
):
    if str(ctx.author.id) != config["owner"]:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Contact {await bot.fetch_user(int(config['owner']))}",
                description="You need to be added as owner to run this command!",
                color=0x7982c9
            )
        )

    if (
        not (str(user.id) in open("assets/whitelist.txt", "r").read().splitlines())
        and str(user.id) != config["owner"]
    ):
        embed = discord.Embed(
            title="User Not Whitelisted!",
            description=f"{user} is currently not whitelisted.",
            color=0x7982c9
        )

        return await ctx.respond(embed=embed)

    elif str(user.id) == config["owner"]:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Already Owner!",
                description=f"You are currently the owner! You cannot unwhitelist yourself.",
                color=0x7982c9
            )
        )

    else:
        with open("assets/whitelist.txt", "r+") as whitelist:
            whitelisted = whitelist.readlines()
            whitelist.seek(0)
            for line in whitelisted:
                if not (str(user.id) in line):
                    whitelist.write(line)
            whitelist.truncate()

        embed = discord.Embed(
            title="Success",
            description=f"Successfully Removed {user}",
            color=0x7982c9
        )

        return await ctx.respond(embed=embed)

@bot.slash_command(
    guild_ids=[config["guild_id"]],
    name="givetokens",
    description="Allows you to give a person nitro tokens.",
)
async def givetokens(
    ctx,
    user: discord.Option(discord.Member, "Member to give tokens to.", required=True),
    amount: discord.Option(int, "Amount of tokens to give", required=True),
    months: discord.Option(int, "Uses 1m or 3m stock to boost servers", required=True)
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0x7982c9
            )
        )

    if months == 1:
        filename = "assets/1m_tokens.txt"
    if months == 3:
        filename = "assets/3m_tokens.txt"

    if amount > len(open(filename, "r").read().splitlines()):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not enough tokens",
                description=f"You are requesting {amount} tokens but there are only {len(open(filename, 'r').read().splitlines())} tokens.",
                color=0x7982c9
            )
        )

    tokens_to_send = []
    with open(filename, "r") as all_tokens:
        tokens = all_tokens.read().splitlines()
        for x in range(amount):
            tokens_to_send.append(tokens[x])
            remove(tokens[x], filename)

    outfile = f"./{user.name}_{amount}_{months}_month(s)_tokens.txt".replace(" ", "")

    with open(outfile, "w") as file:
        for token in tokens_to_send:
            file.write(token + "\n")

        file.close()

        with open(outfile, "rb") as out_tokens:

            channel = await user.create_dm()
            await channel.send(file=discord.File(out_tokens, outfile))

    os.remove(outfile)

    return await ctx.respond(
        embed=discord.Embed(
            title="Success",
            description=f"Successfully sent {amount} {months} month(s) tokens to {user}",
            color=0x7982c9
        )
    )

@bot.slash_command(guild_ids=[config["guild_id"]], name="boost", description="Boosts a discord server.")
async def boost(ctx: discord.ApplicationContext,invite: discord.Option(str,"invite link (can be full link)",required=True,),amount: discord.Option(int, "amount of boosts", required=True),months: discord.Option(int, "1m or 3m stock", required=True),nick: discord.Option(str,"enter your nickname", required=False)):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0x7982c9
            )
        )

    if ".gg/" in invite:
        invite = str(invite).split(".gg/")[1]
    elif "invite/" in invite:
        invite = str(invite).split("invite/")[1]

    if (
        '{"message": "Unknown Invite", "code": 10006}'
        in httpx.get(f"https://discord.com/api/v9/invites/{invite}").text
    ):
        return await ctx.respond(
            embed=discord.Embed(
                title="Error!",
                description=f"discord.gg/{invite} is invalid. Please set a valid invite.",
                color=0x7982c9
            )
        )

    if amount % 2 != 0:
        return await ctx.respond(
            embed=discord.Embed(
                title="Error!",
                description="`amount` must be even.",
                color=0x7982c9
            )
        )

    await ctx.respond(
        embed=discord.Embed(
            title="Started!",
            description=f"```Started Boosting https://discord.gg/{invite} {amount}x```",
            color=0x7982c9
        )
    ) 
    gradient_print("                 Boosting Server: ",invite,"amount of boosts",amount,"months",months, start_color=(0x00C1FF), end_color=(0xfd00ff)) 

    go = time.time()
    tboost(invite, amount, months, nick)
    end = time.time()
    time_went = round(end - go, 2)

    await ctx.edit(
        embed=discord.Embed(
            title="Boosting Finished",
            description=f"```Boosted https://discord.gg/{invite} {amount} times for {months} month\nFinished Boosts: {len(variables.success_tokens)*2}\nFailed Boosts: {len(variables.failed_tokens)*2}```",
            color=0x7982c9
        )
    )
        
    if tboost == False:
        with open('success.txt', 'w') as f:
            for line in variables.success_tokens:
                f.write(f"{line}\n")
            
        with open('failed.txt', 'w') as g:
            for line in variables.failed_tokens:
                g.write(f"{line}\n")
        
        embed2 = DiscordEmbed(title = "Boost Log", description = f"*Failed to boost https://discord.gg/{invite} {amount}x for {months} month(s)*", color = 'FF0004')
        embed2.set_timestamp()
        webhook = DiscordWebhook(url=config["failed_boosts"])
        webhook.add_embed(embed2)
        webhook.execute()
        print()
        print()

        webhook = DiscordWebhook(url=config["failed_boosts"])
        with open("success.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='success.txt')
        with open("failed.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='failed.txt')
        webhook.execute()
            
        os.remove("success.txt")
        os.remove("failed.txt")
                
    elif tboost:
        with open('success.txt', 'w') as f:
            for line in variables.success_tokens:
                f.write(f"{line}\n")
            
        with open('failed.txt', 'w') as g:
            for line in variables.failed_tokens:
                g.write(f"{line}\n")
                    
        embed3 = DiscordEmbed(title = f"Boost Log", description=f"*Boosted https://discord.gg/{invite} {amount}x in {time_went}s for {months} month(s)*\n**Finished Boosts: **`{len(variables.success_tokens)*2}`\n**Failed Boosts: **`{len(variables.failed_tokens)*2}`", color = 'ED00FF')
        embed3.set_timestamp()
        webhook = DiscordWebhook(url=config["boosts_logs"])
        webhook.add_embed(embed3)
        webhook.execute()
        print()
        print()

        webhook = DiscordWebhook(url=config["boosts_logs"])
        with open("success.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='success.txt')
        with open("failed.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='failed.txt')
        webhook.execute()
            
        os.remove("success.txt")
        os.remove("failed.txt")
    
#keep_alive()
bot.run(config["token"])
