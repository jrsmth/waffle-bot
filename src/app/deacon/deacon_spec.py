import logging

from from_root import from_root

from src.app.util.messages.messages import Messages
from src.app.deacon.deacon import handle_king, handle_commoner, update_title
from src.app.model.group.group import Group
from src.app.model.group.group_spec import get_player
from src.app.model.group.record import Record

log = logging.getLogger('src.app.deacon.deacon_spec')

class DeaconSpec:
    messages = Messages(from_root("resources", "messages.properties"))
    group_name = 'group_name'


    def should_return_king_lose_new_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)
        # Given no longer king
        test = get_player('Adam')
        test.streak = 0

        #When
        response = handle_king(log, self.messages, subject, test)

        #Then
        assert 'I dub thee' in response

    def should_return_king_lose_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '', scroll)
        # Given no longer king
        test = get_player('Adam')
        test.streak = 0

        #When
        response = handle_king(log, self.messages, subject, test)

        #Then
        assert 'You are no longer worthy to be King' in response

    def should_return_king_win_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '', scroll)
        # Given no longer king
        test = get_player('Adam')
        test.streak = 5

        #When
        response = handle_king(log, self.messages, subject, test)

        #Then
        assert 'Congratulations, Your Highness!' in response

    def should_return_commoner_lose_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '', scroll)
        # Given no longer king
        test = get_player('Hayden')
        test.streak = 0

        #When
        response = handle_commoner(log, self.messages, subject, test)

        #Then
        assert 'Your kingdom must rebuild!' in response

    def should_return_commoner_start_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)
        # Given no longer king
        test = get_player('Hayden')
        test.streak = 1

        #When
        response = handle_commoner(log, self.messages, subject, test)

        #Then
        assert 'Your kingdom must rebuild!' in response

    def should_return_commoner_start_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)
        # Given no longer king
        test = get_player('Hayden')
        test.streak = 1

        #When
        response = handle_commoner(log, self.messages, subject, test)

        #Then
        assert ('So it begins...' in response or
                'One battle conquered, you are well on the way to have a glorious kingdom!' in response)

    def should_return_commoner_coronation_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 4, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)
        # Given no longer king
        test = get_player('Hayden')
        test.streak = 6

        #When
        response = handle_commoner(log, self.messages, subject, test)

        #Then
        assert 'Vive Rex! The WaffleCrown now rests on your head' in response

    def should_return_commoner_win_message(self):
        players = [get_player('Adam'), get_player('Hayden'), get_player('James')]
        scroll = [Record('Adam', 5, '1', 'today'), Record('Hayden', 3, '2', 'today'), Record('James', 2, '3', 'today')]
        subject = Group(self.group_name, players, '1', scroll)
        # Given no longer king
        test = get_player('Hayden')
        test.streak = 4

        #When
        response = handle_commoner(log, self.messages, subject, test)

        #Then
        assert 'Another battlefield conquered, well done' in response


    def should_update_titles(self):
        test = get_player('Adam')
        test.games = 1

        test.score = 5
        assert update_title(test) =='Knight'
        test.score = 4
        assert update_title(test) == 'Master'
        test.score = 3
        assert update_title(test) == 'Freemen'
        test.score = 2
        assert update_title(test) == 'Commoner'
        test.score = 1
        assert update_title(test) == 'Peasant'
