[section steps]

livecd: [
emerge $eopts --noreplace app-misc/livecd-tools net-dialup/mingetty net-misc/dhcpcd sys-apps/hwsetup dev-util/strace x11-terms/xterm || exit 1

# setup init scripts
rc-update del keymaps boot
rc-update del netmount default

rc-update add autoconfig default
rc-update add fixinittab default

# permit root login via ssh
if [ -e /etc/ssh/sshd_config ]
then
	sed -i -e 's:^#PermitRootLogin\ yes:PermitRootLogin\ yes:' \
		/etc/ssh/sshd_config
fi

# use the public (insecure) ssh key from vagrant
mkdir -p /root/.ssh
chmod 0700 /root/.ssh
curl -s -L https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub > /root/.ssh/authorized_keys

# try to get a network address via dhcp
echo 'dhcpcd eth0' > /etc/ifup.eth0

# for our virtualbox target we need this hostonly interface
echo 'ip link set eth1 up' > /etc/ifup.eth1
echo 'ip addr add 10.99.99.2/24 dev eth1' >> /etc/ifup.eth1

# set gdm
gsettings set org.gnome.desktop.background picture-uri file:////usr/share/backgrounds/funtoo/FuntooSwirl.jpg

# for hwsetup
mkdir -p /etc/sysconfig

# make sure we have the latest pci, usb and hotplug ids
[ -x /sbin/update-pciids ] && /sbin/update-pciids
[ -x /sbin/update-usbids ] && /sbin/update-usbids
[ -x /usr/sbin/update-pciids ] && /usr/sbin/update-pciids
[ -x /usr/sbin/update-usbids ] && /usr/sbin/update-usbids

if [ -d /usr/share/hwdata ]
then
	# If we have uncompressed pci and usb ids files, symlink them.
	[ -f /usr/share/misc/pci.ids ] && [ -f /usr/share/hwdata/pci.ids ] && \
		rm -f /usr/share/hwdata/pci.ids && ln -s /usr/share/misc/pci.ids \
		/usr/share/hwdata/pci.ids
	[ -f /usr/share/misc/usb.ids ] && [ -f /usr/share/hwdata/usb.ids ] && \
		rm -f /usr/share/hwdata/usb.ids && ln -s /usr/share/misc/usb.ids \
		/usr/share/hwdata/usb.ids
	# If we have compressed pci and usb files, we download our own copies.
	[ -f /usr/share/misc/pci.ids.gz ] && [ -f /usr/share/hwdata/pci.ids ] && \
		rm -f /usr/share/hwdata/pci.ids && wget -O /usr/share/hwdata/pci.ids \
		http://pciids.sourceforge.net/v2.2/pci.ids
	[ -f /usr/share/misc/usb.ids.gz ] && [ -f /usr/share/hwdata/usb.ids ] && \
		rm -f /usr/share/hwdata/usb.ids && wget -O /usr/share/hwdata/usb.ids \
		http://www.linux-usb.org/usb.ids
fi

# save some space
emerge --depclean || exit 1
rm -rf /usr/lib/debug || exit 1

# set user and reset passwords
useradd funtoo
passwd -d funtoo
passwd -d root
]
