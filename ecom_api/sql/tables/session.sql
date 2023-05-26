CREATE TABLE `session` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guid` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `language_id` int DEFAULT '1',
  `country_id` int DEFAULT '236',
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
