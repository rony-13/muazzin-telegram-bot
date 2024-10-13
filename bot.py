import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, filters
from datetime import datetime, timedelta
# importing timezone from pytz module
from pytz import timezone
import asyncio
import os

TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token_here'  # Your Telegram Bot token
CHAT_ID = 'your_telegram_group_id'

# Function to get prayer times from Aladhan API without API key
def get_prayer_times(city, country, date, method=1):
    url = f"https://api.aladhan.com/v1/timingsByCity/{date}?city={city}&country={country}&method={method}&school=1&timezonestring&=Asia/Dhaka"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']['timings']
    else:
        return None

# Calculate Tahajjud time (midpoint between today's Isha and tomorrow's Fajr)
def calculate_tahajjud_time(today_isha_time, tomorrow_fajr_time):
    # Convert times into datetime objects
    isha_dt = datetime.strptime(today_isha_time, '%H:%M')
    fajr_dt = datetime.strptime(tomorrow_fajr_time, '%H:%M')

    # If Fajr is past midnight (after 00:00), adjust the day
    if fajr_dt < isha_dt:
        fajr_dt += timedelta(days=1)

    # Calculate midpoint between Isha and Fajr (Tahajjud time)
    tahajjud_time = isha_dt + (fajr_dt - isha_dt) / 2
    return tahajjud_time.strftime('%H:%M')

# Send prayer times as a response
async def send_prayer_times(update: Update, context):
    try:
        city = context.args[0]
        country = context.args[1]
        method = int(context.args[2]) if len(context.args) > 2 else 1
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /prayer City Country [method]")
        return

    today = datetime.now(timezone('Asia/Dhaka')).strftime("%d-%m-%Y")
    # Get tomorrow's date
    tomorrow = (datetime.now(timezone('Asia/Dhaka')) + timedelta(days=1)).strftime("%d-%m-%Y")
    
    # Get today's prayer times
    today_prayer_times = get_prayer_times(city, country, today, method)
    # Get tomorrow's Fajr time for calculating Tahajjud
    tomorrow_prayer_times = get_prayer_times(city, country, tomorrow, method)
    
    if today_prayer_times and tomorrow_prayer_times:
        fajr_today = datetime.strptime(today_prayer_times['Fajr'], "%H:%M").strftime("%I:%M %p")
        dhuhr = datetime.strptime(today_prayer_times['Dhuhr'], "%H:%M").strftime("%I:%M %p")
        asr = datetime.strptime(today_prayer_times['Asr'], "%H:%M").strftime("%I:%M %p")
        maghrib = datetime.strptime(today_prayer_times['Maghrib'], "%H:%M").strftime("%I:%M %p")
        isha_today = datetime.strptime(today_prayer_times['Isha'], "%H:%M").strftime("%I:%M %p")
        fajr_tomorrow = datetime.strptime(tomorrow_prayer_times['Fajr'], "%H:%M").strftime("%I:%M %p")
        
        # Calculate Tahajjud time
        tahajjud = calculate_tahajjud_time(today_prayer_times['Isha'], tomorrow_prayer_times['Fajr'])
        
        message = (f"Prayer times for {city}, {country}:\n"
                   f"Fajr: {fajr_today}\n"
                   f"Dhuhr: {dhuhr}\n"
                   f"Asr: {asr}\n"
                   f"Maghrib: {maghrib}\n"
                   f"Isha: {isha_today}\n"
                   f"Tahajjud (next day): {tahajjud}")
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Could not retrieve prayer times.")

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Please provide your city and country like this: /prayer City Country [method].")

# Prayer command handler
async def prayer(update: Update, context):
    await send_prayer_times(update, context)

# Automated prayer notifications
async def schedule_prayer_notifications(application):
    while True:
        now = datetime.now(timezone('Asia/Dhaka'))
        # Fixed Dhuhr time at 1:30 PM
        dhuhr_time = now.replace(hour=13, minute=30, second=0, microsecond=0)

        # Fetch prayer times for Asr and Maghrib
        prayer_times = get_prayer_times('Dhaka', 'Bangladesh', datetime.now(timezone('Asia/Dhaka')).strftime("%d-%m-%Y"))  # Change to your default city and country
        fajr_time = datetime.strptime(prayer_times['Fajr'], '%H:%M')
        # dhuhr_time = datetime.strptime(prayer_times['Dhuhr'], '%H:%M') + timedelta(minutes=30)
        asr_time = datetime.strptime(prayer_times['Asr'], '%H:%M') + timedelta(minutes=30)
        maghrib_time = datetime.strptime(prayer_times['Maghrib'], '%H:%M') + timedelta(minutes=10)
        isha_time = datetime.strptime(prayer_times['Isha'], '%H:%M') + timedelta(minutes=35)

        # Check if it's time for any prayer and send a notification
        if now.time().strftime("%H:%M") == fajr_time.time().strftime("%H:%M"):
            await application.bot.send_message(chat_id=CHAT_ID, text="It's time for Fajr. As-Salatu khairun min an-naum, As-Salatu khairun min an-naum.")
            await play_adhan_audio(application)
            print(f'Fajr notified: {fajr_time.time().strftime("%H:%M")}')
        elif now.time().strftime("%H:%M") == dhuhr_time.time().strftime("%H:%M"):
            await application.bot.send_message(chat_id=CHAT_ID, text="It's time for Dhuhr (1:30 PM).")
            await play_adhan_audio(application)
            print(f'Dhuhr notified: {dhuhr_time.time().strftime("%H:%M")}')
        elif now.time().strftime("%H:%M") == asr_time.time().strftime("%H:%M"):
            await application.bot.send_message(chat_id=CHAT_ID, text="It's time for Asr.")
            await play_adhan_audio(application)
            print(f'Asr notified: {asr_time.time().strftime("%H:%M")}')
        elif now.time().strftime("%H:%M") == maghrib_time.time().strftime("%H:%M"):
            await application.bot.send_message(chat_id=CHAT_ID, text="It's time for Maghrib.")
            await play_adhan_audio(application)
            print(f'Magrib notified: {maghrib_time.time().strftime("%H:%M")}')
        elif now.time().strftime("%H:%M") == isha_time.time().strftime("%H:%M"):
            await application.bot.send_message(chat_id=CHAT_ID, text="It's time for Isha.")
            await play_adhan_audio(application)
            print(f'Isha notified: {isha_time.time().strftime("%H:%M")}')

        # Check every minute
        await asyncio.sleep(60)  # Sleep for 60 seconds

async def play_adhan_audio(application):
    # Optionally play an Adhan audio (replace 'audio_file_path' with your own file)
    adhan_path = os.path.join(os.getcwd(), 'allah-ho-akbar-4969.mp3')  # Replace with your file path
    # await application.bot.send_audio(chat_id=CHAT_ID, audio=open(adhan_path, 'rb'))
    with open(adhan_path, 'rb') as adhan_file:
        await application.bot.send_voice(chat_id=CHAT_ID, voice=adhan_file)


def main():
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # bot = application.bot

    # Send the 'Hello, World!' message asynchronously
    # asyncio.run(bot.send_message(chat_id=CHAT_ID, text='Hello, World!'))

    # Add the start and prayer handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('prayer', prayer))

    # Create a new event loop if no loop is currently running
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # No event loop is running
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Schedule the prayer notifications in the background
    loop.create_task(schedule_prayer_notifications(application))

    # Start the bot using polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # No need for asyncio.run() here, simply call the main coroutine
    main()
