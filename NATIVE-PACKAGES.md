# SRCERY Plasma 1.1.0 native KDE packages

The Global Theme is an ordinary Plasma/LookAndFeel KPackage. It contains the
complete color roles, previews and animated logo splash. Its two KNewStuff
dependencies install the matching Plasma Style and wallpaper using KDE's own
package installers. No shell commands, Python installer, layout script or
privileged actions are run by this package.

## From System Settings

Open Colors & Themes / Global Theme / Get New, search for SRCERY Plasma, and
click Install. Close the download dialog, select SRCERY and Apply. Selecting
the wallpaper option applies the grey Srcery logo wallpaper. Panels and widgets
are not replaced because this package has no desktop layout.

## Typography and icons

The theme selects Iosevka. Install that font once through Font Management if
it is not already available. A global-theme KNewStuff dependency only extracts
font files into its download folder; unlike Font Management it does not register
that folder with Fontconfig. We therefore do not advertise such a dependency as
automatic font installation. Until Iosevka is installed, Qt uses its font fallback.
The original manual suite is still available for installing Iosevka, Konsole
profiles, and optional Tela Circle custom gold icons together.

Native packages use the distribution's Breeze widgets, decoration, cursors and
Breeze Dark icons. Tela Circle is optional and remains separately licensed.
GTK/Flatpak application overrides, login manager and Steam videos are outside
the native global-theme package.

## Rebuild

Run `python3 build-native.py --output /path/to/output --style-id STORE_ID
--wallpaper-id STORE_ID`. The output contains three tar.gz archives and SHA256
checksums. Each archive has one ordinary package root, no symlinks and no custom
installation executable. The existing manual installer remains unchanged.
