from __future__ import annotations

import re
from pprint import pformat

import pytest

from bec_docs_pymdown_extensions.matchers import ContainsExpectedOutputMatcher
from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN


@pytest.mark.timeout(100)
def test_samx_summary(bec):
    dev.samx.summary()


def _normalize_read_configuration_output(output: str) -> str:
    return re.sub(r"'timestamp': [0-9.]+", "'timestamp': ", output)


READ_CONFIGURATION_OUTPUT = f"""\
{{'samx_velocity': {{'value': 100, 'timestamp': {PLACEHOLDER_TOKEN}}},
 'samx_acceleration': {{'value': 1, 'timestamp': {PLACEHOLDER_TOKEN}}},
 'samx_tolerance': {{'value': 0.01, 'timestamp': {PLACEHOLDER_TOKEN}}}}}
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(READ_CONFIGURATION_OUTPUT))
def test_samx_read_configuration(bec, assert_expected_output):
    dev.samx.read_configuration()
    config = dev.samx.read_configuration()  # docs-hide
    assert_expected_output(  # docs-hide
        _normalize_read_configuration_output(pformat(config, sort_dicts=False))  # docs-hide
    )  # docs-hide


SIGNAL_ATTRIBUTE = """\
Signal(name=velocity, root_device=samx, enabled=True)
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SIGNAL_ATTRIBUTE))
def test_samx_signal_attribute(bec):
    dev.samx.velocity
    print(dev.samx.velocity)  # docs-hide


PROPERTY_ATTRIBUTE = """\
[-50, 50]
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(PROPERTY_ATTRIBUTE))
def test_samx_property_attribute(bec):
    dev.samx.limits
    print(dev.samx.limits)  # docs-hide
