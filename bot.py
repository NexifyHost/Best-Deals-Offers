from telethon.sync import TelegramClient
from telegram import Bot
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Replace with your details
api_id = 'your_api_id'
api_hash = 'your_api_hash'
bot_token = 'your_bot_token'
channel_username = 'channel_you_want_to_scrape'
my_channel_username = '@your_channel_username'
amazon_in_affiliate_tag = 'your_amazon_in_affiliate_tag'
amazon_com_affiliate_tag = 'your_amazon_com_affiliate_tag'
username = 'your_amazon_affiliate_email'
password = 'your_amazon_affiliate_password'
chrome_driver_path = 'path_to_chromedriver'

# Function to extract URLs from messages
def extract_links(message):
    return [word for word in message.split() if word.startswith('http')]

# Function to replace links with your affiliate link
def replace_with_affiliate_link(link):
    if 'amazon.in' in link:
        # Process Amazon.in link
        if 'dp/' in link:
            product_id = link.split('dp/')[1].split('/')[0]
        elif 'product/' in link:
            product_id = link.split('product/')[1].split('/')[0]
        else:
            return link
        # Build Amazon.in link with affiliate tag
        new_link = f"https://www.amazon.in/dp/{product_id}?tag={amazon_in_affiliate_tag}"
        return new_link
    elif 'amazon.com' in link:
        # Process Amazon.com link
        if 'dp/' in link:
            product_id = link.split('dp/')[1].split('/')[0]
        elif 'product/' in link:
            product_id = link.split('product/')[1].split('/')[0]
        else:
            return link
        # Build Amazon.com link with affiliate tag
        new_link = f"https://www.amazon.com/dp/{product_id}?tag={amazon_com_affiliate_tag}"
        return new_link
    return link

# Function to log in to Amazon and get the shortened link using Selenium
def shorten_amazon_link(driver, long_url):
    driver.get(f'https://affiliate-program.amazon.com/home/productlinks/shortlinks?ac-ms-url={long_url}')
    time.sleep(5)
    short_link_element = driver.find_element(By.ID, 'shorten-url-input')
    short_link = short_link_element.get_attribute('value')
    return short_link

# Function to login to Amazon Affiliate using Selenium
def login_to_amazon_affiliate(driver):
    driver.get('https://affiliate-program.amazon.com/')
    driver.find_element(By.ID, 'ap_email').send_keys(username)
    driver.find_element(By.ID, 'continue').click()
    time.sleep(2)
    driver.find_element(By.ID, 'ap_password').send_keys(password)
    driver.find_element(By.ID, 'signInSubmit').click()

# Function to forward the shortened link to your Telegram channel
def forward_to_channel(short_link):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=my_channel_username, text=short_link)

# Initialize WebDriver for Selenium
chrome_service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service)

# Login to Amazon Affiliate account
login_to_amazon_affiliate(driver)

# Telegram client setup to scrape messages
client = TelegramClient('session_name', api_id, api_hash)

# Main function to scrape the channel, replace links, shorten and forward
async def scrape_channel():
    async with client:
        async for message in client.iter_messages(channel_username):
            if message.message:
                links = extract_links(message.message)
                for link in links:
                    # Check if the link is an Amazon link and process accordingly
                    affiliate_link = replace_with_affiliate_link(link)
                    
                    if 'amazon.in' in affiliate_link:
                        # Shorten link for amazon.in
                        short_link = shorten_amazon_link(driver, affiliate_link)
                    elif 'amazon.com' in affiliate_link:
                        # Shorten link for amazon.com
                        short_link = shorten_amazon_link(driver, affiliate_link)
                    else:
                        short_link = affiliate_link  # If not Amazon, use original

                    # Forward the shortened link to your own channel
                    forward_to_channel(short_link)

client.start()
client.loop.run_until_complete(scrape_channel())

# Quit WebDriver after task completion
driver.quit()
