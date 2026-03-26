from __future__ import annotations

from pprint import pformat
import re
from time import sleep

import pytest

from bec_docs_pymdown_extensions.matchers import (
    ContainsExpectedOutputMatcher,
    SignalArrayOutputMatcher,
    SimilarExpectedOutputMatcher,
)
from bec_docs_pymdown_extensions.snippet_preprocessor import PLACEHOLDER_TOKEN

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
    bec.config.load_demo_config()


DEV_OUTPUT = """\
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃         ┃         ┃         ┃         ┃         ┃ Device  ┃ Readout ┃ Device ┃
┃ Device  ┃ Descri… ┃ Status  ┃ ReadOn… ┃ Softwa… ┃  class  ┃ priori… ┃  tags  ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│  eiger  │         │ enabled │  False  │  True   │ ophyd_… │  async  │ {'det… │
│ dyn_si… │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ set()  │
│ pseudo… │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ set()  │
│ hexapod │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│ eyefoc  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  eyex   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  eyey   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│ flyer_… │         │ enabled │  False  │  False  │ ophyd_… │ on_req… │ {'fly… │
│  hrox   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  hroy   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  hroz   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│   hx    │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│   hy    │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│   hz    │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  mbsx   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  mbsy   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  pinx   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  piny   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  pinz   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  samx   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  samy   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  samz   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│  bpm3a  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3b  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3c  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3d  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3i  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3x  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3y  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm3z  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4a  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4b  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4c  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4d  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4i  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4s  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4x  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ bpm4xf  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ bpm4xm  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4y  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ bpm4yf  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ bpm4ym  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm4z  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5a  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5b  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5c  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5d  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5i  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5x  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5y  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm5z  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6a  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6b  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6c  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6d  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6i  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6x  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6y  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  bpm6z  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  curr   │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  diode  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ ebpmdx  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ ebpmdy  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ ebpmux  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ ebpmuy  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│   ftp   │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  temp   │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ transd  │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│  aptrx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  aptry  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bim2x  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bim2y  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm1trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm1try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm2trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm2try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm3trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm3try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm4trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm4try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm5trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm5try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm6trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ bm6try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bpm4r  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bpm5r  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bs1x   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bs1y   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bs2x   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  bs2y   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ burstn  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ burstr  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1a  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1b  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1c  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1d  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1e  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1f  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1g  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ddg1h  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ dettrx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ di2trx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ di2try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ dtpush  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  dtth   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  dttrx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  dttry  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  dttrz  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebcsx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebcsy  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebfi1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebfi2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebfi3  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebfi4  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ ebfzpx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ ebfzpy  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebtrx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebtry  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  ebtrz  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fi1try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fi2try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fi3try  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  fsh1x  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  fsh2x  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ ftrans  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fttrx1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fttrx2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fttry1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ fttry2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  fttrz  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  idgap  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mibd   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mibd1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mibd2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ miroll  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mith   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mitrx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mitry  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mitry1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mitry2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mitry3  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mobd   │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mobdai  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mobdbo  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mobdco  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mobddi  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  mokev  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mopush1 │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ mopush2 │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ moroll1 │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ moroll2 │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  moth1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ moth1e  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  moth2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ moth2e  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ motrx2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  motry  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ motry2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ motrz1  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ motrz1e │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ moyaw2  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl0ch  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl0trxi │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl0trxo │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl0wh  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl1ch  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl1cv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl1trxi │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl1trxo │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl1tryb │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl1tryt │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl1wh  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl1wv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl2ch  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl2cv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl2trxi │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl2trxo │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl2tryb │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl2tryt │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl2wh  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl2wv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl3ch  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl3cv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl3trxi │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl3trxo │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl3tryb │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl3tryt │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl3wh  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl3wv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl4ch  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl4cv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl4trxi │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl4trxo │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl4tryb │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl4tryt │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl4wh  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl4wv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl5ch  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl5cv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl5trxi │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl5trxo │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl5tryb │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ sl5tryt │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl5wh  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sl5wv  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  strox  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  stroy  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  stroz  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sttrx  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│  sttry  │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'bea… │
│ ring_c… │         │ enabled │  False  │  False  │ ophyd_… │ monito… │ {'bea… │
│ monito… │         │ enabled │  False  │  True   │ ophyd_… │  async  │ {'bea… │
│ rt_con… │         │ enabled │  False  │  False  │ ophyd_… │ baseli… │ {'user │
│         │         │         │         │         │         │         │ motor… │
│         │         │         │         │         │         │         │ 'test  │
│         │         │         │         │         │         │         │ devic… │
│ wavefo… │         │ enabled │  False  │  True   │ ophyd_… │  async  │ {'det… │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴────────┘
"""


