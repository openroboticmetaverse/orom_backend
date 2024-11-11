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

2. Save path to this folder as environment variable. 

    Get the current path:
    ```bash
    export OROM_BACKEND_PATH=$(pwd)
    echo $OROM_BACKEND_PATH
    ```
    Open your terminal configuration file (see instructions below, they can vary based on your terminal and operating system) and append the following line:
    enter value at the bottom: `export OROM_BACKEND_PATH=<your previous output>` then restart the terminal

    - For macOS:
      ```bash
      sudo nano ~/.zshrc
      ```
    - For Linux:
      ```bash
      sudo nano ~/.bash_rc
      ```
    - For Windows:
      ```bash
      TODO
      ```


3. Docker Compose 🐳
    ```bash
    docker compose up
    ```

## Development ⌨️
1. Create Admin User
    Now the database is build and you can start using the app. 
    For easier use you can also create an admin to enable the adminpanel under localhost:8000/admin/
    ```bash
    python manage.py createsuperuser
    ```
2. API Testing

    For API testing we are using Hoppscotch. To be added to our workspace message one of us. To run the requests you need to install the [browser extension](https://github.com/hoppscotch/hoppscotch-extension).

3. Django Model Changes 
    When adapting the models.py file, you have to migrate these changes to the current database entries (in development it often is easier to just reseting the whole db and starting from zero)
    ```bash
    docker exec -it orom_backend bash
    ```
    ```bash
    python orom_backend/manage.py makemigrations
    ```
    ```bash
    python orom_backend/manage.py migrate
    ```
    How to start from zero:
    You have to delete the database image and postgres-volume. If you are only working on this project and have no other Docker projects just run: <br>
    (__warning__: Docker will delete all container, images and volumes)
    ```bash
    docker system prune -a
    ```


## Learning Resources
When you are new to Django check out: [Writing your first Django app](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)  <br>
Here you can find the [Django Documentation](https://docs.djangoproject.com) and the [Django REST Documentation](https://www.django-rest-framework.org/)


Enjoy 🎉🥳
