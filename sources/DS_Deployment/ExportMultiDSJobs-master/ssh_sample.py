#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect


def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh dsdev@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
            ssh.sendline(cmd)
            r = ssh.read()
            print(r)
            ret = 0
    except pexpect.EOF:
        print("EOF")
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print("TIMEOUT")
        ssh.close()
        ret = -2
    return ret


ssh_cmd('9.17.174.164', 'aug18aug',
        'sh /gsa/pokgsa/projects/s/siwdw_ds/siwext_ds_dev/siw_rdm/scripts/auto-test/job_status.sh /gsa/pokgsa/projects/s/siwdw_ds/siwext_ds_dev/siw_rdm/config_files/Aut_Test.cfg 1>/gsa/pokgsa/projects/s/siwdw_ds/siwext_ds_dev/siw_rdm/scripts/auto-test/job_status.log')