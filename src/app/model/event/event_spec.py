import json
from from_root import from_root
from src.app.model.event.event import Event


class EventSpec:

    def should_extract_when_waffle_is_only_text_present(self):
        with open(from_root("resources", "test", "event_samples", "event_waffle_score_nothing_else.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert 0 == actual_score
        assert 4 == actual_streak

    def should_extract_when_waffle_is_before_short_text(self):
        with open(from_root("resources", "test", "event_samples", "event_waffle_score_short_text_after.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert 0 == actual_score
        assert 4 == actual_streak

    def should_extract_when_waffle_is_after_short_text(self):
        with open(from_root("resources", "test", "event_samples", "event_waffle_score_short_text_before.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert 0 == actual_score
        assert 4 == actual_streak

    def should_extract_when_waffle_is_before_long_text(self):
        with open(from_root("resources", "test", "event_samples", "event_waffle_score_long_text_after.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert 3 == actual_score
        assert 6 == actual_streak

    def should_extract_when_waffle_is_after_long_text(self):
        with open(from_root("resources", "test", "event_samples", "event_waffle_score_long_text_before.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert 3 == actual_score
        assert 6 == actual_streak

    def should_extract_when_waffle_is_after_false_flags(self):
        with open(from_root("resources", "test", "event_samples", "event_waffle_score_after_fakes.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert 0 == actual_score
        assert 4 == actual_streak

    def should_not_extract_from_invalid_post(self):
        with open(from_root("resources", "test", "event_samples", "event_keyword_match_no_score.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert actual_score is None and actual_streak is None
