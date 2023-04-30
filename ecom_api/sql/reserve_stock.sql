DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `reserve_stock`(IN user_id INT, IN items_json TEXT)
BEGIN
  DECLARE done BOOLEAN DEFAULT FALSE;
  DECLARE current_product_id INT;
  DECLARE current_quantity INT;
  DECLARE items_length INT;
  DECLARE i INT DEFAULT 0;

  -- Get the length of the items array
  SET items_length = JSON_LENGTH(items_json);

  -- Start a transaction
  START TRANSACTION;

  -- Loop through the items
  WHILE i < items_length AND NOT done DO
    -- Get the product_id and quantity for the current item
    SET current_product_id = JSON_EXTRACT(items_json, CONCAT('$[', i, '].product_id'));
    SET current_quantity = JSON_EXTRACT(items_json, CONCAT('$[', i, '].quantity'));

    -- Check and update the stock
    UPDATE product_stock
    SET stock = stock - current_quantity
    WHERE product_id = current_product_id AND stock >= current_quantity;

    -- Check if the stock update was successful
    IF ROW_COUNT() <= 0 THEN
      -- Insufficient stock, rollback the transaction
      ROLLBACK;
      SELECT -1 AS "Result", current_product_id AS "ProductID";
      SET done = TRUE;
    ELSE
      -- Insert the reserved stock information
      INSERT INTO reserved_products(user_id, product_id, reserved_quantity, time)
      VALUES (user_id, current_product_id, current_quantity, NOW());
    END IF;

    -- Increment the loop counter
    SET i = i + 1;
  END WHILE;

  -- Commit the transaction if not done
  IF NOT done THEN
    COMMIT;
    SELECT 0 AS "Result";
  END IF;
END$$
DELIMITER ;
