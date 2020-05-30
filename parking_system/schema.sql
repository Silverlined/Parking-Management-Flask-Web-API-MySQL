CREATE USER IF NOT EXISTS 'zernike_parking_app'@'localhost' IDENTIFIED BY 'laYuEkK9JCAmd8Yc';
CREATE USER IF NOT EXISTS 'billboard'@'localhost' IDENTIFIED BY '3aOzPMneTinxb6tc';
CREATE USER IF NOT EXISTS 'ticket_booth'@'localhost' IDENTIFIED BY 'mMibUQ8BjKsCn0mx';
CREATE USER IF NOT EXISTS 'finance_app'@'localhost' IDENTIFIED BY 'ipHfdfYvhVGDAf3g';
CREATE USER IF NOT EXISTS 'maintanance_app'@'localhost' IDENTIFIED BY 'skqAK4THxblysxRO';
#
CREATE ROLE IF NOT EXISTS parking_system_dev, parking_system_read, parking_system_write;
#
GRANT ALL ON parking_system.* TO parking_system_dev;
GRANT SELECT ON parking_system.* TO parking_system_read;
GRANT INSERT, UPDATE ON parking_system.* TO parking_system_write;
#
GRANT parking_system_read, parking_system_write TO zernike_parking_app@localhost, ticket_booth@localhost;
GRANT parking_system_read TO ticket_booth@localhost, finance_app@localhost, maintanance_app@localhost;
#
SET DEFAULT ROLE ALL TO zernike_parking_app@localhost, billboard@localhost, ticket_booth@localhost, finance_app@localhost, maintanance_app@localhost;
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
    CONSTRAINT FOREIGN KEY(`owner_id`) REFERENCES CarOwner(`owner_id`) ON UPDATE CASCADE ON DELETE SET NULL
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