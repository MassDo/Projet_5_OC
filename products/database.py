# coding:utf-8

"""
    Create database, table and api connection.
"""

from products.functions import *

cnx = mysql.connector.connect(**cte.CONFIG)
my_cursor = cnx.cursor()


def database():

    """
        This function create the database
        and the tables using others functions.
        After that it's create a structured variable (products_final)
        witch contains the products API fields
        checked from empty values and formatted.

        # products_final structure is:

        [[products of cat 1], [products of cat 2], [products of cat 3]]
        Where [products of cat 1] structure is [{first product of cat 1}, ... , {last product of cat 1}]
        Where {first product of cat 1} structure is {'fields':'value', ..., '':''}

        # RESUME

        # product_final structure is:
        [[{'':'', ..., '':''}, ..., {'':'', ..., '':''}], [], []]
        # product_final structure is:
        [[{P0 of cat 1}, ... , {Pn of cat 1}], ..., [{P0 of cat n}, ... , {Pn of cat n}]]
        # product_final structure is:
        [[{}, ..., {}], ..., [{}, ..., {}]]

        this structure is used for the instantiation of TabProducts objects.

    """
       
    # Create and use database
    create_database(my_cursor, cte.DB_NAME)
    try:
        use_database(my_cursor)
                        
    except:        
        print("erreur de création de base de donnée")
        
    # Create Table
    try:
        create_table(my_cursor, cte.CREATE_CATEGORIES)
        create_table(my_cursor, cte.CREATE_PRODUCTS)
        create_table(my_cursor, cte.CREATE_HISTORIQUE)    
    except:
        print("erreur de creation de table")
        pass

    # ----------------------------------------------------------------------------
    # Download and check data ----------------------------------------------------
    # ----------------------------------------------------------------------------
    
    for id_cat, categorie in enumerate(cte.MY_CATEGORIES):
        
        # Products Formatting
        # Download the products from a categorie [{P0}, ..., {Pn}]
        # [{'':'', ..., {}}, ..., {'':'', ..., {}}]
        products_unchecked = download_products(categorie[0])
        # eliminate incomplete product
        products_checked = check_products(products_unchecked)
        # Adding ID_cat at the end of each dictionary
        id_cat += 1
        products_checked = [dict(prod, **{'ID_cat': id_cat})
                            for prod in products_checked]
        # products_checked is [{}, ..., {}] where {} is a product
        # Formatting "nutriments" values from dict to elements
        products_checked_format = formating_data(products_checked)
        products_final.append(products_checked_format)
