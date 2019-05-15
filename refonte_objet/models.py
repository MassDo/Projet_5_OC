#coding:utf-8
from database import my_cursor, cnx, products_final

from repositories import (Tab_categories_repository,
                         Tab_products_repository,
                         Tab_historique_repository)
import constantes as cte 


class Tab_products:

    objects = Tab_products_repository(my_cursor, cnx)

    def __init__(self, *args):
        
        #self.ID_prod  = # afaire
        self.product_name = []
        self.url = []
        self.stores = []
        self.purchase_places = []
        self.code = []
        self.nutrition_grades = []
        self.nova_group = []
        self.sugars_100g = []
        self.salt_100g = []
        self.fat_100g = []
        self.ID_cat = []

        for cat in args[0]:

            for prod in cat:

                self.product_name.append(prod["product_name"])
                self.url.append(prod["url"])
                self.stores.append(prod["stores"])
                self.purchase_places.append(prod["purchase_places"])
                self.code.append(prod["code"])
                self.nutrition_grades.append(prod["nutrition_grades"])
                self.nova_group.append(prod["nova_group"])
                self.sugars_100g.append(prod["sugars_100g"])
                self.salt_100g.append(prod["salt_100g"])
                self.fat_100g.append(prod["fat_100g"])
                self.ID_cat.append(prod["ID_cat"])


class Tab_historique:

    objects = Tab_historique_repository(my_cursor, cnx, buff_cursor)

    def __init__(self, old_ID_prod, new_ID_prod):
        
        self.old_ID_prod = old_ID_prod
        self.new_ID_prod = new_ID_prod

class Tab_categories:

    objects = Tab_categories_repository(my_cursor, cnx)

    def __init__(self, cat_name, cat_description = None):

        #self.ID_hist = # a faire
        self.cat_name = cat_name
        self.cat_description = cat_description

if __name__ == '__main__':

    """
    for name in cte.MY_CATEGORIES:
        try:
            cat = Tab_categories(name)
            cat.objects.fill(name)
        except:
            print("table existante")
            pass
    """
    transaction = Tab_historique(1, 34)
    #transaction.objects.fill(transaction.old_ID_prod, transaction.new_ID_prod)
    pro_trasanction = transaction.objects.show_products(transaction.old_ID_prod, transaction.new_ID_prod)
    print(pro_trasanction)
    #all_product = Tab_products(products_final)
    #all_product.objects.fill()

    #page = all_product.product_name[0:25]
    #tapas_product = all_product.objects.get_product_from_categorie("tapas")
    #print(tapas_product)
    #best_charc = all_product.objects.get_best_product_from_cat("olives")
    #print("BEST CHARCUT \n", best_charc)
    
    

