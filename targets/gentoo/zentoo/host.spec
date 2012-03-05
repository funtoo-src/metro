[collect ../source/stage3.spec]
[collect ../target/stage4.spec]
[collect ../steps/capture/tar.spec]

[section stage4]

name: zentoo-host

[section zentoo/host]

packages: [
	net-firewall/shorewall
	net-firewall/shorewall6
	net-misc/openntpd
	net-misc/openrdate
	sys-apps/smartmontools
	sys-boot/grub
	sys-fs/lvm2
	sys-fs/mdadm
	sys-fs/xfsprogs
	sys-kernel/genkernel
	sys-kernel/zentoo-sources
]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
emerge $eopts $[zentoo/host/packages] || exit 1
]
