import constantes as cte
from functions import *

# MySQL connection
cnx = mysql.connector.connect(**cte.CONFIG)
my_cursor = cnx.cursor()


# Create and activate database
create_database(my_cursor, cte.DB_NAME)
try:
    my_cursor.execute("USE {}".format(cte.DB_NAME)) # select the DB
except mysql.connector.error as err:
    print(err)
    
# Create Table
try:
    create_table(my_cursor, cte.CREATE_CATEGORIES)
    create_table(my_cursor, cte.CREATE_PRODUCTS)
    create_table(my_cursor, cte.CREATE_HISTORIQUE)    
except:
    print("erreur de creation de table")
    pass

#-----------------------------------------------------------------------------
# Download and check data ----------------------------------------------------
#-----------------------------------------------------------------------------

products_final = []
for id_cat, categorie in enumerate(cte.MY_CATEGORIES):
    
    # Products Formatting
    products_unchecked = download_products(categorie[0]) # Download the products from a categorie [{P0}, ..., {Pn}]
                                                         #[{'':'', ..., {}}, ..., {'':'', ..., {}}]
    products_checked = check_products(products_unchecked) # eliminate incomplete product
        
    # Adding ID_cat at the end of each dictionary
    id_cat += 1
    products_checked = [dict(prod,**{'ID_cat':id_cat}) for prod in products_checked]  # products_checked is [{}, ..., {}] where
                                                       # {} is a product
    # Formating "nutriments" values from dict to elements
    products_checked_format = formating_data(products_checked) # [{'':'', ..., '':''}, ..., {'':'', ..., '':''}] 
    products_final.append(products_checked_format) 

# products_final structure is: 
# [[products of cat 1], [products of cat 2], [products of cat 3]]
# Where [products of cat 1] structure is [{P0 of cat 1}, ... , {Pn of cat 1}]
# Where {first product of cat 1} structure is {'fields':'value', ..., '':''}
# RESUME
# product_final structure is:
# [[{'':'', ..., '':''}, ..., {'':'', ..., '':''}], [], []]

# [[{P0 of cat 1}, ... , {Pn of cat 1}], ..., [{P0 of cat n}, ... , {Pn of cat n}]]

# [[{}, ..., {}], ..., [{}, ..., {}]]






    