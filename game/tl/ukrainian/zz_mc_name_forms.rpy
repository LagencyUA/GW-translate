
# ============================================================
# Ukrainian translation mod - Main character name declension
# Ren'Py 8.3.x
# ============================================================


# ------------------------------------------------------------
# 1. Persistent-in-save data
# ------------------------------------------------------------

default mc_forms = {}


# ------------------------------------------------------------
# 2. Name declension helpers
# ------------------------------------------------------------

init -502 python:

    MC_CASES = (
        ("nom", "Називний"),
        ("gen", "Родовий"),
        ("dat", "Давальний"),
        ("acc", "Знахідний"),
        ("ins", "Орудний"),
        ("loc", "Місцевий"),
        ("voc", "Кличний"),
    )

    # Якщо колись запитання зміни імені зміниться - МІНЯТИ ТУТ!
    MC_NAME_PROMPT = (
        "{i}Do you remember your name? Human.\n"
        " {size=-10}{i}Default name Ryo{i}."
    )

    def mc_is_name_prompt(prompt):
        return (
            isinstance(prompt, str)
            and prompt == MC_NAME_PROMPT
        )

    def mc_get_base_name():
        """
        Отримує актуальне ім'я героя.
        Намагаємося отримати Character mc і його ім'я.
        Якщо немає, на всякий вертаємо дефолтне Ryo
        (хоча такого випадку не має бути)
        """

        mc_char = getattr(store, "mc", None)

        if isinstance(mc_char, renpy.character.ADVCharacter):
            return str(mc_char)

        return "Ryo"

    def mc_ensure_forms(base_name=None):
        """
        Перевіряє наявність форм і за потреби
        ініціалізує відсутні форми базовим ім'ям.

        Використовується також для старих сейвів,
        що створені до використання моду.
        """

        if base_name is None:
            base_name = mc_get_base_name()

        if not isinstance(base_name, str) or not base_name.strip():
            base_name = "Ryo"

        base_name = base_name.strip()

        forms = getattr(store, "mc_forms", None)

        if not isinstance(forms, dict):
            forms = {}

        for case, label in MC_CASES:
            value = forms.get(case)

            if not isinstance(value, str) or not value.strip():
                forms[case] = base_name

        forms.setdefault("indeclinable", False)

        store.mc_forms = forms

        return forms

    def mc_set_forms(base_name, values, indeclinable=False):
        """
        Зберігає форми імені.

        base_name: називний відмінок
        values: словник форм
        indeclinable: чи не відмінюється ім'я
        """

        if not isinstance(base_name, str) or not base_name.strip():
            base_name = "Ryo"

        base_name = base_name.strip()

        forms = {
            "nom": base_name,
            "indeclinable": bool(indeclinable),
        }

        for case, label in MC_CASES:

            if case == "nom":
                forms[case] = base_name
                continue

            value = values.get(case, base_name)

            if not isinstance(value, str) or not value.strip():
                value = base_name

            forms[case] = value.strip()

        if forms["indeclinable"]:
            for case, label in MC_CASES:
                forms[case] = base_name

        store.mc_forms = forms

    def name_form(case):
        """
        Повертає форму імені для заданого відмінка.

        Приклади:
            name_form("nom")
            name_form("gen")
            name_form("dat")
            name_form("acc")
            name_form("ins")
            name_form("loc")
            name_form("voc")
        """

        forms = mc_ensure_forms()

        if forms.get("indeclinable", False):
            return forms.get("nom", mc_get_base_name())

        value = forms.get(case)

        if isinstance(value, str) and value.strip():
            return value

        return forms.get("nom", mc_get_base_name())

    def mc_initialize_forms():
        """
        Ініціалізує відсутні форми імені,
        зберігаючи вже налаштовані.
        """
        mc_ensure_forms(mc_get_base_name())



# ------------------------------------------------------------
# 3. Name input screen
# ------------------------------------------------------------

