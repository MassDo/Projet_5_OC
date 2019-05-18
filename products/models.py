#coding:utf-8
import mysql.connector
from products.repositories import (Tab_categories_repository,
                                    Tab_products_repository,
                                    Tab_historique_repository)
import products.constantes as cte 

# MySQL connection
cnx = mysql.connector.connect(**cte.CONFIG)
my_cursor = cnx.cursor()

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

    objects = Tab_historique_repository(my_cursor, cnx)

    def __init__(self, old_ID_prod = None, new_ID_prod = None):
        
        self.old_ID_prod = old_ID_prod
        self.new_ID_prod = new_ID_prod

class Tab_categories:

    objects = Tab_categories_repository(my_cursor, cnx)

    def __init__(self, cat_name = None, cat_description = None):

        #self.ID_hist = # a faire
        self.cat_name = cat_name
        self.cat_description = cat_description

    def __iter__(self):
        return self
