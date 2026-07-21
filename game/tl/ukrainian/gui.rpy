## Динамічне підключення шрифтів для української мови
init python early hide:
    import renpy
    if 'tl_font_dic' not in globals():
        global tl_font_dic
        tl_font_dic = dict()
        global old_load_face
        old_load_face = renpy.text.font.load_face

        def my_load_face(fn, *args):
            # Якщо увімкнено українську мову
            if renpy.game.preferences.language == "ukrainian":
                # Перевіряємо, який саме шрифт гра намагається завантажити,
                # і підміняємо його на українську версію
                if fn == "fonts/PinkChicken-Regular.ttf":
                    fn = "fonts/ukr/PlaypenSans-Medium.ttf"
                elif fn == "fonts/Sacred Bridge Demo.ttf":
                    fn = "fonts/ukr/Monomakh-Regular.ttf"
                elif fn == "fonts/Ebrima.ttf":
                    fn = "fonts/ukr/Arial.ttf"
                elif fn == "fonts/Bohemian Soul.otf":
                    fn = "fonts/ukr/Lobster-Regular.ttf"
                elif fn == "fonts/Mandaly.ttf":
                    fn = "fonts/ukr/Caveat-Bold.ttf"
                    
            return old_load_face(fn, *args)
            
        renpy.text.font.load_face = my_load_face

    # Цю частину з reload_all залишаємо для коректного перезавантаження інтерфейсу (Shift+R)
    old_reload_all = renpy.reload_all
    def my_reload_all():
        renpy.text.font.free_memory()
        renpy.text.font.load_face = old_load_face
        ret = old_reload_all()
        renpy.reload_all = old_reload_all
        return ret
    renpy.reload_all = my_reload_all

# Додаємо динамічний колбек для зміни розміру шрифтів при зміні мови
# Ці блоки спрацьовують АВТОМАТИЧНО і виключно для української мови.

translate ukrainian style say_dialogue:
    size 30          # Зменшуємо основний сюжетний текст
    line_spacing 1   # Додаємо мікро-відступ між рядками, щоб читалося легше

translate ukrainian style say_label:
    size 46          # Зменшуємо імена персонажів

translate ukrainian style choice_button_text:
    size 28          # Зменшуємо текст у кнопках вибору сюжету

## Перевизначаємо меню налаштувань, щоб додати українську мову як опцію вибору мови
init 10 screen preferences():
    tag menu


    use game_menu(_("Options"), scroll="viewport"):

        vbox:
            xpos .05
            ypos .5
            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        text _("Display") style "options_label_text"
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    text _("Rollback Side") style "options_label_text"
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    text _("Skip") style "options_label_text"
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    style_prefix "check"
                    text _('language') style "options_label_text"

## Лікуємо баг з відображенням буліта перед англійською мовою, коли активна українська мова за допомогою примусового модифікатора selected
                    textbutton _('English') action [ SetVariable("spanish_active", False), Language(None) ] selected (renpy.game.preferences.language is None)
                    textbutton _('Español') action [SetVariable("spanish_active", True),  Language('Spanish') ] selected (renpy.game.preferences.language == 'Spanish')

## Кнопка для перемикання на українську мову
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

## ПЕРЕВИЗНАЧЕННЯ СТАРТОВОГО МЕНЮ ВИБОРУ МОВИ (CHOOSE LANGUAGE)
# Ставимо init 15, щоб перекрити оригінальний екран з menus.rpy
init 15 screen choose_language():
    modal True
    
    # Додаємо українську мову в тайтл. Загортаємо її у тег {font}, 
    # бо оригінальний Ebrima.ttf може не підтримувати кирилицю на старті!
    text "Choose your language / Elije tu idioma / {font=fonts/ukr/Arial.ttf}Оберіть мову{/font}" font "fonts/Ebrima.ttf" color "#FFE8C9" outlines [((absolute(2), "#091519", absolute(0), absolute(0)))] align (.5, .3) text_align .5
    
    hbox:
        align (.5, .5)
        spacing 120 # Трохи зменшили відстань з 200 до 120, щоб три кнопки ідеально встали в ряд

        # Кнопка англійської мови
        button:
            xysize (311, 87)
            focus_mask "bg/icons/choose_bg.png"
            hover_focus_mask im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            idle_background "bg/icons/choose_bg.png"
            hover_background im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            text "{font=fonts/Ebrima.ttf}{size=+10}English" align (.5, .45) outlines [((absolute(2), "#091519", absolute(0), absolute(0)))]
            action [ SetVariable("spanish_active", False), Return() ]

        # Кнопка іспанської мови
        button:
            xysize (311, 87)
            focus_mask "bg/icons/choose_bg.png"
            hover_focus_mask im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            idle_background "bg/icons/choose_bg.png"
            hover_background im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            text "{font=fonts/Ebrima.ttf}{size=+10}Español" align (.5, .45) outlines [((absolute(2), "#091519", absolute(0), absolute(0)))]
            action [  SetVariable("spanish_active", True), Language('Spanish'), Return() ]

        # НАША НОВА КНОПКА УКРАЇНСЬКОЇ МОВИ:
        button:
            xysize (311, 87)
            focus_mask "bg/icons/choose_bg.png"
            hover_focus_mask im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            idle_background "bg/icons/choose_bg.png"
            hover_background im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            # Примусово вказуємо шрифт Arial, щоб слово відобразилося кирилицею без кубиків
            text "{font=fonts/ukr/Arial.ttf}{size=+10}Українська" align (.5, .45) outlines [((absolute(2), "#091519", absolute(0), absolute(0)))]
            # Логіка: вимикаємо іспанський режим і вмикаємо нашу локалізацію
            action [ SetVariable("spanish_active", False), Language('ukrainian'), Return() ]