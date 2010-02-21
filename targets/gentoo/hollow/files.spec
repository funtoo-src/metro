[section hollow/files]

make.conf: [
# These settings were set by the metro build script that automatically built this stage.
# Please consult the make.conf(5) man-page for details.

# build-time functionality
USE="$[portage/USE:zap]"

# host and optimization settings
CHOST="$[portage/CHOST:zap]"
CFLAGS="$[portage/CFLAGS:zap]"
CXXFLAGS="$[portage/CXXFLAGS:zap]"
LDFLAGS="$[portage/LDFLAGS:zap]"

# advanced masking
ACCEPT_KEYWORDS="$[portage/ACCEPT_KEYWORDS:zap]"
ACCEPT_LICENSE="*"

# advanced features
EMERGE_DEFAULT_OPTS="--quiet --with-bdeps=y --binpkg-respect-use=y --keep-going --usepkg"
PORTAGE_NICENESS="15"
EBEEP_IGNORE="yes"
FEATURES="buildpkg collision-protect noinfo parallel-fetch preserve-libs sfperms strict unmerge-orphans userpriv usersandbox"

# logging related variables:
PORTAGE_ELOG_SYSTEM="save echo"
PORTAGE_ELOG_CLASSES="warn error info log qa"

# internationalization
LINGUAS="en"
]

locale.gen: [
# /etc/locale.gen: list all of the locales you want to have on your system
#
# The format of each line:
# <locale> <charmap>
#
# Where <locale> is a locale located in /usr/share/i18n/locales/ and
# where <charmap> is a charmap located in /usr/share/i18n/charmaps/.
#
# All blank lines and lines starting with # are ignored.
#
# For the default list of supported combinations, see the file:
# /usr/share/i18n/SUPPORTED
#
# Whenever glibc is emerged, the locales listed here will be automatically
# rebuilt for you.  After updating this file, you can simply run `locale-gen`
# yourself instead of re-emerging glibc.

en_GB.UTF-8 UTF-8
en_US.UTF-8 UTF-8
]

resolv.conf: [
nameserver 8.8.4.4
nameserver 8.8.8.8
]
