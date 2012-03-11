[collect ../source/stage3.spec]
[collect ../target/stage4.spec]
[collect ../steps/capture/tar.spec]

[section stage4]

target/name: base

packages: [
	app-admin/chef
	app-admin/denyhosts
	app-admin/lib_users
	app-admin/logrotate
	app-admin/pwgen
	app-admin/pydf
	app-admin/sudo
	app-admin/syslog-ng
	app-admin/sysstat
	app-arch/atool
	app-arch/xz-utils
	app-backup/duply
	app-editors/vim
	app-misc/colordiff
	app-misc/mc
	app-misc/tmux
	app-portage/eix
	app-portage/elogv
	app-portage/gentoolkit
	app-portage/layman
	app-portage/portage-utils
	app-portage/porticron
	app-shells/bash-completion
	app-text/dos2unix
	dev-util/lockrun
	dev-util/strace
	dev-vcs/git
	mail-client/mailx
	net-analyzer/bwm-ng
	net-analyzer/iptraf-ng
	net-analyzer/mtr
	net-analyzer/netcat
	net-analyzer/nmap
	net-analyzer/tcpdump
	net-analyzer/tcptraceroute
	net-analyzer/traceroute
	net-dns/bind-tools
	net-ftp/lftp
	net-misc/dhcpcd
	net-misc/keychain
	net-misc/telnet-bsd
	net-misc/whois
	sys-apps/ack
	sys-apps/ethtool
	sys-apps/hdparm
	sys-apps/iproute2
	sys-apps/pciutils
	sys-apps/unscd
	sys-fs/ncdu
	sys-process/dcron
	sys-process/htop
	sys-process/iotop
	sys-process/lsof
]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
emerge $eopts --noreplace mail-mta/postfix || exit 1
emerge $eopts --noreplace $[stage4/packages] || exit 1
rc-update add syslog-ng default
rc-update add dcron default
]
