import pyfiglet
import os

def config():
	print("\n")
	os.system('rclone config')

def welcome():
	print(pyfiglet.figlet_format('CloudCrypter'))
	print("\t\t\t\t\t\t\t\tBy Akash Kumar Sharma")
	print("\n\n\n\n>1] Configure Cloud accounts\n\n>2] Upload a files\n\n>3] Exit")
	inp=int(input("\n: "))
	if inp==1:
		config()
	elif inp==3:
		print("Thanks for using it. visit https://github.com/aks060")
		exit()
welcome()