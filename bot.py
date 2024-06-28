import discord
import json
import os
from colorama import Fore, init
from discord.ext import commands

config_file = 'config.json'


init()

print(f'{Fore.GREEN}')
print('$$$$$$$$  $$\                                               $$\       $$$$$$$\             $$\     ')
print('$$  __$$\ \__|                                              $$ |      $$  __$$\            $$ |    ')
print('$$ |  $$ |$$\  $$$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$\   $$$$$$$ |      $$ |  $$ | $$$$$$\ $$$$$$\   ')
print('$$ |  $$ |$$ |$$  _____|$$  _____|$$  __$$\ $$  __$$\ $$  __$$ |      $$$$$$$\ |$$  __$$\\_$$  _|  ')
print('$$ |  $$ |$$ |\$$$$$$\  $$ /      $$ /  $$ |$$ |  \__|$$ /  $$ |      $$  __$$\ $$ /  $$ | $$ |    ')
print('$$ |  $$ |$$ | \____$$\ $$ |      $$ |  $$ |$$ |      $$ |  $$ |      $$ |  $$ |$$ |  $$ | $$ |$$\ ')
print('$$$$$$$  |$$ |$$$$$$$  |\$$$$$$$\ \$$$$$$  |$$ |      \$$$$$$$ |      $$$$$$$  |\$$$$$$  | \$$$$  |')
print('\_______/ \__|\_______/  \_______| \______/ \__|       \_______|      \_______/  \______/   \____/ ')
print(f'{Fore.RESET}')
print("")
print("")

if not os.path.exists(config_file):
    print(f"Config file '{config_file}' not found. Creating a new one...")
    default_config = {
        'token': 'YOUR_DISCORD_TOKEN',
        'prefix': '!',
        'owner_id': 'YOUR_DISCORD_ID'
    }
    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=4)
    print(f"Config file created. Please edit '{config_file}' with your bot's token and other settings.")
    exit()
else:
    with open(config_file) as f:
        config = json.load(f)
    print("Configs are loaded correctly")


    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

    @bot.event
    async def on_ready():
            print(f'{bot.user} ist mit Discord verbunden!')


    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'Invalid command, {ctx.author.mention}. Please check the command name and try again ⚠️')
        else:
            raise error

    @bot.command(name='test')
    async def test(ctx):
        await ctx.send('This is a test message!')
        print("Message has been sent")

    @bot.command(name='info')
    async def info(ctx):
        await ctx.channel.purge(check=lambda m: m.author == bot.user and len(m.embeds) > 0)
        embed = discord.Embed(
            title="Info",
            description="This is a test",
            color=discord.Color.red()
        )

        embed.set_author(name=client, url="", icon_url="https://cdn3.emoji.gg/emojis/3456-frieren-sus.png")
        embed.set_thumbnail(url="https://64.media.tumblr.com/616d0c6ba0f2963b74d36fb4cdbb4aa0/e22be3e4cd0ed6c9-ac/s540x810/ef7e5857e7aa29654dabb17ddba22f093233626c.gifv")

        await ctx.send(embed=embed)

    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} from the server.')

    @bot.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} from the server.')

    @bot.command(name='userinfo')
    async def userinfo(ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"User Info: {member.name}",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Username", value=member.name, inline=False)
        embed.add_field(name="Discriminator", value=member.discriminator, inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Created Account", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles]), inline=False)

        await ctx.send(embed=embed)


    @bot.command(name='stop', help='Stops the bot.')
    @commands.is_owner()
    async def stop_bot(ctx):
        if ctx.author.id == config['owner_id']:
             if bot.is_closed():
                await ctx.send('Stopping the bot...')
                await bot.close()

    if __name__ == '__main__':
        bot.run(config['token'])