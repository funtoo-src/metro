[collect ../source/stage4.spec]
[collect ../target/stage4.spec]
[collect ../steps/kernel.spec]
[collect ../steps/livecd.spec]
[collect ../steps/capture/livecd.spec]

[section stage4]

source/name: base
target/name: installcd

packages: [
	net-misc/ntp
	sys-apps/gptfdisk
	sys-apps/kmod
	sys-fs/lvm2
	sys-fs/xfsprogs
]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]

# build livecd kernel
$[[steps/kernel/build]]
$[[steps/kernel/clean]]

# merge useful packages
emerge $eopts --noreplace $[stage4/packages] || exit 1

rc-update add devicemapper boot
rc-update add lvm boot

# common livecd steps
$[[steps/livecd]]
]

[section files]

# add some extra space so we scroll all the mingetty output out of the viewport
motd/extra: [










 >>> Welcome to the $[release/name] Minimal Installation CD!

 >>> The root password on this system has been set to "$[livecd/passwd]".
]
