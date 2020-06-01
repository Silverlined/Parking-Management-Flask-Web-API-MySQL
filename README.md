# Parking Management API
## Introduction
---
Zernike Facilities is in the process of building a new parkinglot - P7. P7 will be ticketless and will keep track of which parking places are available/occupied. This inspired management to order the creation of a new parking app and to upgrade the old parking lots to the new system. As a future engineer you receive the order to develop the new system that will manage the parking lots.
## Development procedure
---
### 1. Setup the Application
`The application will be based on the micro web framework - Flask.`
### 2. Define and Access the Database
`The application will use a MySQL database.`
>Note: I will be using the *MySQL connector/Python* as my database API wrapper. `mysql-connector` is an all-in python module supported by MySQL.
### 3. Create Blueprints & Views
>A Blueprint is a way to organize a group of related views and other code. A "view" function is the code you write to respond to requests to your application. Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Rather than registering views and other code directly with an application, they are collected and registered together with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
### 4. Use Templates & Static Files
>Templates are files, usually html, that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates.

## Usage
---
Responses will have the form: (Enveloped)
```json
{
    "data": "Mixed type holding the content of the response",
    "meesage": "Description of what happened"
}
```
Subsequent response definitions will only detail the expected value of the `data` field.

---

### *Users*

#### Registering a new user

**Definition**

`POST /auth/register`

**Arguments**

- `"email":string` an unique email address of the customer
- `"password":string` a password of minimum length 8 characters
- `"customer_type":string` the type of customer (working at RUG/Hanze)
- `"student_employee_code":string` the student/employee unquie university code
- `"first_name":string` the first name of the customer
- `"surname":string` the surname name of the customer
- `"tel_number":string` the phone number of the customer
- `"payment_method":string` the preferred payment method for the customer
>`"owner_id":uuid` is generated and stored in addition

**Response**

- `201 Created` on success
---
#### Loging in

**Definition**

`POST /auth/login`

**Arguments**

- `"email":string`
- `"password":string`

**Response**

- `204 No Content` on success
>`"owner_id":uuid` is stored in cookies of the session
---
#### Registering a new car

**Definition**

`POST /api/v1/users/register-car`

**Arguments**

- `"license_plate":string` license plate of the car
- `"brand_name":string` brand of the car
- `"fuel_type":string` fuel type of the car
>`"owner_id":uuid` is read from the cookies

**Response**

- `201 Created` on success
```json
{
    "license_plate": "AAABB123",
    "brand_name": "Volvo",
    "fuel_type": "Gasoline",
    "owner_id": "123e4567-e89b-12d3-a456-426614174000"
}
```
---
#### Requesting user's invoice

**Definition**

`GET /api/v1/users/invoice`

**Arguments**

- `"month":string` the month, specifying the invoice
>`"owner_id":uuid` is read from the cookies

If there is no active session, the user is redirected to login 

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

Containing a list of car records with parking time and total cost

```json
{
    "0": {
    "license_plate": "AAABB123",
    "check_in": "2020-05-12 10:00:00",
    "check_out": "2020-05-13 10:30:00",
    "total_time": "24.50",
    "parking_cost": "29.40"
    },
    "1": {
    "license_plate": "AAABB123",
    "check_in": "2020-05-19 10:00:00",
    "check_out": "2020-05-19 11:00:00",
    "total_time": "1.00",
    "parking_cost": "1.20"
    }
}
```

---

### *Billboard*

#### Requesting parking lots information (available/occupied spacess)

**Definition**

`GET /api/v1/billboard/info?is-occupied=`

**Arguments**

