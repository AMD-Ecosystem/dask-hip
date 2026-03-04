#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import re
import sys
from pathlib import Path

LICENSE_RE = re.compile(r"SPDX-License-Identifier:\s*(.+)")
AMD_COPYRIGHT_RE = re.compile(
    r"SPDX-FileCopyrightText:\s*Copyright \(c\)\s*"
    r"([0-9]{4}|[0-9]{4}[-–][0-9]{4})\s*Advanced Micro Devices, Inc\."
)


def check_file(path: Path) -> list[str]:
    errors = []
    text = path.read_text(errors="ignore")

    # --- SPDX-License-Identifier check ---
    license_matches = LICENSE_RE.findall(text)
    if not license_matches:
        errors.append("Missing SPDX-License-Identifier")
    else:
        # At least one must contain MIT
        if not any("MIT" in lic for lic in license_matches):
            errors.append("SPDX-License-Identifier does not include MIT")

    # --- AMD copyright check ---
    copyright_matches = AMD_COPYRIGHT_RE.findall(text)
    if not copyright_matches:
        errors.append(
            "Missing AMD SPDX-FileCopyrightText "
            "(must match: Copyright (c) <year or range> Advanced Micro Devices, Inc.)"
        )

    return errors


def main():
    status = 0
    for filename in sys.argv[1:]:
        path = Path(filename)
        if not path.is_file():
            continue

        errors = check_file(path)
        if errors:
            status = 1
            print(f"{filename}:")
            for err in errors:
                print(f"  - {err}")

    sys.exit(status)


if __name__ == "__main__":
    main()
