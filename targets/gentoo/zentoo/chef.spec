[collect ../source/stage3.spec]
[collect ../target/stage4.spec]
[collect ../steps/capture/tar.spec]

[section stage4]

name: zentoo-chef

[section zentoo/chef]

packages: [
	app-admin/chef-server
]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
emerge $eopts $[zentoo/chef/packages] || exit 1
]
