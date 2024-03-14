import os
while True:
	choice = input("was möchtest du tun? 1. upload 2. download 3. exit-->")
	if choice == "1":
		os.system("python3 split.py")
	if choice == "2":
		os.system("python3 download.py")
	if choice == "3":
		exit(0)
