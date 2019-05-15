#coding:utf-8
import os
import functions
import mysql.connector
import constantes as cte

# ----------------------------------------------------------------------------
# DATABASE -------------------------------------------------------------------
# ----------------------------------------------------------------------------

# MySQL connection setting
cnx = mysql.connector.connect(**cte.CONFIG)
my_cursor = cnx.cursor()
#my_cursor.execute("DROP DATABASE purbeurre")

# creation and activation of the database
#functions.create_database(my_cursor, cte.DB_NAME)
try:
    my_cursor.execute("USE {}".format(cte.DB_NAME)) # select the DB
except mysql.connector.error as err:
    print(err)
    
# Create Table
try:
    my_cursor.execute(cte.CREATE_CATEGORIES) # table tab_categories
    my_cursor.execute(cte.CREATE_PRODUCTS)   # table tab_products
    my_cursor.execute(cte.CREATE_HISTORIQUE)
except:
    pass

# Fill the tables ***************************************************** A FAIRE
#my_cursor.executemany(cte.SQL_ADD_CAT, cte.MY_CATEGORIES) # inser cat_name
#cnx.commit()

for id_cat, categorie in enumerate(cte.MY_CATEGORIES):
    
    # Products Formatting
    products_unchecked = functions.download_products(categorie[0]) # Download the products from a categorie
    products_checked = functions.check_products(products_unchecked)

    # Adding ID_cat adding id-cat at the end of each dictionary
    id_cat += 1
    products_checked = [dict(prod, **{'ID_cat':id_cat}) for prod in products_checked]

    # Formating "nutriments" values from dict to elements
    products_checked_format = functions.formating_data(products_checked)

    # Fill TABLE PRODUCTS
    #my_cursor.executemany(cte.SQL_ADD_PROD, products_checked_format)
    #cnx.commit()

# ----------------------------------------------------------------------------
# INTERFACE ------------------------------------------------------------------
# ----------------------------------------------------------------------------

# MENU

