---
related:
  - title: File writing
    url: learn/file-writer/index.md
  - title: DefaultFormat and the default HDF5 layout
    url: learn/file-writer/default-format.md
  - title: BEC Signals
    url: learn/devices/bec-signals.md
---

# Async and Sync File Writing

BEC file writing has two complementary responsibilities:

- write asynchronous device data continuously during the scan
- write the final master file after the scan from data collected in scan storage

Both are important in beamline operation. High-throughput data cannot always be buffered safely until the end of a scan, and delaying all writes until completion would increase memory pressure and delay finishing the scan.

We will refer to the two different operation modes of the file writer service as "sync writing" and "async writing". The former refers to the final master file write that happens after the scan completes, while the latter refers to the continuous writing of async device data during the scan.

## Sync writing

The main master file is written by the normal file-writer path after the scan completes.

Synchronous data is collected continuously during the scan and bundled in scan storage. In a step scan, this includes readings from all normal and hinted signals of monitored devices. Typical examples are BPMs and temperature sensors on scanning motors. These readings are triggered by BEC.

## Async writing

At the same time, asynchronous data flows are also collected. Devices that produce asynchronous data are usually more complex and push data to BEC at their own pace. Examples include NIDAQ, PandaBox, Falcon detectors, and multi-channel scaler cards.

The amount of async data can differ significantly from sync data and can vary strongly between devices. For this reason, BEC treats asynchronous data separately and writes it continuously during the scan. This design allows BEC to handle high data volumes robustly.

The async writer supports multiple async update modes to accommodate different device behaviors and data patterns:

- `add`
- `add_slice`
- `replace`
