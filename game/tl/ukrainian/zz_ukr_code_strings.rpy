# Додаємо змінну у дефоли, щоб вона зберігалася у сейвах
default current_game_label = None

init python:
    import os
    # =========================================================================
    # 📚 СЛОВНИК КОНТЕКСТНИХ ЗАМІН ТЕКСТУ
    #
    # Ключ:
    #   Шуканий токен.
    #
    # Значення:
    #   Список правил у форматі:
    #
    #   ("Новий текст", "screen", "назва_екрана")
    #   ("Новий текст", "label", "назва_лейбла")
    #
    # =========================================================================

    contextual_text_replacements = {
        # Фікс перекладу назви клавіші у меню допомоги
        "Увійти": [("Enter", "screen", "help")],

        # Переклад пустого статусу рангу
        "N/A": [("Н/Д", "screen", "cc_stats")],

        # Переклад сповіщення зловлених риб
        "E rank fish!": [("E-рангова риба", "label", "end_fishing")],
        "D rank fish!": [("D-рангова риба", "label", "end_fishing")],
        "C rank fish!": [("C-рангова риба", "label", "end_fishing")],
        "B rank fish!": [("B-рангова риба", "label", "end_fishing")],
        "A rank fish!": [("A-рангова риба", "label", "end_fishing")],
        "S rank fish!": [("S-рангова риба", "label", "end_fishing")],

        # Переклад назв предметів у меню підтвердження купівлі
        "Melon Pan": [("динну булочку", "screen", "buy_confirm_screen")],
        "Ні": [(" Ні", "screen", "buy_confirm_screen")],        # Виправлення положення
        'You bought 1 Melon Pan!': [("Ти купив динну булочку!", "screen", "notify_stack")]
    }
    # Зберігаємо старий replace_text, якщо він був визначений грою.
    _original_replace_text = config.replace_text

    # =========================================================================
    # 📍 ВІДСТЕЖЕННЯ ПОТОЧНОГО LABEL
    # =========================================================================

    def track_current_label(label_name, jumped):
        # Запам'ятовує останній label, до якого дійшов Ren'Py.
        # label_name -- ім'я label.
        # jumped     -- True, якщо перехід був зроблений через jump/call.

        # Відкидуємо службові лейбли, що починаються з _.
        # Таким чином заміна при завантаженні має правильно працювати.
        if label_name.startswith("_"): 
            return
        renpy.store.current_game_label = label_name


    # Реєструємо callback для відстеження label.
    #
    # Захист від повторної реєстрації потрібен, якщо цей код
    # буде перезавантажуватися під час розробки.
    if not hasattr(renpy.store, "_contextual_label_callback_registered"):
        config.label_callbacks.append(track_current_label)
        renpy.store._contextual_label_callback_registered = True

    # Атрибутний пошук назви поточного екрану, що будується
    def get_current_screen_name():
        curr_screen = "None"
        try:
            curr = renpy.current_screen()

            if curr:
                sn = (
                    getattr(curr, "screen_name", None)
                    or getattr(curr, "name", None)
                )

                if isinstance(sn, (tuple, list)) and len(sn) > 0:
                    curr = sn[0]

                elif isinstance(sn, str):
                    curr = sn

        except Exception:
            return None
        return curr
    
    # Отримання поточного лейблу з контексту
    def get_current_game_label():
        try:
            return getattr(renpy.store, "current_game_label", None)
        except Exception:
            return None

    # =========================================================================
    # ⚙️ ДЕБАГ-ПЕРЕМИКАЧ ТА ЛОГУВАННЯ
    # =========================================================================
    if not hasattr(renpy.store, "debug_text_log_active"):
        renpy.store.debug_text_log_active = False

    DEBUG_LOG_FILE = os.path.join(
        renpy.config.gamedir,
        "replacement_debug.log"
    )

    def toggle_text_debug_log():
        renpy.store.debug_text_log_active = not renpy.store.debug_text_log_active

        if renpy.store.debug_text_log_active:
            try:
                with open(DEBUG_LOG_FILE, "w", encoding="utf-8") as f:
                    f.write("=== DEBUG TOKEN LOG STARTED ===\n\n")
            except Exception:
                pass

            renpy.notify(
                "Дебаг токенів: УВІМКНЕНО (replacement_debug.log)"
            )

        else:
            renpy.notify("Дебаг токенів: ВИМКНЕНО")


    # Реєструємо гарячу клавішу Shift + F8
    config.keymap["toggle_text_debug"] = ["shift_K_F8"]
    config.underlay.append(
        renpy.Keymap(toggle_text_debug=toggle_text_debug_log)
    )


    def write_token_to_debug_log(s, status="TOKEN"):
        # Записує токен та поточний контекст у debug-файл.

        if not getattr(renpy.store, "debug_text_log_active", False):
            return

        curr_label = get_current_game_label() or "None"
        curr_screen = get_current_screen_name() or "None"

        # ЗАПИС У ФАЙЛ
        try:
            with open(DEBUG_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(
                    f"[{status}] "
                    f"{repr(s)} | "
                    f"Screen: {repr(curr_screen)} | "
                    f"Label: {repr(curr_label)}\n"
                )

        except Exception:
            pass

    # =========================================================================
    # 🔍 ПЕРЕВІРКА АКТИВНОГО SCREEN
    # =========================================================================

    def is_screen_active(screen_name):

        # 1. Перевіряємо, чи screen уже зареєстрований як активний.
        try:
            if renpy.get_screen(screen_name):
                return True
        except Exception:
            pass


        # 2. Перевіряємо screen, який будується прямо зараз.
        if screen_name == get_current_screen_name():
            return True

        return False


    # =========================================================================
    # 🔍 ПЕРЕВІРКА АКТИВНОГО LABEL
    # =========================================================================

    def is_label_active(target_label):
        return target_label == get_current_game_label()


    # =========================================================================
    # 🧠 ОСНОВНИЙ CONTEXTUAL REPLACEMENT ENGINE
    # =========================================================================

    def smart_contextual_replace_text(s):

        # Спочатку передаємо текст старому replace_text, якщо він існував.
        if _original_replace_text:
            s = _original_replace_text(s)

        # DEBUG
        write_token_to_debug_log(s, status="TOKEN")

        if s not in contextual_text_replacements:
            return s

        rules = contextual_text_replacements[s]

        # Зручність:
        # якщо передано один tuple замість списку,
        # автоматично перетворюємо його на список.
        if isinstance(rules, tuple):
            rules = [rules]

        # Перевіряємо всі правила для цього тексту.
        for new_text, ctx_type, ctx_target in rules:

            # SCREEN
            if ctx_type == "screen":
                if is_screen_active(ctx_target):
                    write_token_to_debug_log(new_text, status="REPLACED")
                    return new_text

            # LABEL
            elif ctx_type == "label":
                if is_label_active(ctx_target):
                    write_token_to_debug_log(new_text, status="REPLACED")
                    return new_text

        # Якщо жодне контекстне правило не підійшло,
        # повертаємо оригінальний текст.
        return s

    # =========================================================================
    # 🚀 АКТИВУЄМО CONTEXTUAL TEXT ENGINE
    # =========================================================================
    config.replace_text = smart_contextual_replace_text