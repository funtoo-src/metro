[collect ../source/stage4.spec]
[collect ../target/stage4.spec]
[collect ../steps/capture/tar.spec]

[section stage4]

source/name: base
target/name: chef-server

packages: [
	app-admin/chef-server
]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
emerge $eopts $[stage4/packages] || exit 1
]
