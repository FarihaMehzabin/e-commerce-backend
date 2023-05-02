DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_expired_reservations`()
BEGIN
  DECLARE done BOOLEAN DEFAULT FALSE;
  DECLARE current_product_id INT;
  DECLARE current_quantity INT;

  -- Create a cursor to get the expired reservations
  DECLARE cur CURSOR FOR
    SELECT product_id, reserved_quantity
    FROM reserved_products
    WHERE TIMESTAMPDIFF(MINUTE, time, UTC_TIMESTAMP()) > 5
    FOR UPDATE;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  -- Start a transaction
  START TRANSACTION;

  OPEN cur;

  -- Loop through the expired reservations
  read_loop: LOOP
    FETCH cur INTO current_product_id, current_quantity;

    IF done THEN
      LEAVE read_loop;
    END IF;

    -- Update the product_stock table
    UPDATE product_stock
    SET stock = stock + current_quantity
    WHERE product_id = current_product_id;

    IF ROW_COUNT() > 0 THEN
    -- Delete the reservation
      DELETE FROM reserved_products
      WHERE product_id = current_product_id
      AND TIMESTAMPDIFF(MINUTE, time, UTC_TIMESTAMP()) > 5;
      IF ROW_COUNT() > 0 THEN
        -- Commit the transaction
        COMMIT;
      ELSE
        -- Rollback the transaction if there's an error
        ROLLBACK;
      END IF;
    ELSE
      -- Rollback the transaction if there's an error
      ROLLBACK;
    END IF;
  END LOOP read_loop;

  -- Close the cursor
  CLOSE cur;

  SELECT 0 AS "Result";
END$$
DELIMITER ;
