# Doctime Backend

Welcome to the Doctime backend repository. Doctime is a doctor booking application built with Django REST framework and Django Channels.

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)


## Project Overview
Doctime is a full-stack project that provides a platform for users to book appointments with doctors. The backend is built using Django REST framework for RESTful APIs and Django Channels for real-time communication. This README focuses on the backend component of the project.

## Prerequisites
Before you begin, ensure you have the following prerequisites:

  

-  Make sure you have Python installed on your  system. You can download and install Python from the official website: https://www.python.org/

- Install Postgres on your system. You can    download and install Postgres from the official website: https://www.postgresql.org/


## Installation
1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/slimshady808/doctime-backend.git
   ```

2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virtual environment:
- On Linux/macOS:
  ```
  source venv/bin/activate
  ```
- On Windows:
  ```
  venv\Scripts\activate
  ```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Configure your environment variables
You can view and manage the environmental variables in your `.env` file. Open it to set the necessary configuration values for your Doctime backend. A list of all available environmental variables can be found in the [Environment Variables](#environment-variables) section below.

6. Apply database migrations:
```
python manage.py migrate
```
7. Run the development server:
```
daphne doctime_backend.asgi:application

```

8. Access the project in your web browser at [http://localhost:8000/](http://localhost:8000/).


That's it! You're all set to run the backend of DocTime with Django, Daphne, Channels, and Postgres. Integrate this backend with the frontend to create a complete doctor management app. 

## Environment Variables

The following environmental variables should be set in your `.env` file:


- `PUBLIC_KEY` and `SECRET_KEY_R` (for Razorpay)
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `AUTH_USER_MODEL`
- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_USE_TLS`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DB_ENGINE`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
