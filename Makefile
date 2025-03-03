.PHONY: install_dependencies migrate makemessages compilemessages update_clamav

# Установка зависимостей
install_dependencies:
	@echo "Checking if requirements.txt changed..."
	pip install -r requirements.txt;

# Применение миграций
migrate:
	docker exec -it django python manage.py makemigrations && docker exec -it django python manage.py migrate

# Генерация файлов переводов
translate:
	docker exec -it django sh -c "apt-get update && apt-get install -y gettext && python manage.py makemessages -l ru -l en -l de -i 'venv' -i 'static' -i 'node_modules' -i 'media'"
	docker exec -it django sh -c "chown -R 1000:1000 /app/locale"

# Компиляция файлов переводов
compile:
	docker exec -it django sh -c "apt-get update && apt-get install -y gettext && python manage.py compilemessages"

# Обновление базы данных ClamAV
update_clamav:
	docker exec -it clam freshclam

static:
	docker exec -it django python manage.py collectstatic

test:
	docker exec -it django python manage.py test blog.tests

superuser:
	docker exec -it django python manage.py createsuperuser