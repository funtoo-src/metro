[collect ../steps/symlink.spec]

[section target]

class: virtualbox

name: $[virtualbox/target/name]-$[:subarch]-$[:build]-$[:version]
name/latest: $[virtualbox/target/name]-$[path/mirror/link/suffix]
name/full_latest: $[virtualbox/target/name]-$[:subarch]-$[:build]-$[path/mirror/link/suffix]

[section trigger]

ok/run: [
#!/bin/bash

install -d $[path/mirror/target/control]/version/virtualbox || exit 1
echo "$[target/version]" > $[path/mirror/target/control]/version/virtualbox/$[virtualbox/target/name] || exit 1

$[[trigger/ok/symlink]]
]
