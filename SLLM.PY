import discord
from discord.ext import commands
from openai import ChatCompletion, OpenAI

# Set up Discord bot
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Get the localhost port from user input
localhost_port = input("Enter the localhost port: ")

# Get the Discord token from user input
discord_token = input("Enter your Discord token: ")

# Get the system message from user input
system_message = input("Enter the system message: ")

# Initialize OpenAI
openai = OpenAI(base_url=f"http://localhost:{localhost_port}/v1", api_key="not-needed")

# Dictionary to store user messages
user_messages = {}

# Dictionary to store bot responses
bot_responses = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Ensure that commands are processed

    if bot.user.mentioned_in(message):
        # Get the user message content
        user_message_content = user_messages.get(message.author.id, "")

        # Ensure the user message content is not empty
        if user_message_content.strip():
            completion = openai.chat.completions.create(
                model="local-model",  # this field is currently unused
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message_content}
                ],
                temperature=0.7,
            )

            model_response = completion.choices[0].message.content if completion.choices else "I have nothing to say."

            # Store the bot's response
            bot_responses[message.author.id] = model_response

            await message.channel.send(model_response)
        else:
            await message.channel.send("I don't have any previous message from you.")

        # Remember the user message
        user_messages[message.author.id] = message.content

@bot.command()
async def clear_memory(ctx):
    user_messages.clear()
    bot_responses.clear()
    await ctx.send("Memory cleared successfully.")

bot.run(discord_token)
