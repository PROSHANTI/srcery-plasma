# SRCERY Plasma

Unofficial community adaptation by **SHANTI** for KDE Plasma 6.

![SRCERY preview](theme/contents/previews/preview.png)

Charcoal backgrounds, parchment text, gold highlights and the official Srcery
logo. **Version 1.2.0 is one self-contained Global Theme package.**

## Install with KDE

Open **System Settings → Colors & Themes → Global Theme → Get New**, search for
**SRCERY Plasma**, and click Install or Update. Close the download dialog,
select SRCERY, and Apply.

[KDE Store](https://store.kde.org/p/2380677/) ·
[Latest GitHub release](https://github.com/PROSHANTI/srcery-plasma/releases/latest)

The package contains the color scheme, previews, animated Plasma splash and
grey logo wallpaper. It uses the Breeze components included with KDE and
downloads no companion themes. No terminal commands, separate installer,
layout replacement or administrator privileges are required.

Your chosen icons, wallpaper/slideshow, panels and widgets are preserved.
The embedded wallpaper is available as the theme's native default asset; KDE
keeps the current desktop wallpaper when applying appearance settings only.
Iosevka is requested if already available; otherwise Qt selects an available
font fallback automatically. The theme does not install fonts or external
icon sets. Applications with independent GTK/Flatpak styling may retain their
own appearance. The splash is for entering the Plasma desktop.

## Upgrades

1.2.0 updates directly from the original manual 1.0.0 suite and the 1.1.0 native
release. It no longer attempts to update their separate Plasma Style packages,
so the missing package-type metadata in the old style cannot block installation.
The old style files are left intact; the current theme selects built-in Breeze.
Historical releases and sources remain in Git history.

## Source and verification

`theme/` is the complete installable KPackage. `build.py` creates a reproducible
archive and SHA256 checksum for release maintainers:

    python3 build.py --output dist

The regression script in `tests/` runs in temporary home directories and separate
D-Bus sessions. It checks clean installation, nonstandard XDG paths, updates from
1.0.0 and 1.1.0, recovery after an interrupted update, actual Plasma component
colors, embedded wallpaper resolution, and preservation of icon selection,
slideshows and panels.

## Credits

Theme adaptation by SHANTI, MIT. Official logo by Daniel Berg and srcery-colors
contributors, CC BY 4.0, with unchanged geometry and colors:
https://github.com/srcery-colors/srcery-assets . Breeze is provided by KDE.
See `NOTICE`, `theme/LICENSE`, and `theme/LICENSES`. No affiliation or endorsement
by KDE or the Srcery project is claimed.
