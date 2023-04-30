DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_product_categories`(IN `p_product_id` INT, IN `p_category_ids` TEXT)
BEGIN
    -- Delete the previous entries for the selected product using the product_id
    DELETE FROM product_category WHERE product_id = p_product_id;

    -- Add new entries inside the table for the product
    SET @category_id_list = p_category_ids;
    SET @single_category_id = NULL;

    WHILE LENGTH(@category_id_list) > 0
    DO
        -- Get the next category_id from the list
        IF LOCATE(',', @category_id_list) > 0
        THEN
            SET @single_category_id = SUBSTRING(@category_id_list, 1, LOCATE(',', @category_id_list) - 1);
            SET @category_id_list = SUBSTRING(@category_id_list, LOCATE(',', @category_id_list) + 1);
        ELSE
            SET @single_category_id = @category_id_list;
            SET @category_id_list = '';
        END IF;

        -- Insert the new entry
        INSERT INTO product_category (product_id, category_id) VALUES (p_product_id, @single_category_id);
    END WHILE;
END$$
DELIMITER ;
