up:
	docker-compose up --build

build:
	docker-compose build

down:
	docker-compose down

#c=<command>
run:
	docker-compose exec app python manage.py $(c)