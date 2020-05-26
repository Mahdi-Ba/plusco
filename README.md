
![](https://gpapp.gardeshpay.com/static/img/gardeshpayfinal.png)
## Requirements
- Python (3.5, 3.6, 3.7, 3.8)
- Mysql (optional)
## Installation 
- Create  virtual environment(optional)
- Install the dependencies and devDependencies  
```sh
$ pip install -r requirements.txt
```

- Copy  talent/settings_sample.py to  talent/settings.py
```sh
$ cp  settings_sample.py settings.py
```
- Set DataBase Connection in talent/settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test@test',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
        },
    }
}
```
- Create Table In DataBase   
```sh
$ python manage.py migrate
```
- Create Super User
```sh
$ python manage.py createsuperuser
```
- Run Server and admin route  http://127.0.0.1:8000/admin
```sh
$ python manage.py runserver
```


License
----

Gardeshpay
