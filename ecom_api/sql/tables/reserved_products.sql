CREATE TABLE `reserved_products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `reserved_quantity` int NOT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `time` (`time`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
