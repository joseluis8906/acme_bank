test:
	cd src && python3 -m unittest *_test.py

run:
	pipenv lock --requirements > requirements.txt
	docker-compose run --service-ports acme_bank	

clean:
	docker-compose down --remove-orphans
