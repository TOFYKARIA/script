# Инструкция по копированию файлов

## Способ 1: Через командную строку

1. Создайте директорию и перейдите в неё:
```bash
mkdir -p /opt/rule34bot
cd /opt/rule34bot
```

2. Скопируйте файлы, используя команду curl:
```bash
# Загрузка bot.py
curl -o bot.py https://raw.githubusercontent.com/your-repo/rule34bot/main/bot.py

# Загрузка config.py
curl -o config.py https://raw.githubusercontent.com/your-repo/rule34bot/main/config.py

# Загрузка install.sh
curl -o install.sh https://raw.githubusercontent.com/your-repo/rule34bot/main/install.sh
```

## Способ 2: Через редактор кода

1. Создайте файлы через редактор:
```bash
cd /opt/rule34bot
nano bot.py     # Вставьте содержимое bot.py
nano config.py  # Вставьте содержимое config.py
nano install.sh # Вставьте содержимое install.sh
```

## Способ 3: Через графический интерфейс

1. Откройте файловый менеджер
2. Перейдите в директорию `/opt/rule34bot`
3. Создайте новые файлы с соответствующими именами
4. Скопируйте содержимое каждого файла через буфер обмена

## После копирования

1. Установите правильные права доступа:
```bash
chmod +x install.sh  # Делаем скрипт установки исполняемым
chmod 644 bot.py config.py  # Устанавливаем права на чтение для файлов
```

2. Проверьте наличие всех файлов:
```bash
ls -l /opt/rule34bot
```

Вы должны увидеть:
- bot.py
- config.py
- install.sh

## Проверка целостности файлов

Убедитесь, что все файлы скопированы корректно:
```bash
cat bot.py | wc -l     # Должно быть около 290 строк
cat config.py | wc -l  # Должно быть около 31 строки
cat install.sh | wc -l # Должно быть около 77 строк
```