init -501 screen input(prompt):

    style_prefix "input"

    # Змінні екрана.
    default stage = 0
    default name_value = mc_get_base_name()

    default f_nom = ""
    default f_gen = ""
    default f_dat = ""
    default f_acc = ""
    default f_ins = ""
    default f_loc = ""
    default f_voc = ""

    default indeclinable = False

    # У редакторі одночасно існує лише одне поле input.
    # None означає, що жодна форма зараз не редагується.
    default active_case = None

    if mc_is_name_prompt(prompt):

        key "K_RETURN" action NullAction()
        key "K_KP_ENTER" action NullAction()

        add Solid("#00000099")

        frame:
            xalign 0.5
            yalign 0.5
            xmaximum 1050
            xfill True
            padding (30, 25)
            background "#20242A"

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 14

                if stage == 0:

                    text prompt:
                        style "input_prompt"
                        xalign 0.5

                    input value ScreenVariableInputValue("name_value"):
                        style "mc_forms_input"
                        id "input"
                        length 40
                        xfill True

                    textbutton "Далі: відмінювання":
                        style "mc_forms_button_primary"
                        text_style "mc_forms_button_text"
                        xalign 0.5
                        action [
                            SetScreenVariable("name_value", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_nom", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_gen", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_dat", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_acc", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_ins", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_loc", name_value.strip() or "Ryo"),
                            SetScreenVariable("f_voc", name_value.strip() or "Ryo"),
                            SetScreenVariable("active_case", None),
                            SetScreenVariable("stage", 1)
                        ]

                    textbutton "Пропустити налаштування":
                        style "mc_forms_button_primary"
                        text_style "mc_forms_button_text"
                        xalign 0.5
                        action [
                            Function(
                                mc_set_forms,
                                name_value.strip() or "Ryo",
                                {},
                                True
                            ),
                            Return(name_value.strip() or "Ryo")
                        ]

                else:

                    text "Відмінювання імені":
                        style "mc_forms_title"

                    text "Ім'я: [name_value]":
                        style "mc_forms_text"

                    text "Натисни на форму, щоб редагувати її. Одночасно редагується лише одне поле.":
                        style "mc_forms_text"

                    textbutton "Ім'я не відмінюється":
                        style "mc_forms_button_toggle"
                        text_style "mc_forms_button_text"
                        xalign 0.5
                        selected indeclinable
                        action [
                            ToggleScreenVariable("indeclinable"),
                            SetScreenVariable("active_case", None)
                        ]

                    if not indeclinable:

                        viewport:
                            xfill True
                            ymaximum 430
                            scrollbars "vertical"
                            mousewheel True

                            vbox:
                                spacing 10

                                hbox:
                                    spacing 12
                                    text "Називний (хто?):":
                                        style "mc_forms_label"

                                    if active_case == "nom":
                                        input value ScreenVariableInputValue("name_value"):
                                            id "mc_input_nom"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[name_value]":
                                            id "mc_input_nom_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "nom")

                                hbox:
                                    spacing 12
                                    text "Родовий (кого?):":
                                        style "mc_forms_label"

                                    if active_case == "gen":
                                        input value ScreenVariableInputValue("f_gen"):
                                            id "mc_input_gen"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[f_gen]":
                                            id "mc_input_gen_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "gen")

                                hbox:
                                    spacing 12
                                    text "Давальний (кому?):":
                                        style "mc_forms_label"

                                    if active_case == "dat":
                                        input value ScreenVariableInputValue("f_dat"):
                                            id "mc_input_dat"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[f_dat]":
                                            id "mc_input_dat_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "dat")

                                hbox:
                                    spacing 12
                                    text "Знахідний: (кого?)":
                                        style "mc_forms_label"

                                    if active_case == "acc":
                                        input value ScreenVariableInputValue("f_acc"):
                                            id "mc_input_acc"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[f_acc]":
                                            id "mc_input_acc_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "acc")

                                hbox:
                                    spacing 12
                                    text "Орудний (ким?):":
                                        style "mc_forms_label"

                                    if active_case == "ins":
                                        input value ScreenVariableInputValue("f_ins"):
                                            id "mc_input_ins"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[f_ins]":
                                            id "mc_input_ins_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "ins")

                                hbox:
                                    spacing 12
                                    text "Місцевий (на кому?):":
                                        style "mc_forms_label"

                                    if active_case == "loc":
                                        input value ScreenVariableInputValue("f_loc"):
                                            id "mc_input_loc"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[f_loc]":
                                            id "mc_input_loc_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "loc")

                                hbox:
                                    spacing 12
                                    text "Кличний:":
                                        style "mc_forms_label"

                                    if active_case == "voc":
                                        input value ScreenVariableInputValue("f_voc"):
                                            id "mc_input_voc"
                                            style "mc_forms_input"
                                            length 40
                                            xfill True
                                    else:
                                        textbutton "[f_voc]":
                                            id "mc_input_voc_button"
                                            style "mc_forms_input_display"
                                            text_style "mc_forms_input_display_text"
                                            xfill True
                                            action SetScreenVariable("active_case", "voc")

                    else:
                        text "Використовуватиметься одна форма імені.":
                            style "mc_forms_hint"

                    null height 8

                    hbox:
                        xalign 0.5
                        spacing 30

                        textbutton "Назад":
                            style "mc_forms_button_primary"
                            text_style "mc_forms_button_text"
                            action [
                                SetScreenVariable("active_case", None),
                                SetScreenVariable("stage", 0)
                            ]

                        textbutton "Зберегти":
                            style "mc_forms_button_primary"
                            text_style "mc_forms_button_text"
                            action [
                                Function(
                                    mc_set_forms,
                                    name_value.strip() or "Ryo",
                                    {
                                        "nom": name_value,
                                        "gen": f_gen,
                                        "dat": f_dat,
                                        "acc": f_acc,
                                        "ins": f_ins,
                                        "loc": f_loc,
                                        "voc": f_voc,
                                    },
                                    indeclinable
                                ),
                                Return(name_value.strip() or "Ryo")
                            ]

    else:

        # Оригінальна поведінка input для інших запитів,
        # наприклад для введення назви села.
        window:
            has vbox

            if renpy.variant("mobile"):
                xalign 0.5
                xpos 500
                xsize gui.dialogue_width
                ypos gui.dialogue_ypos

            xalign 0.5
            xpos 0.5
            xsize gui.dialogue_width
            ypos -400

            text prompt style "input_prompt"
            input id "input"


