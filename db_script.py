import mysql.connector
import names

db = mysql.connector.connect(
    host="localhost", user="root", password="password", database="ecommerce"
)

cursor = db.cursor()

# cursor.execute("CREATE DATABASE ecommerce")

cursor.execute(
    f"CREATE TABLE product (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price INT)"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`product` ADD COLUMN `company_id` INT NULL DEFAULT 1 AFTER `price`, ADD COLUMN `unit` INT NULL DEFAULT 1 AFTER `company_id`, ADD COLUMN `item_weight` VARCHAR(45) NULL DEFAULT '100g' AFTER `unit`, ADD COLUMN `brand` VARCHAR(45) NULL DEFAULT 'xyz' AFTER `item_weight`;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`product` CHANGE COLUMN `product_description` `product_description` VARCHAR(255) NULL DEFAULT 'a nice product' AFTER `price`"
)

cursor.execute(
    "CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255))"
)

cursor.execute(
    f"CREATE TABLE transactions (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product_id INT, value INT)"
)


cursor.execute(
    "CREATE TABLE `ecommerce`.`company` (`id` INT NOT NULL AUTO_INCREMENT,`name` VARCHAR(255) NULL,PRIMARY KEY (`id`))"
)

cursor.execute(
    "CREATE TABLE `ecommerce`.`Category` (`id` INT NOT NULL AUTO_INCREMENT,`name` VARCHAR(45) NULL, PRIMARY KEY (`id`))"
)

cursor.execute(
    "CREATE TABLE `ecommerce`.`product_category` ( `product_id` INT NOT NULL,`category_id` INT NULL, PRIMARY KEY (`product_id`));"
)

cursor.execute(
    "CREATE TABLE `ecommerce`.`company_user` (`company_id` INT NULL DEFAULT 1,`user_id` INT NULL)"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`company_user` ADD INDEX `company_id_idx` (`company_id` ASC) VISIBLE; ALTER TABLE `ecommerce`.`company_user` ADD CONSTRAINT `company_id` FOREIGN KEY (`company_id`) REFERENCES `ecommerce`.`company` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`company_user` ADD INDEX `user_id_idx` (`user_id` ASC) VISIBLE; ALTER TABLE `ecommerce`.`company_user` ADD CONSTRAINT `user_ID` FOREIGN KEY (`user_id`) REFERENCES `ecommerce`.`user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`company_user` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT AFTER `company_id`, ADD PRIMARY KEY (`id`);"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`company_user` CHANGE COLUMN `id` `id` INT NOT NULL AUTO_INCREMENT FIRST;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`transactions` ADD COLUMN `txn_time` DATETIME NULL DEFAULT '2023-01-20 15:06:25' AFTER `value`;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`transactions` CHANGE COLUMN `value` `value` DECIMAL(13,2) NULL DEFAULT NULL ; ALTER TABLE `ecommerce`.`product` CHANGE COLUMN `price` `price` DECIMAL(13,2) NULL DEFAULT NULL ; ALTER TABLE `ecommerce`.`company_user` DROP FOREIGN KEY `company_id`;ALTER TABLE `ecommerce`.`company_user` ADD CONSTRAINT `ID` FOREIGN KEY (`company_id`) REFERENCES `ecommerce`.`company` (`ID`) ON DELETE RESTRICT ON UPDATE CASCADE; ALTER TABLE `ecommerce`.`product` CHANGE COLUMN `product_description` `product_description` NVARCHAR(255) NULL DEFAULT 'a nice product' ;"
)

cursor.execute("ALTER TABLE `ecommerce`.`product_category` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, CHANGE COLUMN `product_id` `product_id` INT NULL , DROP PRIMARY KEY, ADD PRIMARY KEY (`id`); ")

cursor.execute("ALTER TABLE `ecommerce`.`user` ADD COLUMN `password` VARCHAR(255) NOT NULL DEFAULT 'password' AFTER `last_name`;")

cursor.execute("ALTER TABLE `ecommerce`.`user` ADD COLUMN `username` VARCHAR(45) NOT NULL DEFAULT 'username' AFTER `id`,DROP PRIMARY KEY, ADD PRIMARY KEY (`id`, `username`); ")

cursor.execute("ALTER TABLE `ecommerce`.`user` ADD COLUMN `salt` VARCHAR(45) NULL AFTER `password`;")

cursor.execute("ALTER TABLE `ecommerce`.`user` DROP COLUMN `username`, DROP PRIMARY KEY, ADD PRIMARY KEY (`id`);")

cursor.execute("ALTER TABLE `ecommerce`.`user` ADD COLUMN `username` VARCHAR(45) NULL AFTER `id`, CHANGE COLUMN `salt` `salt` VARCHAR(255) NULL DEFAULT NULL , ADD UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE ;")

pro = ["chair", "table", "pen", "pencil", "phone"]
price = 100
company = [
    "Pattern -iServe-",
    "Zappos" "Asurion, LLC",
    "Utopia Deals",
    "Carlyle",
    "AnkerDirect",
    "topshoesUS",
    "YH-Goods",
    "AilunUS",
    "Orva Stores",
    "GORILLA COMMERCE",
    "Hour Loop",
    "Fintie",
    "Just Love Fashion",
    "Galactic Shop",
    "River Colony Trading",
    "Arch of the High Sierras",
    "eSupplements",
    "Supershieldz",
    "Hey Dude Official",
]
categories = [("furniture",), ("stationary",), ("electronics",)]

# populating product table
for x in range(5):
    sql = f"INSERT INTO product (name, price) VALUES (%s, %s)"
    val = pro[x], price

    price = price + 100

    cursor.execute(sql, val)

    db.commit()


# populating user table
for i in range(100):
    print(names.get_first_name())

    sql = f"INSERT INTO user (first_name, last_name) VALUES (%s, %s)"
    val = names.get_first_name(), names.get_last_name()

    cursor.execute(sql, val)

    db.commit()

# populating company table
for i in range(len(company)):
    sql = f"INSERT INTO company (name) VALUES (%s)"

    val = (company[i],)

    cursor.execute(sql, val)

    db.commit()

# populating category table
sql = f"INSERT INTO Category (name) VALUES (%s)"
val = categories

cursor.executemany(sql, val)

db.commit()

# populating product_category table

arr = ["1", "1", "2", "2", "3"]

for i in range(5):
    sql = f"INSERT INTO product_category (product_id, category_id) VALUES (%s, %s)"
    val = (
        i + 1,
        arr[i],
    )
    cursor.execute(sql, val)

db.commit()

# populating company_user table
sql = f"INSERT INTO company_user (user_id) VALUES (%s)"
val = [("1",), ("2",), ("3",), ("4",), ("5",)]

cursor.executemany(sql, val)

db.commit()


cursor.close()
db.close()
