#!/bin/bash

# Создание директории
mkdir -p /opt/rule34bot
cd /opt/rule34bot

# Скачивание файлов
wget -O bot.py https://raw.githubusercontent.com/your-repo/rule34bot/main/bot.py
wget -O config.py https://raw.githubusercontent.com/your-repo/rule34bot/main/config.py
wget -O api_client.py https://raw.githubusercontent.com/your-repo/rule34bot/main/api_client.py

# Установка прав
chmod 644 bot.py config.py api_client.py

echo "Файлы успешно загружены в /opt/rule34bot"
