import discord
from discord.ext import commands
import json
import aiohttp
import os
import asyncio
import os.path
import yt_dlp as youtube_dl
from colorama import Fore, init
from typing import Literal, Optional

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
    intents.guilds

    bot = commands.Bot(command_prefix=config['prefix'], intents=intents, sync_commands=True)
    tree = bot.tree
    guild_id = 918167061086228570
    guild = discord.Object(id=guild_id)



    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # Bind to ipv4 since ipv6 addresses cause issues sometimes
    }

    ytdl = youtube_dl.YoutubeDL(ytdl_opts)

# FFmpeg Optionen
    ffmpeg_opts = {
        'executable': r'C:\Users\moric\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe',  # Pfad zur ffmpeg.exe hinzufügen
        'before_options': '-nostdin',
        'options': '-vn',
    }

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = data.get('url')

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                data = data['entries'][0]

            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)
        
    @bot.event
    async def on_ready():
            print(f'{bot.user} ist mit Discord verbunden!')
            await tree.sync()
            game = discord.Game("an Mou67")
            await bot.change_presence(status=discord.Status.online, activity=game)
    
    @bot.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'Invalid command, {ctx.author.mention}. Please check the command name and try again ⚠️')
        else:
            raise error

    @bot.command(
        name='info'
    )
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

    @bot.command(
            name='userinfo',
            description='will you give user information'
            )
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

    @tree.command(
        name="kick",
        description="Kicks a user from the server",
    )
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.display_name} has been kicked. Reason: {reason}")


    @tree.command(
    name='meme',
    description='will you give an meme'
    )
    async def meme(interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                if response.status == 200:
                    data = await response.json()
                    meme_url = data["url"]
                    await interaction.response.send_message(meme_url)
                else:
                    await interaction.response.send_message("No meme has been found try again laiter")

    class Stop_button(discord.ui.View):
        @discord.ui.button(label="Stop Me", style=discord.ButtonStyle.red, emoji='🛑')
        async def stop_button_callback(self, button: discord.ui.Button, interaction):
             if interaction.user.id == config['owner_id']:
                await interaction.response.send_message("Stopping Bot!")
                await asyncio.sleep(5)
                await bot.close()

    @tree.command(
        name="stop",
        description="Will Stop the Bot",
    )
    async def stop(ctx):
        await ctx.send("You sure that you want to stop the bot!", view=Stop_button())
        await asyncio.sleep(5)
        await bot.close()
    
    @tree.context_menu(name="Get User ID")
    async def get_user_id(ctx: discord.Interaction, message: discord.Message):
        await ctx.response.send_message(f"User ID: `{message.author.id}`")

    @tree.context_menu(name="Get Message ID")
    async def get_user_id(ctx: discord.Interaction, message: discord.Message):
        await ctx.response.send_message(f"Message ID: `{message.id}`")
            
    game = discord.Activity(type=discord.ActivityType.listening, name="/Play")

    class StatusView(discord.ui.View):
        @discord.ui.button(style=discord.ButtonStyle.green, label="Online", emoji='🟢')
        async def online_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Status Set Online")
            await bot.change_presence(status=discord.Status.online, activity=game)
        @discord.ui.button(style=discord.ButtonStyle.gray, label="Offline", emoji='⚫')
        async def offline_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Status Set Offline")
            await bot.change_presence(status=discord.Status.offline, activity=None)
        @discord.ui.button(style=discord.ButtonStyle.primary, label="Idle", emoji='🟠')
        async def idle_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Status Set Idle")
            await bot.change_presence(status=discord.Status.idle, activity=None)


    
    @tree.command(
        name="status",
        description="Set the bot's status",
    )
    async def status(interaction: discord.Interaction):
        view = StatusView()
        await interaction.response.send_message("Select a status", view=view)

    @tree.command(name="play", description="Spielt einen Song von YouTube")
    async def play(interaction: discord.Interaction, url: str):
        if not interaction.user.voice:
            await interaction.response.send_message("Du musst in einem Sprachkanal sein, um diesen Befehl zu benutzen.", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            vc = await voice_channel.connect()
        else:
            vc = interaction.guild.voice_client

        await interaction.response.defer()

        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        vc.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.followup.send(f'Spiele: {player.title}')

    YOUR_SERVER_ID = 918167061086228570
    YOUR_CHANNEL_ID = 1255556189836808283

    @bot.event
    async def on_guild_join(guild):
    # Finde deinen speziellen Server und Kanal
        target_guild = bot.get_guild(YOUR_SERVER_ID)
        if target_guild is not None:
            channel = target_guild.get_channel(YOUR_CHANNEL_ID)
            if channel is not None:
                embed = discord.Embed(
                    title="Ich bin einem neuen Server beigetreten!",
                    description=f"Servername: {guild.name}\nServer ID: {guild.id}",
                    color=discord.Color.blue()
                )

                if guild.icon:
                    embed.set_thumbnail(url=guild.icon.url)

                embed.add_field(name="Mitgliederzahl", value=guild.member_count)

                await channel.send(embed=embed)
            else:
                print(f"Kein Kanal mit der ID {YOUR_CHANNEL_ID} gefunden in deinem Server")
        else:
            print(f"Kein Server mit der ID {YOUR_SERVER_ID} gefunden")

    

    if __name__ == '__main__':
        bot.run(config['token'])