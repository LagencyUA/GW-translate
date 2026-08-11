init 999 screen quick_menu():
    variant "touch"

    zorder 100
    if quick_menu:
        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0
            yoffset -25
            spacing 25
            textbutton _("Back"):
                action Rollback()
                text_size 36
            textbutton _("Skip"):
                action Skip() alternate Skip(fast=True, confirm=True)
                text_size 36
            textbutton _("Auto"):
                action Preference("auto-forward", "toggle")
                text_size 36
            textbutton _("Menu"):
                action ShowMenu()
                text_size 36
            textbutton _("Hide"):
                action HideInterface()
                text_size 36

init 999 screen say(who, what):
    variant "touch"

    style_prefix "say"

    window:
        id "window"
        yoffset -35

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"