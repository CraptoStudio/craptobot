import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.message_reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.content.lower() == 'roles':
        roles_message = await message.channel.send("Choose your role from these reactions:")
        
        # Define the roles and corresponding reactions
        roles_data = {
            "Role 1": "🔵",
            "Role 2": "🟢",
            "Role 3": "🔴",
            "Role 4": "🟡",
            "Role 5": "🟣",
            "Role 6": "🟠",
            "Role 7": "⚪",
            "Role 8": "⚫",
            "Role 9": "🟤",
            "Role 10": "🟦",
        }
        
        # Add reactions to the roles_message
        for reaction in roles_data.values():
            await roles_message.add_reaction(reaction)
    
    # Check for the "delete" command
    if message.content.startswith('delete'):
        try:
            _, number = message.content.split()
            number = int(number)
            
            # Check if the user has the necessary permissions to delete messages
            if message.author.guild_permissions.manage_messages:
                await message.delete()
                
                # Fetch and delete the specified number of messages
                deleted = await message.channel.purge(limit=number + 1)
                
                # Send a confirmation message
                await message.channel.send(f"Deleted {len(deleted) - 1} messages.")
            else:
                await message.channel.send("You don't have the necessary permissions to delete messages.")
        except ValueError:
            await message.channel.send("Invalid syntax. Use 'delete [number]' to delete messages.")
    
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    
    roles_data = {
        "🔵": "Role 1",
        "🟢": "Role 2",
        "🔴": "Role 3",
        "🟡": "Role 4",
        "🟣": "Role 5",
        "🟠": "Role 6",
        "⚪": "Role 7",
        "⚫": "Role 8",
        "🟤": "Role 9",
        "🟦": "Role 10",
    }
    
    if reaction.emoji in roles_data:
        role_name = roles_data[reaction.emoji]
        role = discord.utils.get(user.guild.roles, name=role_name)
        
        if role:
            await user.add_roles(role)
            await user.send(f"You've been given the role: {role_name}")

# Run the bot
bot.run('YOUR_BOT_TOKEN')
