[section path/mirror]

target/basename: $[target/name].iso

[section steps]

capture: [
#!/bin/bash

# create cd root
cdroot=$[path/mirror/target]
cdroot=${cdroot%.*}
if [ ! -d $cdroot ]
then
	install -d $cdroot || exit 1
fi
touch $cdroot/livecd

# create livecd filesystem with squashfs
squashout=$cdroot/image.squashfs
mksquashfs $[path/chroot/stage] $squashout
if [ $? -ge 1 ]
then
	rm -f "$squashout" "$cdroot" "$[path/mirror/target]"
	exit 1
fi

# copy bootloader and kernel
install -d $cdroot/boot/grub/fonts || exit 1
cp -T $[path/chroot/stage]/boot/kernel* $cdroot/boot/kernel || exit 1
cp -T $[path/chroot/stage]/boot/initramfs* $cdroot/boot/initramfs || exit 1
cp -T $[path/chroot/stage]/boot/System.map* $cdroot/boot/System.map || exit 1
cp -r $[livecd/grub]/* $[livecd/grub/themes] $cdroot/boot/grub/ || exit 1
cp  $[livecd/grub/font] $cdroot/boot/grub/fonts/ || exit 1

cat > $cdroot/boot/grub/grub.cfg << "EOF"
set timeout 3

insmod iso9660
insmod udf
insmod squashfs4

search --file /livecd --set root
if loadfont /boot/grub/fonts/unicode.pf2; then
   set gfxmode=640x480
   insmod all_video
   insmod efi_gop
   insmod efi_uga
   terminal_output gfxterm
fi
set menu_color_normal=cyan/blue
set menu_color_highlight=blue/cyan

menuentry "Funtoo Linux LiveCD" --class gnu-linux --class os {
	echo 'Loading Linux kernel ...'
	linux  /boot/kernel root=/dev/ram0 looptype=squashfs loop=/image.squashfs cdroot quiet
	initrd /boot/initramfs
}
menuentry 'Reboot' {
	reboot
}
EOF

# Create iso image
grub-mkrescue -J -l -R \
	-A "$[livecd/name]" \
	-o $[path/mirror/target] \
	$cdroot/ || exit 1

# Extract EFI image from iso
install -d $cdroot/isotmp $cdroot/efitmp
mount $[path/mirror/target].iso $cdroot/isotmp
mount $cdroot/isotmp/efi.img $cdroot/efitmp
cp -r $cdroot/efitmp/* $cdroot/
umount $cdroot/efitmp
umount $cdroot/isotmp
rm $[path/mirror/target].iso
rm -r $cdroot/efitmp $cdroot/isotmp

# Recreate iso image
grub-mkrescue -J -l -R \
	-A "$[livecd/name]" \
	-o $[path/mirror/target] \
	$cdroot/ || exit 1

rm -rf $cdroot || exit 1
]
