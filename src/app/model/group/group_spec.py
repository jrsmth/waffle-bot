from datetime import datetime
import pytest

from src.app.model.group.group import Group
from src.app.model.group.player import Player
from src.app.model.group.record import Record


class GroupSpec:
    group_name = 'group_name'
    datetime_format = '%d/%m/%Y'

    def should_not_update_scroll_if_new_streak_lower_than_the_lowest_record_streak(self):
        """ Should not update scroll if new streak lower than the lowest record streak """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10), Player('3', 'James', 2, '3', 1000, 10)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)

        test = Player('4', 'Maciej', 1, '4', 1000, 10)

        # When
        subject.update_scroll(test)

        # Then : scroll is left untouched
        assert subject.scroll is scroll

    def should_update_scroll_if_new_streak_lower_than_the_lowest_record_streak_but_scroll_has_capacity(self):
        """ Should update scroll if new streak lower than the lowest record streak but scroll has capacity"""
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        subject = Group(self.group_name, players, '1', scroll)

        test = Player('4', 'Maciej', 2, '4', 1000, 10)
        # Note :: streaks are defined as being >= 2

        # When
        subject.update_scroll(test)

        # Then : test is added to the scroll
        assert subject.scroll == [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), test.get_record()]

    def should_update_existing_record_if_player_streak_is_active_on_the_scroll(self):
        """ Should update existing record if worthy player streak is active on the scroll """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10),
                   Player('3', 'James', 2, '3', 1000, 10)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)

        test = Player('1', 'Adam', 5, '1', 1005, 10)

        # When
        subject.update_scroll(test)

        # Then : 'Adam' Record with streak id '1' should be updated
        updated_record = [x for x in subject.scroll if x.streak_id == test.streak_id][0]
        assert updated_record.streak == 5

    def should_not_add_score_as_scroll_entry_unworthy_by_min_streak(self):
        """ Should add no new record as player streak score is not worthy """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        subject = Group(self.group_name, players, '1', scroll)

        test = Player('James', 1, '3', 1005)

        # When
        subject.update_scroll(test)

        # Then : The scroll is not updated. Subject scroll should equal the defined scroll.
        assert scroll == subject.scroll

    def should_add_record_but_not_exceed_scroll_size(self):
        """ Should add the new record but remove the lowest scoring record to stick to scroll size """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('Maciej', 2, '2', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('James', 5, '3', 1005)

        # When
        subject.update_scroll(test)

        expected_scroll = [Record('James', 5, '3', datetime.today().strftime(self.datetime_format)),
                           Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]

        assert expected_scroll == subject.scroll

    def should_add_new_record_if_worthy_streak_is_not_active_on_the_scroll_and_scroll_below_capacity(self):
        """ Should add new record if worthy streak is not active on the scroll and scroll below capacity """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        subject = Group(self.group_name, players, '1', scroll)

        test = Player('1', 'Adam', 5, '3', 1005, 11)

        # When
        subject.update_scroll(test)

        # Then : 'Adam' Record w/streak id '1' should be preserved; second 'Adam' Record added w/streak id '2'
        # Note : also expect scroll to be sorted upon update
        expected_record = Record('Adam', 5, '3', datetime.today().strftime(self.datetime_format))
        expected_scroll = [expected_record, Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        difference = [x for x in subject.scroll if x not in expected_scroll]
        assert len(difference) == 0

    def should_replace_an_old_record_if_worthy_streak_is_not_active_on_the_scroll_and_scroll_at_capacity(self):
        """ Should replace an old record if worthy streak is not active on the scroll and scroll at capacity """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10),
                   Player('3', 'James', 2, '3', 1000, 10)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)

        test = Player('1', 'Adam', 5, '4', 1005, 11)

        # When
        subject.update_scroll(test)

        # Then : 'Adam' Record w/streak id '1' should be preserved; second 'Adam' Record added w/streak id '2'
        # Note : also expect scroll to be sorted upon update
        expected_record = Record('Adam', 5, '4', datetime.today().strftime(self.datetime_format))
        expected_scroll = [expected_record, Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        difference = [x for x in subject.scroll if x not in expected_scroll]
        assert len(difference) == 0

    def should_dethrone_king_by_crowning_next_highest_player(self):
        """ Should dethrone king by crowning next highest player """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10), Player('3', 'James', 2, '3', 1000, 10)]
        subject = Group(self.group_name, players, '1', [])

        test = Player('1', 'Adam', 0, '1', 1000, 10)

        # When
        subject.update_player(test)
        subject.dethrone()

        # Then : King is Hayden
        assert subject.king == '2'
        players = [Player('1', 'Adam', 4, '1', 1000, 10), Player('2', 'Hayden', 3, '2', 1000, 10), Player('3', 'James', 2, '3', 1000, 10)]
        subject = Group(self.group_name, players, '1', [])

        test = Player('1', 'Adam', 0, '1', 1000, 10)

        # When
        subject.update_player(test)
        subject.dethrone()
        # Then : King is Hayden
        assert subject.king == '2'

    def should_dethrone_king_and_king_stays_same_with_other_player_updated(self):
        players = [Player('1', 'Adam', 5, '1', 1000, 10), Player('2', 'Hayden', 4, '2', 1000, 10)]
        subject = Group(self.group_name, players, '1', [])

        test = Player('1', 'Adam', 0, '1', 1000, 11)

        # When
        subject.update_player(test)
        subject.dethrone()
        # Then : King is Hayden
        assert subject.king == '2'

        # And another player goes who is not the king
        test_adam = Player('1', 'Adam', 1, '3', 1000, 12)
        subject.update_player(test_adam)

        # Then : King is still Hayden
        assert subject.king == '2'

    def should_reset_streak_id_when_player_has_streak_of_zero(self):
        """ Should reset streak id when player has streak of zero """
        # Given
        players = [Player('1','Adam', 4, '1', 1000, 10)]
        subject = Group(self.group_name, players, '1', [])

        test = Player('1', 'Adam', 0, '1', 1000, 10)

        # When
        subject.update_player(test)

        # Then : Adam should have new streak id
        assert [x for x in subject.players if x.name == 'Adam'][0].streak_id != '1'

    def should_not_reset_streak_id_when_player_has_non_zero_streak(self):
        """ Should not reset streak id when player has non-zero streak """
        # Given
        players = [Player('1', 'Adam', 4, '1', 1000, 10)]
        subject = Group(self.group_name, players, '1', [])

        test = Player('1', 'Adam', 5, '1', 1000, 10)

        # When
        subject.update_player(test)

        # Then : Adam should have new streak id
        assert [x for x in subject.players if x.name == 'Adam'][0].streak_id == '1'
