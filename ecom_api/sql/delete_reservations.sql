CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_reservations`(IN user_id INT)
BEGIN
  -- Declare necessary variables
  DECLARE order_id INT;
  DECLARE current_product_id INT;
  DECLARE current_quantity INT;
  DECLARE success TINYINT;
  DECLARE failed_product_id INT DEFAULT NULL;
  DECLARE done BOOLEAN DEFAULT FALSE;
  
  -- Declare cursor to fetch product_ids and quantities from order_items using order_id
  DECLARE cur CURSOR FOR SELECT product_id, quantity FROM order_items WHERE order_id = order_id;
  
  -- Declare a continue handler for the cursor when no more rows are found
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  
  -- check if any reservations exist
  SELECT product_id, reserved_quantity
    FROM reserved_products
    WHERE user_id = user_id
    FOR UPDATE;

  -- Check if any rows were affected by the DELETE statement
  IF ROW_COUNT() > 0 THEN
    -- If rows were affected, set the success flag to 1
    -- Delete the reservations for the given user_id
  DELETE FROM reserved_products
  WHERE user_id = user_id;

    SET success = 1;
  ELSE
    -- If no rows were affected, background poller removed the reservations
    SET success = 0;

    -- Start a transaction
    START TRANSACTION;
    
    -- try and check if stock is available anymore

    -- Get the order_id from the order table using the user_id
    SELECT id FROM `order` WHERE user_id = user_id INTO order_id;

    -- Open cursor to fetch product_ids and quantities from order_items
    OPEN cur;
    FETCH cur INTO current_product_id, current_quantity;

    -- Loop through the order_items
    WHILE NOT done DO
      -- Update the stock in product_stock table
      UPDATE product_stock
      SET stock = stock - current_quantity
      WHERE product_id = current_product_id AND stock >= current_quantity;

      -- Check if the stock update was successful
      IF ROW_COUNT() <= 0 THEN
        -- Insufficient stock, rollback the transaction
        ROLLBACK;
        SET success = -1;
        SET failed_product_id = current_product_id;
        SET done = TRUE;
      ELSE
        -- Fetch the next product_id and quantity from order_items
        FETCH cur INTO current_product_id, current_quantity;
      END IF;
    END WHILE;

    -- Close the cursor for order_items
    CLOSE cur;

    -- If the stock update was successful, commit the transaction and set the success flag to 1
    IF success = 0 THEN
      COMMIT;
      SET success = 1;
    END IF;
  END IF;
  
    -- Get the order_id from the order table using the user_id
    SELECT id FROM `order` WHERE user_id = user_id INTO order_id;
  
  -- Update the order status based on the success flag
	IF success = 1 THEN
	UPDATE `order`
	SET status = 1
	WHERE user_id = user_id AND id = order_id;
    
	ELSEIF success = -1 THEN
	UPDATE `order`
	SET status = 5
	WHERE user_id = user_id AND id = order_id;
	END IF;

  -- Return the result using a SELECT statement
  SELECT success, failed_product_id;

END