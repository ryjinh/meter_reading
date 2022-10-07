# Flow File Processor

## Overview

Django application with a very basic API implementation, which allows users to process D0010 electricity flow files, view and filter their contents within the Django Admin page, and allows meter reading data to be accessed via HTTP request.

## Features

### API

API has two basic endpoints

- `[GET] /api/v1/mpan/{mpan_core}/readings/` which displays all meter readings for an MPAN
- `[GET] /api/v1/mpan/{mpan_core}/readings?from={dt}&to={dt}` which shows all meter readings for an MPAN within a date range (if `FROM` is excluded, then all meter readings before `TO` date will be displayed, if `TO` is excluded, then all readings after `FROM` date will be displayed)

### Examples

`http://localhost:8000/api/v1/mpan/1200023305967/readings/?to=2020-03-01`

```json
{
    "status": "ok",
    "readings": [
        {
            "register_id": "S",
            "mpan_core": "1200023305967",
            "meter_id": "F75A 00802",
            "reading_value": "56311.0",
            "reading_taken_at": "2016-02-22T00:00:00Z",
            "reading_flag": "VALID",
            "reading_method": "NOT_VIEWED_BY_AN_AGENT_OR_NON_SITE_VISIT",
            "file_name": "meter_reading/resources/flow_files/ex_flow_file.uff"
        }
    ],
    "mpan_core": "1200023305967",
    "url": "/api/v1/mpan/1200023305967/readings/"
}
```

`http://localhost:8000/api/v1/mpan/1200023305967/readings/?to=2020-03-01`

```json
{
    "status": "ok",
    "readings": [
        {
            "register_id": "S",
            "mpan_core": "1200023305967",
            "meter_id": "F75A 00802",
            "reading_value": "56311.0",
            "reading_taken_at": "2020-02-22T00:00:00Z",
            "reading_flag": "VALID",
            "reading_method": "NOT_VIEWED_BY_AN_AGENT_OR_NON_SITE_VISIT",
            "file_name": "meter_reading/resources/flow_files/ex_flow_file2.uff"
        },
        {
            "register_id": "S",
            "mpan_core": "1200023305967",
            "meter_id": "F75A 00802",
            "reading_value": "56311.0",
            "reading_taken_at": "2016-02-22T00:00:00Z",
            "reading_flag": "VALID",
            "reading_method": "NOT_VIEWED_BY_AN_AGENT_OR_NON_SITE_VISIT",
            "file_name": "meter_reading/resources/flow_files/ex_flow_file.uff"
        }
    ],
    "mpan_core": "1200023305967",
    "url": "/api/v1/mpan/1200023305967/readings/"
}
```

## How to run the application

```bash
pipenv install # alternatively, you install dependencies from requirements.txt
make setup # will handle migrations, db seed and start createsuperuser flow
# username will be 'admin' and you will be prompted for password
python3 manage.py runserver
```

- Database will be seeded with data from example flow file, so should be ready for you to check out after above steps completed!

File Processor

```bash
python manage.py file_processor meter_reading/resources/flow_files
```

- above runs flow file processing on a directory of files, but individual files within the `flow_files` folder may also be specified

Tests

```bash
python3 manage.py test
```

### Notes

I understand that a few things (including things I may fail to mention here 😅) may raise some questions, so I've added some explanation below:

- `api.models.ReadingJson` >> I know that it is not idiomatic at all in Django to use a custom queryset in order to seralise to JSON, my intention here was just to use as few third-party libraries as possible (i.e. Django REST Framework)
- **Tests** >> still developing in this area, and one of the reasons I'm interested in working with a larger team, including more senior engineers, is so I can learn how to write more meaningful tests and grow as a developer 😁
