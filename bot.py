from telethon.sync import TelegramClient
from telegram import Bot
import requests

api_id = 'your_api_id'
api_hash = 'your_api_hash'
channel_username = 'channel_you_want_to_scrape'
bot_token = 'your_bot_token'
affiliate_tag = 'your_affiliate_tag'
bitly_token = 'your_bitly_token'
client = TelegramClient('session_name', api_id, api_hash)

def extract_links(message):
    # Function to extract URLs from the message text
    return [word for word in message.split() if word.startswith('http')]

def replace_with_affiliate_link(link):
    if 'amazon' in link:
        if 'dp/' in link:
            product_id = link.split('dp/')[1].split('/')[0]
        elif 'product/' in link:
            product_id = link.split('product/')[1].split('/')[0]
        else:
            return link
        new_link = f"https://www.amazon.com/dp/{product_id}?tag={affiliate_tag}"
        return new_link
    return link

def shorten_amazon_link(link):
    headers = {
        'Authorization': f'Bearer {bitly_token}',
        'Content-Type': 'application/json',
    }
    data = {"long_url": link}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('link')
    return link

def forward_to_channel(short_link):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id='@your_channel_username', text=short_link)

async def scrape_channel():
    async with client:
        async for message in client.iter_messages(channel_username):
            if message.message:
                links = extract_links(message.message)
                for link in links:
                    affiliate_link = replace_with_affiliate_link(link)
                    short_link = shorten_amazon_link(affiliate_link)
                    forward_to_channel(short_link)

client.start()
client.loop.run_until_complete(scrape_channel())
