apt-get -y update
apt install -y python3.8
apt install -y python3-pip
python3 -m pip install Django
apt-get install sqlite3 libsqlite3-dev
pip3 install django-request-logging
#following needed for postgres
apt-get install -y libpq-dev python-dev
pip3 install psycopg2
pip3 install cryptography==2.3
pip3 install requests==2.20.0
pip3 install httplib2==0.18.0
pip3 install pyxdg==0.26
pip3 install twisted==20.3.0
pip3 install urllib3==1.24.2

#get docker
wget -qO- https://get.docker.com | sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose



