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
cat << "EOF" > /etc/locale.gen
$[[hollow/files/locale.gen]]
EOF
locale-gen
]

stage4: [
emerge $eopts -C mail-mta/ssmtp mail-mta/nullmailer || exit 1
rm -f /var/mail
emerge $eopts net-mail/mailbase -1 || exit 1
emerge $eopts mail-mta/postfix || exit 1
emerge $eopts $[hollow/stage4/packages] || exit 1
]
