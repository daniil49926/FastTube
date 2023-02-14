# FastTube
![Build status](https://github.com/daniil49926/FastTube/actions/workflows/checks.yml/badge.svg?branch=main)
![Build status](https://github.com/daniil49926/FastTube/actions/workflows/tests.yml/badge.svg?branch=main)

Asynchronous API service for video hosting.

This project is designed for high-load fault-tolerant use. That is, maintaining a high online user base.

This project offers an authorized user the ability to download a video with the ability to view it using the built-in video player. Unauthorized users can also view videos posted by other users.

[FastTubeAnalytics](https://github.com/daniil49926/FastTubeAnalytics) is an auxiliary project written in golang, used to collect analytical data.

## Technology stack

- Python 3.10.5
- FastAPI 0.89.1
- Postgresql
- Redis

## Before run

Before you start working, you need to create an .env file, using the [.env.template](https://github.com/daniil49926/FastTube/blob/main/.env.template) as template.

Also, to work correctly, you need to create a file for logging. In the root of the project, you need to create a logs folder. In the logs folder, you need to create a FastTube.log file.

## Install dependence
```
pip install -r requirements.txt
```

## Run
```
cd src
python app.py
```

## Description of methods

<details>
<summary> List of available endpoints </summary>

1. A simple endpoint for health check:

**Request**
```
GET /healthchecker/v1/test
```

<details>
<summary>Response 200</summary>

```json
{
  "result": "OK"
}
```

</details>

2. Request to get user:

**Request**
```
GET /user/v1/users/{uid:integer}
```

<details>
<summary>Response 200</summary>

```json
{
  "name": "string",
  "surname": "string",
  "username": "string",
  "gender": 0,
  "email": "user@example.com",
  "id": 0,
  "created_at": "2023-02-14T17:20:23.916Z",
  "is_active": 0
}
```

</details>

<details>
<summary>Response 404</summary>

```json
{
  "message": "string"
}
```

</details>

<details>
<summary>Response 422</summary>

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

</details>

3. Request to add user.

**Request**
```
POST /user/v1/users
```

<details>
<summary>Request body *required</summary>

```json
{
  "name": "string",
  "surname": "string",
  "username": "string",
  "gender": 0,
  "email": "user@example.com",
  "password": "string"
}
```

</details>

<details>
<summary>Response 200</summary>

```json
{
  "name": "string",
  "surname": "string",
  "username": "string",
  "gender": 0,
  "email": "user@example.com",
  "id": 0,
  "created_at": "2023-02-14T17:23:37.941Z",
  "is_active": 0
}
```

</details>

<details>
<summary>Response 422</summary>

**Response 422**
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

</details>

more methods in progress...


</details>