- `"is-occupied":boolean` request either free (=0) or occupied (=1) spaces

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "0": {
    "name": "Zernike P7",
    "non_charging": 45,
    "charging": 10,
    },
    "1": {
    "name": "Zernike P6",
    "non_charging": 10,
    "charging": 25,
    }
}
```
---

### *Maintenance*

#### List of currently parked cars

**Definition**

`GET /api/v1/maintenance/list-cars?with-owner=`

**Arguments**

- `"with-owner":boolean` request data with owner information (with-owner=1), default=0

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "0": {
    "license_plate": "AAABB123",
    "brand_name": "Volvo",
    "fuel_type": "Diesel",
    },
    "1": {
    "license_plate": "AAABB124",
    "brand_name": "BMW",
    "fuel_type": "Gasoline",
    }
}
```
or if `with-owner`=1
```json
{
    "0": {
    "license_plate": "AAABB123",
    "brand_name": "Volvo",
    "first_name": "First",
    "surname": "Surname",
    "space_id": "46",
    "discount_rate": "10",
    },
    "1": {
    "license_plate": "AAABB124",
    "brand_name": "BMW",
    "first_name": "Firstname",
    "surname": "Surname",
    "space_id": "32",
    "discount_rate": "20",
    }
}
```
---
#### Sensor alert
Checking if the amount of checked-in cars corresponds to the amount of cars detected by the sensors

**Definition**

`GET /api/v1/maintenance/sensor-alert`

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "detected": "20",
    "checked_in": "19",
    "alert": "true",
}
```
---
#### Requesting amount of cars overview

**Definition**

`GET /api/v1/maintenance/overview-cars?group-by=`

**Arguments**

- `"group-by": string` request data grouped by either `hour, day, month or year`

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

if `group-by`=hour
```json
{
    "0": {
    "year": "2020",
    "month": "5",
    "day": "19",
    "hour": "12",
    "n_cars": "10",
    },
}
```
or if `group-by`=day
```json
{
    "0": {
    "year": "2020",
    "month": "5",
    "day": "19",
    "n_cars": "50",
    },
}
```
or if `group-by`=month
```json
{
    "0": {
    "year": "2020",
    "month": "5",
    "n_cars": "1000",
    },
}
```
or if `group-by`=year
```json
{
    "0": {
    "year": "2020",
    "n_cars": "10000",
    },
}
```
---

### *Finance*

#### List of parked cars durting a certain date-range

**Definition**

`GET /api/v1/finance/list-cars?start-date=&end-date=`

**Arguments**

- `"start-date": string` starting date filter, must be in format `%Y-%m-%d %H:%M:%S`
- `"end-date": string` ending date filter, must be in format `%Y-%m-%d %H:%M:%S`

If no arguments are given, the request will be redirected to respond with list of currently parked cars

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "0": {
    "owner_id": "123e4567-e89b-12d3-a456-426614174000",
    "license_plate": "AAABB123",
    "brand_name": "Volvo",
    "fuel_type": "Gasoline"
    }
}
```
---
#### Requesting invoice of a car owner

**Definition**

`GET /api/v1/finance/invoices/<email>/<month>`

**Arguments**

- `"email": string`
- `"month": string` 

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "0": {
    "license_plate": "AAABB123",
    "check_in": "2020-05-19 10:00:00",
    "check_out": "2020-05-19 11:00:00",
    "total_time": "1.00",
    "parking_cost": "1.20",
    "is_paid": "0",
    }
}
```
---
#### Requesting monthly invoices per car owner

**Definition**

`GET /api/v1/finance/invoices/all`

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "owner_id": {
                "January":{
                    "0":{
                        "owner_id": "123e4567-e89b-12d3-a456-426614174000",
                        "license_plate": "AAABB123",
                        "space_id": "46",
                        "check_in": "2020-05-19 10:00:00",
                        "check_out": "2020-05-19 11:00:00",
                        "total_time": "1.00",
                        "parking_cost": "1.20",
                        "is_paid": "0",
                        }
                    }
            }
}
```
---
#### Requesting overview of the unpaid invoices

**Definition**

`GET /api/v1/finance/unpaid`

**Response**

- `500 Internal Server Error` on failure
- `200 OK` on success

```json
{
    "0": {
    "record_id": "123e4567-e89b-12d3-a456-426614174000",
    "license_plate": "AAABB123",
    "space_id": "46",
    "check_in": "2020-05-19 10:00:00",
    "check_out": "2020-05-19 11:00:00",
    "total_time": "1.00",
    "parking_cost": "1.20",
    "is_paid": "0",
    }
}
```
--- 
