from ts import Node
from .c_canary_factory import CCanaryFactory

class SimpleTestCanaryFactory(CCanaryFactory):
    def create_begin_test_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_end_test_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_begin_unit_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_end_unit_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_state_tweet(self, _: Node, prefix: str, postfix: str) -> str:
        return f"{prefix}TWEET();{postfix}"