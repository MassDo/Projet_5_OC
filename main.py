# coding:utf-8

"""
    This main module regrouping
    the checking of first connection
    and the structure of the menu interface.
"""

from products.database import database, products_final

from products.models import (TabProducts,
                             TabHistorique,
                             TabCategories,
                             cnx,
                             my_cursor)

import products.constantes as cte


from products.functions import first_connection, recover_database_data

# Creation of the database and download data from API if first connection
if first_connection(my_cursor): 
    database()

    # MENU
    for name in cte.MY_CATEGORIES:
        cat = TabCategories()
        cat.objects.fill(name)
        
    all_product = TabProducts(products_final)
    all_product.objects.fill()
# if not first con, recover the products structure from    
else:
    recover_database_data(my_cursor)
    all_product = TabProducts(products_final)

# MAIN MENU ------------------------------------------------------------------
main_loop = 1
while main_loop:
    menu = 1
    change_food = 1
    print("\n\n\n\n\n\n\n\n\t********** MENU PRINCIPAL **********\n")
    print("\t1 - Quel aliment souhaitez-vous remplacer ?\
\n\t2 - Retrouver mes aliments substitués.")

    # main menu choice
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

        # MENU CATEGORIES ----------------------------------------------------
        while change_food:
            # CATEGORIES DISPLAY
            print("\n\t********** CATEGORIES **********\n")
            for num, cat in enumerate(cte.MY_CATEGORIES):
                num+=1
                print("\t", num, "-", cat[0])

            limit = 25
            offset = 0
            cat_choice = 1
            display_food_1 = 1

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
                # last ID_prod of a categories
                last_ID = all_product.objects.get_id(ID_cat)[-1][0]
                # first ID_prod of a categories
                first_ID = all_product.objects.get_id(ID_cat)[0][0]
                start = first_ID - 1
                start_ident = 0                
                end = first_ID + 24
                end_ident = 25

                # DISPLAY FOOD BY 25 -----------------------------------------
                while display_food_2:

                    name = all_product.product_name[start:end]
                    ident = all_product.objects.get_id(ID_cat)
                    ident = ident[start_ident:end_ident]
                    
                    print("\n************************ LISTE ****************\
********\n*")
                    for el in zip(ident, name):
                        print("*\t", el[0][0], "-", el[1].replace("\n", ""))
                        last_ID_display = el[0][0]
                    print("\n SUITE 's', RETOUR 'r'")              
                        
                    # Food
                    food_choice = 1
                    while food_choice: 
                        user_input = input("\nSélectionnez l'aliment :  ")                                                          
                        if user_input.lower() == "s" \
                                and last_ID_display != last_ID:
                            start += 25
                            start_ident += 25
                            end += 25
                            end_ident += 25
                            food_choice = 0                                
                        elif user_input.lower() == "r" \
                                and last_ID_display != (first_ID +24):
                            start -= 25
                            start_ident -= 25
                            end -= 25
                            end_ident -= 25
                            food_choice = 0                                         
                        else:                                
                            try:                       
                                user_input = int(user_input) 
                                ID_prod_old = user_input                          
                                display_food_2 = 0
                                food_choice = 0 
                            except:
                                continue 

                    # requete de trie
                best_food = \
                    all_product.objects.get_best_product_from_cat(ID_cat)

                print("\n==============================\
==========  Meilleur produit ========================================")
                print("****** PRODUIT: {}".format(best_food[1]), "\n")
                print("****** LIEN: {}".format(best_food[2]), "\n")
                print("****** LIEUX D'ACHAT: {}, {}".format(best_food[3],
                                                            best_food[4]))
                print("=================================\
==================================================================\n")

                # VALIDATION OF CHANGING PRODUCT -----------------------------
                again = 1 
                while again:
                    replace = input("Voulez vous valider\
 le remplacement du produit ? 'o/n'").lower()
                    if replace in ("o", "n"):                    
                        again = 0                         
                        if replace == "o":                                    
                            transaction = TabHistorique(ID_prod_old,
                                                        int(best_food[0]))
                            try:
                                transaction.objects.fill(
                                    transaction.old_id_prod,
                                    transaction.new_id_prod)
                                print("\nProduit enregistré avec succès")
                            except:
                                print("Error with products remplacement")

                        user_input = input("\nretour menu principal 'm'\
, 'q' pour quitter,  autre touche pour continuer:...").lower()
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

    # MENU HISTORIQUE --------------------------------------------------------
    else:
        # historic display
        menu_hist = 1
        while menu_hist:

            print("Votre historique de produits remplacés est:\n")
            temp = TabHistorique()            
            historic = temp.objects.show_products_old_new()
            if not historic:
                print("\t\tL'historique est vide")                

            for counter,transac in enumerate(historic):
                counter += 1  
                prod_trans = (transac[0],transac[1])

                print("\t{} - Ancien produit: {} //\
 Nouveau produit: {} ".format(
                        counter,
                        prod_trans[0][1],
                        prod_trans[1][1]))

                print("\t\tAncien url:\n\t\t{}\n\t\t\
 Nouveau url:\n\t\t{} \n\n".format(
                                prod_trans[0][2],
                                prod_trans[1][2]))
                
            menu_hist = 0

        user_input = input("\n'q' pour quitter, autre touche pour\
 retourner au menu principal:").lower()

        if user_input == "m":
            pass

        if user_input == "q":
            
            main_loop = 0
            print(" \n fermeture du logiciel, aurevoir !\n")

cnx.close()
