import json
from from_root import from_root
from src.app.model.event.event import Event


def extract_and_validate(file_name, expected_score, expected_streak):
    with open(from_root("resources", "test", "event_samples", file_name)) as event_file:
        event_dict = json.load(event_file)

    event = Event(event_dict)

    actual_score = event.get_score()
    actual_streak = event.get_streak()

    assert expected_score == actual_score
    assert expected_streak == actual_streak


class EventSpec:

    def should_extract_when_waffle_is_only_text_present(self):
        extract_and_validate("event_waffle_score_nothing_else.json", 0, 4)

    def should_extract_when_waffle_is_before_short_text(self):
        extract_and_validate( "event_waffle_score_short_text_after.json", 0, 4)

    def should_extract_when_waffle_is_after_short_text(self):
        extract_and_validate("event_waffle_score_short_text_before.json", 0, 4)

    def should_extract_when_waffle_is_before_long_text(self):
        extract_and_validate("event_waffle_score_long_text_after.json", 3, 6)

    def should_extract_when_waffle_is_after_long_text(self):
        extract_and_validate("event_waffle_score_long_text_before.json", 3, 6)

    def should_extract_when_waffle_is_after_false_flags(self):
        extract_and_validate("event_waffle_score_after_fakes.json", 0, 4)

    def should_extract_when_waffle_is_broken_streak(self):
        extract_and_validate("event_waffle_streak_over.json", 0, 0)

    def should_not_extract_from_invalid_post(self):
        with open(from_root("resources", "test", "event_samples", "event_keyword_match_no_score.json")) as event_file:
            event_dict = json.load(event_file)

        event = Event(event_dict)

        actual_score = event.get_score()
        actual_streak = event.get_streak()

        assert actual_score is None and actual_streak is None
