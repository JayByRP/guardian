import os
import asyncio
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from discord import app_commands, Intents, Client, Interaction
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Discord bot
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)

# Initialize FastAPI
app = FastAPI()

# Define allowed role IDs
ALLOWED_ROLES = [
    1307013563650412605,
    1307013564850114560,
    1307013559745511446
]

# Define templates
TEMPLATES = {
    "template1": """
> Thank you for submitting your RP sample!
> Unfortunately, we have a strict policy of
> not allowing minors to participate in this
> community. As such, we are unable to
> grant you access to the server at this time.
> 
> We wish you the best and encourage you to
> explore age-appropriate communities until
> you meet our age requirement. Thank you
> for understanding. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip(),
    
    "template2": """
> Thank you for submitting your RP sample!
> Unfortunately, we noticed that it was not
> submitted in a Google Document format,
> or that it is inaccessible. To proceed with
> your application, please make sure that:
> 
> - your sample is pasted in a Google Doc.
> - the document has the right permission:
>   - "anyone with the link can view."
> 
> Please reach out if you need assistance
> with sharing your sample. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip(),
    
    "template3": """
> Thank you for submitting your RP sample!
> Unfortunately, after careful review, we’ve
> determined that the sample does not meet
> our literacy standards. Thank you for your
> understanding, and we wish you the best
> in your roleplaying journey. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip(),
    
    "template4": """
> Thank you for submitting your RP sample!
> We appreciate the effort you’ve put into it.
> However, after careful review, a few areas
> could be improved to better align with the
> literacy standards of our server. Before we
> approve your application, please review the
> RP sample requirement guide at the top of
> the channel, right under the pinned banner.
> 
> We encourage you to revise and resubmit
> your sample once you have addressed the
> fixes. If after careful revision you would like
> specific examples or further guidance, feel
> free to reach out—we’d be happy to help!
> Looking forward to reading your improved
> writing sample. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip(),
    
    "template5": """
> Thank you for submitting your RP sample!
> After careful review, we’re thrilled to let
> you know that it has been accepted. Your
> writing meets our literacy and creativity
> standards, and we’re excited to see you
> bring your characters to life in our server.
> 
> Before you continue, we suggest you pick
> your #❧・colors and #❧・roles, then                     <#channel_id>
> greet everyone in the #❧・main﹒chat.
> We've prepared a [server guide](<https://docs.google.com/document/d/1jTfgXNh8guuxCgNGfAguUpDH9dZdamACisBYQvFs6oo/edit?usp=sharing>) to help
> you navigate the different categories with
> ease, and know each channel's purpose.
> 
> If you have any questions or need guidance,
> don’t hesitate to reach out. We can’t wait
> to roleplay with you! Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip(),
    
    "template6": """
> Thank you for submitting your character.
> Unfortunately, after careful review, we've
> noticed that you either didn't follow the
> template instructions, or that you didn't
> take a good look at the server's lore. We
> strongly recommend revisiting the docs
> to familiarize yourself with everything.
> 
> Since the required information was not
> properly provided, we will not continue
> reading your bio until it's properly fixed.
> Please revise your bio accordingly and
> resubmit it for review. Should you have
> questions or require clarification, you
> may reach out. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip(),
    
    "template8": """
> Thank you for submitting your character!
> After careful review, we’re thrilled to let
> you know that they have been accepted.
> We found the bio to be well-aligned with
> our guidelines and lore; the OC fits well
> into the world we've created, and we’re
> excited to see them in action.
> 
> Before you continue, we suggest you
> remove your #✧・wanted﹒list post,
> if applicable, or that you talk with the
> person who posted the ad to bring it
> down. Take a look at our #✧・directory,
> and add your OC to the list. If you have
> any questions or need guidance, don’t
> hesitate to reach out. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip()
}

def has_required_role(member_roles: List[int]) -> bool:
    """Check if the user has any of the required roles."""
    return any(role.id in ALLOWED_ROLES for role in member_roles)

# Template commands
@tree.command(name="template1", description="Posts template 1")
async def post_template1(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template1"])

@tree.command(name="template2", description="Posts template 2")
async def post_template2(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template2"])

@tree.command(name="template3", description="Posts template 3")
async def post_template3(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template3"])

@tree.command(name="template4", description="Posts template 4")
async def post_template4(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template4"])

@tree.command(name="template5", description="Posts template 5")
async def post_template5(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template5"])

@tree.command(name="template6", description="Posts template 6")
async def post_template6(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template6"])

@tree.command(
    name="template7",
    description="Posts character rejection template with customizable feedback"
)
@app_commands.describe(
    comment1="First paragraph (required)",
    comment2="Second paragraph (optional)",
    comment3="Third paragraph (optional)",
    comment4="Fourth paragraph (optional)",
    comment5="Fifth paragraph (optional)"
)
async def post_template7(
    interaction: Interaction,
    comment1: str,
    comment2: str = None,
    comment3: str = None,
    comment4: str = None,
    comment5: str = None,
):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return

    # Build comments section
    comments = [f"**[1] ::** {comment1}"]
    
    # Add optional comments if provided
    optional_comments = [comment2, comment3, comment4, comment5]
    for i, comment in enumerate(optional_comments, start=2):
        if comment:
            comments.append(f"**[{i}] ::** {comment}")

    template = f"""
> Thank you for submitting your character.
> We appreciate the effort you've put into it.
> However, after careful review, there are
> some elements of your submission that
> need attention. Address them carefully:
> 
{chr(10).join(f'> {comment}\n> \n' for comment in comments)}
> 
> We encourage you to revise and resubmit
> your character once you've addressed the
> fixes. If after careful revision you would like
> specific examples or further guidance, feel
> free to reach out—we'd be happy to help!
> Looking forward to reading your improved
> writing sample. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
""".strip()

    # Send message without showing command user
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(template)

@tree.command(name="template8", description="Posts template 8")
async def post_template8(interaction: Interaction):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(TEMPLATES["template8"])

# FastAPI endpoints
@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Discord bot events
@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')
    await tree.sync()

# Ping function for bot health check
async def ping_discord_bot():
    while True:
        try:
            if not client.is_closed():
                logger.info("✓ Discord bot connection active")
            else:
                logger.warning("❌ Discord bot connection lost. Attempting to reconnect...")
                try:
                    await start_discord_bot()
                except Exception as e:
                    logger.error(f"❌ Failed to reconnect Discord bot: {e}")
        except Exception as e:
            logger.error(f"Error in ping_discord_bot: {e}")
        await asyncio.sleep(60)

async def start_discord_bot():
    await client.start(os.getenv("DISCORD_TOKEN"))

# FastAPI lifecycle events
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_discord_bot())
    asyncio.create_task(ping_discord_bot())

@app.on_event("shutdown")
async def shutdown_event():
    if client.is_ready():
        await client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))