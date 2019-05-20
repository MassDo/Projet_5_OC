# coding:utf-8

"""
    This module regroup the methods called
    by the class attribute "objects" from the
    classes of the module "models".

    The goal of this module is to set a layer of abstraction
    that deal with the sql queries.

"""

from products.settings import products_final
from products.functions import use_database

 
class BaseRepository:
    """
        This parent class is used to give
        cursor and connection in heritage.
    """

    def __init__(self, my_cursor, cnx):

        self.my_cursor = my_cursor
        self.cnx = cnx


class TabCategoriesRepository(BaseRepository):
    """
        Class used to regroup the methods used
        to manipulate the table "tab_categories".

    """

    def fill(self, cat_name):
        """
            fill the table with cat_name
        """
        sql = """INSERT INTO purbeurre.tab_categories (cat_name) VALUES (%s)"""
        self.my_cursor.execute(sql, cat_name)
        self.cnx.commit()


class TabProductsRepository(BaseRepository):
    """
        Class used to regroup the methods used
        to manipulate the table "tab_products".

    """

    def fill(self):
        """
            fill the table with the object's attributes
        """
        use_database(self.my_cursor)
        sql = """ INSERT INTO tab_products(
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
        for cat in products_final:
            self.my_cursor.executemany(sql, cat)
            self.cnx.commit()

    def get_product_from_categorie(self, categorie):

        """
            return a list of the categorie's products: [(), ..., ()]
            where the tuple are filled with product columns fields
            () = (ID_prod, product_name, ..., ID_cat)
        """

        sql = """ 
                SELECT ID_cat FROM tab_categories
                WHERE cat_name = '{}'
            """.format(categorie)

        self.my_cursor.execute(sql)
        id_cat = self.my_cursor.fetchall()

        sql = """
                SELECT * FROM tab_products
                WHERE ID_cat = {}
            """.format(int(id_cat[0][0]))

        self.my_cursor.execute(sql)

        return self.my_cursor.fetchall()

    def get_best_product_from_cat(self, ID_cat):

        """
            return a list of the fields of the best food
            for categories
        """

        sql = """ 
                SELECT * FROM tab_products
                WHERE ID_cat = {} 
                ORDER BY 
                        nova_group ASC,
                        nutrition_grades ASC,
                        CAST(fat_100g as DECIMAL(5, 3)) ASC,
                        CAST(sugars_100g as DECIMAL(5, 3)) ASC,
                        CAST(salt_100g as DECIMAL(5, 3)) ASC                
            """.format(ID_cat)

        self.my_cursor.execute(sql)
        liste_aliments_tries = self.my_cursor.fetchall()

        return liste_aliments_tries[0]

    def get_id(self, ID_cat):
        """
            get the list of the products's id
            for a categorie
        """

        sql = """
                SELECT ID_prod 
                FROM tab_products
                WHERE ID_cat = {}
            """.format(ID_cat)
        self.my_cursor.execute(sql)

        return self.my_cursor.fetchall()


class TabHistoriqueRepository(BaseRepository):
    """
        Class used to regroup the methods
        to manipulate the table "tab_historique".

    """
       
    def fill(self, old_id_prod, new_id_prod):
        """
            fill the table with the object's attributes
        """
        sql = """
                INSERT INTO tab_historique(old_id_prod, new_id_prod)
                VALUES (%s, %s)
            """
        self.my_cursor.execute(sql, (old_id_prod, new_id_prod))
        self.cnx.commit() 

    def show_products_old_new(self):
        """
            show the fields of the old and new products
        """
        
        sql = """
                SELECT old_id_prod, new_id_prod
                FROM tab_historique                
        """
        self.my_cursor.execute(sql)
        transactions = self.my_cursor.fetchall()

        historique_all = []
        for transac in transactions:
            historique_transac = []
            for id_prod in transac:        

                sql = """
                        SELECT * FROM tab_products
                        WHERE ID_prod = {}
                    """.format(id_prod)

                self.my_cursor.execute(sql)
                prod = self.my_cursor.fetchone()
                historique_transac.append(prod)
            historique_all.append(historique_transac)         

        return historique_all
        # historique_all structure:
        # [[(old1), (new1)], [(old2), (new2)], ..., [(old n), (new n)]]
