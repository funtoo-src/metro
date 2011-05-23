[collect ../stage/common.spec]
[collect ../stage/capture/tar.spec]
[collect ../stage/stage3-derivative.spec]
[collect ../stage/symlink.spec]
[collect ./steps.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.$[target/compression]

[section target]

name: stage4-$[:subarch]-$[:build]-$[:version]
name/current: stage4-current

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/hollow/setup]]

export USE="$[portage/USE] bindist"
$[[steps/hollow/stage4]]
]

[section trigger]

ok/run: [
$[[trigger/ok/symlink]]
]

[section portage]

ROOT: /
