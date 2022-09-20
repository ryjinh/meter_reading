setup:
	python3 manage.py makemigrations api && python3 manage.py migrate &&\
	python3 manage.py file_processor meter_reading/resources/flow_files/ &&\
	python3 manage.py createsuperuser --username admin --email "" --skip-checks

.PHONY: setup