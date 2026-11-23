# ===================== database.py — БАЗА БИЛАН ИШЛАШ =====================
# Бу файлда фақат базага ёзиш ва ундан ўқиш функциялари туради.

from datetime import datetime   # datetime = сана ва вақт. Буюртма қачон берилганини ёзиш учун
import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)   # conn = уланиш
        self.cur = self.conn.cursor()                                   # cursor = SQL бажарувчи

    def create_user(self, chat_id):   # янги фойдаланувчи қўшиш
        self.cur.execute("""insert into user(chat_id) values (?)""", (chat_id,))
        self.conn.commit()   # commit = сақлаш

    def update_user_data(self, chat_id, key, value):   # фойдаланувчининг битта устунини янгилаш
        self.cur.execute(f"""update user set {key} = ? where chat_id = ?""", (value, chat_id))
        self.conn.commit()

    def get_user_by_chat_id(self, chat_id):   # chat_id бўйича фойдаланувчини олиш
        self.cur.execute("""select * from user where chat_id = ?""", (chat_id, ))
        user = dict_fetchone(self.cur)
        return user

    def get_categories_by_parent(self, parent_id=None):   # ота-категория бўйича категорияларни олиш
        if parent_id:
            self.cur.execute("""select * from category where parent_id = ?""", (parent_id, ))
        else:   # parent_id бўш бўлса → энг юқори категориялар
            self.cur.execute("""select * from category where parent_id is NULL""")

        categories = dict_fetchall(self.cur)
        return categories

    def get_category_parent(self, category_id):   # категориянинг отасини олиш (Back учун)
        self.cur.execute("""select parent_id from category where id = ?""", (category_id, ))
        category = dict_fetchone(self.cur)
        return category

    # ========== 46-дарс: МАҲСУЛОТЛАР ==========
    # products by category = категория бўйича маҳсулотлар
    def get_products_by_category(self, category_id):
        self.cur.execute("""select * from product where category_id = ?""", (category_id, ))
        products = dict_fetchall(self.cur)   # рўйхат
        return products

    # product by id = id бўйича битта маҳсулот
    def get_product_by_id(self, product_id):
        self.cur.execute("""select * from product where id = ?""", (product_id, ))
        product = dict_fetchone(self.cur)   # битта луғат
        return product

    # ========== 47-дарс: САВАТ ВА БУЮРТМА ==========

    # product for cart = сават учун маҳсулот. Маҳсулот билан бирга КАТЕГОРИЯ НОМИНИ ҳам олади.
    # inner join = иккита жадвални боғлаш (product.category_id = category.id бўйича)
    # as cat_name_uz = "категория номини cat_name_uz деб номла" (product'нинг name_uz'и билан аралашмаслиги учун)
    def get_product_for_cart(self, product_id):
        self.cur.execute(
            """select product.*, category.name_uz as cat_name_uz, category.name_ru as cat_name_ru 
            from product inner join category on product.category_id = category.id where product.id = ?""",
            (product_id, )
        )
        product = dict_fetchone(self.cur)
        return product

    # create order = буюртма яратиш. Икки қадамда ишлайди:
    # 1) "order" жадвалига битта буюртма ёзилади (ким, тўлов тури, локация, вақт)
    # 2) "order_product" жадвалига саватдаги ҳар бир маҳсулот ёзилади
    def create_order(self, user_id, products, payment_type, location):
        # status = ҳолат (1 = янги буюртма). datetime.now() = ҳозирги вақт
        # "order" қўштирноқда, чунки order — SQL'нинг ўз сўзи (order by)
        self.cur.execute(
            """insert into "order"(user_id, status, payment_type, longitude, latitude, created_at) values (?, ?, ?, ?, ?, ?)""",
            (user_id, 1, payment_type, location.longitude, location.latitude, datetime.now())
        )
        self.conn.commit()
        # max(id) = энг катта id → ҳозиргина яратилган буюртманинг рақами
        self.cur.execute(
            """select max(id) as last_order from "order" where user_id = ?""", (user_id, )
        )
        last_order = dict_fetchone(self.cur)['last_order']   # last_order = охирги буюртма
        # products = сават: {"маҳсулот_id": сони}. key = id, val = сони
        for key, val in products.items():
            self.cur.execute(
                """insert into "order_product"(product_id, order_id, amount, created_at) values (?, ?, ?, ?)""",
                (int(key), last_order,  int(val), datetime.now())   # amount = миқдор
            )
        self.conn.commit()

    # user orders = фойдаланувчининг буюртмалари (status = 1 бўлганлари)
    # ⚠️ Бу функция ҳали ҳеч қаерда ишлатилмаяпти
    def get_user_orders(self, user_id):
        self.cur.execute(
            """select * from "order" where user_id = ? and status = 1""", (user_id, )
        )
        orders = dict_fetchall(self.cur)
        return orders

    # order products = битта буюртманинг маҳсулотлари (номи ва нархи билан)
    # ⚠️ Бу ҳам ҳали ишлатилмаяпти
    def get_order_products(self, order_id):
        self.cur.execute(
            """select order_product.*, product.name_uz as product_name_uz, product.name_ru as product_name_ru, 
            product.price as product_price from order_product inner join product on order_product.product_id = product.id
            where order_id = ?""", (order_id, ))
        products = dict_fetchall(self.cur)
        return products


def dict_fetchall(cursor):   # ҳамма натижани луғатлар рўйхати қилиб қайтаради
    columns = [col[0] for col in cursor.description]   # устун номлари
    return [
        dict(zip(columns, row))   # {'устун': қиймат, ...}
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):   # битта натижани луғат қилиб қайтаради (йўқ бўлса False)
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
