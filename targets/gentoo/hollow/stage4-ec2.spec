[collect ../stage/common.spec]
[collect ../stage/capture/ami.spec]
[collect ../stage/stage3-derivative.spec]
[collect ./steps.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.bz2

[section target]

name: stage4-ec2-$[target/subarch]-$[target/version]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/hollow/setup]]

export USE="$[portage/USE] bindist"
$[[steps/hollow/stage4]]

# setup some stuff, so we can run out-of-the-box
env-update && source /etc/profile
cp /usr/share/zoneinfo/$[[hollow/ec2/timezone]] /etc/localtime

emerge $eopts $[[hollow/ec2/packages]]

for service in $[[hollow/ec2/services]]; do
	rc-update add ${service} default
done

sed -i -e 's/^# \(%wheel\tALL=(ALL)\tALL\)$/\1/' /etc/sudoers
]

[section portage]

ROOT: /
