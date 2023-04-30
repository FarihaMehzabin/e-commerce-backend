DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_order_and_items`(
    IN p_user_id INT,
    IN p_address_line_1 VARCHAR(255),
    IN p_city VARCHAR(255),
    IN p_postcode VARCHAR(10),
    IN p_items JSON
)
BEGIN
    DECLARE v_order_id INT;
    DECLARE v_index INT DEFAULT 0;
    DECLARE v_item JSON;

    -- Insert order into Order table
    INSERT INTO `order` (user_id, date, status, address_line_1, city, postcode)
    VALUES (p_user_id, UTC_TIMESTAMP(), 0, p_address_line_1, p_city, p_postcode);

    -- Get the inserted order ID
    SET v_order_id = LAST_INSERT_ID();

    -- Loop through items and insert into OrderItems table
    WHILE v_index < JSON_LENGTH(p_items) DO
        SET v_item = JSON_EXTRACT(p_items, CONCAT('$[', v_index, ']'));

        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES (
            v_order_id,
            JSON_UNQUOTE(JSON_EXTRACT(v_item, '$.product_id')),
            JSON_EXTRACT(v_item, '$.quantity')
        );

        SET v_index = v_index + 1;
    END WHILE;
END$$
DELIMITER ;
