-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 05, 2020 at 01:51 PM
-- Server version: 8.0.20
-- PHP Version: 7.3.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parking_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `Car`
--

CREATE TABLE `Car` (
  `license_plate` varchar(10) NOT NULL,
  `owner_id` binary(16) DEFAULT NULL,
  `brand_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fuel_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Car`
--

INSERT INTO `Car` (`license_plate`, `owner_id`, `brand_name`, `fuel_type`) VALUES
('AAACCC598', 0xf039a1f495cc11eab97d3ca9f450324c, 'Shelly', 'Gasoline'),
('AADBC809', 0xf039a1f495cc11eab97d3ca9f450324c, 'Volvo', 'Gasoline'),
('AAVV1223', 0xf039a1f495cc11eab97d3ca9f450324c, 'BMW', 'Hydrogen'),
('AAVV1230', 0xf039a1f495cc11eab97d3ca9f450324c, 'Daewoo', 'Gasoline'),
('AAVV1232', 0xf039a1f495cc11eab97d3ca9f450324c, 'BMW', 'Gasoline'),
('AAVV1233', 0xf039a1f495cc11eab97d3ca9f450324c, 'Ford', 'Diesel'),
('AAVV1234', 0xf039a1f495cc11eab97d3ca9f450324c, '', ''),
('AAVV1235', 0xf039a1f495cc11eab97d3ca9f450324c, 'BMW', 'Gasoline'),
('AAVV1236', 0xf039a1f495cc11eab97d3ca9f450324c, 'Daewoo', 'Gasoline'),
('AAVV1237', 0xf039a1f495cc11eab97d3ca9f450324c, 'Ford', 'Diesel'),
('AAVV1239', 0xf039a1f495cc11eab97d3ca9f450324c, 'Daewoo', 'Gasoline'),
('AAXX134', 0xf039a1f495cc11eab97d3ca9f450324c, 'Holden', 'Diesel'),
('ADCXZ879', 0xf039a1f495cc11eab97d3ca9f450324c, NULL, NULL),
('ADSCV23', 0xf039a1f495cc11eab97d3ca9f450324c, 'BMW', 'Diesel'),
('ADSCV24', 0xf039a1f495cc11eab97d3ca9f450324c, 'BMW', 'Diesel'),
('HSDAX878', 0xae66c8fca72311ea9f5f3ca9f450324c, 'Suzuki', 'Electric'),
('ZXAS1232', NULL, 'Ford', 'Gasoline'),
('ZXAS1234', 0xf039a1f495cc11eab97d3ca9f450324c, 'Daewoo', 'Diesel');

-- --------------------------------------------------------

--
-- Table structure for table `CarOwner`
--

CREATE TABLE `CarOwner` (
  `owner_id` binary(16) NOT NULL,
  `customer_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `student_employee_code` char(10) DEFAULT NULL,
  `discount_rate` decimal(4,2) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `surname` varchar(20) DEFAULT NULL,
  `tel_number` char(10) DEFAULT NULL,
  `email` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` char(82) NOT NULL,
  `payment_method` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `CarOwner`
--

INSERT INTO `CarOwner` (`owner_id`, `customer_type`, `student_employee_code`, `discount_rate`, `first_name`, `surname`, `tel_number`, `email`, `password`, `payment_method`) VALUES
(0x7bfbab30a72811eaa08f3ca9f450324c, 'student', '234567', NULL, 'garry', 'gg', '0689123454', 'gary@gmail.com', '$5$rounds=535000$mHEtj5lfBvffDYV4$JA3/aLr9gE3/0Zz4LbuXDuTP66nifFo1hlZt5R0NEQC', 'manual_payment'),
(0xae66c8fca72311ea9f5f3ca9f450324c, 'student', '567412', '0.00', 'Jason', 'Born', '061234874', 'born@gmail.com', '$5$rounds=535000$7mXgyNhnowQF25aO$xGYNO6oSX1MfJ7wH/Kfypby1AwoGphSSg7wm0g/guY3', 'manual_payment'),
(0xbc8bb4f29f9d11eaab733ca9f450324c, 'Student', '', NULL, '', '', '', 'test@hanze.nl', '$5$rounds=535000$A5FrgFRomnjtnXcb$cl4bbOvjoZrXeVTZuRqVK4LgwmjEmU/8BVT2a4FakX0', 'direct_debit'),
(0xf039a1f495cc11eab97d3ca9f450324c, 'RUG', '611412', '50.00', 'Ivan', 'Ivanov', '0612345678', 'test@gmail.com', '$5$rounds=535000$A5FrgFRomnjtnXcb$cl4bbOvjoZrXeVTZuRqVK4LgwmjEmU/8BVT2a4FakX0', 'Direct Debit');

-- --------------------------------------------------------

--
-- Table structure for table `CarRecord`
--

CREATE TABLE `CarRecord` (
  `record_id` binary(16) NOT NULL,
  `license_plate` varchar(10) NOT NULL,
  `space_id` smallint UNSIGNED NOT NULL,
  `check_in` datetime NOT NULL,
  `check_out` datetime DEFAULT NULL,
  `is_paid` bit(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `CarRecord`
--

INSERT INTO `CarRecord` (`record_id`, `license_plate`, `space_id`, `check_in`, `check_out`, `is_paid`) VALUES
(0x05f9de1ea25c11ea80ff3ca9f450324c, 'ADCXZ879', 46, '2020-05-30 11:57:51', '2020-05-30 13:50:54', b'0'),
(0x2a5c4d9ea26d11eaa05d3ca9f450324c, 'ADCXZ879', 46, '2020-05-30 14:00:33', '2020-05-30 14:00:40', b'0'),
(0x2d125688a26c11ea8e793ca9f450324c, 'ADCXZ879', 46, '2020-05-30 13:53:28', '2020-05-30 13:53:33', b'0'),
(0x2e5f7a40a32311eabceb3ca9f450324c, 'ADCXZ879', 46, '2020-05-31 11:43:29', NULL, b'0'),
(0x39f54bf4a72511ea9e753ca9f450324c, 'HSDAX878', 42, '2020-06-05 14:08:12', NULL, b'0'),
(0x3b13e12ca72411ea88733ca9f450324c, 'HSDAX878', 42, '2020-06-05 14:01:04', '2020-06-05 14:07:45', b'0'),
(0x63c9b568a26c11eab6003ca9f450324c, 'ADCXZ879', 46, '2020-05-30 13:55:00', '2020-05-30 13:55:02', b'0'),
(0x7505ed0aa26d11ea8fed3ca9f450324c, 'ADCXZ879', 46, '2020-05-30 14:02:39', '2020-05-30 14:02:42', b'0'),
(0xba3e2c3aa26c11eabdbe3ca9f450324c, 'ADCXZ879', 46, '2020-05-30 13:57:25', '2020-05-30 13:57:27', b'1');

-- --------------------------------------------------------

--
-- Table structure for table `ParkingLot`
--

CREATE TABLE `ParkingLot` (
  `lot_id` binary(16) NOT NULL,
  `name` varchar(15) NOT NULL,
  `location` varchar(50) DEFAULT NULL,
  `capacity_all` smallint UNSIGNED NOT NULL,
  `capacity_charging` smallint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ParkingLot`
--

INSERT INTO `ParkingLot` (`lot_id`, `name`, `location`, `capacity_all`, `capacity_charging`) VALUES
(0xb7c542c395cc11ea85ac3ca9f450324c, 'Zernike P7', 'Nettelbosje 2, 9747 AD Groningen', 60, 10);

-- --------------------------------------------------------

--
-- Table structure for table `ParkingSpace`
--

CREATE TABLE `ParkingSpace` (
  `space_id` smallint UNSIGNED NOT NULL,
  `lot_id` binary(16) NOT NULL,
  `space_type` varchar(15) NOT NULL,
  `sensor_id` smallint UNSIGNED DEFAULT NULL,
  `is_occupied` bit(1) NOT NULL,
  `hourly_tariff` decimal(3,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ParkingSpace`
--

INSERT INTO `ParkingSpace` (`space_id`, `lot_id`, `space_type`, `sensor_id`, `is_occupied`, `hourly_tariff`) VALUES
(0, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 0, b'0', '1.20'),
(1, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 1, b'0', '1.20'),
(2, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 2, b'0', '1.20'),
(3, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 3, b'0', '1.20'),
(4, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 4, b'0', '1.20'),
(5, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 5, b'0', '1.20'),
(6, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 6, b'0', '1.20'),
(7, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 7, b'0', '1.20'),
(8, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 8, b'0', '1.20'),
(9, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 9, b'0', '1.20'),
(10, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 10, b'0', '1.20'),
(11, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 11, b'0', '1.20'),
(12, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 12, b'0', '1.20'),
(13, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 13, b'0', '1.20'),
(14, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 14, b'0', '1.20'),
(15, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 15, b'0', '1.20'),
(16, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 16, b'0', '1.20'),
(17, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 17, b'0', '1.20'),
(18, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 18, b'0', '1.20'),
(19, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 19, b'0', '1.20'),
(20, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 20, b'1', '1.20'),
(21, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 21, b'0', '1.20'),
(22, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 22, b'0', '1.20'),
(23, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 23, b'0', '1.20'),
(24, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 24, b'0', '1.20'),
(25, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 25, b'1', '1.20'),
(26, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 26, b'0', '1.20'),
(27, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 27, b'0', '1.20'),
(28, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 28, b'0', '1.20'),
(29, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 29, b'0', '1.20'),
(30, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 30, b'0', '1.20'),
(31, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 31, b'0', '1.20'),
(32, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 32, b'0', '1.20'),
(33, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 33, b'0', '1.20'),
(34, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 34, b'0', '1.20'),
(35, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 35, b'0', '1.20'),
(36, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 36, b'0', '1.20'),
(37, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 37, b'0', '1.20'),
(38, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 38, b'0', '1.20'),
(39, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 39, b'0', '1.20'),
(40, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 40, b'0', '1.20'),
(41, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 41, b'0', '1.20'),
(42, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 42, b'1', '1.20'),
(43, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 43, b'0', '1.20'),
(44, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 44, b'0', '1.20'),
(45, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 45, b'0', '1.20'),
(46, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 46, b'1', '1.20'),
(47, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 47, b'0', '1.20'),
(48, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 48, b'0', '1.20'),
(49, 0xb7c542c395cc11ea85ac3ca9f450324c, 'non_charging', 49, b'0', '1.20'),
(50, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 50, b'0', '1.32'),
(51, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 51, b'0', '1.32'),
(52, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 52, b'0', '1.32'),
(53, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 53, b'0', '1.32'),
(54, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 54, b'0', '1.32'),
(55, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 55, b'0', '1.32'),
(56, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 56, b'0', '1.32'),
(57, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 57, b'0', '1.32'),
(58, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 58, b'0', '1.32'),
(59, 0xb7c542c395cc11ea85ac3ca9f450324c, 'charging', 59, b'0', '1.32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Car`
--
ALTER TABLE `Car`
  ADD PRIMARY KEY (`license_plate`),
  ADD KEY `owner_id` (`owner_id`);

--
-- Indexes for table `CarOwner`
--
ALTER TABLE `CarOwner`
  ADD PRIMARY KEY (`owner_id`);

--
-- Indexes for table `CarRecord`
--
ALTER TABLE `CarRecord`
  ADD PRIMARY KEY (`record_id`),
  ADD KEY `space_id` (`space_id`),
  ADD KEY `license_plate` (`license_plate`);

--
-- Indexes for table `ParkingLot`
--
ALTER TABLE `ParkingLot`
  ADD PRIMARY KEY (`lot_id`);

--
-- Indexes for table `ParkingSpace`
--
ALTER TABLE `ParkingSpace`
  ADD PRIMARY KEY (`space_id`),
  ADD KEY `lot_id` (`lot_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Car`
--
ALTER TABLE `Car`
  ADD CONSTRAINT `Car_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `CarOwner` (`owner_id`);

--
-- Constraints for table `CarRecord`
--
ALTER TABLE `CarRecord`
  ADD CONSTRAINT `CarRecord_ibfk_1` FOREIGN KEY (`license_plate`) REFERENCES `Car` (`license_plate`),
  ADD CONSTRAINT `CarRecord_ibfk_2` FOREIGN KEY (`space_id`) REFERENCES `ParkingSpace` (`space_id`),
  ADD CONSTRAINT `CarRecord_ibfk_3` FOREIGN KEY (`license_plate`) REFERENCES `Car` (`license_plate`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ParkingSpace`
--
ALTER TABLE `ParkingSpace`
  ADD CONSTRAINT `ParkingSpace_ibfk_1` FOREIGN KEY (`lot_id`) REFERENCES `ParkingLot` (`lot_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
