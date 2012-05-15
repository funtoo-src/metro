[section steps/kernel]

build: [
echo > /etc/fstab || exit 1
emerge $eopts --noreplace sys-kernel/genkernel $[livecd/kernel/package] || exit 1
curl -k -L -s 'http://git.overlays.gentoo.org/gitweb/?p=proj/genkernel.git;a=blob_plain;f=arch/x86_64/kernel-config;h=627ca9e542ebda473f0cb344836bf26eeba7a918;hb=b476a988ea2559904bcb40cc44633d237f790823' > /tmp/kconfig
genkernel $[livecd/kernel/opts:lax] \
	--kernel-config=/tmp/kconfig \
	--cachedir=/var/tmp/cache/kernel \
	--modulespackage=/var/tmp/cache/kernel/modules.tar.bz2 \
	--minkernpackage=/var/tmp/cache/kernel/kernel-initrd.tar.bz2 \
	all || exit 1
]

clean: [
emerge -C sys-kernel/genkernel $[livecd/kernel/package] || exit 1
rm -rf /usr/src/linux-* /usr/src/linux || exit 1
]
