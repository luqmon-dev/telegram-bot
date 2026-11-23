# ===================== methods.py — ЁРДАМЧИ ФУНКЦИЯЛАР =====================
# Бир неча жойда ишлатиладиган функциялар. Такрорланмаслик учун шу ерга йиғилган.

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
import globals


# send_main_menu = бош менюни юбориш (пастдаги катта тугмалар)
def send_main_menu(context, chat_id, lang_id, message_id=None):
    buttons = [
        [KeyboardButton(text=globals.BTN_ORDER[lang_id])],    # 🛒 Буюртма қилиш
        [KeyboardButton(text=globals.BTN_MY_ORDERS[lang_id]), KeyboardButton(text=globals.BTN_ABOUT_US[lang_id])],  # Буюртмаларим | Биз ҳақимизда
        [KeyboardButton(text=globals.BTN_COMMENTS[lang_id]), KeyboardButton(text=globals.BTN_SETTINGS[lang_id])]     # Фикр | Созламалар
    ]
    if message_id:
        # ⚠️ edit_message_text фақат Inline тугмалар билан ишлайди — бу шох хато беради (ҳозир ишлатилмаяпти)
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
    else:
        context.bot.send_message(   # янги хабар юбориш
            chat_id=chat_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )


# ========== 46-дарс ==========
# 45-дарсда бу цикл 3 жойда такрорланган эди. Энди битта функцияга олинди (DRY қоидаси).

# send_category_buttons = категория тугмаларини ясаш (ҳар қаторда 2 тадан)
def send_category_buttons(categories, lang_id):
    buttons = []   # ҳамма қаторлар
    row = []       # битта қатор
    for i in range(len(categories)):
        row.append(
            InlineKeyboardButton(
                text=categories[i][f'name_{globals.LANGUAGE_CODE[lang_id]}'],   # name_uz ёки name_ru
                callback_data=f"category_{categories[i]['id']}"                 # масалан "category_1"
            )
        )

        # 2 та бўлса ёки охирги тоқ тугма бўлса → қаторни ёпамиз
        if len(row) == 2 or (len(categories) % 2 == 1 and i == len(categories) - 1):
            buttons.append(row)
            row = []
    return buttons   # тайёр тугмаларни қайтарамиз


# send_product_buttons = маҳсулот тугмаларини ясаш. Худди юқоридагидек,
# фақат callback_data бошқача: "category_product_5" (5 = маҳсулот id'си)
def send_product_buttons(products, lang_id):
    buttons = []
    row = []
    for i in range(len(products)):
        row.append(
            InlineKeyboardButton(
                text=products[i][f'name_{globals.LANGUAGE_CODE[lang_id]}'],
                callback_data=f"category_product_{products[i]['id']}"
            )
        )

        if len(row) == 2 or (len(products) % 2 == 1 and i == len(products) - 1):
            buttons.append(row)
            row = []

    return buttons

from math import radians, sin, cos, asin, sqrt   # math = математика кутубхонаси


# get_distance_km = икки нуқта орасидаги масофани км да ҳисоблаш (Haversine формуласи)
def get_distance_km(lat1, lon1, lat2, lon2):
    R = 6371                                  # Ернинг радиуси, км
    dlat = radians(lat2 - lat1)               # кенгликлар фарқи (радианда)
    dlon = radians(lon2 - lon1)               # узунликлар фарқи
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))              # натижа: километр