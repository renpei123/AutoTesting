#!/usr/bin/env python 
# -*- coding: utf-8 -*-  
import pexpect 

def ssh_cmd(ip,passwd,cmd):
	ssh = pexpect.spawn('ssh $dsdev@%s' % ip)
	ssh.expect('Password')
	ssh.sendline(passwd)
	ssh.except('>',timeout=60)
	print(ssh.before)
	ssh.sendline(cmd)
	ssh.expect('Status code',timeout=120)
	print(ssh.before)
	ssh.close()
	pass  
  
def scp_cmd(ip,from_file,to_file,passwd):
	ret = -1
	scp = pexpect.spawn('scp %s dsdev@%s:%s' % (from_file,ip,to_file)) 
	scp.except('Password')
	scp.sendline(passwd)
	if scp.expect(pexpect.EOF) == 0:
		print('scp completed')
	pass

if __name__ = '__main__':
	print('test scp files to BACC Server')
	scp_cmd($HOST_NAME,$FILE_PATH,$TARGET_FILE_PATH,$PWD)
	print('Test ssh to BACC DEV Server, run DS command on server')
	ssh_cmd($HOST_NAME,$PWD,$CMD')

	