[section zentoo/files]

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
PORTAGE_NICENESS="15"
EBEEP_IGNORE="yes"
FEATURES="collision-protect noinfo parallel-fetch preserve-libs sfperms strict unmerge-orphans userpriv usersandbox"

# logging related variables:
PORTAGE_ELOG_SYSTEM="save echo"
PORTAGE_ELOG_CLASSES="warn error info log qa"

# internationalization
LINGUAS="en"
]

resolv.conf: [
nameserver 8.8.4.4
nameserver 8.8.8.8
]
