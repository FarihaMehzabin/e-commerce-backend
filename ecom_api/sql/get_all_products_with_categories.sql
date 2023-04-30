DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all_products_with_categories`()
BEGIN
    SELECT p.*, pc.category_id
    FROM product p
    LEFT JOIN product_category pc ON p.id = pc.product_id;
END$$
DELIMITER ;
