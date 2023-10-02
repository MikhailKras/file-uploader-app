# Deployment Instructions

- Clone this git repo

```batch
git clone https://github.com/MikhailKras/file-uploader-app
```

- Change your working directory to the `weather-buddy` directory:

```batch
cd file-uploader-app
```

- Build docker image:

```batch
docker compose build app
```

- Up docker compose:

```batch
docker compose up -d
```

- Use the following health check endpoint: http://localhost:5678/healthcheck

# Testing

You can run tests for the application using the following command:

```batch
docker exec app_container bash -c "pytest tests"
```

# API Documentation

This documentation provides an overview of the endpoints and functionality of the FileUploader App API.

After starting the project, you will have access to the project documentation in swagger: [localhost:5678/docs](http://localhost:5678/docs)

## Table of Contents

- [Upload a CSV File](#upload-a-csv-file)
- [Get Information About Uploaded Files](#get-information-about-uploaded-files)
- [Fetch Data from a CSV File](#fetch-data-from-a-csv-file)
- [Delete a File](#delete-a-file)
- [Check the Health of the Service](#check-the-health-of-the-service)

## Check the Health of the Service

**Endpoint:** `/healthcheck`

Check the health of the service to ensure it is working properly.

- **HTTP Method:** GET

### Request Parameters

- None

### Request Example (CURL)

```bash
curl -X 'GET' \
  'http://localhost:5678/healthcheck' \
  -H 'accept: application/json'
```

### Responses

- **HTTP Status 200 (OK)**
  - Description: Service is healthy.
  - Response Body Example:
    ```json
    {
      "message": "It works!"
    }
    ```


## Upload a CSV File

**Endpoint:** `/upload_file`

Upload a CSV file, store it on the server, and record information in a database.

- **HTTP Method:** POST

### Request Body

- Content Type: `multipart/form-data`

### Request Parameters

- None

### Request Example (CURL)

```bash
curl -X 'POST' \
  'http://localhost:5678/upload_file' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/file.csv;type=text/csv'
```


### Responses

- **HTTP Status 201 (Created)**
  - Description: File upload status
  - Response Body Example:
    ```json
    {
      "message": "File uploaded successfully."
    }
    ```

- **HTTP Status 400 (Bad Request)**
  - Description: The request is invalid or the file format is not supported.
  - Response Body Example:
    ```json
    {
      "detail": "File must be a CSV file."
    }
    ```

## Get Information About Uploaded Files

**Endpoint:** `/files`

Retrieve information about files that have been uploaded and recorded in the database.

- **HTTP Method:** GET

### Request Parameters

- None

### Request Example (CURL)

```bash
curl -X 'GET' \
  'http://localhost:5678/files' \
  -H 'accept: application/json'
```

### Responses

- **HTTP Status 200 (OK)**
  - Description: Successful response
  - Response Body Example:
    ```json
    [
      {
        "id": 1,
        "file_name": "example1.csv",
        "uploaded_time": "2023-10-02 12:34:56",
        "column_names": ["model", "color", "cost"]
      },
      {
        "id": 2,
        "file_name": "example2.csv",
        "uploaded_time": "2023-10-02 13:45:00",
        "column_names": ["name", "age", "city"]
      }
    ]
    ```

## Fetch Data from a CSV File

**Endpoint:** `/fetch_data`

Fetch, sort, and filter data from a CSV file.

- **HTTP Method:** POST

### Request Body

- Content Type: `application/json`

### Request Example (CURL)

```bash
curl -X 'POST' \
  'http://localhost:5678/fetch_data?file_name=example.csv' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sort_by": ["column1", "column2"],
  "sort_orders": ["asc", "desc"],
  "filter_by": ["column3", "column4"],
  "filter_values": ["value1", "value2"]
}'

```

#### Request Parameters

- `file_name` (optional): The name of the file to fetch data from.
- `file_id` (optional): The ID of the file to fetch data from.

### Responses

- **HTTP Status 200 (OK)**
  - Description: Successful response
  - Response Body Example:
    ```json
    [
      {
        "column1": "value1",
        "column2": "value2",
        "column3": "value3"
      },
      {
        "column1": "value4",
        "column2": "value5",
        "column3": "value6"
      }
    ]
    ```

- **HTTP Status 400 (Bad Request)**
  - Description: Invalid input or parameter values.
  - Response Body Example:
    ```json
    {
      "detail": "Either 'file_id' or 'file_name' is required."
    }
    ```

- **HTTP Status 404 (Not Found)**
  - Description: File not found.
  - Response Body Example:
    ```json
    {
      "detail": "File not found."
    }
    ```

## Delete a File

**Endpoint:** `/delete_file`

Delete a file by providing either its name or ID.

- **HTTP Method:** DELETE

### Request Parameters

- `file_name` (optional): The name of the file to delete.
- `file_id` (optional): The ID of the file to delete.

### Request Example (CURL)

```bash
curl -X 'DELETE' \
  'http://localhost:5678/delete_file?file_name=example.csv' \
  -H 'accept: application/json'
```

### Responses

- **HTTP Status 200 (OK)**
  - Description: File deleted successfully.
  - Response Body Example:
    ```json
    {
      "detail": "File deleted successfully."
    }
    ```

- **HTTP Status 400 (Bad Request)**
  - Description: Invalid input or parameter values.
  - Response Body Example:
    ```json
    {
      "detail": "Only one of 'file_id' or 'file_name' can be provided."
    }
    ```

- **HTTP Status 404 (Not Found)**
  - Description: File not found.
  - Response Body Example:
    ```json
    {
      "detail": "File not found."
    }
    ```
    
---

*API Documentation generated using OpenAPI 3.1.0*

