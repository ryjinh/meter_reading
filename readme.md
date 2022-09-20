# Flow File Processor

## Overview
Django application with a very basic API implementation, which allows users to process D0010 flow files, view and filter their contents within the Django Admin page, and allows meter reading data to be accessed via HTTP request.

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

Nothing special here, just like a basic Django application :)

```bash
python3 manage.py makemigrations api && python manage.py migrate
python3 manage.py runserver
```

Tests

```bash
python3 manage.py test
```
