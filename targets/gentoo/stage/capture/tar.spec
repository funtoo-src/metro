[section steps]

capture: [
#!/bin/bash
outdir=`dirname $[path/mirror/target]`
if [ ! -d $outdir ]
then
	install -d $outdir || exit 1
fi
tarout="$[path/mirror/target]"
tarout="${tarout%.*}"
tar cpf $tarout -C $[path/chroot/stage] .
if [ $? -ge 2 ]
then
	echo "failed! removing tar file"
	rm -f "$tarout" "$[path/mirror/target]"
	exit 1
fi

echo -n "Compressing $[path/mirror/target] using "
case "$[target/compression]" in
	bz2)
		if [ -e /usr/bin/pbzip2 ]
		then
			echo "pbzip2..."
			pbzip2 -p4 $tarout
		else
			echo "bzip2..."
			bzip2 $tarout
		fi
		;;
	xz)
		if [ -e /usr/bin/pxz ]
		then
			echo "pxz..."
			pxz $tarout
		else
			echo "xz..."
			xz $tarout
		fi
		;;
	gz)
		echo "gzip..."
		gzip $tarout
		;;

	*)
		echo "Unrecognized compression format $[target/compression] specified for stage tarball."
                exit 1
                ;;
esac
if [ $? -ne 0 ]
then
	echo "Compression error - aborting."
	rm -f $[path/mirror/target]
	exit 99
fi
]


