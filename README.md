<p align="center">
  <a href="https://www.openroboticmetaverse.org">
    <img alt="orom" src="https://raw.githubusercontent.com/openroboverse/knowledge-base/main/docs/assets/icon.png" width="100" />
  </a>
</p>
<h1 align="center">
  🤖 open robotic metaverse - robotics platform 🌐
</h1>

## Overview 🔍

This project serves as the backend of the robotic metaverse, that brings robotic projects in one place.


## Technology Stack 🛠️
- Backend Framework: Django and Django REST
- Database: Postgres

## Setup ⚙️

1. Clone the Repo 📥

```bash
git clone https://github.com/openroboticmetaverse/orom_backend.git
```

```bash
cd orom_backend
```

2. Docker Compose 🐳

```bash
docker compose up
```
The server will automatically start. Sometimes only the database but not the webserver starts. Then run instead:
```bash
docker compose up --build
```

3. On the first startup: After starting the docker container open a second terminal and run:
```bash
docker exec -it orom_backend bash
```
```bash
cd orom_backend
```
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
Now the database is build and you can start using the app. 
For easier use you can also create an admin to enable the adminpanel under localhost:8000/admin/
```bash
python manage.py createsuperuser
```

## Learning Resources
When you are new to Django check out: [Writing your first Django app](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)  <br>
Here you can find the [Django Documentation](https://docs.djangoproject.com) and the [Django REST Documentation](https://www.django-rest-framework.org/)


Enjoy 🎉🥳
