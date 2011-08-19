[collect ../stage/common.spec]
[collect ../stage/capture/tar.spec]
[collect ../stage/stage3-derivative.spec]
[collect ../stage/symlink.spec]

[section path/mirror]

target: $[:target/subpath]/$[target/name].tar.$[target/compression]

[section target]

name: $[:build]-$[zentoo/name]-$[:subarch]-$[:version]
name/current: $[:build]-$[zentoo/name]-$[:subarch]-current

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/zentoo/run:zap]]
]

[section trigger]

ok/run: [
$[[trigger/ok/symlink]]
]

[section portage]

ROOT: /
