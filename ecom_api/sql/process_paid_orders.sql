DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `process_paid_orders`(IN user_id INT, IN order_id INT)
BEGIN
 -- Declare a variable to store the row count
  DECLARE reservation_count INT;


  -- Check if any reservations exist
  SELECT COUNT(*) INTO reservation_count
  FROM reserved_products
  WHERE user_id = user_id;

  -- If reservation_count > 0, delete the reservations for the given user_id
  IF reservation_count > 0 THEN
    DELETE FROM reserved_products
    WHERE user_id = user_id;
    
   IF ROW_COUNT() > 0 THEN
  -- Update the order status to paid
    UPDATE `order`
    SET status = 1
    WHERE user_id = user_id AND id = order_id;
    
    SELECT 0 AS "Result";
   ELSE 
    SELECT -1 AS "Result";
    
   END IF;
   
  ELSE
   SELECT -1 AS "Result";
  END IF;

END$$
DELIMITER ;
