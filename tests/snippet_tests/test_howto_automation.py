from __future__ import annotations

import pytest
from bec_lib.bl_states import DeviceWithinLimitsStateConfig

from bec_docs_pymdown_extensions.matchers import ContainsExpectedOutputMatcher

# fmt: off
SHOW_ALL_STATES_OUTPUT = """                                Beamline States                                 
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Name           ┃ Type            ┃ Parameters      ┃ Status ┃ Label          ┃
┃                ┃                 ┃                 ┃        ┃                ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ samx_in_limits │ DeviceWithinLi… │ device=samx     │ valid  │ Device samx    │
│                │                 │ low_limit=-10.0 │        │ within limits  │
│                │                 │ high_limit=10.0 │        │                │
│                │                 │ tolerance=0.1   │        │                │
│                │                 │                 │        │                │
└────────────────┴─────────────────┴─────────────────┴────────┴────────────────┘
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SHOW_ALL_STATES_OUTPUT))
def test_show_all_bl_states(bec):
    samx_config = DeviceWithinLimitsStateConfig(name="samx_in_limits", device="samx", low_limit=-10, high_limit=10)  # docs-hide
    bec.beamline_states.add(samx_config) # docs-hide
    bec.beamline_states.show_all()

# fmt: on
