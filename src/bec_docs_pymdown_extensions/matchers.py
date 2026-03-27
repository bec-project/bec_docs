from abc import ABC, abstractmethod
from difflib import Differ, SequenceMatcher

from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN


class ExpectedOutputMatcher(ABC):
    def __init__(self, expected_output: str) -> None:
        self._expected_output = expected_output
        self._differ = Differ()

    @abstractmethod
    def check(self, output) -> bool: ...

    def diff(self, output) -> str:
        return "\n".join(
            self._differ.compare(
                self._expected_output.replace(PLACEHOLDER_TOKEN, "").splitlines(),
                output.splitlines(),
            )
        )


class ContainsExpectedOutputMatcher(ExpectedOutputMatcher):
    def __init__(self, expected_output: str) -> None:
        super().__init__(expected_output)
        self._differ = Differ()

    def check(self, output):
        return self._expected_output.replace(PLACEHOLDER_TOKEN, "") in output


class SimilarExpectedOutputMatcher(ExpectedOutputMatcher):
    def __init__(self, expected_output: str, ratio: float = 0.9) -> None:
        super().__init__(expected_output)
        self._expected_ratio = ratio

    def check(self, output):
        return SequenceMatcher(None, self._expected_output, output).ratio() >= self._expected_ratio
