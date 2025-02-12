#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Начинаем установку Rule34 бота...${NC}"

# Создание директории
mkdir -p /opt/rule34bot
cd /opt/rule34bot

# Функция для создания файла
create_file() {
    local filename=$1
    local content=$2
    echo "$content" > "$filename"
    echo -e "${GREEN}Создан файл: ${filename}${NC}"
}

# Создание bot.py
echo -e "${YELLOW}Создание bot.py...${NC}"
create_file "bot.py" "$(cat << 'EOF'
[Содержимое bot.py из текущей версии]
EOF
)"

# Создание config.py
echo -e "${YELLOW}Создание config.py...${NC}"
create_file "config.py" "$(cat << 'EOF'
[Содержимое config.py из текущей версии]
EOF
)"

# Создание api_client.py
echo -e "${YELLOW}Создание api_client.py...${NC}"
create_file "api_client.py" "$(cat << 'EOF'
[Содержимое api_client.py из текущей версии]
EOF
)"

# Создание install.sh
echo -e "${YELLOW}Создание install.sh...${NC}"
create_file "install.sh" "$(cat << 'EOF'
[Содержимое install.sh из текущей версии]
EOF
)"

# Установка прав
chmod +x install.sh
chmod 644 bot.py config.py api_client.py

echo -e "${GREEN}Все файлы успешно созданы в /opt/rule34bot${NC}"
echo -e "${YELLOW}Для установки бота выполните:${NC}"
echo -e "./install.sh"