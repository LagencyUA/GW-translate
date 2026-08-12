default quick_menu_scale = 3
init 999 screen quick_menu():
    variant "touch"

    zorder 100
    if quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0
            yoffset get_quick_menu_offset(quick_menu_scale)
            spacing get_quick_menu_spacing(quick_menu_scale)
            textbutton _("Back"):
                action Rollback()
                text_size get_quick_menu_text_size(quick_menu_scale)
            textbutton _("Skip"):
                action Skip() alternate Skip(fast=True, confirm=True)
                text_size get_quick_menu_text_size(quick_menu_scale)
            textbutton _("Auto"):
                action Preference("auto-forward", "toggle")
                text_size get_quick_menu_text_size(quick_menu_scale)
            textbutton _("Menu"):
                action ShowMenu()
                text_size get_quick_menu_text_size(quick_menu_scale)
            textbutton _("Hide"):
                action HideInterface()
                text_size get_quick_menu_text_size(quick_menu_scale)

init 999 screen say(who, what):
    variant "touch"

    style_prefix "say"

    window:
        id "window"
        yoffset get_say_offset(quick_menu_scale)

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

init python:
    quick_menu_scale_variants = [
        {
            "text_size": 30,
            "spacing": 10,
            "q_m_offset": 0,
            "say_offset": 0
        },
        {
            "text_size": 32,
            "spacing": 15,
            "q_m_offset": -5,
            "say_offset": -15
        },
        {
            "text_size": 34,
            "spacing": 20,
            "q_m_offset": -15,
            "say_offset": -25
        },
        {
            "text_size": 36,
            "spacing": 25,
            "q_m_offset": -25,
            "say_offset": -35
        },
        {
            "text_size": 38,
            "spacing": 30,
            "q_m_offset": -35,
            "say_offset": -45
        }
    ]
    def get_quick_menu_text_size(scale):
        return quick_menu_scale_variants[scale]["text_size"]
    def get_quick_menu_spacing(scale):
        return quick_menu_scale_variants[scale]["spacing"]
    def get_quick_menu_offset(scale):
        return quick_menu_scale_variants[scale]["q_m_offset"]
    def get_say_offset(scale):
        return quick_menu_scale_variants[scale]["say_offset"]
