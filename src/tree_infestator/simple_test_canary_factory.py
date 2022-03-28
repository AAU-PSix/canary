from .canary_factory import CanaryFactory

class SimpleTestCanaryFactory(CanaryFactory):
    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_state_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"