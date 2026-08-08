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