#!/usr/bin/env python3
"""Applies this project's changes to the upstream MJ PDF source tree.

Usage: python3 ci/apply_changes.py <path-to-upstream-source>
"""
import re
import sys
from pathlib import Path

APP_ID_SUFFIX = ".translationfix"
VERSION_SUFFIX = "-translation-fix"
APP_NAME = "MJ PDF Fix"


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        sys.exit(f"Expected exactly one match of {old!r} in {path}, found {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"patched {path}")


def main():
    root = Path(sys.argv[1])
    gradle = root / "app" / "build.gradle"

    # 1. Install next to the Google Play version instead of replacing it.
    replace_once(
        gradle,
        "        release {\n            debuggable false\n",
        "        release {\n"
        f"            applicationIdSuffix \"{APP_ID_SUFFIX}\"\n"
        f"            versionNameSuffix \"{VERSION_SUFFIX}\"\n"
        "            debuggable false\n",
    )

    # 2. Lint is a development check; it must not block this personal build.
    replace_once(gradle, "checkReleaseBuilds = true", "checkReleaseBuilds = false")

    # 3. A distinct launcher name so the two installed apps can be told apart.
    strings = root / "app" / "src" / "main" / "res" / "values" / "strings.xml"
    replace_once(
        strings,
        '<string name="mj_app_name" translatable="false">MJ PDF</string>',
        f'<string name="mj_app_name" translatable="false">{APP_NAME}</string>',
    )


if __name__ == "__main__":
    main()
