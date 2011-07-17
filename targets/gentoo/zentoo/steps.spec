[collect ./files.spec]

[section steps/zentoo]

setup: [
# the quotes below prevent variable expansion of anything inside make.conf
cat << "EOF" > /etc/make.conf
$[[zentoo/files/make.conf]]
EOF
cat << "EOF" > /etc/resolv.conf
$[[zentoo/files/resolv.conf]]
EOF
]

stage4: [
emerge $eopts mail-mta/postfix || exit 1
emerge $eopts $[zentoo/stage4/packages] || exit 1

rc-update add udev sysinit || exit 2

for i in udev-postmount dcron syslog-ng; do
	rc-update add $i default || exit 2
done
]
