from __future__ import annotations

from pprint import pformat
from time import sleep

import pytest

from bec_docs_pymdown_extensions.matchers import (
    ContainsExpectedOutputMatcher,
    NumberUUIDSimilarOutputMatcher,
    SimilarExpectedOutputMatcher,
)
from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN

# fmt: off
SHOW_ALL_COMMANDS_OUTPUT = """\
              User macros
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃         Name          ┃ Description ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│      macro_test       │             │
│ macro_test_takes_time │             │
└───────────────────────┴─────────────┘
                                     Scans
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃            Name             ┃                  Description                   ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│           acquire           │ A simple acquisition at the current position.  │
│   _close_interactive_scan   │  An interactive scan for one or more motors.   │
│       close_scan_def        │                                                │
│      close_scan_group       │                                                │
│     cont_line_fly_scan      │  A continuous line fly scan. Use this scan if  │
│                             │   you want to move a motor continuously from   │
│                             │         start to stop position whilst          │
│       cont_line_scan        │  A continuous line scan. Use this scan if you  │
│                             │  want to move a motor continuously from start  │
│                             │            to stop position whilst             │
│         device_rpc          │                                                │
│         fermat_scan         │       A scan following Fermat's spiral.        │
│       hexagonal_scan        │  Scan two motors in a hexagonal grid pattern.  │
│ _interactive_read_monitored │  Read the devices that are on readoutPriority  │
│                             │                  "monitored".                  │
│    _interactive_trigger     │ Send a trigger to all enabled devices that are │
│                             │            on softwareTrigger mode.            │
│          line_scan          │      A line scan for one or more motors.       │
│          list_scan          │ A scan following the positions specified in a  │
│                             │                     list.                      │
│        monitor_scan         │ Readout all primary devices at each update of  │
│                             │             the monitored device.              │
│             mv              │     Move device(s) to an absolute position     │
│   _open_interactive_scan    │  An interactive scan for one or more motors.   │
│        open_scan_def        │                                                │
│       round_roi_scan        │   A scan following a round-roi-like pattern.   │
│         round_scan          │  A scan following a round shell-like pattern   │
│                             │ with increasing number of points in each ring. │
│                             │  The scan starts at the inner ring and moves   │
│                             │                   outwards.                    │
│       round_scan_fly        │    A fly scan following a round shell-like     │
│                             │                    pattern.                    │
│          grid_scan          │       Scan two or more motors in a grid.       │
│          time_scan          │     Trigger and readout devices at a fixed     │
│                             │                   interval.                    │
│             umv             │   Move device(s) to an absolute position and   │
│                             │  show live updates. This is a blocking call.   │
│                             │           For non-blocking use Move.           │
│     custom_testing_scan     │      A line scan for one or more motors.       │
│  device_progress_grid_scan  │ A scan that simulates device progress updates. │
└─────────────────────────────┴────────────────────────────────────────────────┘
"""
# fmt: on


@pytest.mark.timeout(100)
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SHOW_ALL_COMMANDS_OUTPUT))
def test_show_all_commands(bec):
    bec.show_all_commands()


