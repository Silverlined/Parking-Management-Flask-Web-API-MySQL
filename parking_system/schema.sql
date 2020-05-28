#
CREATE TABLE IF NOT EXISTS `ParkingLot`(
    `lot_id` BINARY(16) NOT NULL,
    `name` VARCHAR(15) NOT NULL,
    `location` VARCHAR(50),
    `capacity_all` SMALLINT UNSIGNED NOT NULL,
    `capacity_charging` SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY(`lot_id`)
);
#
CREATE TABLE IF NOT EXISTS `ParkingSpace`(
    `space_id` SMALLINT UNSIGNED NOT NULL,
    `lot_id` BINARY(16) NOT NULL,
    `space_type` VARCHAR(15) NOT NULL,
    `sensor_id` SMALLINT UNSIGNED,
    `is_occupied` BIT NOT NULL,
    `hourly_tariff` DECIMAL(3, 2) NOT NULL,
    PRIMARY KEY(`space_id`),
    FOREIGN KEY(`lot_id`) REFERENCES ParkingLot(`lot_id`)
);
#
CREATE TABLE IF NOT EXISTS `CarOwner`(
    `owner_id` BINARY(16) NOT NULL,
    `customer_type` VARCHAR(10),
    `student_employee_code` CHAR(10),
    `discount_rate` DECIMAL(4, 2),
    `first_name` VARCHAR(20),
    `surname` VARCHAR(20),
    `tel_number` CHAR(10),
    `email` VARCHAR(30) NOT NULL,
    `password` CHAR(82) NOT NULL,
    `payment_method` VARCHAR(15),
    PRIMARY KEY(`owner_id`)
);
#
CREATE TABLE IF NOT EXISTS `Car`(
    `license_plate` VARCHAR(10) NOT NULL,
    `owner_id` BINARY(16),
    `brand_name` VARCHAR(20),
    `fuel_type` VARCHAR(10),
    PRIMARY KEY(`license_plate`),
    CONSTRAINT
    FOREIGN KEY(`owner_id`) REFERENCES CarOwner(`owner_id`) ON UPDATE CASCADE ON DELETE SET NULL
);
#
CREATE TABLE IF NOT EXISTS `CarRecord`(
    `record_id` BINARY(16) NOT NULL,
    `license_plate` VARCHAR(10) NOT NULL,
    `space_id` SMALLINT UNSIGNED,
    `check_in` DATETIME NOT NULL,
    `check_out` DATETIME,
    `is_paid` BIT NOT NULL,
    PRIMARY KEY(`record_id`),
    CONSTRAINT `CarRecord_ibfk_1` FOREIGN KEY (`license_plate`) REFERENCES `Car` (`license_plate`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `CarRecord_ibfk_2` FOREIGN KEY (`space_id`) REFERENCES `ParkingSpace` (`space_id`)
);