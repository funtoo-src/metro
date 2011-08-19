[collect ./generator.spec]

[section zentoo]

name: host

[section zentoo/host]

packages: [
	sys-boot/grub
	sys-fs/lvm2
	sys-fs/mdadm
	sys-fs/xfsprogs
	sys-kernel/genkernel
	sys-kernel/vserver-sources
]

[section steps/zentoo]

run: [
emerge $eopts $[zentoo/host/packages] || exit 1
]