# ============================================================
# MC Name Forms — UI Styles
# ============================================================

# ------------------------------------------------------------
# Заголовок редактора
# ------------------------------------------------------------

style mc_forms_title:
    font "fonts/KyivRegion-Regular.ttf"
    size 54
    color "#FFFFFF"
    text_align 0.5
    xalign 0.5


# ------------------------------------------------------------
# Основний текст
# ------------------------------------------------------------

style mc_forms_text:
    font "fonts/PlaypenSans-Medium.ttf"
    size 30
    color "#FFFFFF"


# ------------------------------------------------------------
# Допоміжний текст / підказки
# ------------------------------------------------------------

style mc_forms_hint:
    font "fonts/PlaypenSans-Medium.ttf"
    size 24
    color "#BBBBBB"
    text_align 0.5


# ------------------------------------------------------------
# Підписи відмінків
# ------------------------------------------------------------

style mc_forms_label:
    font gui.interface_text_font
    size 38
    color "#EAEAEA"
    yalign 0.5


# ------------------------------------------------------------
# Поля введення
# ------------------------------------------------------------

style mc_forms_input:
    font "fonts/PlaypenSans-Medium.ttf"
    size 38
    color "#FFFFFF"
    outlines [(1, "#00000080", 0, 0)]

    xpadding 10
    ypadding 7

    background "#303640"
    hover_background "#3B4552"

    xfill True


# ------------------------------------------------------------
# Кнопка — базовий стиль
# ------------------------------------------------------------

style mc_forms_button:
    font gui.interface_text_font
    size 36

    color "#FFFFFF"
    hover_color "#FFFFFF"
    insensitive_color "#888888"

    text_align 0.5
    xalign 0.5

    xpadding 22
    ypadding 10

    background Frame(
        Solid("#343B47"),
        12, 12
    )

    hover_background Frame(
        Solid("#4A586B"),
        12, 12
    )

    insensitive_background Frame(
        Solid("#292D34"),
        12, 12
    )


# ------------------------------------------------------------
# Основна / підтверджувальна кнопка
# ------------------------------------------------------------

style mc_forms_button_primary is mc_forms_button:
    background Frame(
        Solid("#E4D0B1"),
        12, 12
    )

    hover_background Frame(
        Solid("#af9d81"),
        12, 12
    )


# ------------------------------------------------------------
# Кнопка перемикача «Ім'я не відмінюється»
# ------------------------------------------------------------

style mc_forms_button_toggle is mc_forms_button:
    background Frame(
        Solid("#343B47"),
        12, 12
    )

    hover_background Frame(
        Solid("#4A586B"),
        12, 12
    )

    selected_background Frame(
        Solid("#E4D0B1"),
        12, 12
    )

    selected_hover_background Frame(
        Solid("#af9d81"),
        12, 12
    )


# ------------------------------------------------------------
# Текст усередині кнопок
# ------------------------------------------------------------

style mc_forms_button_text:
    font gui.interface_text_font
    size 36

    color "#ffffff"
    hover_color "#FFFFFF"
    insensitive_color "#888888"

    selected_color "#FFFFFF"

    text_align 0.5
    outlines [(1, "#000000d0", 0, 0)]


# ------------------------------------------------------------
# Кнопки-замінники неактивних полів редактора.
# Натискання на таку кнопку перемикає її в єдиний активний input.
# ------------------------------------------------------------

style mc_forms_input_display is mc_forms_button:
    xalign 0.0
    xfill True
    xpadding 10
    ypadding 7
    background Frame(Solid("#303640"), 12, 12)
    hover_background Frame(Solid("#3B4552"), 12, 12)

style mc_forms_input_display_text:
    font "fonts/PlaypenSans-Medium.ttf"
    size 38
    color "#FFFFFF"
    hover_color "#FFFFFF"
    outlines [(1, "#00000080", 0, 0)]
    text_align 0.0



# ------------------------------------------------------------
# 4. Name form usage examples
# ------------------------------------------------------------
#
# [name_form('nom')] - Називний
# [name_form('gen')] - Родовий
# [name_form('dat')] - Давальний
# [name_form('acc')] - Знахідний
# [name_form('ins')] - Орудний
# [name_form('loc')] - Місцевий
# [name_form('voc')] - Кличний
#
# Example:
#
# translate ukrainian strings:
#
#     old "I saw [mc]."
#     new "Я побачив [name_form('acc')]."
#
#     old "Give it to [mc]."
#     new "Віддай це [name_form('dat')]."
#
# ============================================================