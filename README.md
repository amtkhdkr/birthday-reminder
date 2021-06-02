# birthday-reminder

A simple hello world app which demonstrates various DevOps/SRE concepts

This application accepts the user's date of birth as a PUT call and can respond to the user by wishing them on their
birthday or it will mention the number of days till the current year's birth day.

### Example response

- If username’s birthday is in N days:

```shell
{ “message”: “Hello, <username>! Your birthday is in N day(s)” }
```

- If username’s birthday is today:

```shell
{ “message”: “Hello, <username>! Happy birthday!” }
```

### System Details

JSON API is written using [Flask](https://flask.palletsprojects.com/en/2.0.x/) and
[Python](https://www.python.org/downloads/)

User data is persisted in [Postgres](https://www.postgresql.org/download/). The connnection between these two is handled
using the [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) library.

![Block Diagram](docs/block_diagram.png)

### Local test workflow

Build the images and spin up the containers:

```shell
docker-compose up -d --build
docker-compose exec server python manage.py recreate_db
docker-compose exec server python manage.py seed_db
```

Test it out at:

- A ping response from the container at [http://localhost:8080/](http://localhost:8080/)
- All entries visible at [http://localhost:8080//hello/all](http://localhost:8080//hello/all)
- To see the details of a new user:

```shell
  curl http://localhost:5000/hello/ironman
```

- To add a new username you can use the PUT verb

```shell
  curl -X PUT -d '{"dateOfBirth":"1993-01-01"}' -H "Content-Type: application/json" localhost:8080/hello/captainmarvel
```

When you want to shut down the application:

`docker-compose down`

The postgresql database image uses a very simple SQL database [create.sql](services/db/create.sql) which is needed to initialize the database with the
proper table to contain the names and birthday dates schema.


#### Deployment Requirements
If you are using Cloud Shell, skip to the next section.

1. Install gcloud <https://cloud.google.com/sdk/install>
2. Install kubectl <https://kubernetes.io/docs/tasks/tools/install-kubectl/>
3. Install docker <https://docs.docker.com/install/>

#### Google Container Registry Image Setup
You can use the provided cloud build files to build and push images of the App and Database for use in K8s.

[cloudbuild.yaml](services/app/cloudbuild.yaml) for Flask App helps create image: gcr.io/birthday-reminder-amt/birthday-reminder:1.0.0

[cloudbuild.yaml](services/db/cloudbuild.yaml) for Postgres DB helps create image: gcr.io/birthday-reminder-amt/birthday-reminder-db:1.0.0

#### Create a GKE cluster
- Enable Google Cloud and set up region and zone.
    `gcloud init`
- Enable the GKE API & billing:
    `gcloud services enable container.googleapis.com`

Send request to the service:

```shell
curl -w "\n" $(kubectl get svc birthday-reminder -ojsonpath='{.status.loadBalancer.ingress[0].ip}')
```
Visit [Trace List](https://console.cloud.google.com/traces/list) to check traces generated.
    Click on any trace in the graph to see the Waterfall View.

Clean up GKE cluster/pods/services
```shell
gcloud container clusters delete demo
```
