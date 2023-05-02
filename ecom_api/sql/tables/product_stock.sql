CREATE TABLE `product_stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
