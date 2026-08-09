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

        # Перевіряємо, чи є поточний текст у нашому словнику замін
        if s in contextual_text_replacements:
            rules = contextual_text_replacements[s]

            # Зручність: якщо передано один кортеж замість списку, загортаємо у список
            if isinstance(rules, tuple):
                rules = [rules]

            # Проходимо по всіх правилах для цього слова
            for new_text, ctx_type, ctx_target in rules:
                
                # Перевірка контексту для ЕКРАНІВ
                if ctx_type == "screen" and renpy.get_screen(ctx_target):
                    return new_text

                # Перевірка контексту для СЮЖЕТНИХ ЛЕЙБЛІВ
                elif ctx_type == "label" and renpy.current_label() == ctx_target:
                    return new_text

        return s

    # Активуємо наш контекстний двигун у Ren'Py
    config.replace_text = smart_contextual_replace_text