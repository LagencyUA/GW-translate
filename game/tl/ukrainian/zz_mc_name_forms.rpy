# ============================================================
# Ukrainian translation mod — Main character name declension
# Ren'Py 8.3.x
# ============================================================

# ------------------------------------------------------------
# 1. Data stored in the save
# ------------------------------------------------------------

default mc_forms = {}


# ------------------------------------------------------------
# 2. Name declension helpers
# ------------------------------------------------------------

init -502 python:
    MC_FORM_FIELDS = (
        ("nom", "Називний", "хто?", "name_value"),
        ("gen", "Родовий", "кого?", "f_gen"),
        ("dat", "Давальний", "кому?", "f_dat"),
        ("acc", "Знахідний", "кого?", "f_acc"),
        ("ins", "Орудний", "ким?", "f_ins"),
        ("loc", "Місцевий", "на кому?", "f_loc"),
        ("voc", "Кличний", "", "f_voc"),
    )
    MC_CASES = tuple((case, label) for case, label, question, variable in MC_FORM_FIELDS)
    MC_DEFAULT_NAME = "Ryo"

    # If the original prompt changes, update it here.
    MC_NAME_PROMPT = (
        "{i}Do you remember your name? Human.\n"
        " {size=-10}{i}Default name Ryo{i}."
    )

    def mc_is_name_prompt(prompt):
        return isinstance(prompt, str) and prompt == MC_NAME_PROMPT

    def mc_normalize_name(value, fallback=MC_DEFAULT_NAME):
        """Return a non-empty, trimmed name."""
        if not isinstance(value, str) or not value.strip():
            return fallback
        return value.strip()

    def mc_get_base_name():
        """Get the current protagonist name, falling back to the default."""
        mc_char = getattr(store, "mc", None)
        if isinstance(mc_char, renpy.character.ADVCharacter):
            return mc_normalize_name(str(mc_char))
        return MC_DEFAULT_NAME

    def mc_ensure_forms(base_name=None):
        """Initialize missing forms; also supports saves created before this mod."""
        base_name = mc_normalize_name(
            mc_get_base_name() if base_name is None else base_name
        )
        forms = getattr(store, "mc_forms", None)
        if not isinstance(forms, dict):
            forms = {}

        for case, _label in MC_CASES:
            forms[case] = mc_normalize_name(forms.get(case), base_name)

        forms["indeclinable"] = bool(forms.get("indeclinable", False))
        store.mc_forms = forms
        return forms

    def mc_set_forms(base_name, values, indeclinable=False):
        """Save the protagonist's name forms."""
        base_name = mc_normalize_name(base_name)
        values = values if isinstance(values, dict) else {}
        forms = {"nom": base_name, "indeclinable": bool(indeclinable)}

        for case, _label in MC_CASES:
            if case != "nom":
                forms[case] = mc_normalize_name(values.get(case), base_name)

        if forms["indeclinable"]:
            for case, _label in MC_CASES:
                forms[case] = base_name

        store.mc_forms = forms

    def name_form(case):
        """Return a requested form: nom, gen, dat, acc, ins, loc, or voc."""
        forms = mc_ensure_forms()
        if forms["indeclinable"]:
            return forms["nom"]
        return forms.get(case, forms["nom"])

    def mc_initialize_forms():
        """Initialize missing forms without overwriting forms already saved."""
        mc_ensure_forms(mc_get_base_name())


# ------------------------------------------------------------
# 3. Name input screen
# ------------------------------------------------------------

