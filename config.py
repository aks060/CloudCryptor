import os

out=os.system('touch /testforclouddecrypter')
if out!=0:
	print("Please run as root")
	exit()
else:
	print('working fine')
	os.system('rm /testforclouddecrypter')

print("Installing Necessary package....")
os.system("apt install rclone gpg")

print("\nInstalling pyfiglet...")
os.system("pip3 install pyfiglet")