#coding:utf-8
import constantes as cte 
from database import products_final

class Base_repository:

    def __init__(self, my_cursor, cnx, buff_cursor = None):

        self.my_cursor = my_cursor
        self.cnx = cnx
        

class Tab_categories_repository(Base_repository):
    
    def fill(self, cat_name):
        """
            fill the table with the object's attributes
        """
        SQL = """INSERT INTO tab_categories (cat_name) VALUES (%s)"""
        self.my_cursor.execute(SQL, cat_name)
        self.cnx.commit()       
    

class Tab_products_repository(Base_repository):

    def fill(self):
        """
            fill the table with the object's attributes
        """
        SQL = """ INSERT INTO tab_products(
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
            self.my_cursor.executemany(SQL, cat)
            self.cnx.commit()

    def get_product_from_categorie(self, categorie):

        """
            return a list of the categorie's products: [(), ..., ()]
            where the tuple are filled with product columns fields
            () = (ID_prod, product_name, ..., ID_cat)
        """

        SQL = """ 
                SELECT ID_cat FROM tab_categories
                WHERE cat_name = '{}'
            """.format(categorie)

        self.my_cursor.execute(SQL)
        id_cat = self.my_cursor.fetchall()
        
        SQL = """
                SELECT * FROM tab_products
                WHERE ID_cat = {}
            """.format(int(id_cat[0][0]))

        self.my_cursor.execute(SQL)
        
        return self.my_cursor.fetchall()

    def get_best_product_from_cat(self, categorie):

        """
            return a list of the fields of the best food
            for categorie
        """

        SQL = """ 
                SELECT ID_cat FROM tab_categories
                WHERE cat_name = '{}'
            """.format(categorie)

        self.my_cursor.execute(SQL)
        id_cat = self.my_cursor.fetchall()[0][0]

        SQL = """ 
                SELECT * FROM tab_products
                WHERE ID_cat = {} 
                ORDER BY 
                        nova_group ASC,
                        nutrition_grades ASC,
                        CAST(fat_100g as DECIMAL(5, 3)) ASC,
                        CAST(sugars_100g as DECIMAL(5, 3)) ASC,
                        CAST(salt_100g as DECIMAL(5, 3)) ASC                
            """.format(id_cat)

        self.my_cursor.execute(SQL)
        liste_aliments_tries = self.my_cursor.fetchall()

        return liste_aliments_tries[0]



class Tab_historique_repository(Base_repository):

       
    def fill(self, old_ID_prod, new_ID_prod):
        """
            fill the table with the object's attributes
        """
        SQL = """
                INSERT INTO tab_historique(old_ID_prod, new_ID_prod)
                VALUES (%s, %s)
            """
        self.my_cursor.execute(SQL, (old_ID_prod, new_ID_prod))
        self.cnx.commit() 

    def show_products_old_new(self, old_ID_prod, new_ID_prod):
        """
            show the fields of the old and news products
        """
        historique = []
        for id_prod in (old_ID_prod, new_ID_prod):        

            SQL = """
                    SELECT * FROM tab_products
                    WHERE ID_prod = {}
                """.format(id_prod)

            self.my_cursor.execute(SQL)
            prod = self.my_cursor.fetchone()
            historique.append(prod)         

        return historique
