# Parking Management API
## Introduction
---
Zernike Facilities is in the process of building a new parkinglot - P7. P7 will be ticketless and will keep track of which parking places are available/occupied. This inspired management to order the creation of a new parking app and to upgrade the old parking lots to the new system. As a future engineer you receive the order to develop the new system that will manage the parking lots.

## Database Structure
---
<img src=./parking_system/static/images/erd.png width=640>

- `ParkingLot` table:
    - `lot_id` column
        - *data type*: BINARY(16), storing an UUID, SMALLINT is also possible;
        - *description*: Primary key, to store an unique identifier for each parking lot;
    - `name` column 
        - *data type*: VARCHAR(15), variable-length string with limit of 15 characters;
        - *description*: to store the name of the parking lot (e.g. "Zernike P7");
    - `location` column 
    - *data type*: VARCHAR(50), variable-length string with limit of 50 characters;
        - *description*: to store information about the location of the lot;
    - `capacity_all` column 
        - *data type*: SMALLINT UNSIGNED, max. 65535;
        - *description*: to store the number of all parking spaces (*charing + non-charging*) at the parking lot;
    - `capacity_electric` column
        - *data type*: SMALLINT UNSIGNED, max. 65535;
        - *description*: to store the number of *charging* parking spaces at the parking lot;
- `ParkingSpace` table:
    - `space_id` column
        - *data type*: SMALLINT UNSIGNED, max. 65535;
        - *description*: Primary key, to store an unique identifier for each parking space/spot;
    - `lot_id` column 
        - *data type*: BINARY(16), storing an UUID;
        - *description*: Foreign key, referring to an instance of the "parent" table, specifying to which parking lot does this space belong to;
    - `space_type` column
        - *data type*: VARCHAR(15), variable-length string with limit of 15 characters;
        - *description*: to store information about the type of the parking space (*charing/non-chargin*);
    - `sensor_id` column
        - *data type*: SMALLINT UNSIGNED, max. 65535;
        - *description*: if sensor is present, to uniquely identify which one is attached to the parking space;
    - `is_occupied` column
        - *data type*: BIT, either 0 or 1;
        - *description*: Binary number (0 or 1) to represent the current state (either free or occupied) of the parking space;
    - `hourly_tariff` column
        -  *data type*: DECIMAL(3,2), efficient way to store numbers representing monetary value;
        - *description*: to specify the parking fee of the space per hour;
- `CarRecord` table:
(a record stores infomation about a single visit of a car to the parking lot, i.e. history)
    - `record_id` column 
        - *data type*: BINARY(16), storing an UUID, INT or BIGINT is also possible;
        - *description*: Primary key, to store an unique indentifier for each record;
    - `license_plate` column
        - *data type*: VARCHAR(10), variable-length string with limit of 10 characters. License plates are usually not longer than 10 characters;
        - *description*: Foreign key, referring to an instance of the Car table, specifying to which car does this record belong to;
    - `space_id` column
        - *data type*: SMALLINT UNSIGNED, max. 65535;
        - *description*: Foreign key, referring to an instance of the ParkingSpace table, specifying based on which parking space was this record created (i.e. where was the car parked during this visit/record);
    - `check_in` column
        - *data type*: DATETIME;
        - *description*: to store information about the check-in time of the car;
    - `check_out` column
        - *data type*: DATETIME;
        - *description*: to store information about the check-out time of the car;
    - `is_paid` column
        - *data type*: BIT, either 0 or 1;
        - *description*: Binary number (0/1) to specify if the parking visit is paid or not.
- `Car` table:
    - `license_plate` column
        - *data type*: VARCHAR(10), variable-length string with limit of 10 characters. License plates are usually not longer than 10 characters;
        - *description*: Primary key, to store the license plate information of the car which uniquely identifies it;
    - `owner_id` column 
        - *data type*: BINARY(16), UUIDs address security concerns and  prevent guessing of the owner id;
        - *description*: Foreign key, referring to an instance of the CarOwner table, specifying to which owner does this car belong to;
    - `brand_name` column
        - *data type*: VARCHAR(20), variable-length string with limit of 20 characters;
        - *description*: to store information about the brand of the car;
    - `fuel_type` column
        - *data type*: VARCHAR(10), variable-length string with limit of 10 characters;
        - *description*: to store information about the fuel type of the car;
