manage.py:
	docker-compose -f $(f) run --rm web bash -c "python /home/django/app/manage.py $(cmd)"

run_web:
	docker-compose -f $(f) run --rm web bash -c "$(cmd)"

