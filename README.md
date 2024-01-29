# Proballer team scraper

## Requirements

- Docker: https://www.docker.com/
- Python v3+: https://www.python.org/downloads/ (https://www.youtube.com/watch?v=2faQMy72k3A)

### Get Started with the script

```shell
pip install requests
pip install beautifulsoup4 mysql-connector-python
pip install pandas
pip install lxml
```

### Get started with mysql database

```shell
docker run -it --rm --name mysql -p3306:3306 -v mysql-volume:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=proballer mysql:8.3.0
docker exec -it mysql bash
mysql -u root -p
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
```

You can view and manage data with Dbeaver.