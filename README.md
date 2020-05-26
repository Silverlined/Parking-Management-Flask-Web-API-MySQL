# Parking Management API
## Introduction
Zernike Facilities is in the process of building a new parkinglot - P7. P7 will be ticketless and will keep track of which parking places are available/occupied. This inspired management to order the creation of a new parking app and to upgrade the old parking lots to the new system. As a future engineer you receive the order to develop the new system that will manage the parking lots.
## Procedure
---
## 1. Setup the Application
`Flask application`
## 2. Define and Access the Database
`The application will use a MySQL database to store any parking related data`
>Note: I will be using the *MySQL connector/Python* as my database API wrapper. `mysql-connector` is an all-in python module supported by MySQL.
## 3. Create Blueprints and Views
`A view function is the code you write to respond to requests to your application. Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Flask can also go the other direction and generate a URL to a view based on its name and arguments.`
## 4. Use Templates & Static Files
`The template files will be stored in the templates directory inside the *parking_system* package. Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates.`

### Entity relationship diagram
<img src=./res/erd.png width=600>


## TODO: Finish the readme file accordingly...
## Usage

### List all devices

**Definition**

`GET /devices`

**Response**

- `200 OK` on success

```json
[
    {
        "identifier": "floor-lamp",
        "name": "Floor Lamp",
        "device_type": "switch",
        "controller_gateway": "192.1.68.0.2"
    },
    {
        "identifier": "samsung-tv",
        "name": "Living Room TV",
        "device_type": "tv",
        "controller_gateway": "192.168.0.9"
    }
]
```

### Registering a new device

**Definition**

`POST /devices`

**Arguments**

- `"identifier":string` a globally unique identifier for this device
- `"name":string` a friendly name for this device
- `"device_type":string` the type of the device as understood by the client
- `"controller_gateway":string` the IP address of the device's controller

If a device with the given identifier already exists, the existing device will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "identifier": "floor-lamp",
    "name": "Floor Lamp",
    "device_type": "switch",
    "controller_gateway": "192.1.68.0.2"
}
```

## Lookup device details

`GET /device/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
    "identifier": "floor-lamp",
    "name": "Floor Lamp",
    "device_type": "switch",
    "controller_gateway": "192.1.68.0.2"
}
```

## Delete a device

**Definition**

`DELETE /devices/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `204 No Content` on success
