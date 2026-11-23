# ===================== globals.py — УМУМИЙ МАТНЛАР ВА СОЗЛАМАЛАР =====================
# Ботдаги ҳамма матнлар шу ерда. {1: "...", 2: "..."} → 1 = ўзбекча, 2 = русча.

WELCOME_TEXT = "Xush kelibsiz / Добро пожаловать!"   # WELCOME = хуш келибсиз
CHOOSE_LANG = "Tilni tanlang / Выберите язык!"       # CHOOSE = танла, LANG = тил
BTN_LANG_UZ = "Uzbek tili"                           # BTN (button) = тугма
BTN_LANG_RU = "Русский язык"

# STATES = ҳолатлар
STATES = {
    "reg": 1,        # рўйхатдан ўтиш
    "menu": 2,       # бош меню
    "settings": 3    # 47: созламалар (тилни алмаштириш)
}
LANGUAGE_CODE = {    # тил коди → базадаги name_uz / name_ru устунлари учун
    1: "uz",
    2: "ru"
}
TEXT_LANG_WARNING = "Iltimos tillardan birini tanlang!\nПожалуйста, выберите один из языков!"   # WARNING = огоҳлантириш
TEXT_ENTER_FIRST_NAME = {          # исмни киритинг
    1: "Iltimos ismingizni kiriting!",
    2: "Пожалуйста, введите ваше имя!"
}
TEXT_ENTER_LAST_NAME = {           # фамилияни киритинг
    1: "Iltimos familiyangizni kiriting!",
    2: "Пожалуйста, введите свою фамилию!"
}
BTN_SEND_CONTACT = {               # контакт юбориш тугмаси
    1: "Yuborish",
    2: "Отправить"
}
TEXT_ENTER_CONTACT = {
    1: "Iltimos telefon raqamingizni yuboring yoki <<Yuborish>> tugmasini bosing!",
    2: "Отправьте свой номер телефона или нажмите кнопку <<Отправить>>!"
}
TEXT_MAIN_MENU = {                 # бош меню
    1: "🏠 Asosiy menyu",
    2: "🏠 Главное меню"
}
BTN_ORDER = {                      # ORDER = буюртма
    1:"🛒 Buyurtma qilish",
    2:"🛒 Заказать"
}
TEXT_ORDER = {
    1: "Kategoriylardan birini tanlang!",
    2: "Выбери одну из категорий!"
}
BTN_MY_ORDERS = {                  # менинг буюртмаларим
    1:"🛍 Buyurtmalarim",
    2:"🛍 Мои заказы"
}
BTN_ABOUT_US = {                   # ABOUT US = биз ҳақимизда (олдин "EVOS Oilasi" эди)
    1:"👨‍👩‍👦 Biz haqimizda",
    2:"👨‍👩‍👦 O нас"              # ⚠️ "O" лотин ҳарфида ёзилган, кирилл "О" бўлиши керак
}
BTN_KORZINKA = {                   # KORZINKA (русча "корзинка") = сават
    1: "🛍 Xarid qilish",
    2: "🛍 Покупка товаров",      # ⚠️ ХАТО: калит 21 эмас, 2 бўлиши керак! Русча танлаганда бот хато беради
}
BTN_COMMENTS = {                   # COMMENTS = фикрлар
    1:"✍️Fikr bildirish",
    2:"✍️комментарий"
}
BTN_SETTINGS = {                   # SETTINGS = созламалар
    1:"⚙️Sozlamalar",
    2:"⚙️Настройки"
}

# ========== 46-дарс ==========
TEXT_PRODUCT_PRICE = {             # PRICE = нарх
    1: "Narx:",
    2: "Цена:"
}
TEXT_PRODUCT_DESC = {              # DESC (description) = тавсиф, таркиби
    1: "Tarkibi:",
    2: "Состав:"
}

# ========== 47-дарс ==========

AT_KORZINKA = {                    # "саватда"
    1: "Savatchada",
    2: "В корзине"
}

ALL = {                            # ALL = ҳаммаси, жами
    1: "Jami",
    2: "Все"                       # ⚠️ русчада "Итого" тўғрироқ
}

ZAKAZ = {                          # (русча "заказ") = буюртма. ⚠️ Ҳеч қаерда ишлатилмаяпти
    1: "Buyurtma",
    2: "Заказ"
}

SUM = {                            # сўм
    1: "so'm",
    2: "сум"
}

ABOUT_COMPANY = {                  # компания ҳақида матн. <b>...</b> = қалин ёзув (HTML)
    1: "Biz <b>F-18 backend dasturchilar guruhi</b>miz! "
         "\n\nBirgalikda biznesingizni rivojlantiramiz va uni "
         "zamonaviy uslubda ommaga taqdim qilamiz!\n\n"
         "<b>BIZ SIZ HAQINGIZDA QAYG'URAMIZ!!!</b>",
    2: "Мы <b>F-18 backend dasturchilar guruhi</b>!"
       "\n\nМы будем развивать ваш бизнес вместе"
       "и представляем публике в современном стиле!\n\n"
       "<b>МЫ ЗАБОТИМСЯ О ВАС !!!</b>"
}

NO_ZAKAZ = {                       # "буюртма йўқ"
    1: "Siz hali birorta buyurtma bermadingiz!",
    2: "Вы еще не разместили ни одного заказа!"
}

SEND_LOCATION = {                  # локация юбориш тугмаси
    1: "📍 Lokatsiya jo'nating",
    2: "📍 Отправить местоположение"
}

# ========== Етказиб бериш ==========
SHOP_LAT = 39.6547      # шаурмахонанинг кенглиги (latitude). Кейин ўз манзилингизга алмаштиринг
SHOP_LON = 66.9758      # шаурмахонанинг узунлиги (longitude)
DELIVERY_KM = 10        # етказиб бериш радиуси, км

TEXT_ORDER_ACCEPTED = {
    1: "✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog'lanamiz.",
    2: "✅ Ваш заказ принят! Скоро мы с вами свяжемся."
}
TEXT_TOO_FAR = {
    1: "🙏 Kechirasiz, biz faqat 10 km gacha yetkazib beramiz.\nSiz {km} km uzoqdasiz. Buyurtmani o'zingiz olib ketishingiz mumkin.",
    2: "🙏 Извините, мы доставляем только до 10 км.\nВы в {km} км от нас. Вы можете забрать заказ самостоятельно."
}