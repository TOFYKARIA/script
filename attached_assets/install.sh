#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Установка Rule34 Telegram бота...${NC}"

# Проверка наличия Python и pip
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Установка Python...${NC}"
    apt update
    apt install -y python3 python3-pip
fi

# Создание директории
echo -e "${YELLOW}Создание директории...${NC}"
mkdir -p /opt/rule34bot/logs
cd /opt/rule34bot

# Установка зависимостей
echo -e "${YELLOW}Установка зависимостей...${NC}"
pip3 install aiogram aiohttp python-dotenv

# Создание .env файла
echo -e "${YELLOW}Настройка конфигурации...${NC}"
if [ ! -f .env ]; then
    echo -e "${GREEN}Введите токен бота от @BotFather:${NC}"
    read -r token
    echo "BOT_TOKEN=$token" > .env
    echo -e "${GREEN}Токен сохранен в файле .env${NC}"
else
    echo -e "${YELLOW}Файл .env уже существует${NC}"
fi

# Проверка наличия необходимых файлов
required_files=("bot.py" "config.py" "api_client.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}Ошибка: файл $file не найден${NC}"
        echo -e "Пожалуйста, убедитесь что все необходимые файлы скопированы в директорию"
        exit 1
    fi
done

# Создание systemd сервиса
echo -e "${YELLOW}Настройка автозапуска...${NC}"
SERVICE_FILE="/etc/systemd/system/rule34bot.service"

if [ ! -f "$SERVICE_FILE" ]; then
    echo -e "${YELLOW}Создание systemd сервиса...${NC}"
    cat > "$SERVICE_FILE" << 'EOF'
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

    systemctl daemon-reload
    systemctl enable rule34bot
    systemctl start rule34bot
    echo -e "${GREEN}Сервис создан и запущен${NC}"
else
    echo -e "${YELLOW}Сервис уже существует${NC}"
    systemctl restart rule34bot
fi

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
echo -e "Для проверки статуса используйте: ${YELLOW}systemctl status rule34bot${NC}"
echo -e "Для просмотра логов используйте: ${YELLOW}journalctl -u rule34bot -f${NC}"