from datetime import datetime
import pytest

from src.app.model.group.group import Group
from src.app.model.group.player import Player
from src.app.model.group.record import Record


@pytest.fixture
def fake_envs(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', 'REDIS_TOKEN')
    monkeypatch.setenv('REDIS_URL', 'redis://REDIS_URL')
    monkeypatch.setenv('SLACK_BOT_TOKEN', 'BOT_TOKEN')
    monkeypatch.setenv('SLACK_SIGNING_SECRET', 'SLACK_SECRET')
    monkeypatch.setenv('SLACK_SCOPES', '["SCOPE_ONE", "SCOPE_2"]')
    monkeypatch.setenv('DEBUG', 'False')
    monkeypatch.setenv('PORT', '3000')
    monkeypatch.setenv('SCROLL_MIN_STREAK', '2')
    monkeypatch.setenv('SCROLL_MAX_LIST', '3')


@pytest.fixture
def config_initialise():
    from src.app.config.config import Config
    config = Config()

    return config


class GroupSpec:
    group_name = 'group_name'
    datetime_format = '%d/%m/%Y'

    def should_not_update_scroll_if_new_streak_lower_than_the_lowest_record_streak(self, fake_envs, config_initialise):
        """ Should not update scroll if new streak lower than the lowest record streak """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000), Player('James', 2, '3', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('Maciej', 1, '4', 1000)

        # When
        subject.update_scroll(test, config_initialise)

        # Then : scroll is left untouched
        assert subject.scroll is scroll

    def should_update_scroll_if_new_streak_lower_than_the_lowest_record_streak_but_scroll_has_capacity(self, fake_envs,
                                                                                                       config_initialise):
        """ Should update scroll if new streak lower than the lowest record streak but scroll has capacity"""
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('Maciej', 2, '4', 1000)
        # Note :: streaks are defined as being >= 2

        # When
        subject.update_scroll(test, config_initialise)

        # Then : test is added to the scroll
        assert subject.scroll == [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), test.get_record()]

    def should_update_existing_record_if_player_streak_is_active_on_the_scroll(self, fake_envs, config_initialise):
        """ Should update existing record if worthy player streak is active on the scroll """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000), Player('James', 2, '3', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('Adam', 5, '1', 1005)

        # When
        subject.update_scroll(test, config_initialise)

        # Then : 'Adam' Record with streak id '1' should be updated
        updated_record = [x for x in subject.scroll if x.streak_id == test.streak_id][0]
        assert updated_record.streak is 5

    def should_not_add_score_as_scroll_entry_unworthy_by_min_streak(self, fake_envs, config_initialise):
        """ Should add no new record as player streak score is not worthy """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('James', 1, '3', 1005)

        # When
        subject.update_scroll(test, config_initialise)

        # Then : The scroll is not updated. Subject scroll should equal the defined scroll.
        assert scroll == subject.scroll

    def should_add_record_but_not_exceed_scroll_size(self, fake_envs, config_initialise):
        """ Should add the new record but remove the lowest scoring record to stick to scroll size """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('Maciej', 2, '2', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('James', 5, '3', 1005)

        # When
        subject.update_scroll(test, config_initialise)

        expected_scroll = [Record('James', 5, '3', datetime.today().strftime(self.datetime_format)),
                           Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]

        assert expected_scroll == subject.scroll

    def should_add_new_record_if_worthy_streak_is_not_active_on_the_scroll_and_scroll_below_capacity(self, fake_envs,
                                                                                                     config_initialise):
        """ Should add new record if worthy streak is not active on the scroll and scroll below capacity """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('Adam', 5, '3', 1005)

        # When
        subject.update_scroll(test, config_initialise)

        # Then : 'Adam' Record w/streak id '1' should be preserved; second 'Adam' Record added w/streak id '2'
        # Note : also expect scroll to be sorted upon update
        expected_record = Record('Adam', 5, '3', datetime.today().strftime(self.datetime_format))
        expected_scroll = [expected_record, Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        difference = [x for x in subject.scroll if x not in expected_scroll]
        assert len(difference) is 0

    def should_replace_an_old_record_if_worthy_streak_is_not_active_on_the_scroll_and_scroll_at_capacity(self,
                                                                                                         fake_envs,
                                                                                                         config_initialise):
        """ Should replace an old record if worthy streak is not active on the scroll and scroll at capacity """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000), Player('James', 2, '3', 1000)]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), scroll)

        test = Player('Adam', 5, '4', 1005)

        # When
        subject.update_scroll(test, config_initialise)

        # Then : 'Adam' Record w/streak id '1' should be preserved; second 'Adam' Record added w/streak id '2'
        # Note : also expect scroll to be sorted upon update
        expected_record = Record('Adam', 5, '4', datetime.today().strftime(self.datetime_format))
        expected_scroll = [expected_record, Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today')]
        difference = [x for x in subject.scroll if x not in expected_scroll]
        assert len(difference) is 0

    def should_dethrone_king_by_crowning_next_highest_player(self):
        """ Should dethrone king by crowning next highest player """
        # Given
        players = [Player('Adam', 4, '1', 1000), Player('Hayden', 3, '2', 1000), Player('James', 2, '3', 1000)]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), [])

        test = Player('Adam', 0, '1', 1000)

        # When
        subject.update_player(test)
        subject.dethrone()

        # Then : King is Hayden
        assert subject.king == Player('Hayden', 3, '2', 1000)

    def should_reset_streak_id_when_player_has_streak_of_zero(self):
        """ Should reset streak id when player has streak of zero """
        # Given
        players = [Player('Adam', 4, '1', 1000)]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), [])

        test = Player('Adam', 0, '1', 1000)

        # When
        subject.update_player(test)

        # Then : Adam should have new streak id
        assert [x for x in subject.players if x.name == 'Adam'][0].streak_id != '1'

    def should_not_reset_streak_id_when_player_has_non_zero_streak(self):
        """ Should not reset streak id when player has non-zero streak """
        # Given
        players = [Player('Adam', 4, '1', 1000)]
        subject = Group(self.group_name, players, Player('Adam', 4, '1', 1000), [])

        test = Player('Adam', 5, '1', 1000)

        # When
        subject.update_player(test)

        # Then : Adam should have new streak id
        assert [x for x in subject.players if x.name == 'Adam'][0].streak_id == '1'
