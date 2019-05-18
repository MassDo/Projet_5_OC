#coding:utf-8
import requests
import mysql.connector
import constantes as cte

"""
    Functions used in the main module
"""

def create_database(cursor, name):
    """
        Create a database named after "name" if 
        it doesn't exist.       
    """
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
 
def create_table(cursor, SQL_request): #valide
    """
        Create table if 
        it doesn't exist.

        request (type==str) is the SQL request for the 
        creation of the table. 
    """
    try:
        cursor.execute(SQL_request)
    except mysql.connector.Error as err:
        print("Failed creating table: {}".format(err))

def download_products(categorie): #valide
    """
        get the rows products from a categorie 
        from the API in .json
        
    """
    API_PAYLOAD = {"action":"process",
           "tagtype_0":"categories",
           "tag_contains_0":"contains",
           "tag_0":"tapas",
           "page_size":1000,
           "json":1
           }
    API_PAYLOAD["tag_0"] = categorie
    try:
        r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=API_PAYLOAD).json()
        products_unchecked = r["products"]        
        return products_unchecked    # [{}, ..., {}]
    except:
        print("Error whith api request")

def check_products(products=list): #valide
    """
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
        this function is replacing the element "nutriment"
        by the tuple of his elements.

        Example:
        
        >>> formating_data([{"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}}, {"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}}])
        [{'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4}, {'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4}]

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



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print("test succesfull")




