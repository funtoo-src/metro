[collect ../stage/common.spec]
[collect ../stage/capture/tar.spec]
[collect ../stage/stage3-derivative.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.bz2

[section target]

name: stage4-$[target/subarch]-$[target/version]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
export USE="$[portage/USE] bindist"

emerge -C mail-mta/ssmtp || exit 1
rm -f /var/mail
emerge net-mail/mailbase -1n || exit 1
emerge mail-mta/postfix || exit 1

emerge $eopts $[hollow/stage4/packages] || exit 1
]

[section portage]

ROOT: /