main_loop = 1
while main_loop:# ___________________________________________________________________________________________________________________________
    menu = 1
    change_food = 1
    print("\n********** MENU PRINCIPAL **********\n")
    print("\t1 - Quel aliment souhaitez-vous remplacer ?\n\t2 - Retrouver mes aliments substitués.")

    # MENU CHOICE# ___________________________________________________________________________________________________________________________
    while menu:        
        try:
            menu_choice = int(input("\nchoix:"))
            if menu_choice in range(1,3):
                menu = 0
            else:
                print("\nVeuillez saisir le numéro 1 ou 2")
        except:
            print("\nVeuillez saisir le numéro 1 ou 2")

    if menu_choice == 1:
        
        # MENU 1
        while change_food:# ___________________________________________________________________________________________________________________________

            # CAT DISPLAY
            print("\n********** CATEGORIES **********\n")
            for num, cat in enumerate(cte.MY_CATEGORIES):
                num+=1
                print("\t", num, "-", cat[0])

            limit = 25
            offset = 0
            cat_choice = 1
            display_food_1 = 1
            
            food_last = 1

            # CAT CHOICE
            while cat_choice:

                try:
                    ID_cat = int(input("\nSélectionnez la catégorie:"))
                    if ID_cat in range(1,4):
                        cat_choice = 0
                    else:
                        print("\nVeuillez saisir un numéro entre 1 et 3")
                except:
                    print("\nVeuillez saisir un numéro entre 1 et 3")

            while display_food_1:

                # Display Food
                display_food_2 = 1
                while display_food_2:# ___________________________________________________________________________________________________________________________
                    
                    SQL = """ SELECT ID_prod, product_name FROM tab_products
                            WHERE ID_cat = {}
                            LIMIT {}
                            OFFSET {}
                    """.format(ID_cat, limit, offset)

                    my_cursor.execute(SQL)
                    food = my_cursor.fetchall() # food = ((id_prod_1, nom_pro_1), (id_prod_2, nom_pro_2) )
                    print("\n************************ LISTE ************************\n*")
                    for prod in food:
                        print("*\t", prod[0], "-", prod[1].replace("\n", "")) 
                    print("\n SUITE 's', RETOUR 'r'")                
                        
                    # Food
                    food_choice = 1
                    while food_choice: 

                        user_input = input("\nSélectionnez l'aliment :  ")
                              
                        if user_input.lower() == "s":
                            offset += 25
                            try:
                                food[-1][0]
                            except:
                                offset -= 25
                                print("\n FIN DE LISTE !!!!!\n")

                            food_choice = 0 
                        elif user_input.lower() == "r" and offset != 0:
                            offset -= 25 
                            food_choice = 0          
                        else:
                            try:
                                user_input = int(user_input)                            
                                display_food_2 = 0
                                food_choice = 0 
                            except:
                                continue

                    # requete de trie
                SQL = """ 
                        SELECT * FROM tab_products
                        WHERE ID_cat = {} 
                        ORDER BY 
                                nova_group ASC,
                                nutrition_grades ASC,
                                CAST(fat_100g as DECIMAL(5, 3)) ASC,
                                CAST(sugars_100g as DECIMAL(5, 3)) ASC,
                                CAST(salt_100g as DECIMAL(5, 3)) ASC                
                """.format(ID_cat)

                my_cursor.execute(SQL)
                liste_aliments_tries = my_cursor.fetchall()            
                print("\n========================================  Meilleur produit ========================================")
                
                print("****** PRODUIT: {}".format(liste_aliments_tries[0][1]), "\n")
                print("****** LIEN: {}".format(liste_aliments_tries[0][2]), "\n")
                print("****** LIEUX D'ACHAT: {}, {}".format(liste_aliments_tries[0][3],\
                    liste_aliments_tries[0][4]))
                print("===================================================================================================\n") 

                again = 1            
                while again:
                    replace = input("Voulez vous valider le remplacement du produit ? 'o/n'").lower()
                    
                    if replace in ("o", "n"):                    
                        again = 0 
                        
                        if replace == "o":                                    
                            SQL_ADD_HIST = """
                                            INSERT INTO tab_historique (old_ID_prod, new_ID_prod)
                                            VALUES (%s, %s)
                            """
                            my_cursor.execute(SQL_ADD_HIST, (user_input, liste_aliments_tries[0][0])) 
                            cnx.commit()
                            print("\nProduit enregistré avec succès")

                        user_input = input("\nretour menu principal 'm', 'q' pour quitter,  autre touche pour continuer:...").lower()            
                        if user_input == "m":
                            change_food = 0
                            display_food_1 = 0
                            display_food_2 = 0 

                        if user_input == "q":
                            change_food = 0
                            display_food_1 = 0
                            display_food_2 = 0
                            main_loop = 0
                            print(" \n fermeture du logiciel, aurevoir !\n")            

    # MENU 2
    else:
    # affichage de l'historique
        menu_hist = 1
        while menu_hist:

            SQL_GET_HIST = """ SELECT * FROM tab_historique """
            my_cursor.execute(SQL_GET_HIST)
            changes = my_cursor.fetchall()

            print("Votre historique de produits remplacés est:\n")
            
            for change in changes:
                        
                SQL_OLD = """ 
                        SELECT product_name, url
                        FROM tab_products
                        WHERE ID_prod = {}""".format(change[1])
                SQL_NEW = """ 
                        SELECT product_name, url
                        FROM tab_products
                        WHERE ID_prod = {}""".format(change[2])

                my_cursor.execute(SQL_OLD)
                old_prod = my_cursor.fetchall()
                my_cursor.execute(SQL_NEW)
                new_prod = my_cursor.fetchall()

                print("\t{} - Ancien produit: {} // Nouveau produit: {} ".format(change[0],\
                old_prod[0][0], new_prod[0][0]))
                print("\t\tAncien url:\n\t\t{}\n\t\tNouveau url:\n\t\t{} \n\n".format(old_prod[0][1], new_prod[0][1]))
                
            menu_hist = 0

        user_input = input("\n'q' pour quitter, autre touche pour retourner au menu principal:").lower()

        if user_input == "m":
            pass

        if user_input == "q":
            
            main_loop = 0
            print(" \n fermeture du logiciel, aurevoir !\n") 

os.system("pause")

# VALIDE