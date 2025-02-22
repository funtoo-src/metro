[section path/mirror]

target/basename: $[target/name].box

[section steps]

capture: [
#!/bin/bash
vm=$[target/name]

vgroot=$[path/mirror/target]
vgroot=${vgroot%.*}
if [ ! -d $vgroot ]
then
	install -d $vgroot || exit 1
fi

ovfout=$vgroot/box.ovf
VBoxManage export $vm -o $ovfout || exit 1

mac=$(VBoxManage showvminfo $vm --machinereadable|sed -e 's/macaddress1="\(.*\)"/\1/;tn;d;:n')

cat <<EOF > $vgroot/Vagrantfile
Vagrant::Config.run do |config|
  # This Vagrantfile is auto-generated by vagrant package to contain
  # the MAC address of the box. Custom configuration should be placed in
  # the actual Vagrantfile in this box.
  config.vm.base_mac = "${mac}"
end

# Load include vagrant file if it exists after the auto-generated
# so it can override any of the settings
include_vagrantfile = File.expand_path("../include/_Vagrantfile", __FILE__)
load include_vagrantfile if File.exist?(include_vagrantfile)
EOF

tarout="$[path/mirror/target]"
tar cpf $tarout -C $vgroot . || exit 1

rm -rf $vgroot
]
