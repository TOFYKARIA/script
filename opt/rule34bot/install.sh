#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Установка Rule34 Telegram бота...${NC}"

# Проверка root прав
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Запустите скрипт с правами root (sudo)${NC}"
    exit 1
fi

# Установка зависимостей
echo -e "${YELLOW}Установка системных зависимостей...${NC}"
apt update
apt install -y python3 python3-pip

# Установка Python библиотек
echo -e "${YELLOW}Установка Python библиотек...${NC}"
pip3 install aiogram aiohttp python-dotenv

# Создание директорий
echo -e "${YELLOW}Настройка директорий...${NC}"
mkdir -p /opt/rule34bot/logs
cd /opt/rule34bot

# Настройка окружения
echo -e "${YELLOW}Настройка конфигурации...${NC}"
if [ ! -f .env ]; then
    echo -e "${GREEN}Введите токен бота от @BotFather:${NC}"
    read -r token
    echo "BOT_TOKEN=$token" > .env
    echo -e "${GREEN}Токен сохранен в файле .env${NC}"
fi

# Создание systemd сервиса
echo -e "${YELLOW}Настройка автозапуска...${NC}"
cat > /etc/systemd/system/rule34bot.service << EOF
[Unit]
Description=Rule34 Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/rule34bot
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=/opt/rule34bot/.env
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd и запуск сервиса
systemctl daemon-reload
systemctl enable rule34bot
systemctl start rule34bot

# Проверка статуса
echo -e "${YELLOW}Проверка статуса бота...${NC}"
sleep 2
if systemctl is-active --quiet rule34bot; then
    echo -e "${GREEN}Бот успешно установлен и запущен!${NC}"
else
    echo -e "${YELLOW}Внимание: Бот установлен, но есть проблемы с запуском${NC}"
    echo -e "Проверьте логи командой: ${YELLOW}journalctl -u rule34bot -n 50${NC}"
fi

echo -e "\n${GREEN}Установка завершена!${NC}"
echo -e "Для управления ботом используйте следующие команды:"
echo -e "${YELLOW}systemctl status rule34bot${NC} - проверка статуса"
echo -e "${YELLOW}systemctl restart rule34bot${NC} - перезапуск бота"
echo -e "${YELLOW}systemctl stop rule34bot${NC} - остановка бота"
echo -e "${YELLOW}journalctl -u rule34bot -f${NC} - просмотр логов"
