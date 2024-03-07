
-- Dumping database structure for address_scraper
CREATE DATABASE IF NOT EXISTS `address_scraper` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `address_scraper`;

-- Dumping structure for table address_scraper.pages_and_addresses
CREATE TABLE IF NOT EXISTS `pages_and_addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `page` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `address_str` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `html_str` longtext,
  `organized_address` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `page` (`page`)
) ENGINE=InnoDB AUTO_INCREMENT=2140 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;