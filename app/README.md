## Prerequisites
* Docker or Python3.10+pipenv

## Start the app using Python

In [app](.) directory run:
```shell
pipenv install
pipenv run python run.py
```
The Flask endpoints will be accessible by [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Start the app using Docker

In [app](.) directory run:
```shell
docker build --no-cache -t el-api-db:latest .
docker run --rm -d -p 5000:5000 el-api-db:latest
```

The Flask endpoints will be accessible by [http://127.0.0.1:5000](http://127.0.0.1:5000)