# TweetAnalyzer
Twitter Research Data Retrieval And Analysis

View sqlite3 db:
	python manage.py dbshell
	.tables will show all tables
	PRAGMA table_info(table_name) will list all columns

Generate Django Secret Key: (thanks https://humberto.io/blog/tldr-generate-django-secret-key/)
	python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

Used this tutorial to begin Digital Ocean Terraform set-up:
	https://www.digitalocean.com/community/tutorials/how-to-use-terraform-with-digitalocean
