init 999 python:
    ### Назви риб
    if "fish_rank_mapping" in globals():
        orig_fish_rank_mapping = fish_rank_mapping.copy()

        ua_fish_rank_mapping = {
            "1": ("bg/icons/fish/catch_fish/ecatch_", "E-рангова риба"),
            "2": ("bg/icons/fish/catch_fish/dcatch_", "D-рангова риба"),
            "3": ("bg/icons/fish/catch_fish/ccatch_", "C-рангова риба"),
            "4": ("bg/icons/fish/catch_fish/bcatch_", "B-рангова риба"),
            "5": ("bg/icons/fish/catch_fish/acatch_", "A-рангова риба"),
            "6": ("bg/icons/fish/catch_fish/ccatch_", "S-рангова риба")
        }

        def update_fish_rank_language():
            if renpy.game.preferences.language == "ukrainian":
                fish_rank_mapping.update(ua_fish_rank_mapping)
            else:
                fish_rank_mapping.update(orig_fish_rank_mapping)

        config.change_language_callbacks.append(update_fish_rank_language)
        update_fish_rank_language()

    ### Лікування підмін
    # =========================================================================
    # 📚 СЛОВНИК КОНТЕКСТНИХ ЗАМІН ТЕКСТУ
    #
    # Ключ: Шуканий рядок (який уже пройшов переклад або оригінальний)
    # Значення: Список правил у форматі:
    #   ("Новий текст", "screen", "назва_екрана")   -- для меню/інтерфейсу
    #   ("Новий текст", "label", "назва_лейбла")   -- для сюжету/діалогів
    # =========================================================================
    contextual_text_replacements = {
        "Увійти": [("Enter", "screen", "help")]
    }

    _original_replace_text = config.replace_text

    def smart_contextual_replace_text(s):
        # Перевіряємо, чи був старий обробник у грі (щоб нічого не зламати)
        if _original_replace_text:
            s = _original_replace_text(s)

        ## Перевірка поточного екрану
        def is_screen_active(screen_name):
            # 1. Перевіряємо, чи екран вже зареєстрований як активний
            if renpy.get_screen(screen_name):
                return True

            # 2. Перевіряємо, чи екран будується прямо зараз в цей мікрокадр
            try:
                curr = renpy.current_screen()
                if curr:
                    # Отримуємо назву екрана, який зараз у процесі генерації
                    sn = getattr(curr, "screen_name", None) or getattr(curr, "name", None)
                    if isinstance(sn, (tuple, list)) and len(sn) > 0:
                        sn = sn[0]
                    if sn == screen_name:
                        return True
            except Exception:
                pass

            return False

        # Перевіряємо, чи є поточний текст у нашому словнику замін
        if s in contextual_text_replacements.keys():
            rules = contextual_text_replacements[s]

            # Зручність: якщо передано один кортеж замість списку, загортаємо у список
            if isinstance(rules, tuple):
                rules = [rules]

            # Проходимо по всіх правилах для цього слова
            for new_text, ctx_type, ctx_target in rules:
                
                is_text_in_screen = (ctx_type == "screen" and is_screen_active(ctx_target))
                is_text_in_label = (ctx_type == "label" and renpy.current_label() == ctx_target)
                if is_text_in_screen or is_text_in_label:
                    return new_text

        return s

    # Активуємо наш контекстний двигун у Ren'Py
    config.replace_text = smart_contextual_replace_text