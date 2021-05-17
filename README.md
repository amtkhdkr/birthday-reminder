# birthday-reminder
A simple hello world app which demonstrates various DevOps/SRE concepts


### Docker

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

Run the migrations and seed the database:

```sh
$ docker-compose exec server python manage.py recreate_db
$ docker-compose exec server python manage.py seed_db
```

Test it out at:

1. A ping response from the container at [http://localhost:5001/](http://localhost:5001/)
2. All entries visible at [http://localhost:5001//hello/all](http://localhost:5001//hello/all)
