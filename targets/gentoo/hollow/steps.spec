[collect ./files.spec]

[section steps/hollow]

setup: [
# the quotes below prevent variable expansion of anything inside make.conf
cat << "EOF" > /etc/make.conf
$[[hollow/files/make.conf]]
EOF
cat << "EOF" > /etc/resolv.conf
$[[hollow/files/resolv.conf]]
EOF
]

stage4: [
emerge $eopts mail-mta/postfix || exit 1
emerge $eopts $[hollow/stage4/packages] || exit 1

rc-update add udev sysinit || exit 2

for i in udev-postmount dcron rsyslog; do
	rc-update add $i default || exit 2
done
]
