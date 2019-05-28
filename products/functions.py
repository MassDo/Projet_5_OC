# coding:utf-8

"""
    Functions used in the main and database modules
"""

import requests
import mysql.connector

from products.settings import products_final
import products.constantes as cte


def first_connection(cursor):
    """
        return 1 if database "purbeurre" doesn't exist   
    """
    flag = 1
    cursor.execute("SHOW DATABASES")
    result = cursor.fetchall()
    for db in result:
        if cte.DB_NAME in db:
            flag = 0
    return flag


def create_database(cursor, name):
    """
        Create a database named after "name" if 
        it doesn't exist.       
    """
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
        print("\nPremière utilisation\n\
Création de la base de données.\n Veuillez patienter quelques secondes ...")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

    
def use_database(cursor):
    """
        Select the database nemed
        in the constantes module.
    """

    cursor.execute("USE {}".format(cte.DB_NAME))

    
def create_table(cursor, sql_request):
    """
        Create table if it doesn't exist.

        request (type==str) is the sql request for the
        creation of the table. 
    """
    try:
        cursor.execute(sql_request)
    except mysql.connector.Error as err:
        print("Failed creating table: {}".format(err))


def download_products(categorie):
    """
        get the rows products from a categorie 
        from the API in .json
        
    """
    api_payload = {
                    "action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "tag_0": categorie,
                    "page_size": 1000,
                    "json": 1
                    }

    try:
        r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=api_payload).json()
        products_unchecked = r["products"]        
        return products_unchecked
    except:
        print("Error whith api request")


def check_products(products):
    """
        products is a list.

        delete product with incomplete fields from the products list
        and return a list of complete products.
    """
    products_checked = []     

    for prod in products:
        prod_checked = {} 
        product_is_complete = True

        for key1 in cte.prod_keys:
            try:
                if key1 == "nutriments":
                    nut_checked = {}
                    nutriment_is_complete = True 

                    for key2 in cte.nutri_keys:
                        try:                    
                            if prod[key1][key2] is not "":
                                nut_checked[key2] = prod[key1][key2]
                            else:
                                nutriment_is_complete = False
                                break
                        except:
                            nutriment_is_complete = False
                            break

                    if nutriment_is_complete:
                        prod_checked[key1] = nut_checked
                elif key1 is not "nutriment" and prod[key1] is not "":
                    prod_checked[key1] = prod[key1]
                else:
                    product_is_complete = False
                    break
            except:
                product_is_complete = False
                break

        if product_is_complete and nutriment_is_complete:
            products_checked.append(prod_checked)

    return products_checked


def formating_data(products):
    """
        this function is into a dict of one product.
        Merging the nutriment dict into product dict
        and deleting the nutriment key from product's keys.

        Example:
        
        >>> formating_data([\
        {"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}},\
        {"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}}])
        [{'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4},\
 {'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4}]

    """
    products_format = []
    for prod in products:
        for key in list(prod):
            if key is "nutriments":
                temp = prod[key]
                del prod[key]
                prod = {**prod, **temp}
                products_format.append(prod)
    return products_format


def recover_database_data(cursor):
    """
        this function recover the data
        of the products fields from the database.

        the data goes into the global variable
        "products_final" in a special structure form.

        products_final structure is:

        [[{}, ..., {}], ..., [{}, ..., {}]]

    """

    use_database(cursor)
    prod_keys = [           
            "product_name",
            "url",
            "stores",
            "purchase_places",      
            "code",
            "nutrition_grades",
            "nova_group",
            "sugars_100g",
            "salt_100g",
            "fat_100g",
            "ID_cat"]
    
    for cat in range(1, 4):

        sql = """
        SELECT product_name,
                url,
                stores,
                purchase_places,
                code,
                nutrition_grades,
                nova_group,
                sugars_100g,
                salt_100g,
                fat_100g,
                ID_cat
                
        FROM tab_products
        WHERE ID_cat = {}
        """.format(cat)
        cursor.execute(sql)
        
        temp_list = []        
        for food in cursor.fetchall():
            food_dict = {}
            for ident, key in enumerate(prod_keys):
                food_dict[key] = food[ident]        

            temp_list.append(food_dict)

        products_final.append(temp_list)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
