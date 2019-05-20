# coding:utf-8

"""
    This module regroup the classes
    that modelise the database's tables

    Each class represent a table
"""
import mysql.connector
from products.repositories import (TabCategoriesRepository,
                                   TabProductsRepository,
                                   TabHistoriqueRepository)
import products.constantes as cte 

# MySQL connection
cnx = mysql.connector.connect(**cte.CONFIG)
my_cursor = cnx.cursor()


class TabProducts:
    """
        model of the tab_products
    """

    objects = TabProductsRepository(my_cursor, cnx)

    def __init__(self, *args):

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


class TabHistorique:
    """
        model of the tab_products
    """

    objects = TabHistoriqueRepository(my_cursor, cnx)

    def __init__(self, old_id_prod = None, new_id_prod = None):
        
        self.old_id_prod = old_id_prod
        self.new_id_prod = new_id_prod


class TabCategories:
    """
        model of the tab_products
    """

    objects = TabCategoriesRepository(my_cursor, cnx)

    def __init__(self, cat_name = None, cat_description = None):

        self.cat_name = cat_name
        self.cat_description = cat_description

    def __iter__(self):
        return self
