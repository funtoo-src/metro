import os, sys, time, types, glob
import subprocess

from catalyst_support import MetroError, ismount

from .base import BaseTarget

class VirtualboxTarget(BaseTarget):
    def __init__(self, settings):
        BaseTarget.__init__(self, settings)

        # we need a source archive
        self.required_files.append("path/mirror/source")
        self.required_files.append("path/mirror/generator")

        self.cmds["modprobe"] = "/sbin/modprobe"
        self.cmds["vbox"] = "/usr/bin/VBoxManage"

        # vm config
        self.name = "metro_"+self.settings["target/name"]
        self.basedir = self.settings["path/work"]+"/vm"

        if self.settings["target/arch"] == "amd64":
            self.ostype = "Gentoo_64"
        else:
            self.ostype = "Gentoo"

    def run(self):
        if self.target_exists("path/mirror/target"):
            self.run_script("trigger/ok/run", optional=True)
            return

        if self.settings["target/arch"] not in ["amd64", "x86"]:
            raise MetroError, "VirtualBox target class only supports x86 targets"

        self.check_required_files()

        # load virtualbox modules
        self.load_modules()

        # before we start - clean up any messes
        self.destroy_vm()
        self.clean_path(recreate=True)

        self.start_vm()

        # 60 seconds should be enough to boot
        # a better heuristic would be nice though
        time.sleep(60)

        try:
            self.upload_file(glob.glob(self.settings["path/mirror/source"])[0])
            self.upload_file(glob.glob(self.settings["path/mirror/snapshot"])[0])

            self.run_script_in_vm("steps/virtualbox/prerun", optional=True)
            self.run_script_in_vm("steps/virtualbox/run")
            self.run_script_in_vm("steps/virtualbox/postrun", optional=True)
        except:
            #self.destroy_vm()
            raise

        # wait a few seconds so that the VM can shutdown itself
        time.sleep(15)

        self.shutdown_vm()
        self.run_script("steps/capture")
        self.run_script("trigger/ok/run", optional=True)

        #self.destroy_vm()
        #self.clean_path()

    def load_modules(self):
        for mod in ["vboxdrv", "vboxpci", "vboxnetadp", "vboxnetflt"]:
            self.cmd(self.cmds["modprobe"]+" "+mod)

    def vbm(self, cmd):
        self.cmd(self.cmds["vbox"]+" "+cmd)

    def start_vm(self):
        # create vm
        self.vbm("createvm --name %s --ostype %s --basefolder '%s' --register" % (self.name, self.ostype, self.basedir))
        self.vbm("modifyvm %s --rtcuseutc on --boot1 disk --boot2 dvd --boot3 none --boot4 none" % (self.name))
        self.vbm("modifyvm %s --memory %s" % (self.name, self.settings["virtualbox/memory"]))
        self.vbm("modifyvm %s --vrde on --vrdeport 3389 --vrdeauthtype null" % (self.name))

        # create hard drive
        self.vbm("createhd --filename '%s/%s.vdi' --size $((%s*1024)) --format vdi" % (self.basedir, self.name, self.settings["virtualbox/hddsize"]))
        self.vbm("storagectl %s --name 'SATA Controller' --add sata --controller IntelAhci --bootable on --sataportcount 2" % (self.name))
        self.vbm("storageattach %s --storagectl 'SATA Controller' --type hdd --port 0 --medium '%s/%s.vdi'" % (self.name, self.basedir, self.name))

        # attach generator
        self.vbm("storageattach %s --storagectl 'SATA Controller' --type dvddrive --port 1 --medium '%s'" % (self.name, self.settings["path/mirror/generator"]))

        # create hostonly network
        ifcmd = self.cmds["vbox"]+" hostonlyif create 2>/dev/null | /bin/egrep -o 'vboxnet[0-9]+'"
        self.ifname = subprocess.check_output(ifcmd, shell=True).strip()
        self.vbm("hostonlyif ipconfig %s --ip 10.99.99.1" % (self.ifname))

        # setup vm networking
        self.vbm("modifyvm %s --nic1 nat --nic2 hostonly" % (self.name))
        self.vbm("modifyvm %s --hostonlyadapter2 %s" % (self.name, self.ifname))

        # start the vm
        self.vbm("startvm %s --type headless" % (self.name))

    def shutdown_vm(self):
        try:
            self.vbm("controlvm %s poweroff && sleep 5" % (self.name))
        except:
            pass

    def destroy_vm(self):
        self.shutdown_vm()

        # determine virtual network if we don't have it
        if not hasattr(self, "ifname"):
            ifcmd = self.cmds["vbox"]+" list hostonlyifs|grep -B3 10.99.99.1|head -n1|awk '{print $2}'"
            self.ifname = subprocess.check_output(ifcmd, shell=True).strip()

        try:
            self.vbm("unregistervm %s --delete" % (self.name))
        except:
            pass

        try:
            self.vbm("hostonlyif remove %s" % (self.ifname))
        except:
            pass

    def ssh_options(self):
        ssh_id = self.settings["path/config"]+"/keys/vagrant"
        os.chmod(ssh_id, 0400)
        return [
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "GlobalKnownHostsFile=/dev/null'",
            "-i", ssh_id,
            "-q"
        ]

    def ssh_pipe_to_vm(self, cmd, scp=False):
        cmd = ["ssh"] + self.ssh_options() + [
            "root@10.99.99.2",
            cmd
        ]

        return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sys.stdout)

    def run_script_in_vm(self, key, optional=False):
        if not self.settings.has_key(key):
            if optional:
                return
            raise MetroError, "run_script: key '%s' not found." % (key,)

        if type(self.settings[key]) != types.ListType:
            raise MetroError, "run_script: key '%s' is not a multi-line element." % (key, )

        print "run_script_in_vm: running %s..." % key

        ssh = self.ssh_pipe_to_vm("/bin/bash -s")
        ssh.stdin.write("\n".join(self.settings[key]))
        ssh.stdin.close()
        ssh.wait()

    def upload_file(self, path):
        print "Uploading \"%s\"" % (path)
        cmd = ["scp"] + self.ssh_options() + [
            path,
            "root@10.99.99.2:/tmp/"+os.path.basename(path)
        ]
        ssh = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sys.stdout)
        ssh.stdin.close()
        ssh.wait()

# vim: ts=4 sw=4 et
