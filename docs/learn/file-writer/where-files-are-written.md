---
related:
  - title: File writing
    url: learn/file-writer/introduction.md
---

# Where Files Are Written

In BEC itself, the actual write location is determined from the server-side service configuration, in particular `file_writer.base_path`.

On PSI deployments, the server reads this from `deployment_configs/server.yaml`, for example:

```yaml
redis:
  host: x99sa-bec-001.psi.ch
  port: 6379
file_writer:
  base_path: /sls/x99sa/data/$account/raw
log_writer:
  base_path: /var/log/bec
```

This server-side config is written automatically during deployment. The file writer then uses `file_writer.base_path` as the fixed starting point for all scan files.

!!! tip
    Changes to the beamline-wide base path are deployment changes. If your beamline needs a different top-level layout, contact the BEC support team.

## Account-dependent base paths

- If the configured path contains `$account`, BEC substitutes the currently active account into the path.
- If the configured path does not contain `$account`, but an account is active, BEC appends the account name as an extra subdirectory.
- If no account is active, BEC uses the base path as-is.

With a configuration such as:

```yaml
file_writer:
  base_path: /sls/x99sa/data/$account/raw
```

and an active account `p12345`, the effective write base path becomes:

```text
/sls/x99sa/data/p12345/raw
```

## Default Directory Structure

Below that base path, BEC creates scan-number based directories. In the default layout, scan `1234` is placed under:

```text
S01000-01999/S01234
```

and the file base name starts with:

```text
S01234
```

So a typical master file path looks like:

```text
/sls/x99sa/data/p12345/raw/S01000-01999/S01234/S01234_master.h5
```

The scan directory can also contain additional files written during the same scan, for example detector data files from large detectors such as:

```text
S01234_eiger.h5
```

The master file is usually the main entry point and can link to these additional files.

## Modifying the Structure

Scans can modify parts of the file layout through additional scan arguments.

### The `file_suffix` scan argument

Scans can provide a `file_suffix` argument, for example:

```py
scans.line_scan(..., file_suffix="sampleA")
```

If BEC uses the default scan-bundle structure, it adds this suffix to the scan directory name, for example:

```text
S01000-01999/S01234_sampleA
```

The same suffix is also appended to filenames that BEC generates for the scan. For example, the master file becomes:

```text
/sls/x99sa/data/p12345/raw/S01000-01999/S01234_sampleA/S01234_master_sampleA.h5
```

Additional files created during the same scan can use the same suffix as well. For example, a detector file may be written as:

```text
/sls/x99sa/data/p12345/raw/S01000-01999/S01234_sampleA/S01234_eiger_sampleA.h5
```

### The `file_directory` scan argument

Scans can also provide a `file_directory` argument. This does not replace the configured base path. Instead, it defines the relative directory below the fixed server-side base path.

For example, if a scan is started with:

```py
scans.line_scan(..., file_directory="test_run")
```

then BEC writes below:

```text
/sls/x99sa/data/p12345/raw/test_run
```

and the file base name still follows the normal scan-number naming, for example:

```text
/sls/x99sa/data/p12345/raw/test_run/S01234_master.h5
```

If `file_directory` is not provided, BEC falls back to the default scan-bundle directory structure such as `S01000-01999/S01234`.

## Why users cannot escape the base path

Users cannot escape this base path from the client side.

- The server already fixes the write root through `file_writer.base_path`.
- User-provided `file_directory` values are validated and normalized before the final path is constructed.
- BEC checks that the resolved file path stays inside the configured base path.

This prevents one user from writing into another user's directory.

