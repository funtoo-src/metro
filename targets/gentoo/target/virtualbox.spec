[collect ../steps/symlink.spec]

[section target]

class: virtualbox

name: $[virtualbox/target/name]-$[:subarch]-$[:build]-$[:version]
name/current: $[virtualbox/target/name]-current

[section trigger]

ok/run: [
#!/bin/bash

install -d $[path/mirror/target/control]/version/virtualbox || exit 1
echo "$[target/version]" > $[path/mirror/target/control]/version/virtualbox/$[virtualbox/target/name] || exit 1

$[[trigger/ok/symlink]]
]
