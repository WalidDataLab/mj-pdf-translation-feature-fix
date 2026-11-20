# mj-pdf-translation-feature-fix

A personal build of **[MJ PDF](https://gitlab.com/mudlej_android/mj_pdf_reader)**, the open-source Android PDF reader by **Mudlej**. It solves one daily annoyance: having to pick a translation app every time you translate selected text.

## The problem

In MJ PDF 3.1.0 (the Google Play version), tapping **Translate** on selected text opens a list of every translation app on the phone, **every single time**. There is no way to set a default app, so reading a document in a foreign language means one extra tap for every translation.

## Investigation

1. **Read the upstream source.** The newer code on the `main` branch already contains the fix:
   - a **Settings → Translation → Translation app** option to pick one app, or keep *Ask every time*;
   - an **Always use this app** checkbox in the picker dialog;
   - a fallback: if the saved app is uninstalled, the app asks again instead of failing.
2. **Checked the release.** The feature is not in the 3.1.0 changelog and the Play version does not show it. It exists in the source but has not been released yet.
3. **Conclusion.** Nothing needed rewriting. The fastest fix was to **build the current source myself** and install it today.

## What this project does

The repository does not copy the app's source. It holds a small, reproducible build pipeline:

| File | Role |
| --- | --- |
| `.github/workflows/build.yml` | GitHub Actions pipeline: downloads the upstream source, builds the native libraries and the APK, signs it, and publishes it as a release |
| `ci/apply_changes.py` | The changes applied on top of upstream, each one checked to match exactly once so an upstream change fails loudly instead of silently |
| `ci/release.p12` | Signing key, created by the first build and reused so every new build can update the previous one |

### Changes applied to upstream

1. **Installs next to the Play version.** The package ID gets the suffix `.translationfix`, so the Google Play app, its library and its history stay untouched.
2. **Separate name.** The launcher label is **MJ PDF Fix**, so the two icons can be told apart.
3. **Lint does not block the build.** Release lint is a development check and is turned off for this personal build.

### Build pipeline

1. Free disk space on the runner (the PDFium checkout is large).
2. Download the upstream source from GitLab.
3. Apply `ci/apply_changes.py`.
4. Install the pinned Android SDK parts: platform 36, build tools 36.0.0, NDK 28.2, CMake 3.22.1.
5. Build **PDFium from source with MJ PDF's Arabic text patches** for `arm64-v8a`, cached between runs. The first build takes about an hour; later builds take a few minutes.
6. Build the release APK with R8 minification.
7. Sign it with `apksigner` and publish it as a GitHub release.
8. If a step fails, save the last 400 log lines to `logs/last-failure.log` so the failure can be diagnosed without opening the Actions UI.

## Install

1. Open **Releases** in this repository and download `MJ-PDF-Fix.apk` on the phone.
2. Install it. Allow installing from your browser or file manager if Android asks.
3. In **MJ PDF Fix**, go to **Settings → Translation**, set *Translate with* to **Installed apps**, then set **Translation app** to your translator.
4. Optional: in the Play version, make a **Backup** from its settings, then restore it in MJ PDF Fix to bring your library and bookmarks over.

The APK targets 64-bit ARM phones (almost every phone from the last few years), on Android 6.0 or newer.

## Skills shown

Reading an unfamiliar Kotlin/Android codebase, release and version analysis, CI/CD with GitHub Actions, native NDK builds, APK signing, and reproducible builds based on patches.

## License and credit

MJ PDF is © Mudlej and contributors, licensed under **GPLv3**. This project only automates building it, with the small changes listed above, and is distributed under the same license. All credit for the app goes to the original author: https://mudlej.com/projects/mj-pdf
