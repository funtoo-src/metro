#!/bin/bash --login
method="rsync"
metro="$(dirname $0)/../metro"
mp=$($metro -k path/mirror 2>/dev/null)
if [ -z "$mp" ]; then
	echo "Could not get path/mirror from metro configuration; exiting."
	exit 1
else
	echo "Mirroring $mp..."
fi
LAST_YEAR=$( date +%Y -d "-1 years" )
EXTRA_EXCLUDES="--exclude=selinux* --exclude=*2019-* --delete-excluded"
EXCLUDES="--exclude .* --exclude *.cme --exclude *.cme.run --exclude *.progress --exclude stage1*.tar* --exclude stage2*.tar* --exclude *.tar --exclude=*-${LAST_YEAR}-*.tar.xz"
$mp/../metro/scripts/buildrepo index.xml
$mp/../metro/scripts/indexr.py $mp
if [ "$method" == "rclone" ]; then
	# RCLONE SYNC UP TO BACKBLAZE, THEN HAVE DIRECT-PULL PULL DOWN FROM BACKBLAZE
	SPEEDS="--b2-chunk-size=18M --b2-upload-cutoff=36M --transfers=14 --checkers=28 --bwlimit=20M"
	rclone -Pl $EXCLUDES $EXTRA_EXCLUDES $SPEEDS sync $mp b2:funtoo-mirror
	rclone cleanup b2:funtoo-mirror
	if [ "$1" == "half" ]; then
		echo "Only performing first half of mirroring operation."
		echo "This part is done."
		exit 0
	fi
	ssh -p 1022 drobbins@direct-pull.funtoo.org rclone sync -lP b2:funtoo-mirror/ /home/mirror/funtoo/
elif [ "$method" == "rsync" ]; then
	# SYNC DIRECTLY FROM THIS SYSTEM TO DIRECT-PULL:
	rsync -azve "ssh -p 1022" --delete $mp/ drobbins@direct-pull.funtoo.org:/home/mirror/funtoo/ $EXCLUDES $EXTRA_EXCLUDES --progress --stats
else
	echo "Unknown sync method: $method"
	exit 1
fi
ssh -p 1022 drobbins@direct-pull.funtoo.org 'find /home/mirror/funtoo -type f -exec chmod 0644 {} \;'
ssh -p 1022 drobbins@direct-pull.funtoo.org 'find /home/mirror/funtoo -type d -exec chmod 0755 {} \;'
ssh -p 1022 root@www.funtoo.org /etc/init.d/memcached restart
