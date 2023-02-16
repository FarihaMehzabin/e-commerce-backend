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

cursor.execute(
    "ALTER TABLE `ecommerce`.`product_category` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, CHANGE COLUMN `product_id` `product_id` INT NULL , DROP PRIMARY KEY, ADD PRIMARY KEY (`id`); "
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`user` ADD COLUMN `password` VARCHAR(255) NOT NULL DEFAULT 'password' AFTER `last_name`;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`user` ADD COLUMN `username` VARCHAR(45) NOT NULL DEFAULT 'username' AFTER `id`,DROP PRIMARY KEY, ADD PRIMARY KEY (`id`, `username`); "
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`user` ADD COLUMN `salt` VARCHAR(45) NULL AFTER `password`;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`user` DROP COLUMN `username`, DROP PRIMARY KEY, ADD PRIMARY KEY (`id`);"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`user` ADD COLUMN `username` VARCHAR(45) NULL AFTER `id`, CHANGE COLUMN `salt` `salt` VARCHAR(255) NULL DEFAULT NULL , ADD UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE ;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`company` ADD COLUMN `username` VARCHAR(45) NULL AFTER `name`,ADD COLUMN `password` VARCHAR(255) NOT NULL AFTER `username`, ADD COLUMN `salt` VARCHAR(255) NULL AFTER `password`;"
)

cursor.execute(
    "CREATE TABLE `ecommerce`.`session` (`id` INT NOT NULL AUTO_INCREMENT, `guid` VARCHAR(255) NULL, PRIMARY KEY (`id`)); "
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`user` DROP COLUMN `salt`; ALTER TABLE `ecommerce`.`company` DROP COLUMN `salt`;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`session` ADD COLUMN `user_id` INT NULL AFTER `guid`,ADD COLUMN `company_id` INT NULL AFTER `user_id`,ADD COLUMN `language_id` INT NULL AFTER `company_id`,ADD COLUMN `created_date` DATETIME NULL AFTER `language_id`;"
)

cursor.execute(
    "ALTER TABLE `ecommerce`.`session` ADD COLUMN `country_id` INT NULL AFTER `language_id`; ALTER TABLE `ecommerce`.`user` ADD COLUMN `country_id` INT NULL AFTER `password`, ADD COLUMN `language_id` INT NULL AFTER `country_id`; CREATE TABLE `ecommerce`.`country` (`id` INT NOT NULL AUTO_INCREMENT,`country` VARCHAR(255) NULL,PRIMARY KEY (`id`)); CREATE TABLE `ecommerce`.`language` (`id` INT NOT NULL AUTO_INCREMENT,`language` VARCHAR(100) NULL,PRIMARY KEY (`id`)); ALTER TABLE `ecommerce`.`user` CHANGE COLUMN `country_id` `country_id` INT NULL DEFAULT 236 ,CHANGE COLUMN `language_id` `language_id` INT NULL DEFAULT 1 ; ALTER TABLE `ecommerce`.`session` CHANGE COLUMN `language_id` `language_id` INT NULL DEFAULT 1 ,CHANGE COLUMN `country_id` `country_id` INT NULL DEFAULT 236 ;"
)


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