- `CarOwner` table;
    - `owner_id` column 
        - *data type*: BINARY(16), UUIDs address security concerns and  prevent guessing of the owner id;
        - *description*: Primary key, to store an unique identifier for each owner;
    - `customer_type` column
        - *data type*: VARCHAR(10), variable-length string with limit of 10 characters (Student/Hanze/RUG);
        - *description*: to store infomation about the relation the owner has to the parking lot, e.g. working at Hanze UAS or RUG, or beign a student;
    - `student_employee_code` column
        - *data type*: CHAR(10), constant-length string with limit of 10 characters, university codes are usually standard and have constant length;
        - *description*: if available, to store information about the unique code related to the universities;  
    - `discount_rate` column
        -  *data type*: DECIMAL(4,2), efficient way to store numbers representing percentage value;
        - *description*: to store information about the discount the owner receives for his parking records;
    - `first_name` column
        - *data type*: VARCHAR(20), variable-length string with limit of 20 characters;
        - *description*: to store information about the first name of the owner;
    - `surname` column
        - *data type*: VARCHAR(20), variable-length string with limit of 20 characters;
        - *description*: to store information about the surname of the owner;
    - `tel_number` column
        - *data type*: CHAR(10), constant-length string with limit of 10 characters, telephone numbers are usually standard and have constant length;
        - *description*: to store the telephone number of the owner;
    - `email` column
        - *data type*: VARCHAR(30), variable-length string with limit of 30 characters;
        - *description*: to store the email of the owner;
    - `password` column
        - *data type*: CHAR(82), constant-length string with limit of 82 characters, hashing algorithms produces large strings which are difficult to reverse;
        - *description*: to store a hashed version of the password of the owner, used for login and verification with the app;
    - `payment_method` column
        - *data type*: VARCHAR(15), variable-length string with limit of 15 characters (manual/direct debit);
        - *description*: to store information about the method the owner prefers to pay out his parking cost (via manual payments or direct debit);

#### Different devices connect to the API 
- `Users` - can login or register and receive information through the Zernike Parking app, thus require SELECT, INSERT, UPDATE privileges (parking_system_read + parking_system_write ROLEs)
- `Billboard` - should request and receive information about the parking spaces, thus requires SELECT privileges (parking_system_read ROLE)
- `Ticket booth` - can register visitors and request an overview of the available spaces, thus requires SELECT, INSERT, UPDATE privileges (parking_system_read + parking_system_write ROLEs)
- `Cameras` - require INSERT, UPDATE privileges to store information about the license plate and the parking spaces of the cars (parking_system_write ROLE)
- `Sensors` - require UPDATE privileges to store information about the parking spaces, whether they are free or occupied (parking_system_write ROLE)
- `Finance app` - should request past information about the overall state of the lot, thus requires SELECT privileges (parking_system_read ROLE)
- `Maintenance app` - should have access to all and thus require complete admin privileges

## Development Process
---
### 1. Define and Access the Database
`The application will use a MySQL database.`
>Note: I will be using the *MySQL connector/Python* as my database API wrapper. `mysql-connector` is an all-in python module supported by MySQL.
### 2. Use Pipenv
>Pipenv is a tool that creates a virtualenv and manages the project dependencies.
### 3. Setup the Application
`The application will be based on the micro web framework - Flask.`
### 4. Create Blueprints & Views
>A Blueprint is a way to organize a group of related views and other code. A "view" function is the code you write to respond to requests to your application. Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Rather than registering views and other code directly with an application, they are collected and registered together with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
### 5. Use Templates & Static Files
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
