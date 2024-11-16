import os
import asyncio
import logging
from typing import List
from fastapi import FastAPI
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

def parse_mentions(mentions_str: str) -> List[str]:
    """Parse comma-separated mentions string into a list of user IDs."""
    if not mentions_str:
        return []
    return [mention.strip() for mention in mentions_str.split(',')]

# Template commands with ping support
@tree.command(name="checkpoint_minor", description="Denies access to underage users")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template1(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template1']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

    await interaction.response.send_message(response_message)

@tree.command(name="checkpoint_format", description="Denies access to user because of wrong RP sample format or invalid access")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template2(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template2']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

@tree.command(name="checkpoint_literacy", description="Denies access to user because of insufficient literacy")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template3(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template3']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

@tree.command(name="checkpoint_fixes", description="Denies access to user because of needed fixes in RP sample")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template4(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template4']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

@tree.command(name="checkpoint_approved", description="Allows access to user and changes user roles")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template5(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template5']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

    roles_to_add = ["1307013628326580295", "1307013626200326205"]
    role_to_remove = "1307013626917421088"
    successful_updates = []
    failed_updates = []

    logger.info(f"Starting role update process for mentions: {mention_list}")

    for user_id in mention_list:
        logger.info(f"Processing user ID: {user_id.strip('<@!>')}")
        user = interaction.guild.get_member(int(user_id.strip('<@!>')))
        
        if user:
            logger.info(f"Found user: {user.name} with ID: {user.id}")
            try:
                for role_id in roles_to_add:
                    role = interaction.guild.get_role(role_id)
                    if role and role not in user.roles:
                        await user.add_roles(role)
                        successful_updates.append(f"Added {role.name} to {user.mention}")
                        logger.info(f"Successfully added role {role.name} to {user.mention}")

                role = interaction.guild.get_role(role_to_remove)
                if role and role in user.roles:
                    await user.remove_roles(role)
                    successful_updates.append(f"Removed {role.name} from {user.mention}")
                    logger.info(f"Successfully removed role {role.name} from {user.mention}")

            except Exception as e:
                failed_updates.append(f"{user.mention}: {str(e)}")
                logger.error(f"Failed to update roles for {user.mention}: {str(e)}")

        else:
            logger.warning(f"User  with ID {user_id.strip('<@!>')} not found in the guild.")

    # Send the ephemeral message with the results
    ephemeral_message = "Roles updated successfully for:\n" + "\n".join(successful_updates) if successful_updates else "No roles were updated successfully."

    if failed_updates:
        ephemeral_message += "\n\nFailed to update roles for:\n" + "\n".join(failed_updates)

    await interaction.followup.send(ephemeral_message, ephemeral=True)

@tree.command(name="bio_inconsistency", description="Denies bio approval because user didn't follow instructions or didn't read RP info")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template6(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template6']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

@tree.command(
    name="bio_fixes",
    description="Denies bio approval because fixes are to be made. Include fixes in up to 5 comments"
)
@app_commands.describe(
    mentions="Users to ping (comma-separated, e.g., @user1, @user2)",
    comment1="First paragraph (required)",
    comment2="Second paragraph (optional)",
    comment3="Third paragraph (optional)",
    comment4="Fourth paragraph (optional)",
    comment5="Fifth paragraph (optional)"
)
async def post_template7(
    interaction: Interaction,
    mentions: str,
    comment1: str,
    comment2: str = None,
    comment3: str = None,
    comment4: str = None,
    comment5: str = None
):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return

    comments = [f"**[1]** :: {comment1}"]
    optional_comments = [comment2, comment3, comment4, comment5]
    for i, comment in enumerate(optional_comments, start=2):
        if comment:
            comments.append(f"> **[{i}]** :: {comment}")

    template = """
> Thank you for submitting your character.
> We appreciate the effort you've put into it.
> However, after careful review, there are
> some elements of your submission that
> need attention. Address them carefully:
> 
> {comments}
> 
> 
> We encourage you to revise and resubmit
> your character once you've addressed the
> fixes. If after careful revision you would like
> specific examples or further guidance, feel
> free to reach out—we'd be happy to help!
> Looking forward to reading your improved
> writing sample. Best regards,

*⸻ 𝐓𝐡𝐞 𝐒𝐭𝐚𝐟𝐟 𝐓𝐞𝐚𝐦*
    """.strip().format(comments="\n> \n".join(comments))

    response_message = template+"\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

@tree.command(name="bio_approved", description="Approves bio and changes user roles")
@app_commands.describe(mentions="Users to ping (comma-separated, e.g., @user1, @user2)")
async def post_template8(interaction: Interaction, mentions: str):
    if not has_required_role(interaction.user.roles):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    response_message = f"{TEMPLATES['template8']}\n"
    
    if mentions:
        mention_list = parse_mentions(mentions)
        if mention_list:
            ping_message = " ".join(mention_list)
            response_message += f"{ping_message}\n``` ```"

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