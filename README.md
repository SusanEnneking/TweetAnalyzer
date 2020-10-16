# TweetAnalyzer


## Twitter Research Data Retrieval And Analysis ##

Before you can use this code, you'll need to get a developer account from [Twitter](https://developer.twitter.com/en/apply-for-access). Back when I did it, it took a few days for Twitter to approve my request and provide keys.

Once you have keys and you've set up your [app](https://developer.twitter.com/en/apps/create), you are ready to use this code.

To get started, if you want to use Vagrant, download [Vagrant](https://www.vagrantup.com/docs/installation) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads) on your host machine. And create the directory you want the project in and navigate to that directory.  Then...

1. Vagrant Up.  This will use the VagrantFile info to build your vagrant machine and provision it with the lines in provision.sh.

2. Vagrant ssh into your vagrant box and cd /vagrant.

3. Source your environement. Use env.sample to set up your environment variables. The base configuration will use sqllite, so you don't have to have a postgresdb to run it.

4. Start the django server.

5. Set yourself up as an admin (python manage.py createsuperuser)

You'll need to increase the allowed number of tweets in the researcher table because the default is zero.

Now you can log in as the super user you just created and get going.  

#### Helpful Info (as in I can't remember anything) ####

##### View sqlite3 db: #####
	python manage.py dbshell
	.tables will show all tables
	PRAGMA table_info(table_name) will list all columns

##### Generate Django Secret Key: --thanks [Humberto Rocha](https://humberto.io/blog/tldr-generate-django-secret-key/) #####
	python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

##### Used [Jan Giacomelli's tutorial](https://testdriven.io/blog/django-lets-encrypt/) for [my current production set up](https://tweetsforresearch.com) #####
	I wasn't using their base project so a few things were different.  Mostly, I didn't try to set up the Postgresql db on the same server.  I have it set up on a managed db server in Digtial Ocean.


##### Used [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-terraform-with-digitalocean) to begin Digital Ocean Terraform set-up: #####
	I didn't end up using this set_up.  The Terraform for my current Digital Ocean set up is a Todo item.

##### If you want to test a staging deploy and don't want to hit Letsencrypt's prod limits, put this line in the env_staging_proxy-companion.env file: #####
	export ACME_CA_URI=https://acme-staging-v02.api.letsencrypt.org/directory

##### Helpful Docker Commands: #####
	docker system prune (get rid of all containers once you don't need them)
	docker-compose -f docker-compose.prod.yml down -v (stop all of your running containers)
	docker-compose -f docker-compose.prod.yml up -d --build (build and bring containers up)
	sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear (collect static files)
	docker logs {container id} (show container logs)
	docker ps -a (list containers) (list container ids)
	docker exec -it {container id} bash (open shell in container)
