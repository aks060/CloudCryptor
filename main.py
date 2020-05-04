#!/usr/bin/python3
import pyfiglet
import os, threading, sys

args=sys.argv
print(args)

drivename=''
gpgudi=''
def config():
	print("\n")
	print("[+] Config Cloud Accounts\n\n[1] Create\n[2] List\n[3] Delete\n[4] Home")
	inp=int(input(">"))
	if inp==4:
		return
	elif inp==1:
		name=input("Name> ")
		acctype=int(input("\n[1] Google Drive\n[2] Dropbox\n[3] Microsoft OneDrive\nDrive Type> "))
		if acctype==1:
			acctype='drive'
		elif acctype==2:
			acctype='dropbox'
		elif acctype==3:
			acctype='onedrive'
		else:
			print("Error")
			exit()

		print("\n\nCreating disk...")
		os.system("rclone config create "+name+" "+acctype)

		print("\n\nFor more configuration usr rclone command..")

	else:
		print("\n\nThis option is not supported by use yet. Please use rclone for these options...\n\n")

	#os.system('rclone config')
def gtdr():
	global drivename
	if drivename=='':
		print("Remotes available: ")
		listdrives()
		print("\n")
		drivename=input('Enter Drive name: ')
	else:
		tmp=input("Enter Drive name ["+drivename+"]: ")
		if tmp!='':
			drivename=tmp
	return drivename

def gtuid():
	global gpgudi
	if gpgudi=='':
		print("GPG Uid available: ")
		listkeys()
		gpgudi=input("\nEnter the uid here: ")
	else:
		tmp=input("\nEnter the uid here ["+gpgudi+"]:")
		if tmp!='':
			gpgudi=tmp
	return gpgudi

def listdrives():
	os.system('rclone listremotes')

def listkeys():
	os.system('gpg -k')

def upload(files):
	drivename=gtdr()
	os.system('mkdir -p cryptoupload')
	dest=''
	dest=input('Upload destination (Default root): ')
	#os.system('mv '+files+' cryptoupload/')
	ret=os.system('rclone copy -P cryptoupload/ '+drivename+':"'+dest+'"')
	if ret!=0:
		print("\n\nSorry some error occured")
		return
	print("\n\nRemoving files from local drive...")
	os.system('rm -r cryptoupload/')
	print("\n\nTask Completed successfully...")

def encfile(path):
	print("Working on path: ", path)
	os.system('rm -r cryptoupload/')
	gpgudi=gtuid()
	finalpath=''
	encpath=''
	finalenc=[]
	for i in path:
		i=os.path.abspath(i.strip())
		finalpath+=(i+' ')
		encpath+=('"'+i+'.pgp" ')
		#finalpath.append(encpath)
	ret=os.system('gpg -e -r "'+gpgudi+'" --always-trust --multifile --yes '+finalpath)
	'''if ret!=0:
		print("\n\nSome error occured. (If you are trying to encrypt the directory then first zip it or verify it should not contain other directory in it\n")
		exit()'''
	os.system('mkdir -p cryptoupload')
	for i in path:
		print('value of i: '+i[:-1])
		if os.path.isdir(i[:-1]):
			cmd='mv "'+i[:-1]+'/"*.gpg cryptoupload/'
			print("trying to execute: "+cmd)
			os.system(cmd)
		else:
			os.system('mv "'+i+'.gpg" cryptoupload/')
	#os.system('mv *.gpg cryptoupload/')
	upload(encpath)

def listfile(path='', showdir=0):
	drname=gtdr()		#Drive name
	if showdir==0:
		os.system('rclone ls --max-depth 2 '+drname+':'+path)
	else:
		os.system('rclone lsd '+drname+':'+path)

def downfile():
	dname=gtdr()
	guid=gtuid()
	fname='$'
	curdir='/'
	while fname[0]=='$':
		fname=input("\n\nEnter file path separated by comma(,) [$<path> to list files]\n\teg: $/ : will list all the files in root dir\n\t$/dir1 : will list all the files in /dir1\n:")
		if fname[0]=='$':
			curdir=fname[1:]
			listfile(curdir, 0)
	print("\nDownloading file/s "+fname+" to Clouddownload/")
	os.system('mkdir -p Clouddownload')
	fname=fname.split(",")
	for i in fname:
		i=i.strip()
		os.system("rclone copy -P "+dname+':"'+i+'" Clouddownload/')
	os.system('gpg -d -r "'+guid+'" --always-trust --multifile --yes Clouddownload/*.gpg')
	os.system('rm Clouddownload/*.gpg')
	print("\n\nFile Downloaded successfully in Folder Clouddownload...")


def welcome():
	global drivename, gpgudi
	os.system('clear')
	print(pyfiglet.figlet_format('CloudCrypter'))
	print("\t\t\t\t\t\t\t\tBy Akash Kumar Sharma")
	print("\n\n\n\n[+] Please select the options from below\n\n[1] Configure Cloud accounts\n[2] Upload a files\n[3] Download Your File\n[4] List All\n[5] List Directories\n[6] Exit")
	inp=int(input("\n> "))

	if inp==1:
		config()

	elif inp==6:
		print("\nThanks for using it. visit https://github.com/aks060")
		os.popen('firefox https://github.com/aks060')
		exit()
	elif inp==2:
		path=input("Enter path of the file(separated by comma (, ) for multiple files): ")
		path=path.split(',')
		flag=1
		print("Files: \n")
		for j in range(0, len(path)):
			i=path[j]
			i=os.path.abspath(i.strip())
			print(i)
			if not os.path.exists(i):
				flag=0
				break
			if os.path.isdir(i):
				choice=int(input("The given path is directory. \n[1] Zip the folder then upload\n[2]upload files one by one\n: "))
				if choice==1:
					print("Working on it. ")
					exit()
				elif choice==2:
					path[j]+='/*'
		if flag==1:
			enc=input("\nEncrypt this ? (y/n): ")
			if enc=='y' or enc=='Y':
				#outpath=input("Enter your output path: ")
				encfile(path)
			else:
				finalpath=''
				for i in path:
					i=os.path.abspath(i.strip())
					finalpath+=('"'+i+'" ')
				upload(finalpath)

		else:
			print("Files doesnot exist ")
	elif inp==4:
		path=''
		path=input("Enter path of the file to list [Root] : ")
		listfile(path)
	elif inp==5:
		path=''
		path=input("Enter path of the file to list [Root] : ")
		listfile(path, 1)
	elif inp==3:
		downfile()
		

try:
	yes='y'
	while yes=='y' or yes=='Y':
		welcome()
		yes=input("Want to continue? (y/n)")
	print("hello thanks")
except Exception as e:
	raise e
	print("Thanks for using CloudCrypter")
	exit()