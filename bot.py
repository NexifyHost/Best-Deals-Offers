from telethon import TelegramClient, events
import requests
from shortener import Shortener

# Replace with your bot's API ID, API hash, and Amazon affiliate ID
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
affiliate_id = 'YOUR_AFFILIATE_ID'

# Create a Telegram client
client = TelegramClient('session', api_id, api_hash)

# Initialize shortener
shortener = Shortener()

@client.on(events.NewMessage(pattern=r'https?://.*'))
async def handle_link(event):
    # Extract the link from the message
    link = event.text

    # Modify the link with your affiliate ID
    modified_link = link.replace("amazon.com", f"amazon.com?tag={affiliate_id}")

    # Create a shortlink
    short_link = shortener.short(modified_link)

    # Forward the shortlink to your own channel
    await client.send_message('YOUR_CHANNEL_ID', short_link)

with client:
    client.run_until_disconnected()
