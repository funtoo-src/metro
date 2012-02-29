[collect ../stage/stage4-generator.spec]

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

[section steps/stage4]

run: [
emerge $eopts $[zentoo/host/packages] || exit 1
]
