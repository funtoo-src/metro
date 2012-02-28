# Common stuff used when actually building a snapshot
[collect ./global.spec]

[section target]

name: $[portage/name/full]

[section metro]

# This defines what internal Metro class is used to build this target
class: snapshot

[section target]

type: repository

[section path/mirror]

# "current" symlink:
link: $[:snapshot/subpath]/$[portage/name]-current.tar.$[target/compression]
link/dest: $[portage/name/full].tar.$[target/compression]

[section trigger]

ok/run: [
#!/bin/bash
# CREATE current symlink for the snapshot
rm -f $[path/mirror/link]
ln -s $[path/mirror/link/dest] $[path/mirror/link] || exit 3
]

[section steps]

run: [
#!/bin/bash

die() {
	rm -f $[path/mirror/snapshot] $tarout
	echo "$*"
	exit 1
}

# On keyboard interrupt, clean up our partially-completed file...
trap "die Removing incomplete $[path/mirror/snapshot]..." INT

$[[steps/sync]]

echo "Creating $[path/mirror/snapshot]..."
install -d `dirname $[path/mirror/snapshot]` || die "Couldn't create output directory"
tarout="$[path/mirror/snapshot]"
tarout=${tarout%.*}

$[[steps/create]]
$[[steps/pack]]
]

pack: [
echo -n "Compressing $tarout using "
case "$[snapshot/compression]" in
	bz2)
		if [ -e /usr/bin/pbzip2 ]
		then
			echo "pbzip2..."
			pbzip2 -p4 $tarout || die "Snapshot pbzip2 failure"
		else
			echo "bzip2..."
			bzip2 $tarout || die "Snapshot bzip2 failure"
		fi
		;;
	gz)
		echo "gzip..."
		gzip -9 $tarout || die "Snapshot gzip failure"
		;;
	xz)
		if [ -e /usr/bin/pxz ]
		then
			echo "pxz..."
			pxz $tarout || die "Snapshot pxz failure"
		else
			echo "xz..."
			xz $tarout || die "Snapshot xz failure"
		fi
		;;
	*)
		echo "Unrecognized compression format $[snapshot/compression] specified for snapshot."
		exit 1
		;;
esac
echo "Snapshot $[path/mirror/snapshot] created."
]
