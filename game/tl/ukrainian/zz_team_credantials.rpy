init python:
    # Додаємо наш кастомний екран до списку постійних оверлеїв гри
    config.always_shown_screens.append("ukr_menu_credits_overlay")

screen ukr_menu_credits_overlay():
    if renpy.get_screen("main_menu") and renpy.game.preferences.language == "ukrainian":
        imagebutton:
            at smooth_sway
            xpos 5
            ypos 240
            idle "tl/ukrainian/images/17october_team_tg.png"
            hover im.MatrixColor("tl/ukrainian/images/17october_team_tg.png", im.matrix.brightness(0.1))
            action OpenURL("https://t.me/group_17_october")
        text "Перекладено\nкомандою":
            pos (45, 160)
            color "#FFFFFF"
            font "fonts/ukr/PlaypenSans-Medium.ttf"
            text_align 0.5
            outlines [((absolute(3), "#000000", absolute(0), absolute(0)))]
            size 25
            at text_anim_bw
        text "Заходьте до\nнас!":
            pos (15, 320)
            color "#FFFFFF"
            font "fonts/ukr/PlaypenSans-Medium.ttf"
            text_align 0.5
            outlines [((absolute(3), "#000000", absolute(0), absolute(0)))]
            size 25
            at text_anim_bw_2


transform -1 smooth_sway:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    ease 1.5 xoffset 5 yoffset -5 zoom 1.06 rotate 10
    pause .8
    ease 1.5 xoffset 0 yoffset 0 zoom 1.0 rotate 0
    repeat

transform -1 text_anim_bw:
    rotate 16
    zoom 0.95
    easein 1 zoom 1
    easein 1 zoom 0.95
    repeat
transform -1 text_anim_bw_2:
    rotate 5
    zoom 0.95
    easein 1 zoom 1
    easein 1 zoom 0.95
    repeat