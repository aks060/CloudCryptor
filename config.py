import os

if os.geteuid()==0:
	print "Please run as root"
	print("Installing Necessary package....")
	os.system("apt install rclone gpg")
	print("\nInstalling pyfiglet...")
	os.system("pip3 install pyfiglet")
else:
	print "working fine"