init -501 screen input(prompt):
    style_prefix "input"

    default stage = 0
    default name_value = mc_get_base_name()
    default f_gen = ""
    default f_dat = ""
    default f_acc = ""
    default f_ins = ""
    default f_loc = ""
    default f_voc = ""
    default indeclinable = False
    default active_case = None

    if mc_is_name_prompt(prompt):
        # Prevent Enter from accidentally dismissing the screen.
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
                        id "input"
                        style "mc_forms_input"
                        length 40
                        xfill True

                    textbutton "Далі: відмінювання":
                        style "mc_forms_button_primary"
                        text_style "mc_forms_button_text"
                        xalign 0.5
                        action [
                            SetScreenVariable("name_value", mc_normalize_name(name_value)),
                            SetScreenVariable("f_gen", mc_normalize_name(name_value)),
                            SetScreenVariable("f_dat", mc_normalize_name(name_value)),
                            SetScreenVariable("f_acc", mc_normalize_name(name_value)),
                            SetScreenVariable("f_ins", mc_normalize_name(name_value)),
                            SetScreenVariable("f_loc", mc_normalize_name(name_value)),
                            SetScreenVariable("f_voc", mc_normalize_name(name_value)),
                            SetScreenVariable("active_case", None),
                            SetScreenVariable("stage", 1),
                        ]

                    textbutton "Пропустити налаштування":
                        style "mc_forms_button_primary"
                        text_style "mc_forms_button_text"
                        xalign 0.5
                        action [
                            Function(mc_set_forms, mc_normalize_name(name_value), {}, True),
                            Return(mc_normalize_name(name_value)),
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
                            SetScreenVariable("active_case", None),
                        ]

                    if not indeclinable:
                        # The mapping is rebuilt on each screen evaluation so the
                        # display buttons always show the current screen variables.
                        $ mc_form_values = {
                            "nom": name_value,
                            "gen": f_gen,
                            "dat": f_dat,
                            "acc": f_acc,
                            "ins": f_ins,
                            "loc": f_loc,
                            "voc": f_voc,
                        }

                        viewport:
                            xfill True
                            ymaximum 430
                            scrollbars "vertical"
                            mousewheel True

                            vbox:
                                spacing 10

                                for case, label, question, variable in MC_FORM_FIELDS:
                                    hbox:
                                        spacing 12

                                        if question:
                                            text "[label] ([question]):":
                                                style "mc_forms_label"
                                        else:
                                            text "[label]:":
                                                style "mc_forms_label"

                                        if active_case == case:
                                            input value ScreenVariableInputValue(variable):
                                                id "mc_active_input"
                                                style "mc_forms_input"
                                                length 40
                                                xfill True
                                        else:
                                            textbutton mc_form_values[case]:
                                                style "mc_forms_input_display"
                                                text_style "mc_forms_input_display_text"
                                                xfill True
                                                action SetScreenVariable("active_case", case)
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
                                SetScreenVariable("stage", 0),
                            ]

                        textbutton "Зберегти":
                            style "mc_forms_button_primary"
                            text_style "mc_forms_button_text"
                            action [
                                Function(
                                    mc_set_forms,
                                    mc_normalize_name(name_value),
                                    {
                                        "gen": f_gen,
                                        "dat": f_dat,
                                        "acc": f_acc,
                                        "ins": f_ins,
                                        "loc": f_loc,
                                        "voc": f_voc,
                                    },
                                    indeclinable,
                                ),
                                Return(mc_normalize_name(name_value)),
                            ]

    else:
        # Preserve the original input screen for all other prompts (e.g. village name).
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
# 4. UI styles
# ============================================================

style mc_forms_title:
    font "fonts/KyivRegion-Regular.ttf"
    size 54
    color "#FFFFFF"
    text_align 0.5
    xalign 0.5

style mc_forms_text:
    font "fonts/PlaypenSans-Medium.ttf"
    size 30
    color "#FFFFFF"

style mc_forms_hint:
    font "fonts/PlaypenSans-Medium.ttf"
    size 24
    color "#BBBBBB"
    text_align 0.5

style mc_forms_label:
    font gui.interface_text_font
    size 38
    color "#EAEAEA"
    yalign 0.5

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
    background Frame(Solid("#343B47"), 12, 12)
    hover_background Frame(Solid("#4A586B"), 12, 12)
    insensitive_background Frame(Solid("#292D34"), 12, 12)

style mc_forms_button_primary is mc_forms_button:
    background Frame(Solid("#E4D0B1"), 12, 12)
    hover_background Frame(Solid("#af9d81"), 12, 12)

style mc_forms_button_toggle is mc_forms_button:
    background Frame(Solid("#343B47"), 12, 12)
    hover_background Frame(Solid("#4A586B"), 12, 12)
    selected_background Frame(Solid("#E4D0B1"), 12, 12)
    selected_hover_background Frame(Solid("#af9d81"), 12, 12)

style mc_forms_button_text:
    font gui.interface_text_font
    size 36
    color "#FFFFFF"
    hover_color "#FFFFFF"
    insensitive_color "#888888"
    selected_color "#FFFFFF"
    text_align 0.5
    outlines [(1, "#000000d0", 0, 0)]

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
# Usage examples:
# [name_form('nom')] — Називний
# [name_form('gen')] — Родовий
# [name_form('dat')] — Давальний
# [name_form('acc')] — Знахідний
# [name_form('ins')] — Орудний
# [name_form('loc')] — Місцевий
# [name_form('voc')] — Кличний
# ------------------------------------------------------------