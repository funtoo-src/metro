#!/bin/bash

# TODO: convert this to a proper metro target

set -e

NAME="zentoo-host"
SUBARCH=$1
VERSION=$2

VMDIR=/var/tmp/metro/VMs/${NAME}
TARGET=/var/cache/metro/zentoo/${SUBARCH}/${VERSION}/${NAME}-${SUBARCH}-${VERSION}.ova
LINK_TARGET=/var/cache/metro/zentoo/${SUBARCH}/${NAME}-${SUBARCH}-current.ova

# make sure kernel modules are loaded
for m in vbox{drv,netadp,netflt}; do modprobe $m; done

if VBoxManage list vms | grep -q ${NAME}; then
	echo "!!! VM ${NAME} already exists."
	exit 1
fi

VBoxManage createvm --name ${NAME} --ostype Gentoo_64 --basefolder "${VMDIR}" --register
VBoxManage modifyvm ${NAME} --memory 1024 --vram 12 --rtcuseutc on --boot1 disk --boot2 dvd --boot3 none --boot4 none

VBoxManage storagectl ${NAME} --name "IDE Controller"  --add ide  --controller PIIX4     --bootable on
VBoxManage storagectl ${NAME} --name "SATA Controller" --add sata --controller IntelAhci --bootable on --sataportcount 1

VBoxManage createhd --filename "${VMDIR}"/${NAME}.vmdk --size $((80*1024)) --format vmdk
VBoxManage storageattach ${NAME} --storagectl "SATA Controller" --type hdd --port 0 --medium "${VMDIR}"/${NAME}.vmdk

wget -O "${VMDIR}"/zentoo-vbox-quickstart.iso http://www.zentoo.org/downloads/${SUBARCH}/zentoo-vbox-quickstart.iso
VBoxManage storageattach ${NAME} --storagectl "IDE Controller" --type dvddrive --device 0 --port 0 --medium "${VMDIR}"/zentoo-vbox-quickstart.iso

VBoxManage startvm ${NAME} --type headless

echo -n "Waiting for quickstart to finish "
while VBoxManage showvminfo ${NAME}-gen | grep -q State:.*running; do
	echo -n "."
	sleep 30
done
echo

VBoxManage storageattach ${NAME} --storagectl "IDE Controller" --type dvddrive --device 0 --port 0 --medium none

VBoxManage export ${NAME} -o ${TARGET}
chmod 644 ${TARGET}
ln -s ${LINK_TARGET} ${TARGET}

VBoxManage unregistervm ${NAME} --delete
