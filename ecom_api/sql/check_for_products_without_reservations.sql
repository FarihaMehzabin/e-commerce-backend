CREATE DEFINER=`root`@`localhost` PROCEDURE `check_for_products_without_reservations`(IN user_id INT, IN order_id INT)
BEGIN
  -- Declare necessary variables
  DECLARE current_product_id INT;
  DECLARE current_quantity INT;
  DECLARE done BOOLEAN DEFAULT FALSE;

  -- Declare cursor to fetch product_ids and quantities from order_items using order_id
  DECLARE cur CURSOR FOR SELECT product_id, quantity FROM order_items WHERE order_id = order_id;

  -- Declare a continue handler for the cursor when no more rows are found
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  -- Start a transaction
  START TRANSACTION;

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
      SELECT -1 AS "Result", current_product_id AS "ProductID";
      SET done = TRUE;
    ELSE
      -- Fetch the next product_id and quantity from order_items
      FETCH cur INTO current_product_id, current_quantity;
    END IF;
  END WHILE;

  -- Close the cursor for order_items
  CLOSE cur;

  -- Commit the transaction if not done
  IF NOT done THEN
    COMMIT;
    SELECT 0 AS "Result";
  END IF;


END