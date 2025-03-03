# Используем официальный образ Python
FROM python:3.10-slim

# Обновляем и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    clamav \
    clamav-daemon \
    python3-pyclamd \
    pkg-config \
    libmariadb-dev \
    build-essential

# Обновляем базы данных ClamAV
RUN freshclam

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем pip
RUN pip install --upgrade pip

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Указываем порт для приложения
EXPOSE 8000

# Запускаем ClamAV daemon и Django приложение
CMD freshclam && clamav-daemon && python manage.py runserver 0.0.0.0:8000
