# This file defines common settings for all stage4 generators. Stage4
# generators are targets that build on top of a stage3 to produce various
# specialized images such as a webserver, database or container images.

[collect ./common.spec]
[collect ./stage3-derivative.spec]
[collect ../steps/capture/tar.spec]
[collect ../steps/symlink.spec]

[section target]

name: $[stage4/name]-$[:subarch]-$[:version]
name/current: $[stage4/name]-$[:subarch]-current

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/stage4/run]]
]

[section trigger]

ok/run: [
$[[trigger/ok/symlink]]
]

[section portage]

ROOT: /
