## Перевизначаємо стартове меню вибору мови,
## щоб додати українську, як опцію


init 15 screen choose_language:
    modal True
    
    # Додаємо українську мову в тайтл.
    text "Choose your language / Elije tu idioma / {font=tl/ukrainian/fonts/Arial.ttf}Оберіть мову{/font}" font "fonts/Ebrima.ttf" color "#FFE8C9" outlines [((absolute(2), "#091519", absolute(0), absolute(0)))] align (.5, .3) text_align .5
    
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

        # Нова кнопка української мови:
        button:
            xysize (311, 87)
            focus_mask "bg/icons/choose_bg.png"
            hover_focus_mask im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            idle_background "bg/icons/choose_bg.png"
            hover_background im.MatrixColor("bg/icons/choose_bg.png", im.matrix.brightness(0.1))
            # Примусово вказуємо шрифт Arial, щоб слово відобразилося кирилицею без кубиків
            text "{font=tl/ukrainian/fonts/Arial.ttf}{size=+10}Українська" align (.5, .45) outlines [((absolute(2), "#091519", absolute(0), absolute(0)))]
            # Логіка: вимикаємо іспанський режим і вмикаємо нашу локалізацію
            action [ SetVariable("spanish_active", False), Language('ukrainian'), Return() ]