# ===================== main.py — БОТНИНГ АСОСИЙ ФАЙЛИ =====================
# Бот шу файлдан ишга тушади (▶️ Run шу файлда босилади).

# Updater = янгиловчи, CommandHandler = буйруқ ушловчи, CallbackQueryHandler = inline тугма ушловчи
# MessageHandler = хабар ушловчи, Filters = саралагичлар
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler

import methods                        # ёрдамчи функциялар (бош меню)
from database import Database         # база билан ишлаш класси
from register import check            # рўйхатдан ўтишни текшириш
from messages import message_handler  # матн хабарларига жавоб
from inlines import inline_handler    # inline тугмаларга жавоб
import globals                        # матнлар

from config import TOKEN, ADMIN_ID


db = Database("db-evos.db")


def start_handler(update, context):   # /start келганда
    check(update, context)


def contact_handler(update, context):   # контакт юборилганда
    message = update.message.contact.phone_number   # телефон рақам
    user = update.message.from_user
    db.update_user_data(user.id, "phone_number", message)   # базага ёзамиз
    check(update, context)


# ========== 47-дарс: ЛОКАЦИЯ ВА БУЮРТМАНИ ЯКУНЛАШ ==========
# location_handler = жойлашув ушловчи. Мижоз 📍 локация юборганда ишлайди.
# Бу буюртманинг ОХИРГИ қадами: сават → тўлов тури → локация → буюртма тайёр.
def location_handler(update, context):
    db_user = db.get_user_by_chat_id(update.message.from_user.id)
    location = update.message.location  # location = жойлашув (кенглик ва узунлик)
    # шаурмахона билан мижоз орасидаги масофа
    distance = methods.get_distance_km(globals.SHOP_LAT, globals.SHOP_LON, location.latitude, location.longitude)
    text = ""   # сават бўш бўлса ҳам хато чиқмасин
    # payment_type = тўлов тури (1 = нақд, 2 = карта). Олдинги қадамда хотирага ёзилган
    payment_type = context.user_data.get("payment_type", None)
    # create_order = буюртма яратиш. carts = сават (хотирадан оламиз)
    db.create_order(db_user['id'], context.user_data.get("carts", {}), payment_type, location)

    if context.user_data.get("carts", {}):   # сават бўш бўлмаса → буюртма матнини тузамиз
        carts = context.user_data.get("carts")
        text = "\n"
        lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]   # "uz" ёки "ru"
        total_price = 0   # total_price = умумий нарх
        # carts.items() = саватдаги жуфтликлар: {"маҳсулот_id": сони}
        # cart = маҳсулот id'си, val (value) = сони
        for cart, val in carts.items():
            product = db.get_product_for_cart(int(cart))
            # Масалан: "2 x Shaurma Mini"
            text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
            total_price += product['price'] * val   # нарх × сони
        # ALL = жами, SUM = сўм
        text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"
    # ⚠️ Сават бўш бўлса, text яратилмайди ва пастда хато чиқади (UnboundLocalError).
    #    Тузатиш йўли: if'дан олдин text = "" деб ёзиб қўйиш.

    # Админга янги буюртма ҳақида хабар юборамиз
    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"<b>Yangi buyurtma:</b>\n\n"
             f"👤 <b>Ism-familiya:</b> {db_user['first_name']} {db_user['last_name']}\n"
             f"📞 <b>Telefon raqam:</b> {db_user['phone_number']} \n\n"
             f"📏 <b>Masofa:</b> {round(distance, 1)} km\n"
             f"📥 <b>Buyurtma:</b> \n"
             f"{text}",
        parse_mode='HTML'   # parse_mode = матнни ўқиш усули. HTML → <b> қалин ёзув бўлади
    )

    # Админга мижознинг локациясини харита кўринишида юборамиз
    context.bot.send_location(
        chat_id=ADMIN_ID,
        latitude=float(location.latitude),     # latitude = кенглик
        longitude=float(location.longitude)    # longitude = узунлик
    )
    # мижозга жавоб: 10 км ичида бўлса — қабул қилинди, узоқ бўлса — огоҳлантириш
    if distance <= globals.DELIVERY_KM:
        update.message.reply_text(globals.TEXT_ORDER_ACCEPTED[db_user['lang_id']])
    else:
        update.message.reply_text(globals.TEXT_TOO_FAR[db_user['lang_id']].format(km=round(distance, 1)))
    context.user_data.pop("carts", None) # # буюртмадан кейин саватни тозалаймиз
    methods.send_main_menu(context, update.message.from_user.id, db_user['lang_id'])   # бош менюга қайтамиз
# ===========================================================


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))   # 47: локация → location_handler

    updater.start_polling()   # Telegram'дан янги хабарларни сўраб туриш
    updater.idle()            # ботни тўхтатилгунча ишлатиш


if __name__ == '__main__':
    main()
