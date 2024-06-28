# News Aggregator Project Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Project](#running-the-project)
6. [Management Commands](#management-commands)
7. [API Endpoints](#api-endpoints)
8. [Tasks](#tasks)
9. [Models](#models)
10. [Utilities](#utilities)
11. [Logging](#logging)

## Introduction
The News Aggregator project is a Django-based application that fetches news articles from an RSS feed, matches them with trending topics from Google Trends, and enriches the news articles with sentiment scores using OpenAI's GPT-3.5-turbo model. The application supports translation of trends into Ukrainian language.

## Project Structure
```
news_aggregator_project/
├── news_aggregator/
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tasks.py
│ ├── tests.py
│ ├── utils.py
│ ├── views.py
│ └── management/
│ └── commands/
│ ├── clear_news.py
│ └── init.py
├── news_aggregator_project/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py
└── requirements.txt
```

## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/LIcsq/News-Parser.git
    cd news_aggregator_project
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply the migrations:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

## Configuration
1. **API Keys:**
    - Set your OpenAI API key in `settings.py`:
      ```python
      OPENAI_API_KEY = 'your_openai_api_key'
      ```

## Running the Project
1. **Start the development server:**
    ```sh
    python manage.py runserver
    ```

2. **Start the Celery worker:**
    ```sh
    celery -A news_aggregator_project worker --loglevel=info
    ```

## Management Commands
### Clear News
Custom command to delete all news entries:
```sh
python manage.py clear_news
```
## API Endpoints
### List of News

    URL: /api/news/
    Method: GET
    Response: JSON list of news articles with title, link, published date, and sentiment score.

## Tasks
### Update News

## Fetches RSS feed, matches news with Google Trends, and enriches news with sentiment scores.

    Location: news_aggregator/tasks.py
    Commands to run manually:
    ```sh
    python manage.py celery -A news_aggregator_project worker --loglevel=info
    ```
    ```sh
    celery -A djangoProject beat --loglevel=info 
    ```
