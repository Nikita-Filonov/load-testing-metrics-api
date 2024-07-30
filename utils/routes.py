from enum import Enum


class APIRoutes(str, Enum):
    METHODS = '/methods'
    SERVICES = '/services'
    RATIO_RESULTS = '/ratio-results'
    METHOD_RESULTS = '/method-results'
    HISTORY_RESULTS = '/history-results'
    LOAD_TEST_RESULTS = '/load-test-results'
    RESULTS_ANALYTICS = '/results-analytics'
    METHODS_ANALYTICS = '/methods-analytics'

    def as_tag(self) -> str:
        return self[1:]
