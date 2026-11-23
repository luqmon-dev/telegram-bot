# ===================== messages.py — МАТН ХАБАРЛАРИГА ЖАВОБ =====================
# Фойдаланувчи матн ёзса ёки пастки (Reply) тугмани босса — шу файл ишлайди.

import methods
from register import check, check_data_decorator
from database import Database
import globals
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

db = Database("db-evos.db")


@check_data_decorator   # аввал рўйхатдан ўтганини текширади
def message_handler(update, context):
    message = update.message.text                 # ёзилган матн
    user = update.message.from_user
    state = context.user_data.get("state", 0)     # ҳозирги ҳолат
    db_user = db.get_user_by_chat_id(user.id)
    if state == 0:
        check(update, context)

    # ---------- 1: РЎЙХАТДАН ЎТИШ ----------
    elif state == 1:
        if not db_user["lang_id"]:

            if message == globals.BTN_LANG_UZ:
                db.update_user_data(user.id, "lang_id", 1)
                check(update, context)

            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id, "lang_id", 2)
                check(update, context)

            else:
                update.message.reply_text(
                    text=globals.TEXT_LANG_WARNING
                )

        elif not db_user["first_name"]:
            db.update_user_data(user.id, "first_name", message)
            check(update, context)

        elif not db_user["last_name"]:
            db.update_user_data(user.id, "last_name", message)
            # ⚠️ buttons ишлатилмаяпти — ортиқча
            buttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
            ]
            check(update, context)

        elif not db_user["phone_number"]:
            db.update_user_data(user.id, "phone_number", message)
            check(update, context)

        else:
            check(update, context)

    # ---------- 2: БОШ МЕНЮ ----------
    elif state == 2:

        # 🛒 БУЮРТМА ҚИЛИШ
        if message == globals.BTN_ORDER[db_user['lang_id']]:
            categories = db.get_categories_by_parent()   # энг юқори категориялар
            buttons = methods.send_category_buttons(categories=categories, lang_id=db_user["lang_id"])

            # carts = сават. Хотирада сақланади: {"маҳсулот_id": сони}
            # Саватда нимадир бўлса → матнда сават рўйхати ва "Харид қилиш" тугмаси чиқади
            if context.user_data.get("carts", {}):
                carts = context.user_data.get("carts")
                text = f"{globals.AT_KORZINKA[db_user['lang_id']]}:\n\n"   # "Саватда:"
                lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
                total_price = 0
                for cart, val in carts.items():   # cart = id, val = сони
                    product = db.get_product_for_cart(int(cart))
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
                    total_price += product['price'] * val

                text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price}"
                buttons.append(
                    [InlineKeyboardButton(text=globals.BTN_KORZINKA[db_user['lang_id']], callback_data="cart")])

            else:   # сават бўш → оддий "категорияни танланг"
                text = globals.TEXT_ORDER[db_user['lang_id']]
            update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons,
                )
            )

        # 🛍 БУЮРТМАЛАРИМ — базадаги буюртмаларни кўрсатамиз
        elif message == globals.BTN_MY_ORDERS[db_user['lang_id']]:
            orders = db.get_user_orders(db_user['id'])   # базадан шу одамнинг буюртмаларини оламиз
            if orders:                                   # буюртма бор бўлса
                text = "\n"
                lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
                total_price = 0
                for order in orders:                     # ҳар бир буюртма учун
                    text += f"\n📦 №{order['id']} — {order['created_at'][:16]}\n"
                    products = db.get_order_products(order['id'])   # шу буюртманинг маҳсулотлари
                    for p in products:                   # ҳар бир маҳсулот учун
                        text += f"{p['amount']} x {p[f'product_name_{lang_code}']}\n"
                        total_price += p['amount'] * p['product_price']   # сони × нархи
                text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"

                update.message.reply_text(
                    text=f"<b>Ma'lumotlarim:</b>\n\n"
                         f"👤 <b>Ism-familiya:</b> {db_user['first_name']} {db_user['last_name']}\n"
                         f"📞 <b>Telefon raqam:</b> {db_user['phone_number']} \n\n"
                         f"📥 <b>Buyurtmalarim:</b> \n"
                         f"{text}",
                    parse_mode='HTML'
                )

            else:                                        # буюртма йўқ бўлса
                update.message.reply_text(
                    text=globals.NO_ZAKAZ[db_user['lang_id']])   # "ҳали буюртма йўқ"

        # 👨‍👩‍👦 БИЗ ҲАҚИМИЗДА
        elif message == globals.BTN_ABOUT_US[db_user['lang_id']]:
            update.message.reply_text(
                text=globals.ABOUT_COMPANY[db_user['lang_id']],
                parse_mode="HTML"
            )

        # ⚙️ СОЗЛАМАЛАР → тил танлаш тугмаларини чиқарамиз ва ҳолатни 3 га ўтказамиз
        elif message == globals.BTN_SETTINGS[db_user['lang_id']]:
            buttons = [
                [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
            ]
            update.message.reply_text(
                text=globals.CHOOSE_LANG,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )
            context.user_data["state"] = globals.STATES["settings"]
        # ⚠️ ✍️ Фикр билдириш тугмаси ҳали ёзилмаган

    # ---------- 3: СОЗЛАМАЛАР (тилни алмаштириш) ----------
    elif state == 3:
        if message == globals.BTN_LANG_UZ:
            db.update_user_data(db_user['chat_id'], "lang_id", 1)   # тил = ўзбекча
            context.user_data["state"] = globals.STATES["reg"]
            check(update, context)   # check() ҳамма нарса борлигини кўриб, бош менюни янги тилда чиқаради

        elif message == globals.BTN_LANG_RU:
            db.update_user_data(db_user['chat_id'], "lang_id", 2)   # тил = русча
            context.user_data["state"] = globals.STATES["reg"]
            check(update, context)

        else:
            update.message.reply_text(
                text=globals.TEXT_LANG_WARNING
            )

    else:
        update.message.reply_text("Salom")