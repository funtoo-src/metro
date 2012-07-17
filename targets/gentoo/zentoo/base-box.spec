[collect ../source/stage4.spec]
[collect ../target/virtualbox.spec]
[collect ../generator/livecd.spec]
[collect ../steps/virtualbox.spec]
[collect ../steps/capture/vagrant.spec]

[section stage4]

source/name: base

[section virtualbox]

target/name: base

memory: 1024
hddsize: 80

[section livecd]

name: installcd

[section quickstart]

profile: [
. profiles/vagrant-base.sh
stage_uri file://$(ls -1 /tmp/$(basename "$[path/mirror/source]"))
tree_type snapshot file://$(ls -1 /tmp/$(basename "$[path/mirror/snapshot]"))
]
