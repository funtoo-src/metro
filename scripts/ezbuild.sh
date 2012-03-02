#!/bin/bash

# If we are running from fcron, we'll have a clean environment and thus won't
# have proxy settings. So let's make sure we have a good Gentoo environment...

source /etc/profile

die() {
	echo $*
	exit 1
}

do_help() {
	cat << EOF

  Metro Automation Engine Script
  by Daniel Robbins (drobbins@funtoo.org)
  by Benedikt Böhm (hollow@gentoo.org)

  Usage: $0 <build> <arch>..
  Examples:
    # $0 zentoo amd64
    # $0 ~funtoo core2

EOF
}

ROOT=$(realpath $(dirname $0)/../)
METRO="${ROOT}"/metro

if [ $# -lt 2 ]
then
	do_help
	die "This script requires two or more arguments"
fi

BUILD="$1"
VERSION=${VERSION:-$(date +%Y%m%d)}
shift

for SUBARCH in "$@"
do
	nice -n 39 ionice -c 3 $METRO \
		multi: yes \
		multi/mode: ${MODE:-full} \
		target/build: $BUILD \
		target/subarch: $SUBARCH \
		target/version: $VERSION

	#"${ROOT}"/scripts/vbox-create.sh $SUBARCH $VERSION
done
