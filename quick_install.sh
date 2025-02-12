#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Установка Rule34 Telegram бота на VDS...${NC}"

# Создание рабочей директории
echo -e "${YELLOW}Создание рабочей директории...${NC}"
mkdir -p /opt/rule34bot
cd /opt/rule34bot

# Установка зависимостей
echo -e "${YELLOW}Установка зависимостей...${NC}"
apt update
apt install -y python3 python3-pip
pip3 install aiogram aiohttp python-dotenv

# Копирование файлов бота
echo -e "${YELLOW}Копирование файлов бота...${NC}"
cat > /opt/rule34bot/bot.py << 'EOF'
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для поиска изображений.")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Отправьте мне поисковый запрос для поиска изображений.")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Ваш запрос принят, ищу изображения...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
EOF

cat > /opt/rule34bot/.env << EOF
BOT_TOKEN=7948912217:AAEfU6sD3XQfXNaVpPM3XPJKvRvC0mOOfQM
EOF

# Настройка службы systemd
echo -e "${YELLOW}Настройка автозапуска...${NC}"
cat > /etc/systemd/system/rule34bot.service << 'EOF'
[Unit]
Description=Rule34 Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/rule34bot
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Запуск бота
systemctl daemon-reload
systemctl enable rule34bot
systemctl start rule34bot

echo -e "${GREEN}Установка завершена!${NC}"
echo -e "Для проверки статуса используйте: ${YELLOW}systemctl status rule34bot${NC}"
echo -e "Для просмотра логов используйте: ${YELLOW}journalctl -u rule34bot -f${NC}"