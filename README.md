# Cross Platform Installer
A cross platform program installer designed for beginners to get used to linux.  
It works with BASH, ZSH and FISH shells.  
This is the TUI version a gui version is available at:
```
https://github.com/arcnet-cyber/linux-program-installer-gui
```
  
## Implemented Package Managers and Distros

- Pacman
  - Arch Linux✔️
  - Manjaro✔️
  - EndeavourOS✔️
  - Garuda✔️  
- Apt
  - Debian✔️
  - Ubuntu✔️
  - Linux Mint
  - Pop!_OS✔️
  - KDE Neon✔️
  - Kali Linux✔️
  - Parrot OS✔️
  - Bodhi Linux✔️
  - Peppermint OS❓
  - Deepin❓
  - Ubuntu MATE✔️
  - Xubuntu✔️
  - Lubuntu✔️
  - Ubuntu Budgie✔️
- ZypperPacm
  - openSUSE Leap❓
  - openSUSE Tumbleweed✔️
- DNF
  - Fedora✔️
  - CentOS✔️
  - AlmaLinux✔️
  - Rocky Linux❓
- XBPS
  - Void Linux✔️
  
Ticks mean theyre tested by me personally.  
Question marks means it might not work on the full version because i was using LIVE iso's in testing.


If a listed Operating system doesnt work Post it in the issues and I'll try and fix it. Just because it's implemented doesnt mean its functional.


## Installing

### Git-clone method

```
git clone https://github.com/arcnet-cyber/linux-program-installer.git
cd ~/linux-program-installer/XPlatformInstaller
chmod +x setup.sh
chmod +x uninstall.sh
./setup.sh
```
Then reboot your terminal.  
The alias "installer" should then be added.  
Executing "installer" in your Terminal should run the program

### Manual download

1. Download the folder and using terminal, Navigate to its downloaded location (Usually ~/Downloads) and then into its deeper folder called XPlatformInstaller
2. Type the command below to install dependancies and add the alias for you to type into terminal

```
./setup.sh
```
The alias "installer" should then be added 
Executing "installer" in your Terminal should run the program


## Uninstalling

Run uninstall.sh to remove the alias and project files

## Dependancies

So this only runs using shell commandsand Python3 so easy enough to install and test out.
The install.sh script will install the dependancies for you.


## How does it work?

On most linux distributions there is a file at /etc/os-release that has your OS information on it.  
All this program does to help you easily install your programs is read that file and has a list of different package managers and their commands thus streamlinig it

## Why bother when you could just learn the commands?

Because I like distro hopping and sometimes I can't be fucked to learn the commands straight away  

Simple as that


## Current things i find being an issue right now
- [x] Fix void compatibilty
- [x] Fix DNF Visuals
- [x] Add the ability to uninstall files using the cross package mananger

> Still definitly a work in progress but will convert to lower level languages when i can be bothered
