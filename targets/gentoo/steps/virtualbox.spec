[collect ../snapshot/global.spec]

[section steps/virtualbox]

run: [
#!/bin/bash

git clone https://github.com/zentoo/quickstart /tmp/quickstart
pushd /tmp/quickstart

cat <<EOF > profiles/$[target/name].sh
$[[quickstart/profile]]
EOF

./quickstart -d profiles/$[target/name].sh
popd

# halt and sleep until we're killed
halt
sleep 60
]
