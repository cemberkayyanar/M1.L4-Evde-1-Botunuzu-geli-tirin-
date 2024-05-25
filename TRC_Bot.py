import discord
from discord.ext import commands
import openai

# Discord bot ve OpenAI API anahtarınızı burada tanımlayın
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

openai.api_key = OPENAI_API_KEY

# Discord botu oluşturma
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba Kanki! Ben {bot.user}')

@bot.command()
async def yardım(ctx):
    help_text = """
    **Komutlar:**
    /hello - Bot size selam verir.
    /yardım - Bu yardım mesajını gösterir.
    """
    await ctx.send(help_text)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('/'):
        await bot.process_commands(message)
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.content}
        ]
    )
    await message.channel.send(response.choices[0].message['content'].strip())

bot.run(DISCORD_TOKEN)
