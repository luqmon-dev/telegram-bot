# ===================== register.py — РЎЙХАТДАН ЎТИШ =====================
# register = рўйхатдан ўтказиш. Фойдаланувчида нима етишмаётганини текшириб,
# ўшани сўрайди: тил → исм → фамилия → телефон → бош меню.

# ReplyKeyboardRemove = клавиатурани олиб ташлаш (тугмаларни яшириш)
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from database import Database
import globals
import methods   # бош менюни юбориш учун

db = Database("db-evos.db")


# check = текшириш. Ҳар сафар "кейин нимани сўраш керак?" деб текширади
def check(update, context):
    user = update.message.from_user           # хабар юборган одам
    db_user = db.get_user_by_chat_id(user.id)  # базадан ўша одамни қидирамиз

    if not db_user:   # not = эмас. "Базада йўқ бўлса" → янги одам
        db.create_user(user.id)   # базага қўшамиз
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
        ]
        update.message.reply_text(text=globals.WELCOME_TEXT)   # reply_text = матн билан жавоб бериш
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(   # reply_markup = жавобга тугма қўшиш
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]   # user_data = фойдаланувчи хотираси. Ҳолат = 1

    elif not db_user["lang_id"]:   # elif = акс ҳолда агар. Тил танланмаган бўлса
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
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["first_name"]:   # исм йўқ бўлса → исм сўраймиз
        update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],   # танланган тилдаги матн
            reply_markup=ReplyKeyboardRemove()   # тил тугмаларини яширамиз
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["last_name"]:   # фамилия йўқ бўлса → фамилия сўраймиз
        update.message.reply_text(
            text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["state"] = globals.STATES["reg"]

    elif not db_user["phone_number"]:   # телефон йўқ бўлса → контакт тугмасини чиқарамиз
        buttons = [
            # request_contact=True — тугма босилса, Telegram телефон рақамни ўзи юборади
            [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
        ]
        update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True
            )
        )
        context.user_data["state"] = globals.STATES["reg"]

    else:   # else = акс ҳолда. Ҳаммаси бор → бош менюга
        methods.send_main_menu(context, user.id, db_user['lang_id'])
        context.user_data["state"] = globals.STATES["menu"]   # ҳолат = 2 (менюда)


# decorator = безак (бошқа функцияни "ўраб", олдидан текширув қўшади)
# check_data_decorator = "маълумотни текширувчи безак"
# func = ўралаётган функция (бу ерда message_handler)
# ⚠️ Ичидаги код check() билан деярли бир хил — бу такрорланиш (кейин тузатиш мумкин)
def check_data_decorator(func):
    def inner(update, context):   # inner = ички функция
        user = update.message.from_user
        db_user = db.get_user_by_chat_id(user.id)
        state = context.user_data.get("state", 0)   # .get("state", 0) — топилмаса 0 қайтаради

        if state != globals.STATES['reg']:   # != = тенг эмас. Рўйхатдан ўтиш жараёнида бўлмаса

            if not db_user:
                db.create_user(user.id)
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
                ]
                update.message.reply_text(text=globals.WELCOME_TEXT)
                update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["lang_id"]:
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
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["first_name"]:
                update.message.reply_text(
                    text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["last_name"]:
                update.message.reply_text(
                    text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["phone_number"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
                ]
                update.message.reply_text(
                    text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            else:   # ҳаммаси жойида → асл функцияни ишлатамиз
                return func(update, context)

            return False   # бирор нарса етишмаса — асл функция ишламайди

        else:   # рўйхатдан ўтиш жараёнида бўлса → тўғридан-тўғри асл функцияга
            return func(update, context)
    return inner   # ўралган функцияни қайтарамиз
