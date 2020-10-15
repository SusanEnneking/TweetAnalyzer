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

If you want to test and don't want to hit Letsencrypt's prod limits, put this line in the env_staging_proxy-companion.env file:
	export ACME_CA_URI=https://acme-staging-v02.api.letsencrypt.org/directory
