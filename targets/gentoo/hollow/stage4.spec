[collect ../stage/common.spec]
[collect ../stage/capture/tar.spec]
[collect ../stage/stage3-derivative.spec]
[collect ./steps.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.bz2

[section target]

name: stage4-$[target/subarch]-$[target/version]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/hollow/setup]]

export USE="$[portage/USE] bindist"
$[[steps/hollow/stage4]]
]

[section portage]

ROOT: /
