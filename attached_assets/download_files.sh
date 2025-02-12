#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Начинаем загрузку файлов для Rule34 бота...${NC}"

# Создание директории
mkdir -p /opt/rule34bot
cd /opt/rule34bot

# Загрузка файлов с помощью curl
echo -e "${YELLOW}Загрузка bot.py...${NC}"
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/bot.py

echo -e "${YELLOW}Загрузка config.py...${NC}"
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/config.py

echo -e "${YELLOW}Загрузка api_client.py...${NC}"
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/api_client.py

echo -e "${YELLOW}Загрузка install.sh...${NC}"
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/install.sh

# Установка прав
chmod +x install.sh
chmod 644 bot.py config.py api_client.py

echo -e "${GREEN}Все файлы успешно загружены в /opt/rule34bot${NC}"
echo -e "${YELLOW}Для установки бота выполните:${NC}"
echo -e "./install.sh"