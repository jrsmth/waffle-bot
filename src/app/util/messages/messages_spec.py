from from_root import from_root
from src.app.util.messages.messages import Messages


class MessagesSpec:

    subject = Messages(from_root("resources", "test", "messages.properties"))

    def should_return_message_for_given_key_when_it_exists(self):
        message = self.subject.load("key0")
        assert message == "value0"

    def should_return_empty_string_for_given_key_that_does_not_exist(self):
        message = self.subject.load("key-1")
        assert message == ""
