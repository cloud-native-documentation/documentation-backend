# documentation-backend
## Dependency
Django==4.2.1  
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2  
sqlite3
## Setting up the development environment

```shell
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
## Deployment
```shell
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
