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
                elif fn == "Sacred Bridge Demo.ttf": # У деяких рядках використовується такий шлях
                    fn = "fonts/ukr/Monomakh-Regular.ttf"
                elif fn == "fonts/Ebrima.ttf":
                    fn = "fonts/ukr/Arial.ttf"
                elif fn == "fonts/Bohemian Soul.otf":
                    fn = "fonts/ukr/Lobster-Regular.ttf"
                elif fn == "fonts/Mandaly.ttf":
                    fn = "fonts/ukr/Caveat-Bold.ttf"
                    
            return old_load_face(fn, *args)
            
        renpy.text.font.load_face = my_load_face

    # Коректне перезавантаження інтерфейсу (Shift+R)
    old_reload_all = renpy.reload_all
    def my_reload_all():
        renpy.text.font.free_memory()
        renpy.text.font.load_face = old_load_face
        ret = old_reload_all()
        renpy.reload_all = old_reload_all
        return ret
    renpy.reload_all = my_reload_all

## Розміри шрифтів
translate ukrainian style say_dialogue:
    size 30          # Зменшуємо основний сюжетний текст
    line_spacing 1   # Додаємо мікро-відступ між рядками, щоб читалося легше

translate ukrainian style say_label:
    size 46          # Зменшуємо імена персонажів

translate ukrainian style choice_button_text:
    size 28          # Зменшуємо текст у кнопках вибору сюжету


# --- ВАРІАНТ 1: Рубі над текстом ---
translate ukrainian style ukr_ruby_top:
    size 16
    yoffset -38

translate ukrainian style ukr_say_ruby_top is say_dialogue:
    line_spacing 6
    ruby_style style.ukr_ruby_top


# --- ВАРІАНТ 2: Рубі ПІД текстом (твоя ідея) ---
translate ukrainian style ukr_ruby_bottom:
    size 16
    # Додатне значення зміщує текст УНИЗ від базової лінії
    yoffset 38  
    
translate ukrainian style ukr_say_ruby_bottom is say_dialogue:
    # Якщо підказка на останньому рядку
    ruby_style style.ukr_ruby_bottom