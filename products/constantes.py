#coding:utf-8

# Connection
CONFIG = {
        "host":"localhost",
        "user":"root",
        "password":"",
}

DB_NAME = "purbeurre"

# Create tables
CREATE_CATEGORIES = """ CREATE TABLE tab_categories(
                    ID_cat int AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    cat_name varchar(255) NOT NULL,
                    cat_description TEXT
                    ) ENGINE=InnoDB
"""

CREATE_PRODUCTS = """ CREATE TABLE tab_products(
                    ID_prod int AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    product_name varchar(255) NOT NULL,
                    url varchar(255) NOT NULL,
                    stores varchar(255) NOT NULL,
                    purchase_places varchar(255) NOT NULL,
                    code varchar(255) NOT NULL,
                    nutrition_grades varchar(2) NOT NULL,
                    nova_group varchar(2) NOT NULL,
                    sugars_100g varchar(50) NOT NULL,
                    salt_100g varchar(50) NOT NULL,
                    fat_100g varchar(50) NOT NULL,
                    ID_cat int NOT NULL,
                    FOREIGN KEY fk_cat(ID_cat) REFERENCES tab_categories(ID_cat) 
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT                   
                    ) ENGINE=InnoDB

"""
CREATE_HISTORIQUE = """
        CREATE TABLE tab_historique(
        ID_hist int AUTO_INCREMENT PRIMARY KEY NOT NULL,
        old_ID_prod int NOT NULL,
        new_ID_prod int NOT NULL,
        FOREIGN KEY fk_prod_old(old_ID_prod) REFERENCES tab_products(ID_prod),
        FOREIGN KEY fk_prod_old_2(new_ID_prod) REFERENCES tab_products(ID_prod)  
        )ENGINE=InnoDB
"""

# TABLE tab_categories
MY_CATEGORIES = (
                ('tapas',),
                ('olives',),
                ('charcuteries-diverses',)
)
SQL_ADD_CAT = """INSERT INTO tab_categories (cat_name) VALUES (%s)"""

# TABLE tab_products

SQL_ADD_PROD = """ INSERT INTO tab_products(
                product_name,
                url,
                stores,
                purchase_places,
                code,
                nutrition_grades,
                nova_group,
                sugars_100g ,
                salt_100g,
                fat_100g,
                ID_cat                 
                ) 
                VALUES(
                %(product_name)s,
                %(url)s,
                %(stores)s,
                %(purchase_places)s,
                %(code)s,
                %(nutrition_grades)s,
                %(nova_group)s,
                %(sugars_100g)s,
                %(salt_100g)s,
                %(fat_100g)s,
                %(ID_cat)s)
"""

# keys of the products dict Used in the function check_products
prod_keys = [           
            "product_name",
            "url",
            "stores",
            "purchase_places",      # API fields of the product choosed by ADMIN
            "code",
            "nutrition_grades",
            "nova_group",
            "nutriments"
]

nutri_keys = [
            "sugars_100g",
            "salt_100g",            # sub-fields of "nutriments" api fields
            "fat_100g"
]

