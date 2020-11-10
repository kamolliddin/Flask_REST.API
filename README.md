# REST API With Flask & SQL Alchemy

> Item CRUD API using Python Flask, SQL Alchemy, Marshmallow

## Installation 

``` bash

$ pipenv shell
$ pipenv install
$ python
>> from app import db
>> db.create_all()
>> exit()
python app.py
```

## Endpoints

* GET     /item
* GET     /item/:id
* POST    /item
* PUT     /item/:id
* DELETE  /item/:id
