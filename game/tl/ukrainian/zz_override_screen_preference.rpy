## Перевизначаємо меню налаштувань, щоб
## додати українську мову як опцію вибору мови


init 10 screen preferences():
    tag menu
    use game_menu(_("Options"), scroll="viewport"):
        vbox:
            xpos .05
            ypos .5
            hbox:
                box_wrap True
                if renpy.variant("android") or renpy.variant("mobile") or renpy.variant("tablet"):
                    xfill True
                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "radio"
                        text _("Display") style "options_label_text"
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    if renpy.variant("android") or renpy.variant("mobile") or renpy.variant("tablet"):
                        xsize 300    ## Фікс багу, коли на андроїді не поміщається бокс із мовами в одну лінію
                    style_prefix "radio"
                    text _("Rollback Side") style "options_label_text"
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    if renpy.variant("android") or renpy.variant("mobile") or renpy.variant("tablet"):
                        xsize 300    ## Фікс багу, коли на андроїді не поміщається бокс із мовами в одну лінію
                    style_prefix "check"
                    text _("Skip") style "options_label_text"
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    if renpy.variant("android") or renpy.variant("mobile") or renpy.variant("tablet"):
                        xsize 300    ## Фікс багу, коли на андроїді не поміщається бокс із мовами в одну лінію
                    style_prefix "check"
                    text _('language') style "options_label_text"
                    # Лікуємо баг з відображенням буліта перед англійською мовою,
                    # коли активна українська мова за допомогою примусового модифікатора selected
                    textbutton _('English') action [ SetVariable("spanish_active", False), Language(None) ] selected (renpy.game.preferences.language is None)
                    textbutton _('Español') action [SetVariable("spanish_active", True),  Language('Spanish') ] selected (renpy.game.preferences.language == 'Spanish')
                    # Нова нопка для перемикання на українську мову
                    textbutton _('Українська') action [SetVariable("spanish_active", False),  Language('ukrainian') ] selected (renpy.game.preferences.language == 'ukrainian') text_font "fonts/ukr/Arial.ttf"

            null height (4 * gui.pref_spacing)
            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:
                    text _("Text Speed") style "options_barras_text"
                    bar value Preference("text speed") style "options_bar"
                    text _("Auto-Forward Time") style "options_barras_text"
                    bar value Preference("auto-forward time") style "options_bar"

                vbox:
                    if config.has_music:
                        text _("Music Volume") style "options_barras_text"
                        hbox:
                            bar value Preference("music volume") style "options_bar"

                    if config.has_sound:
                        text _("Sound Volume") style "options_barras_text"
                        hbox:
                            bar value Preference("sound volume") style "options_bar"
                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing
                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"
            
            # Додаємо повзунок налаштування розміру швидкого меню
            if renpy.variant("touch"):
                vbox:
                    text "Розмір нижнього швидкого меню" style "options_barras_text"
                    bar value FieldValue(
                        object=persistent,
                        field="quick_menu_scale",
                        range=4,
                        step=1,
                        style="slider"
                    ) style "options_bar"