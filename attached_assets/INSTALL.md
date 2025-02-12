curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/setup_bot.sh
chmod +x setup_bot.sh
./setup_bot.sh
```

2. Введите токен бота при запросе:
   - Получите токен у @BotFather в Telegram
   - Вставьте токен в терминал при запросе

## Способ 2: Ручная установка

1. Создайте директорию и перейдите в неё:
```bash
mkdir -p /opt/rule34bot
cd /opt/rule34bot
```

2. Скопируйте файлы одним из способов:

### Через редактор (nano):
```bash
nano bot.py     # Вставьте содержимое bot.py
nano config.py  # Вставьте содержимое config.py
nano api_client.py # Вставьте содержимое api_client.py
nano install.sh # Вставьте содержимое install.sh
```

### Через curl:
```bash
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/bot.py
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/config.py
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/api_client.py
curl -O https://raw.githubusercontent.com/your-repo/rule34bot/main/install.sh
```

3. Установите права и запустите установку:
```bash
chmod +x install.sh
./install.sh
```

## Проверка установки

1. **Проверьте статус сервиса**:
```bash
systemctl status rule34bot
```
Должен показать: `active (running)`

2. **Проверьте логи**:
```bash
journalctl -u rule34bot -f
```
Должны быть видны сообщения о запуске бота

## Использование бота

1. **Inline режим**:
   - В любом чате введите @имя_вашего_бота и поисковый запрос
   - Пример: `@your_bot_name запрос`

2. **Команды**:
   - `/start` - Начало работы с ботом
   - `/r34 запрос` - Поиск по запросу

## Управление ботом

### Основные команды:
```bash
# Перезапуск бота
systemctl restart rule34bot

# Остановка бота
systemctl stop rule34bot

# Запуск бота
systemctl start rule34bot
```

## Устранение проблем

### Бот не запускается:
1. Проверьте статус:
```bash
systemctl status rule34bot
```

2. Проверьте логи:
```bash
journalctl -u rule34bot -n 100
```

3. Проверьте файл .env:
```bash
cat /opt/rule34bot/.env
```

### Ошибки в работе:
1. Проверьте права доступа:
```bash
ls -l /opt/rule34bot/
```
Все файлы должны быть доступны для чтения

2. Проверьте наличие всех файлов:
```bash
ls /opt/rule34bot/
```
Должны быть: bot.py, config.py, api_client.py, .env

3. Перезапустите сервис:
```bash
systemctl restart rule34bot