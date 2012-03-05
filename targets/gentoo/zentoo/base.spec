[collect ../source/stage3.spec]
[collect ../target/stage4.spec]
[collect ../steps/capture/tar.spec]

[section stage4]

name: zentoo-base

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
]
