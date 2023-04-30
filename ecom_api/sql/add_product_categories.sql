DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_product_categories`(IN `p_product_id` INT, IN `p_category_ids` TEXT)
BEGIN
    -- Declare variables
    DECLARE v_single_category_id INT;
    DECLARE v_category_id_list TEXT DEFAULT p_category_ids;

    -- Iterate through the category_ids
    WHILE LENGTH(v_category_id_list) > 0
    DO
        -- Get the next category_id from the list
        IF LOCATE(',', v_category_id_list) > 0
        THEN
            SET v_single_category_id = SUBSTRING(v_category_id_list, 1, LOCATE(',', v_category_id_list) - 1);
            SET v_category_id_list = SUBSTRING(v_category_id_list, LOCATE(',', v_category_id_list) + 1);
        ELSE
            SET v_single_category_id = v_category_id_list;
            SET v_category_id_list = '';
        END IF;

        -- Insert the new entry
        INSERT INTO product_category (product_id, category_id) VALUES (p_product_id, v_single_category_id);
    END WHILE;
END$$
DELIMITER ;
