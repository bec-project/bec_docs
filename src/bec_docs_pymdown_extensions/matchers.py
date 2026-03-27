from abc import ABC, abstractmethod

from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN


class ExpectedOutputMatcher(ABC):
    def __init__(self, expected_output: str) -> None:
        self._expected_output = expected_output

    @abstractmethod
    def check(self, output) -> bool: ...


class ContainsExpectedOutputMatcher(ExpectedOutputMatcher):
    def check(self, output):
        return self._expected_output.replace(PLACEHOLDER_TOKEN, "") in output
