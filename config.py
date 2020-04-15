import os

if os.geteuid()==0:
	print "Working on it"
	print("Installing Necessary package....")
	os.system("apt install rclone gpg")
	print("\nInstalling pyfiglet...")
	os.system("pip3 install pyfiglet")
else:
	print "Please Run as root"