countries = [
    "Afghanistan",
    "Aland Islands",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia, Plurinational State of",
    "Bonaire, Sint Eustatius and Saba",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cape Verde",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands",
    "Colombia",
    "Comoros",
    "Congo",
    "Congo, The Democratic Republic of the",
    "Cook Islands",
    "Costa Rica",
    "Côte d'Ivoire",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Falkland Islands (Malvinas)",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard Island and McDonald Islands",
    "Holy See (Vatican City State)",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran, Islamic Republic of",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea, Democratic People's Republic of",
    "Korea, Republic of",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao",
    "Macedonia, Republic of",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia, Federated States of",
    "Moldova, Republic of",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestinian Territory, Occupied",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Réunion",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Barthélemy",
    "Saint Helena, Ascension and Tristan da Cunha",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Martin (French part)",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten (Dutch part)",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "South Sudan",
    "Svalbard and Jan Mayen",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan, Province of China",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "United States Minor Outlying Islands",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela, Bolivarian Republic of",
    "Viet Nam",
    "Virgin Islands, British",
    "Virgin Islands, U.S.",
    "Wallis and Futuna",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

languages = [
    ("en", "English"),
    ("sq", "Albanian"),
    ("am", "Amharic"),
    ("ar", "Arabic"),
    ("hy", "Armenian"),
    ("as", "Assamese"),
    ("av", "Avaric"),
    ("ae", "Avestan"),
    ("ay", "Aymara"),
    ("az", "Azerbaijani"),
    ("ba", "Bashkir"),
    ("bm", "Bambara"),
    ("eu", "Basque"),
    ("be", "Belarusian"),
    ("bn", "Bengali"),
    ("bo", "Tibetan"),
    ("bs", "Bosnian"),
    ("br", "Breton"),
    ("bg", "Bulgarian"),
    ("my", "Burmese"),
    ("ca", "Catalan; Valencian"),
    ("cs", "Czech"),
    ("ch", "Chamorro"),
    ("ce", "Chechen"),
    ("zh", "Chinese"),
    ("cv", "Chuvash"),
    ("kw", "Cornish"),
    ("co", "Corsican"),
    ("cr", "Cree"),
    ("cy", "Welsh"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("de", "German"),
    ("nl", "Dutch; Flemish"),
    ("eo", "Esperanto"),
    ("et", "Estonian"),
    ("eu", "Basque"),
    ("ee", "Ewe"),
    ("fo", "Faroese"),
    ("fa", "Persian"),
    ("fj", "Fijian"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("ff", "Fulah"),
    ("Ga", "Georgian"),
    ("de", "German"),
    ("ga", "Irish"),
    ("gl", "Galician"),
    ("gv", "Manx"),
    ("gn", "Guarani"),
    ("gu", "Gujarati"),
    ("ht", "Haitian; Haitian Creole"),
    ("ha", "Hausa"),
    ("he", "Hebrew"),
    ("hz", "Herero"),
    ("hi", "Hindi"),
    ("hr", "Croatian"),
    ("hu", "Hungarian"),
    ("hy", "Armenian"),
    ("ig", "Igbo"),
    ("is", "Icelandic"),
    ("io", "Ido"),
    ("id", "Indonesian"),
    ("ik", "Inupiaq"),
    ("is", "Icelandic"),
    ("it", "Italian"),
    ("jv", "Javanese"),
    ("ja", "Japanese"),
    ("kl", "Kalaallisut; Greenlandic"),
    ("ks", "Kashmiri"),
    ("ka", "Georgian"),
    ("kr", "Kanuri"),
    ("kk", "Kazakh"),
    ("km", "Central Khmer"),
    ("ki", "Kikuyu; Gikuyu"),
    ("rw", "Kinyarwanda"),
    ("ky", "Kirghiz; Kyrgyz"),
    ("kv", "Komi"),
    ("kg", "Kongo"),
    ("ko", "Korean"),
    ("kj", "Kuanyama; Kwanyama"),
    ("ku", "Kurdish"),
    ("lo", "Lao"),
    ("la", "Latin"),
    ("lv", "Latvian"),
    ("li", "Limburgan; Limburger; Limburgish"),
    ("ln", "Lingala"),
    ("lt", "Lithuanian"),
    ("lb", "Luxembourgish; Letzeburgesch"),
    ("lu", "Luba-Katanga"),
    ("lg", "Ganda"),
    ("mk", "Macedonian"),
    ("mh", "Marshallese"),
    ("ml", "Malayalam"),
    ("mi", "Maori"),
    ("mr", "Marathi"),
    ("ms", "Malay"),
    ("Mi", "Micmac"),
    ("mk", "Macedonian"),
    ("mg", "Malagasy"),
    ("mt", "Maltese"),
    ("mn", "Mongolian"),
    ("mi", "Maori"),
    ("ms", "Malay"),
    ("my", "Burmese"),
    ("na", "Nauru"),
    ("nv", "Navajo; Navaho"),
    ("nr", "Ndebele, South; South Ndebele"),
    ("nd", "Ndebele, North; North Ndebele"),
    ("ng", "Ndonga"),
    ("ne", "Nepali"),
    ("nl", "Dutch; Flemish"),
    ("nn", "Norwegian Nynorsk; Nynorsk, Norwegian"),
    ("nb", "Bokmål, Norwegian; Norwegian Bokmål"),
    ("no", "Norwegian"),
    ("oc", "Occitan (post 1500)"),
    ("oj", "Ojibwa"),
    ("or", "Oriya"),
    ("om", "Oromo"),
    ("os", "Ossetian; Ossetic"),
    ("pa", "Panjabi; Punjabi"),
    ("fa", "Persian"),
    ("pi", "Pali"),
    ("pl", "Polish"),
    ("pt", "Portuguese"),
    ("ps", "Pushto; Pashto"),
    ("qu", "Quechua"),
    ("rm", "Romansh"),
    ("ro", "Romanian; Moldavian; Moldovan"),
    ("ro", "Romanian; Moldavian; Moldovan"),
    ("rn", "Rundi"),
    ("ru", "Russian"),
    ("sg", "Sango"),
    ("sa", "Sanskrit"),
    ("si", "Sinhala; Sinhalese"),
    ("sk", "Slovak"),
    ("sk", "Slovak"),
    ("sl", "Slovenian"),
    ("se", "Northern Sami"),
    ("sm", "Samoan"),
    ("sn", "Shona"),
    ("sd", "Sindhi"),
    ("so", "Somali"),
    ("st", "Sotho, Southern"),
    ("es", "Spanish; Castilian"),
    ("sq", "Albanian"),
    ("sc", "Sardinian"),
    ("sr", "Serbian"),
    ("ss", "Swati"),
    ("su", "Sundanese"),
    ("sw", "Swahili"),
    ("sv", "Swedish"),
    ("ty", "Tahitian"),
    ("ta", "Tamil"),
    ("tt", "Tatar"),
    ("te", "Telugu"),
    ("tg", "Tajik"),
    ("tl", "Tagalog"),
    ("th", "Thai"),
    ("bo", "Tibetan"),
    ("ti", "Tigrinya"),
    ("to", "Tonga (Tonga Islands)"),
    ("tn", "Tswana"),
    ("ts", "Tsonga"),
    ("tk", "Turkmen"),
    ("tr", "Turkish"),
    ("tw", "Twi"),
    ("ug", "Uighur; Uyghur"),
    ("uk", "Ukrainian"),
    ("ur", "Urdu"),
    ("uz", "Uzbek"),
    ("ve", "Venda"),
    ("vi", "Vietnamese"),
    ("vo", "Volapük"),
    ("cy", "Welsh"),
    ("wa", "Walloon"),
    ("wo", "Wolof"),
    ("xh", "Xhosa"),
    ("yi", "Yiddish"),
    ("yo", "Yoruba"),
    ("za", "Zhuang; Chuang"),
    ("zh", "Chinese"),
    ("zu", "Zulu"),
]

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


# populating country table

for i in range(len(countries)):

    sql = f"INSERT INTO country (country) VALUES (%s)"
    val = countries[i]

    cursor.execute(sql, val)

    db.commit()

# populating language table

for i in range(len(languages)):

    sql = f"INSERT INTO language (language) VALUES (%s)"
    val = languages[i][0]

    cursor.execute(sql, val)

    db.commit()

cursor.close()
db.close()
