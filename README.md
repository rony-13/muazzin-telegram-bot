# muazzin-telegram-bot
This bot is to call for prayer during office hours at Dhaka. Also it sends back prayers times for today on request

# Telegram Prayer Time Bot with Hadith Translation

A Python-based Telegram bot that provides prayer times, plays the Adhan audio, and sends a daily random Hadith with translation in Bengali.

## Features

- Fetches prayer times for any city using the Aladhan API.
- Automatically sends prayer notifications (Fajr, Dhuhr, Asr, Maghrib, Isha) with configurable delays.
- Plays Adhan audio at the prayer times.
- Sends a random Hadith daily from Sahih al-Bukhari, with translation options.
- Supports Markdown and HTML formatting for beautifully styled messages.
- Can translate the Hadith to Bengali using `deep_translator` or Google Translate API.

## Requirements

- Python 3.7+
- Telegram Bot API token
- Libraries:
  - `python-telegram-bot`
  - `httpx`
  - `deep-translator` (or Google Cloud Translation API if using Google Translate)
  - `requests`
  - `pytz`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/prayer-time-bot.git
    cd muazzin-telegram-bot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Telegram Bot:
   - Create a bot using [BotFather](https://core.telegram.org/bots#botfather) and get the bot token.
   - Replace the `TELEGRAM_BOT_TOKEN` in the code with your own bot token.

4. Optionally, set up Google Cloud Translation API:
   - Enable the Google Cloud Translation API in your [Google Cloud Console](https://cloud.google.com/translate/docs/setup).
   - Generate an API key and store it in your environment variables.

5. Update your environment variables:
    - In a `.env` file or system environment variables:
      ```bash
      TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
      GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"  # Optional, only if using Google Translate
      ```

## Usage

Run the bot with the following command:

```bash
python bot.py
```

The bot will automatically start polling Telegram updates and respond to commands:

### Commands

- `/start` - Start the bot and see instructions.
- `/prayer City Country [method]` - Get prayer times for your location.
  Example: `/prayer Dhaka Bangladesh`

### Automatic Features

- The bot will automatically send prayer notifications and play Adhan audio at specified times.
- A random Hadith is sent daily in English, with optional translation to Bengali.

## Configuration

You can configure the bot by modifying `bot.py` to set default city, country, or customize notification times.

- **Prayer Notification Times**: Configured within the `schedule_prayer_notifications` function.
- **Adhan Audio**: Ensure the correct path for the Adhan audio is set in the `play_adhan_audio` function.

## Translation

The bot can translate Hadith text into Bengali using:

- **deep_translator**: A simple and effective translation library.
- **Google Cloud Translation API**: For more advanced translation needs, using Google’s API.

## Running as a `systemd` Service on Ubuntu

To run the Telegram bot as a `systemd` service on Ubuntu, follow these steps:

### 1. Create the `systemd` Service File

1. **Create a new systemd service file** for the bot:
    ```bash
    sudo nano /etc/systemd/system/telegram-bot.service
    ```

2. **Add the following content** to the file:
    ```ini
    [Unit]
    Description=Telegram Prayer Time Bot Service
    After=network.target

    [Service]
    User=your_user_name_here
    WorkingDirectory=/path/to/your/bot
    ExecStart=/usr/bin/python3 /path/to/your/bot/bot.py
    Restart=on-failure
    Environment="TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here"
    Environment="GOOGLE_API_KEY=your_google_api_key_here"  # Optional

    [Install]
    WantedBy=multi-user.target
    ```

    - Replace `your_user_name_here` with your Linux username.
    - Update the paths for `WorkingDirectory` and `ExecStart` to point to your bot directory and Python script.
    - Add your `TELEGRAM_BOT_TOKEN` and any other environment variables.

### 2. Enable and Start the Service

1. **Reload `systemd`** to recognize the new service:
    ```bash
    sudo systemctl daemon-reload
    ```

2. **Enable the service** so that it starts on boot:
    ```bash
    sudo systemctl enable telegram-bot.service
    ```

3. **Start the service**:
    ```bash
    sudo systemctl start telegram-bot.service
    ```

4. **Check the status** to ensure the bot is running:
    ```bash
    sudo systemctl status telegram-bot.service
    ```

### 3. Logs and Debugging

To view logs for the bot:
```bash
journalctl -u telegram-bot.service -f
```

This will help you track and debug any issues if the bot doesn't start or crashes.

### 4. Stopping and Restarting the Service

To stop the bot:
```bash
sudo systemctl stop telegram-bot.service
```

To restart the bot:
```bash
sudo systemctl restart telegram-bot.service
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add your feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Issues and Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/rony-13/muazzin-telegram-bot/issues).