@pytest.mark.timeout(100)
@pytest.mark.expected_output(SimilarExpectedOutputMatcher(DEV_OUTPUT))
def test_show_all_devices(bec):
    dev.show_all()


INSPECT_OUTPUT = """\
              SimPositioner: samx
 Enabled           True
 Description
 Read only         False
 Software Trigger  False
 Device class      ophyd_devices.SimPositioner
 Readout Priority  baseline
 Device tags       user motors
 Limits            [-50, 50]

                  Current Values
 Signal                Value  Timestamp
 samx                  0      2026-03-30 13:35:46
 samx_setpoint         0      2026-03-30 13:35:46
 samx_motor_is_moving  0      2026-03-30 13:35:46

  Config Signals
 Signal     Value
 tolerance  0.01
 """


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(SimilarExpectedOutputMatcher(INSPECT_OUTPUT, ratio=0.6))
def test_inspect_samx(bec, render_ipython_pretty, assert_expected_output):
    dev.samx
    # ``dev.samx`` is displayed through IPython pretty-printing, not normal stdout capture.
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
    # ``read()`` is documented as a formatted dict; validate that representation explicitly.
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
@pytest.mark.expected_output(SimilarExpectedOutputMatcher(WM_MOVE_OUTPUT, ratio=0.7))
def test_samx_blocking_move(bec):
    scans.umv(dev.samx, 10, relative=False)  # make the move
    dev.samx.wm  # check the move is done


def _wait_for_scan_in_history(bec, scan_report, timeout_s: float = 7.0):
    """Wait until the specific scan appears in history and return it."""
    for _ in range(int(timeout_s / 0.1)):
        latest = bec.history.get_by_scan_id(scan_report.scan.scan_id)
        if latest is not None:
            return latest
        sleep(0.1)
    raise AssertionError("Timed out waiting for the scan to appear in bec.history")


def _normalize_scan_container_summary(output: str) -> str:
    """Strip runtime-specific values from ScanDataContainer summary output."""
    replacements = (
        (r"(\n \tStart time: ).*", r"\1"),
        (r"(\n\tEnd time: ).*", r"\1"),
        (r"(\n\tElapsed time: ).*( s)", r"\1\2"),
        (r"(\n\tScan ID: ).*", r"\1"),
        (r"(\n\tScan number: ).*", r"\1"),
        (r"(\n\tFile: ).*", r"\1"),
    )
    normalized = output
    for pattern, replacement in replacements:
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


SCAN_HISTORY_SIGNAL_OUTPUT = """\
{'timestamp': array([1.77496343e+09, 1.77496343e+09, 1.77496343e+09, 1.77496344e+09,
        1.77496344e+09]),
 'value': array([-0.99140924, -0.49119309, -0.00282538,  0.49814051,  0.99329906])}
"""


SCAN_HISTORY_CONTAINER_OUTPUT = f"""\
ScanDataContainer:
 \tStart time: {PLACEHOLDER_TOKEN}
\tEnd time: {PLACEHOLDER_TOKEN}
\tElapsed time: {PLACEHOLDER_TOKEN} s
\tScan ID: {PLACEHOLDER_TOKEN}
\tScan number: {PLACEHOLDER_TOKEN}
\tScan name: line_scan
\tStatus: closed
\tNumber of points (monitored): 5
\tFile: {PLACEHOLDER_TOKEN}
"""


@pytest.mark.timeout(100)
@pytest.mark.output_capture("manual")
@pytest.mark.expected_output(ContainsExpectedOutputMatcher(SCAN_HISTORY_CONTAINER_OUTPUT))
def test_scan_history_container_summary(bec, assert_expected_output):
    scan_report = scans.line_scan(  # docs-hide
        dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False  # docs-hide
    )  # docs-hide
    scan_report.wait(num_points=True, file_written=True)  # docs-hide
    _wait_for_scan_in_history(bec, scan_report)  # docs-hide
    latest = bec.history[-1]
    print(latest)  # docs-display
    assert_expected_output(_normalize_scan_container_summary(repr(latest)))  # docs-hide


@pytest.mark.timeout(100)
@pytest.mark.output_capture("fd")
@pytest.mark.expected_output(
    SignalArrayOutputMatcher(SCAN_HISTORY_SIGNAL_OUTPUT, value_atol=0.05, value_rtol=0.01)
)
def test_scan_history_signal_arrays(bec):
    scan_report = scans.line_scan(  # docs-hide
        dev.samx, -1, 1, steps=5, exp_time=0.1, relative=False  # docs-hide
    )  # docs-hide
    scan_report.wait(num_points=True, file_written=True)  # docs-hide
    latest = _wait_for_scan_in_history(bec, scan_report)  # docs-hide
    print(latest.devices.samx.samx.read())  # docs-display
