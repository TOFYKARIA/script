#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Начинаем установку бота...${NC}"

# 1. Обновление системы и установка зависимостей
echo -e "${YELLOW}Установка системных зависимостей...${NC}"
apt update
apt install -y python3-pip

# 2. Установка Python библиотек
echo -e "${YELLOW}Установка Python библиотек...${NC}"
pip3 install aiogram aiohttp

# 3. Создание структуры директорий
echo -e "${YELLOW}Создание структуры проекта...${NC}"
mkdir -p /opt/telegram_bot/logs

# 4. Создание скрипта автозапуска
echo -e "${YELLOW}Создание скрипта автозапуска...${NC}"
cat > /opt/telegram_bot/start_bot.sh << 'EOF'
#!/bin/bash
cd /opt/telegram_bot
nohup python3 bot.py > logs/bot.log 2>&1 &
EOF

chmod +x /opt/telegram_bot/start_bot.sh

# 5. Добавление в crontab
echo -e "${YELLOW}Настройка автозапуска...${NC}"
(crontab -l 2>/dev/null; echo "@reboot /opt/telegram_bot/start_bot.sh") | crontab -

# 6. Запрос токена бота
echo -e "${YELLOW}Настройка токена бота...${NC}"
read -p "Введите токен бота от BotFather: " bot_token
echo "BOT_TOKEN=$bot_token" > /opt/telegram_bot/.env

echo -e "${GREEN}Установка завершена!${NC}"
echo -e "${GREEN}Теперь вставьте код бота в файл /opt/telegram_bot/bot.py${NC}"
echo -e "${GREEN}и запустите бота командой:${NC}"
echo -e "${YELLOW}cd /opt/telegram_bot && nohup python3 bot.py > logs/bot.log 2>&1 &${NC}"
