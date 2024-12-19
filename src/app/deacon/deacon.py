import secrets


def handle_king(log, messages, group, player):
    # King lost
    if player.streak == 0:
        log.info(f"[handle_king] The Reign of King {player.name} is over!")
        log.info("[handle_king] Searching for a new King...")
        group.dethrone()
        new_king = group.get_player_by_id(group.king)
        if new_king is not None:
            return messages.load_with_params("result.king.lose.new",[player.name, str(player.prev_streak), new_king.name])
        else:
            return messages.load_with_params("result.king.lose", [player.name, str(player.prev_streak)])
    # King Wins
    else:
        return messages.load_with_params("result.king.win", [str(player.get_average())])

def handle_commoner(log, messages, group, player):
    # ...and loses
    if player.streak == 0:
        log.info(f"[handle_commoner] The Streak of {player.name} has been broken!")
        return messages.load_with_params("result.common.lose", [player.name, str(player.prev_streak)])
    # ...and begins
    elif player.streak == 1:
        log.info(f"[handle_commoner] Player {player.name} has begun their kingdom!")
        random_message = secrets.SystemRandom().randrange(1,2) #NOSONAR
        return messages.load_with_params("result.player.start."+str(random_message), [player.name])
    # ...and wins...
    else:
        # ...and deserves coronation
        if player.streak > group.get_streak_by_id(group.king):
            group.crown(player)
            return messages.load_with_params("result.common.coronation", [player.name])
        else:
            player.title = update_title(player)
            return messages.load_with_params("result.common.win", [player.name, str(player.get_average())])


def update_title(player):
    score = player.get_average()
    if score > 4.0:
        return 'Knight'
    if score > 3.0:
        return 'Master'
    if score > 2.0:
        return 'Freemen'
    if score > 1.0:
        return 'Commoner'
    else:
        return 'Peasant'
