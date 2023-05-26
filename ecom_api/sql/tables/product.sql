CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `price` decimal(13,2) DEFAULT NULL,
  `product_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT 'a nice product',
  `company_id` int DEFAULT '1',
  `unit` int DEFAULT '1',
  `item_weight` varchar(45) DEFAULT '100g',
  `brand` varchar(45) DEFAULT 'xyz',
  PRIMARY KEY (`id`),
  KEY `idx_product_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
