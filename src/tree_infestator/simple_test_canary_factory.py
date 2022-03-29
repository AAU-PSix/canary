from .c_canary_factory import CCanaryFactory

class SimpleTestCanaryFactory(CCanaryFactory):
    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"

    def create_state_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}TWEET();{postfix}"