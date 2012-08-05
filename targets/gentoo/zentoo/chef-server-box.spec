[collect ../source/stage4.spec]
[collect ../target/virtualbox.spec]
[collect ../generator/livecd.spec]
[collect ../steps/virtualbox.spec]
[collect ../steps/capture/vagrant.spec]

[section stage4]

source/name: chef-server

[section virtualbox]

target/name: chef-server

memory: 2048
hddsize: 80

[section livecd]

name: installcd

[section quickstart]

profile: [
. profiles/vagrant-chef-server.sh
stage_uri file://$(ls -1 /tmp/$(basename "$[path/mirror/source]"))
tree_type snapshot file://$(ls -1 /tmp/$(basename "$[path/mirror/snapshot]"))
]
