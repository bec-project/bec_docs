"""Matchers used by docs snippet tests.

The expected-output marker serves two roles:
1. The snippet preprocessor reads the matcher payload and renders the expected output in the docs.
2. The pytest snippet suite compares the live result against that expected output.

Keep matchers focused on how the output should be validated:
- ``ContainsExpectedOutputMatcher`` for stable substrings
- ``SimilarExpectedOutputMatcher`` for mostly-stable rich/text output with timestamps or spacing drift
- ``SignalArrayOutputMatcher`` for structured numeric arrays with tolerances
"""

import math
import re
from abc import ABC, abstractmethod
from difflib import Differ, SequenceMatcher

from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN


class ExpectedOutputMatcher(ABC):
    """Base class for all docs output matchers.

    ``expected_output`` is both the source of truth rendered into the published docs and
    the reference text used by the pytest snippet suite.
    """

    def __init__(self, expected_output: str, contains_html: bool = False) -> None:
        self._expected_output = expected_output
        self.contains_html = contains_html
        self._differ = Differ()

    def strip_html(self, input: str) -> str:
        if not self.contains_html:
            return input
        # 1. Extract content inside <pre>...</pre>
        match = re.search(r"<pre.*?>(.*?)</pre>", input, flags=re.DOTALL | re.IGNORECASE)
        if not match:
            return ""
        pre_content = match.group(1)
        # 2. Remove all HTML tags inside <pre> (keep text + spacing)
        clean = re.sub(r"<[^>]+>", "", pre_content)
        return clean

    @abstractmethod
    def check(self, output) -> bool: ...

    def _normalized_expected_output(self) -> str:
        return self.strip_html(self._expected_output.replace(PLACEHOLDER_TOKEN, ""))

    def diff(self, output) -> str:
        return "\n".join(
            self._differ.compare(
                self._normalized_expected_output().splitlines(), output.splitlines()
            )
        )


class ContainsExpectedOutputMatcher(ExpectedOutputMatcher):
    """Require the expected text to appear verbatim in the live output."""

    def check(self, output):
        return self._normalized_expected_output() in output


class SimilarExpectedOutputMatcher(ExpectedOutputMatcher):
    """Require the live output to stay close to the documented example.

    Use this for rich/IPython output where timestamps, padding, or small floating point
    differences make exact matching too brittle.
    """

    def __init__(
        self, expected_output: str, ratio: float = 0.9, contains_html: bool = False
    ) -> None:
        super().__init__(expected_output, contains_html=contains_html)
        self._expected_ratio = ratio

    def check(self, output):
        return (
            SequenceMatcher(None, self._normalized_expected_output(), output).ratio()
            >= self._expected_ratio
        )


class SignalArrayOutputMatcher(ExpectedOutputMatcher):
    """Validate scan-history style ``{'timestamp': array(...), 'value': array(...)}`` output.

    Timestamps are intentionally treated structurally rather than literally. The matcher
    checks that:
    - both arrays are present
    - the lengths match the documented example
    - values are close within the configured tolerances
    - timestamps are monotonic, if requested
    """

    def __init__(
        self,
        expected_output: str,
        *,
        value_atol: float = 0.05,
        value_rtol: float = 0.0,
        require_monotonic_timestamps: bool = True,
        contains_html: bool = False,
    ) -> None:
        super().__init__(expected_output, contains_html)
        self._value_atol = value_atol
        self._value_rtol = value_rtol
        self._require_monotonic_timestamps = require_monotonic_timestamps

    @staticmethod
    def _extract_series(text: str, key: str) -> list[float] | None:
        match = re.search(rf"'{key}': array\(\[(.*?)\]\)", text, re.DOTALL)
        if not match:
            return None
        numbers = re.findall(r"[-+]?\d*\.?\d+(?:e[-+]?\d+)?", match.group(1), re.IGNORECASE)
        return [float(number) for number in numbers]

    def check(self, output):
        expected_timestamps = self._extract_series(self._expected_output, "timestamp")
        expected_values = self._extract_series(self._expected_output, "value")
        actual_timestamps = self._extract_series(output, "timestamp")
        actual_values = self._extract_series(output, "value")

        if not all(
            series is not None
            for series in (expected_timestamps, expected_values, actual_timestamps, actual_values)
        ):
            return False

        if len(expected_timestamps) != len(actual_timestamps):
            return False
        if len(expected_values) != len(actual_values):
            return False

        for expected, actual in zip(expected_values, actual_values):
            if not math.isclose(
                expected, actual, rel_tol=self._value_rtol, abs_tol=self._value_atol
            ):
                return False

        if self._require_monotonic_timestamps:
            for earlier, later in zip(actual_timestamps, actual_timestamps[1:]):
                if later < earlier:
                    return False

        return True