LOAD_CONFIG_OUTPUT = f"""\
A recovery config was written to {PLACEHOLDER_TOKEN}\
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(LOAD_CONFIG_OUTPUT))
def test_load_demo_config(bec):
    bec.config.reset_config()  # docs-hide
    sleep(1)  # docs-hide
    bec.config.load_demo_config()


DEV_OUTPUT = """\
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃         ┃         ┃         ┃         ┃         ┃ Device  ┃ Reado… ┃ Device  ┃
┃ Device  ┃ Descri… ┃ Status  ┃ ReadOn… ┃ Softwa… ┃  class  ┃ prior… ┃  tags   ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│  eiger  │         │ enabled │  False  │  True   │ ophyd_… │ async  │ {'dete… │
│ dyn_si… │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │  set()  │
│ pseudo… │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │  set()  │
│ hexapod │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│ eyefoc  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  eyex   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  eyey   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│ flyer_… │         │ disabl… │  False  │  False  │ ophyd_… │ on_re… │ {'flye… │
│  hrox   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  hroy   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  hroz   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│   hx    │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│   hy    │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│   hz    │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  mbsx   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  mbsy   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  pinx   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  piny   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  pinz   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  samx   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  samy   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  samz   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'user  │
│         │         │         │         │         │         │        │ motors… │
│  bpm3a  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3b  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3c  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3d  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3i  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3x  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3y  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm3z  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4a  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4b  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4c  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4d  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4i  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4s  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4x  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ bpm4xf  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ bpm4xm  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4y  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ bpm4yf  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ bpm4ym  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm4z  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5a  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5b  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5c  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5d  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5i  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5x  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5y  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm5z  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6a  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6b  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6c  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6d  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6i  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6x  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6y  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  bpm6z  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  curr   │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  diode  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ ebpmdx  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ ebpmdy  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ ebpmux  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ ebpmuy  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│   ftp   │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  temp   │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ transd  │         │ enabled │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│  aptrx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  aptry  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bim2x  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bim2y  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm1trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm1try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm2trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm2try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm3trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm3try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm4trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm4try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm5trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm5try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm6trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ bm6try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bpm4r  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bpm5r  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bs1x   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bs1y   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bs2x   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  bs2y   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ burstn  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ burstr  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1a  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1b  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1c  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1d  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1e  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1f  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1g  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ddg1h  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ dettrx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ di2trx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ di2try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ dtpush  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  dtth   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  dttrx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  dttry  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  dttrz  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebcsx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebcsy  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebfi1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebfi2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebfi3  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebfi4  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ ebfzpx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ ebfzpy  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebtrx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebtry  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  ebtrz  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fi1try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fi2try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fi3try  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  fsh1x  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  fsh2x  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ ftrans  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fttrx1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fttrx2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fttry1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ fttry2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  fttrz  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  idgap  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mibd   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mibd1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mibd2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ miroll  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mith   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mitrx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mitry  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mitry1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mitry2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mitry3  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mobd   │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mobdai  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mobdbo  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mobdco  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mobddi  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  mokev  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mopush1 │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ mopush2 │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ moroll1 │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ moroll2 │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  moth1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ moth1e  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  moth2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ moth2e  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ motrx2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  motry  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ motry2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ motrz1  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ motrz1e │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ moyaw2  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl0ch  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl0trxi │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl0trxo │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl0wh  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl1ch  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl1cv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl1trxi │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl1trxo │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl1tryb │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl1tryt │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl1wh  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl1wv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl2ch  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl2cv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl2trxi │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl2trxo │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl2tryb │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl2tryt │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl2wh  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl2wv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl3ch  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl3cv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl3trxi │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl3trxo │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl3tryb │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl3tryt │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl3wh  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl3wv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl4ch  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl4cv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl4trxi │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl4trxo │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl4tryb │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl4tryt │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl4wh  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl4wv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl5ch  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl5cv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl5trxi │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl5trxo │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl5tryb │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ sl5tryt │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl5wh  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sl5wv  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  strox  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  stroy  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  stroz  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sttrx  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│  sttry  │         │ enabled │  False  │  False  │ ophyd_… │ basel… │ {'beam… │
│ ring_c… │         │ disabl… │  False  │  False  │ ophyd_… │ monit… │ {'beam… │
│ monito… │         │ disabl… │  False  │  True   │ ophyd_… │ async  │ {'beam… │
│ rt_con… │         │ disabl… │  False  │  False  │ ophyd_… │ basel… │ {'test  │
│         │         │         │         │         │         │        │ device… │
│         │         │         │         │         │         │        │  'user  │
│         │         │         │         │         │         │        │ motors… │
│ wavefo… │         │ disabl… │  False  │  True   │ ophyd_… │ async  │ {'dete… │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴────────┴─────────┘
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(SimilarExpectedOutputMatcher(DEV_OUTPUT))
def test_show_all_devices(bec):
    dev.show_all()


INSPECT_OUTPUT = """\
<style>
.r1 {font-style: italic}
.r2 {color: #008080; text-decoration-color: #008080}
.r3 {color: #c0c0c0; text-decoration-color: #c0c0c0}
.r4 {font-weight: bold}
.r5 {color: #808000; text-decoration-color: #808000}
.r6 {color: #7f7f7f; text-decoration-color: #7f7f7f}
.r7 {color: #008000; text-decoration-color: #008000}
</style>
<pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><code style="font-family:inherit"><span class="r1">              SimPositioner: samx              </span>
<span class="r2"> Enabled          </span><span class="r3"> True                        </span>
<span class="r2"> Description      </span><span class="r3">                             </span>
<span class="r2"> Read only        </span><span class="r3"> False                       </span>
<span class="r2"> Software Trigger </span><span class="r3"> False                       </span>
<span class="r2"> Device class     </span><span class="r3"> ophyd_devices.SimPositioner </span>
<span class="r2"> Readout Priority </span><span class="r3"> baseline                    </span>
<span class="r2"> Device tags      </span><span class="r3"> user motors                 </span>
<span class="r2"> Limits           </span><span class="r3"> [-50, 50]                   </span>

<span class="r1">                       Current Values                        </span>
<span class="r4"> Signal                Value             Timestamp           </span>
<span class="r2"> samx                 </span><span class="r5"> 9.99789260545663 </span><span class="r6"> 2026-04-01 14:43:52 </span>
<span class="r2"> samx_setpoint        </span><span class="r5"> 10.0             </span><span class="r6"> 2026-04-01 14:43:52 </span>
<span class="r2"> samx_motor_is_moving </span><span class="r5"> 0                </span><span class="r6"> 2026-04-01 14:43:52 </span>

<span class="r1">  Config Signals  </span>
<span class="r4"> Signal     Value </span>
<span class="r2"> tolerance </span><span class="r7"> 0.01  </span>
</code></pre>
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(
    SimilarExpectedOutputMatcher(INSPECT_OUTPUT, ratio=0.7, contains_html=True)
)
def test_inspect_samx(bec, render_ipython_pretty, assert_expected_output):
    dev.samx
    rendered = render_ipython_pretty(dev.samx)  # docs-hide
    assert_expected_output(rendered)  # docs-hide


READ_OUTPUT = """\
{'samx': {'value': 0, 'timestamp': 1774874622.037339},
 'samx_setpoint': {'value': 0, 'timestamp': 1774873374.7518551},
 'samx_motor_is_moving': {'value': 0, 'timestamp': 1774873374.751864}}
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(SimilarExpectedOutputMatcher(READ_OUTPUT, ratio=0.75))
def test_samx_read(bec, assert_expected_output):
    dev.samx.read()
    readback = dev.samx.read()  # docs-hide
    assert_expected_output(pformat(readback, sort_dicts=False))  # docs-hide


WM_OUTPUT = """\
┏━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃      ┃ readback ┃ setpoint ┃  limits   ┃
┡━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│ samx │  0.0000  │  0.0000  │ [-50, 50] │
└──────┴──────────┴──────────┴───────────┘
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(WM_OUTPUT))
def test_samx_wm(bec):
    dev.samx.wm


WM_MOVE_OUTPUT = """\
PASSED [100%] samx:      0.00 ━━━━━━━━━━━━━━━       9.99 /      10.00 / 100 % 0:00:00 0:00:00
┏━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃      ┃ readback ┃ setpoint ┃  limits   ┃
┡━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│ samx │ 10.0000  │ 10.0000  │ [-50, 50] │
└──────┴──────────┴──────────┴───────────┘
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("fd")
@pytest.mark.expected_output(NumberUUIDSimilarOutputMatcher(WM_MOVE_OUTPUT, ratio=0.7))
def test_samx_blocking_move(bec):
    scans.umv(dev.samx, 10, relative=False)  # make the move
    dev.samx.wm  # check the move is done


SCAN_OUTPUT = """\
Starting scan 4.
+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
|seq. num|  samx  |  bpm4a |  bpm5x | ebpmdy |  temp  | ebpmux |  bpm4c |  bpm6a | bpm4ym | bpm4xf |
+========+========+========+========+========+========+========+========+========+========+========+
|    1   |-1.006  | 108.000| 98.000 | 106.000| 110.000| 106.000| 107.000| 108.000| 97.000 | 101.000|
|    2   |-0.505  | 104.000| 110.000| 95.000 | 107.000| 109.000| 93.000 | 109.000| 103.000| 93.000 |
|    3   |-0.007  | 110.000| 107.000| 97.000 | 102.000| 94.000 | 92.000 | 90.000 | 92.000 | 95.000 |
|    4   |  0.496 | 106.000| 108.000| 102.000| 108.000| 90.000 | 101.000| 98.000 | 93.000 | 91.000 |
|    5   |  1.001 | 98.000 | 90.000 | 106.000| 98.000 | 90.000 | 104.000| 93.000 | 94.000 | 92.000 |
+========+========+========+========+========+========+========+========+========+========+========+
|  Scan 4 finished. Scan ID 63ea523a-0882-48d4-bd73-db3c3197bd55. Elapsed time: 0.83 s             |
+========+========+========+========+========+========+========+========+========+========+========+
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("fd")
@pytest.mark.expected_output(NumberUUIDSimilarOutputMatcher(SCAN_OUTPUT, ratio=0.6))
def test_samx_line_scan(bec):
    scans.line_scan(dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False)


AVAILABLE_WIDGETS_OUTPUT = """\
                                                Available widgets for BEC CLI usage
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Widget Name           ┃ Description                                                                                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ BECMainWindow         │ No description available                                                                              │
│ BECProgressBar        │ A custom progress bar with smooth transitions. The displayed text can be customized using a template. │
│ BECQueue              │ Widget to display the BEC queue.                                                                      │
│ BECShell              │ A WebConsole pre-configured to run the BEC shell.                                                     │
│ BECStatusBox          │ An autonomous widget to display the status of BEC services.                                           │
│ DapComboBox           │ The DAPComboBox widget is an extension to the QComboBox with all avaialble DAP model from BEC.        │
│ DeviceBrowser         │ DeviceBrowser is a widget that displays all available devices in the current BEC session.             │
│ Heatmap               │ Heatmap widget for visualizing 2d grid data with color mapping for the z-axis.                        │
│ Image                 │ Image widget for displaying 2D data.                                                                  │
│ LogPanel              │ Displays a log panel                                                                                  │
│ Minesweeper           │ No description available                                                                              │
│ MonacoWidget          │ A simple Monaco editor widget                                                                         │
│ MotorMap              │ Motor map widget for plotting motor positions in 2D including a trace of the last points.             │
│ MultiWaveform         │ MultiWaveform widget for displaying multiple waveforms emitted by a single signal.                    │
│ PdfViewerWidget       │ A widget to display PDF documents with toolbar controls.                                              │
│ PositionIndicator     │ Display a position within a defined range, e.g. motor limits.                                         │
│ PositionerBox         │ Simple Widget to control a positioner in box form                                                     │
│ PositionerBox2D       │ Simple Widget to control two positioners in box form                                                  │
│ PositionerControlLine │ A widget that controls a single device.                                                               │
│ PositionerGroup       │ Simple Widget to control a positioner in box form                                                     │
│ ResumeButton          │ A button that continue scan queue.                                                                    │
│ RingProgressBar       │ No description available                                                                              │
│ SBBMonitor            │ A widget to display the SBB monitor website.                                                          │
│ ScanControl           │ Widget to submit new scans to the queue.                                                              │
│ ScanProgressBar       │ Widget to display a progress bar that is hooked up to the scan progress of a scan.                    │
│ ScatterWaveform       │ No description available                                                                              │
│ SignalLabel           │ No description available                                                                              │
│ TextBox               │ A widget that displays text in plain and HTML format                                                  │
│ Waveform              │ Widget for plotting waveforms.                                                                        │
│ WebConsole            │ A simple widget to display a website                                                                  │
│ WebsiteWidget         │ A simple widget to display a website                                                                  │
└───────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(SimilarExpectedOutputMatcher(AVAILABLE_WIDGETS_OUTPUT, ratio=0.6))
def test_available_widgets(gui):
    gui.available_widgets
    print(gui.available_widgets)  # docs-hide
    sleep(2)  # docs-hide
