# Как запустить Telegram-бота автошколы на Render

1. Распакуйте архив и загрузите содержимое на GitHub в новый репозиторий.
2. Перейдите в Render.com → New → Web Service
3. Подключите репозиторий и укажите:
   - Build command: pip install -r requirements.txt
   - Start command: python bot.py
4. В разделе Environment добавьте переменные:
   - BOT_TOKEN=ваш_токен_бота
   - MANAGER_CHAT_ID=ID_чата_менеджера
5. Нажмите Deploy и бот будет работать.
