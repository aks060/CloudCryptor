#!/usr/bin/python3
import pyfiglet
import os, threading, sys

args=sys.argv


drivename=''
gpgudi=''
def config():
	if(len(args)==2):
		print("\n\t\t\u001b[1;31mIncomplete Argument Entered \n\t\t\t\u001b[32;1mcheck man page")
		exit()
	
	elif '-name' in args:
		
		acctype = ['drive','dropbox','onedrive']
		if(len(args)==3):
			print("\n\u001b[1;31mThis option is not supported by use yet. Please use rclone for these options...")
			exit()
		
		elif args[(args.index('-name')) + 1] in acctype:
			name=input("Name> ")
			print("\nCreating disk...")
			os.system("rclone config create "+name+" "+args[(args.index('-name')) + 1])
		
			print("\nFor more configuration usr rclone command..")
		elif args[(args.index('-name')) + 1] not in acctype:
			print("\n\t\t\u001b[1;31mThis cloud drive is not supported...")

		
			
	
			


	#os.system('rclone config')
def gtdr():
	global drivename
	if drivename=='':
		print("Remotes available: ")
		listdrives()
		
		drivename=input('\nEnter Drive name: ')
	else:
		tmp=input("\nEnter Drive name ["+drivename+"]: ")
		if tmp!='':
			drivename=tmp
	return drivename

def gtuid():
	global gpgudi
	if gpgudi=='':
		print("\nGPG Uid available: ")
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
	if '-p' in args :
	 fname+=args[(args.index('-p'))+1]
	else:
    		print("No path specified to download files ")
			exit()
	curdir='/'
	while fname[0]=='$':
		# fname=input("\n\nEnter file path separated by comma(,) [$<path> to list files]\n\teg: $/ : will list all the files in root dir\n\t"+"    "+"$/dir1 : will list all the files in /dir1\n:")
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
	# os.system('clear')
	print(pyfiglet.figlet_format('CloudCrypter'))
	print("\t\t\t\t\tBy Akash Kumar Sharma")

	# print("\n\n\n\n[+] Please select the options from below\n\n[1] Configure Cloud accounts\n[2] Upload a files\n[3] Download Your File\n[4] List All\n[5] List Directories\n[6] Exit")
	# inp=int(input("\n> "))

	if "-config" in args :
		config()

	
	elif '-upload' in args:
		# path=input("Enter path of the file(separated by comma (, ) for multiple files): ")
		if(len(args)==2):
			print("\n\t\t\u001b[1;31mIncomplete Argument Entered \n\t\t\t\u001b[32;1mcheck man page")
			exit()
		elif "-path" in args:
			if(len(args)==3):
				print("\n\t\t\u001b[1;31mIncomplete Argument Entered \n\t\t\t\u001b[32;1mcheck man page")
				exit()
			else:
				path = args[(args.index('-path'))+1]
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
					if(len(args)==3):
						print("\n\t\t\u001b[1;31mIncomplete Argument Entered \n\t\t\t\u001b[32;1mcheck man page")
						exit()
				# choice=int(input("The given path is directory. \n[1] Zip the folder then upload\n[2]upload files one by one\n: "))
					else:
						if "-zip" in args:
							print("Working on it. ")
							exit()
						elif "-obo" in args:
								path[j]+='/*'
			

			if flag==1:
				if(len(args)==4):
					print("\n\t\t\u001b[1;31mIncomplete Argument Entered \n\t\t\t\u001b[32;1mcheck man page")
					exit()
				else:
					if "-enc" in args:
			# if enc=='y' or enc=='Y':
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
	# elif args[1]=='-L':
	# 	path=''
	# 	path=input("Enter path of the file to list [Root] : ")
	# 	listfile(path)
	# elif args[1]=='-path':
	# 	path=''
	# 	path=input("Enter path of the file to list [Root] : ")
	# 	listfile(path, 1)
	elif '-download' in args:
		downfile()
	else:
		print("\t\t\u001b[1;31mCheck help by -> \u001b[32;1mmain.py h")
		exit()
		



if(len(args)==1):
		
		print("\n\t\t\u001b[1;31mCheck help at \u001b[32;1mmain.py h")
		exit()
elif(args[1]=='h'):
		
		os.system("man ./cryptocloud")
		
else:
		
		# yes='y'
		# while yes=='y' or yes=='Y':
			welcome()
	# 	  yes=input("Want to continue? (y/n)")
	# print("hello thanks")
			exit()
			


	