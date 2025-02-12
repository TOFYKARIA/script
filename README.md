# Rule34 Telegram Bot

Telegram бот для поиска изображений с автоматической установкой на Debian 11

## Установка

### Способ 1: Быстрая установка

```bash
# Клонируем репозиторий
git clone https://github.com/your-username/rule34bot
cd rule34bot

# Запускаем установщик
chmod +x install.sh
./install.sh
```

### Способ 2: Пошаговая установка

1. Клонируем репозиторий:
```bash
git clone https://github.com/your-username/rule34bot
cd rule34bot
```

2. Создаём директорию и копируем файлы:
```bash
sudo mkdir -p /opt/rule34bot
sudo cp bot.py config.py api_client.py /opt/rule34bot/
```

3. Устанавливаем зависимости:
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install aiogram aiohttp python-dotenv
```

4. Создаём файл с переменными окружения:
```bash
# Создаём .env файл
echo "BOT_TOKEN=ваш_токен_бота" | sudo tee /opt/rule34bot/.env
```

5. Настраиваем сервис:
```bash
sudo tee /etc/systemd/system/rule34bot.service << 'EOF'
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
```

6. Запускаем бота:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rule34bot
sudo systemctl start rule34bot
```

## Проверка работы

1. Проверить статус:
```bash
sudo systemctl status rule34bot
```

2. Посмотреть логи:
```bash
journalctl -u rule34bot -f
```

## Структура файлов

```
/opt/rule34bot/
├── bot.py         # Основной файл бота
├── config.py      # Конфигурация
├── api_client.py  # Клиент для работы с API
└── .env          # Файл с переменными окружения
```

## Использование

1. Получите токен у @BotFather в Telegram
2. Вставьте токен в файл .env
3. Запустите бота через systemd
4. Используйте inline-режим в любом чате: @имя_вашего_бота запрос

## Команды управления

```bash
# Перезапуск бота
sudo systemctl restart rule34bot

# Остановка бота
sudo systemctl stop rule34bot

# Запуск бота
sudo systemctl start rule34bot
```

## Устранение проблем

Если бот не запускается:

1. Проверьте статус:
```bash
sudo systemctl status rule34bot
```

2. Проверьте логи:
```bash
journalctl -u rule34bot -n 100
```

3. Проверьте права доступа:
```bash
ls -l /opt/rule34bot/
```

4. Проверьте файл .env:
```bash
cat /opt/rule34bot/.env
```
