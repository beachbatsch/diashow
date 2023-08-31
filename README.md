Purpose
=======
Mount a remote folder via davfs2.
Synchronize the images and images in subfolders to a local folder.
Show all the images as a diashow and synchronize in intervalls.

Platform
========

Tested with Fedora and Raspbian

Software requirements
=====================
Install 
- feh 
- davfs

> sudo dnf install feh
>
> sudo dnf install davfs 


AUTOMOUNT DAVFS2-SHARE
======================
In the following example the variables are:
- username: dshow
- user-id: 1000
- local folder: /mnt/iserv/
- remote folder: https://subdomain.iserv.de/remote.php/webdav
  
To create a automounted folder in the directory */mnt/iserv* for a user follow these steps:
> `mkdir /mnt/iserv`
>
> `chown dshow:dshow /mnt/iserv`

In Raspbian it was neccessary to reconfigure davfs to allow all users to mount the drive:
> `sudo dpkg-reconfigure davfs2`
>
> --> allow all users to mount --> yes

Add the user to the davfs group:
> `sudo usermod -a -G davfs2` 

Edit the file **/etc/fstab**:
> `sudo vi /etc/fstab`

	https://webdav.iserv.de/	/mnt/iserv/	davfs	user,uid=1000,gid=1000,rw,nofail	0	0

Edit the file **/etc/davfs/secrets**:
> `sudo vi /etc/davfs/secrets`

	https://webdav.iserv.de/	dshow	PASSWORD

Allow the user *dshow* to mount without a password:
> `sudo visudo`

	dshow       ALL=(ALL)       NOPASSWD: /usr/bin/mount

Login the user *dshow* if not happened yet:	
> `crontab -e`

	*/1 * * * * /usr/bin/mount -a

 
APP-FOLDER
==========
Clone the repository
> `mkdir /home/dshow/apps/`
> `cd /home/dshow/apps/`
> `git clone https://github.com/beachbatsch/diashow.git`
 
Mark the bash files executable:
> `sudo chmod +x /home/dshow/apps/diashow/*.sh`


Autostart
=========
To autostart the diashow create a *.desktop-file* in the folder * /home/dshow/.config/autostart*:

	[Desktop Entry]
	Name=Diashow
	Comment=Diashow
	Terminal=true
	Type=Application
	Exec=/home/dshow/apps/mp_diashow/start_scheduler.sh
