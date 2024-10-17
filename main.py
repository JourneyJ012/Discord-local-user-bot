import discord
from discord import app_commands
import requests
import random
import openai
import ollama
import io
from dotenv import load_dotenv
import os
load_dotenv()
bot = discord.Client(intents=discord.Intents.none())
tree = app_commands.CommandTree(bot)
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def hello(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def repeat(interaction: discord.Interaction, *, text: str) -> None:
    await interaction.response.send_message(text)


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def avatar(interaction: discord.Interaction, user_id: str) -> None:
    try:
        user_id = int(user_id)
        user = await bot.fetch_user(user_id)
        if user.avatar:
            avatar_url = user.avatar.url
        else:
            avatar_url = user.default_avatar.url
        await interaction.response.send_message(f"{user.mention}'s avatar: {avatar_url}")
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ping(interaction: discord.Interaction) -> None:
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency}ms")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def quote(interaction: discord.Interaction) -> None:
    response = requests.get("https://api.quotable.io/random")
    data = response.json()
    if response.status_code == 200:
        quote = f"\"{data['content']}\" - {data['author']}"
        await interaction.response.send_message(quote)
    else:
        await interaction.response.send_message("Couldn't fetch a quote at the moment. Try again later!")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def roll_dice(interaction: discord.Interaction, sides: str) -> None:
    try:
        sides = int(sides)
        if response < 1:
            response = f"{response} is less than 1"
        else:
            response = f"You rolled a {random.randint(1, sides)} on a {sides}-sided dice!"
    except:
        response = "You need to input a number."

    await interaction.response.send_message(response)


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def test(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("This is a test command. It does nothing, but if the API ever messes me up, I can try run a new command here.")
    pass


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def userinfo(interaction: discord.Interaction, user: discord.User) -> None:
    embed = discord.Embed(
        title=f"{user.name}'s Info", color=discord.Color.pink())
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.set_thumbnail(url=user.avatar.url)
    await interaction.response.send_message(embed=embed)


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ask_gpt(interaction: discord.Interaction, inputted_value: str) -> None:
    await interaction.response.defer()
    # Hi, creator here, I'm 426038773281718282. Please remove this. This isn't meant to be snook in, it's literally just to show how it works.
    if interaction.user.id not in [426038773281718282]:
        await interaction.followup.send("You are not Echo!")
    else:
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": inputted_value}]
            )
            await interaction.followup.send(content=chat_completion.choices[0].message.content)
        except Exception as e:
            chat_completion = f"Fail! {str(e)}"
            await interaction.followup.send(content=chat_completion)


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def github(interaction: discord.Interaction, username: str, repository: str) -> None:
    await interaction.response.defer()
    url = f'https://api.github.com/repos/{username}/{repository}'
    response = requests.get(url)
    if response.status_code == 200:
        repo_data = response.json()
        embed = discord.Embed(
            title=repo_data['name'], description=repo_data['description'], url=repo_data['html_url'])
        embed.add_field(name='Stars', value=repo_data['stargazers_count'])
        embed.add_field(name='Forks', value=repo_data['forks_count'])
        embed.add_field(name='Open Issues',
                        value=repo_data['open_issues_count'])
        embed.set_footer(text=f'Owner: {repo_data["owner"]["login"]}')
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Repository not found.')


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(model="Run a prompt through Ollama")
@app_commands.choices(model=[
    discord.app_commands.Choice(
        name="Llama (pretty dumb, incredibly fast)", value="llama3.2:1b"),
    discord.app_commands.Choice(
        name="Qwen2.5", value="qwen2.5:7b"),
    discord.app_commands.Choice(
        name="Qwen (coding ver)", value="qwen2.5-coder:7b"),
    discord.app_commands.Choice(
        name="Qwen (math ver)", value="qwen2-math:7b"),
    discord.app_commands.Choice(
        name="Gemma2", value="gemma2:latest")

    ]
)
async def ask_ollama(interaction: discord.Interaction, model: discord.app_commands.Choice[str], prompt: str) -> None:
    await interaction.response.defer()
    print(prompt)

    response = ollama.chat(
        model=model.value, messages=[
            {"role": "user", "content": f"Answer the prompt in less than 100 words and more than 1 word. {prompt}"}
        ]
    )

    if not response['message']['content']:
        response = "The AI generated nothing. Please try again."
    elif len(response['message']['content']) > 1999:
        with io.StringIO() as text_file:
            text_file.write(response['message']['content'])
            text_file.seek(0)
            discord_file = discord.File(text_file, filename="response.txt")
        await interaction.followup.send(content="The AIs response was too long.", file=discord_file)
    elif len(response['message']['content']) < 1999:
        await interaction.followup.send(content=response['message']['content'])
    else:
        await interaction.followup.send(content="The AI messed up, it didn't generate nothing, but it didn't generate correctly. It might have generated too much text.")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def cat(interaction: discord.Interaction) -> None:
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        data = response.json()
        image_url = data[0]['url']
        await interaction.response.send_message(image_url)
    else:
        await interaction.response.send_message("Couldn't fetch a cat image at the moment. Try again later!")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def dog(interaction: discord.Interaction) -> None:
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code == 200:
        data = response.json()
        image_url = data['message']
        await interaction.response.send_message(image_url)
    else:
        await interaction.response.send_message("Couldn't fetch a dog image at the moment. Try again later!")


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def reverse(interaction: discord.Interaction, *, text: str) -> None:
    reversed_text = text[::-1]
    await interaction.response.send_message(reversed_text)


@tree.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(prompt="An AI tries to explain whatever to you")
async def explain_concept(interaction: discord.Interaction, prompt: str) -> None:
    await interaction.response.defer()
    print(prompt)

    response = ollama.chat(
        model="llama3.1:latest", messages=[
            {"role": "user", "content": f"Explain this subject like you're explaining to a 10 year old. Try keep things into less than 200 words. The subject is - {prompt}"}
        ]
    )

    if not response['message']['content']:
        response = "The AI generated nothing. Please try again."
    elif len(response['message']['content']) > 1999:
        with io.StringIO() as text_file:
            text_file.write(response['message']['content'])
            text_file.seek(0)
            discord_file = discord.File(text_file, filename="response.txt")
        await interaction.followup.send(content="The AIs response was too long.", file=discord_file)
    elif len(response['message']['content']) < 1999:
        await interaction.followup.send(content=response['message']['content'])
    else:
        await interaction.followup.send(content="The AI messed up, it didn't generate nothing, but it didn't generate correctly. It might have generated too much text.")


@bot.event
async def on_ready():
    await tree.sync()

token = os.getenv('DISCORD_API_KEY')
bot.run(token)
