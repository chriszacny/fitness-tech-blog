slugname: adventures_in_arch_linux
title: Adventures in Arch Linux
date: 2014-09-02
author: Chris Zacny
category: Programming
tags:
  - linux
  - wizardry
  - adventures

<img src="/static/img/blog_posts/adventures_in_arch_linux/archlinux-logo-dark.png" class="blog-img-center"></img>

    :::python
    def test():
      one = 1
      two = 2
      one + two

As a technologist, I love tinkering and messing around with all kinds of stuff. I continually run some variant of the big 3 OS's out there at home - OS X, Windows, and Linux. The varieties I run depend on latest release cycles, and what I intend to do with the system. Lately, I've been getting a lot more into command line programming and have slowly been moving away from the GUI when engineering software. Specifically, I am an intermediate [emacs](http://www.gnu.org/software/emacs/) user and have been having lots of fun customizing it to fit my working style.

I wanted to switch to a modern Linux distro that wasn't so focused on beginning Linux users and usability ([Ubuntu](http://www.ubuntu.com), [Mint](http://www.linuxmint.com)), but more on advanced Linux users and systems programming ([Slackware](http://www.slackware.com), [Arch Linux](https://www.archlinux.org)). I had tried Arch before and liked it a lot, but never got totally into it due to time constraints and other projects I'd been working on.

I decided to give it another go; this time running in [VMWare Fusion](http://www.vmware.com/products/fusion) (I purchased the Standard Edition) on my MacBook Pro. My intent for this system is:

* Have a system that could be more of a "sandbox" development environment that I wouldn't have to be too worried about trashing (whereas in OS X, I always think, "Hmm... I wonder if installing development package X is going to mess up Y"). A VMWare instance of Arch would be perfect for avoiding this fear.
* To gain more fine-grained control of everything. The advantage Arch has here, is being able to easily install an incredible array of development tools exactly to my linking, and then configure them with the same amount of versatility. With OS X, you get lots of stuff installed and configured for you; good stuff for an awesome GUI and an extremely stable system, but not so much for an experimental development environment.
* Keep my reliance on a GUI to a minimum (not because I don't like GUIs; quite the contrary, but because I'd rather use OS X for that function).
* Become very proficient using emacs such that I have one powerful cross-platform text editor in my toolbox.

My original goal was to use OS X's GUI for building and testing GUI apps and web pages; Arch would become my text editing environment for more low-level development. I'd effectively have the best of both worlds, simply running Arch in its own Mission Control window, and my pure OS X stuff in the others. In the end, I did actually set up a GUI in Arch, albeit rather barebones. Here was my setup experience.

#VMWare Fusion Setup
The setup of VMWare Fusion was pretty much the same as any other OS X application; a simple double-click of the dmg file (and I think I dragged the application into the Applications folder). Once it was installed, I used its friendly UI to set up a new VM with 2 CPU cores, 4 GB of RAM, and 60 GB of Hard Disk space. In addition, I set my guest OS to be: Other Linux 3.x kernel 64-bit.

At that point, I was able to download the latest release of the Arch Linux iso from [here](https://www.archlinux.org/download/) and connect it to the CD / DVD drive of my VM. I then powered on the VM, and was greeted with the Arch Linux Live CD Boot Menu.

#Arch Linux Installation
There are a lot of great things about Arch, but one thing that it really has going for it is its user community and documentation. In fact, when I'm doing a web search for something Linux-related (a general non-distro-specific query), I'm starting to see the Arch Linux wiki near the top of the search results, if it isn't already at the top. So the documentation isn't just beneficial to Arch users; rather, its beneficial to the Linux community as a whole.

That's a good thing because overall, the setup process for Arch is not trivial. You are basically given the reigns to set your system up however you want. That said, I think it is completely doable for anyone with basic command line familiarity. Just make sure you have a second computer close by with this page up in your favorite browser: [The Beginner's Guide](https://wiki.archlinux.org/index.php/Beginners%27_guide).

In my Arch "build", I decided to accept default values where appropriate; as an example, I didn't make separate root and home partitions, (which ultimately caused a problem with GRUB that I mention below).

I did run into a few hiccups though.

* After partitioning and formatting my disk (preconfigured by VMWare as a SCSI disk) using the ext4 filesystem, when I attempted to mount it, using **mount /dev/sda1 /mnt**, I received the following error: *WRITE SAME failed. Manually zeroing.*
    * Basically, per this [VMWare blog post](http://blogs.vmware.com/vsphere/2012/06/low-level-vaai-behaviour.html#more-3129), WRITE SAME is a standard SCSI command to zero out large blocks of the disk. The post specifically mentions that this needs to be enabled on this disk. For me, this was clearly not enabled. However, I couldn't figure out how to enable it in Fusion... It's possible I missed some totally obvious setting. That being said, I solved this by switching the disk type from SCSI to SATA in Fusion. I also set my virtual hard disk to preallocate all needed disk space up front. I am unsure which of these two things got me past the WRITE SAME problem, but my bet would be me changing the disk type to SATA. I wasn't really concerned with using one vs. the other (they both have their pluses and minuses), so switching to SATA for this build was fine from my perspective.
* I missed out on using the GRUB bootloader (what I usually use for my bootloader) because I failed to notice [these instructions](https://wiki.archlinux.org/index.php/Beginners%27_guide#Partition_scheme) in the Beginner's Guide when partitioning... you need to create a 1-2MB BIOS Boot Partition in addition to your primary root partition for GRUB to use. Since I went through the entire installation without doing this, I just decided to go with syslinux vs. starting all over.

#Arch Linux Configuration

## Emacs
When I attempted to install emacs, I was greeted with this message:

<img src="/static/img/blog_posts/adventures_in_arch_linux/setting-up-emacs.png"></img>

So I effectively had three choices. Well, actually four. I decided to CTRL-C and back out... and do some research to see what sort of graphics driver was installed on the system. It appeared to be a VMWare SVGA II Adapter. I was hoping to get some sort of passthrough from my NVIDIA card on the MacBook, but no such luck (yet). So I went with the standard mesa-libgl package, as that seemed to be the "default" libgl provider.

Once that was installed, I had emacs up and running. But it looked... bad. I tried applying a standard theme included with emacs (I like wombat), and it didn't change anything, no colors, nothing. I quickly came to realize that the limited amount of colors and symbols in the standard terminal installed in the Arch kernel made things really, well... ugly. Not to mention lack of anti-aliased fonts and such. The other big problem with just using the standard terminal is the lack of scrolling support. I started messing around with [fbterm](https://wiki.archlinux.org/index.php/Fbterm), which is definitely a promising option, but I backed out due to time constraints.

## Xorg
At this point, I realized the best option would be to install a lightweight GUI with full color support and such. It would also be helpful to have the ability to have multiple terminal windows / emacs sessions open.

To get this going, my first order of business was setting up an Xorg server; however, it didn't go very smoothly. The pacman installation failed when I attempted to do **pacman -S xorg-init** it complained about not being able to find xorg-init on any of the mirrors I was pointing at. However, I quickly came to realize this was likely because I hadn't synchronized with the repository databases for a few days, so I went ahead and did a full upgrade: **pacman -Syu**. I then tried to run **startx**.

It failed with a Segmentation Fault.

After some research I found that this was a potential bug that was just introduced with the official xf86 VMWare driver that was installed by arch. Therefore, I had to venture to the Arch User Repository (AUR) to get a packaged up community version that apparently didn't have the problem. This was all discovered via [this thread](https://bbs.archlinux.org/viewtopic.php?id=185006). I wget'd the driver from there and decided to store my AUR stuff in /opt. Once I had done some chmod-ing to allow my user to write to that location, I untar'd the tar.gz file, cd'd into the untar'd directory, and ran **makepkg**. Stuff started flying across the screen at a billion miles per hour, and being in a non-scrolling window I couldn't tell if there were stack traces or not; it looked like there were some, but I couldn't say for sure. I decided to rebuild using **makepkg -L** and investigate what the heck happened.

Indeed, when I re-ran and examined the build log, there were a ton of C++ compiler warnings, but they all looked to be benign, such as un-needed / un-used declarations and such. After I verified everything, I did **pacman -U xf86-video-vmware-git-20120327-1-x86_64.pkg.tar.xz**. Once that was installed, I tried **startx**, and did not receive an error. I was ready to move on to installing an actual desktop package at this point.

## Gnome
Now for the big decision. I always liked KDE because of the bells and whistles it provides, but felt that Gnome was lighter weight and more simplistic all around. Since lighter weight was definitely what I was trying to go for, I went with Gnome. The nice thing about the "big" desktop environments is that they allow you to install one package, and pretty much everything you need gets installed for that environment. In this case, I did: **pacman -S gnome**. You get a bunch of stuff with this package. I went ahead and accepted it all instead of picking and choosing... better to just get it working and then try and remove what I didn't need. The total download was ~200MB and installed size was ~1.1GB. Not too bad for a GUI desktop these days.

## Startup Configuration
Once that install was done, it was time to start configuring startup behavior since on Arch, GUIs don't just magically start themselves unless you instruct them to. Here is what I did:

1. Checked to make sure gdm.service was able to be started via systemctl. I did this by checking if its unit was installed appropriately by going to: /usr/lib/systemd/system. Sure enough, it was there.
2. I then ran **systemctl enable gdm.service**.
3. Finally, I rebooted.

## In the GUI
To my surprise, the GUI was nicely minimalistic. Here's my current desktop after switching the background and changing resolutions:

<img src="/static/img/blog_posts/adventures_in_arch_linux/basic-gnome.jpg"></img>

Emacs now looked much better. I was able to quickly switch to the wombat theme, set custom fonts, and go from there. Because it worked out of the box (aside from the Xorg problem) and was nicely minimalistic, I was completely fine with booting into Gnome. Pure server-based environments make sense to keep GUIs out of, but in this case, Gnome added to my experience. Here is emacs with the basic wombat theme applied:

<img src="/static/img/blog_posts/adventures_in_arch_linux/basic-emacs.jpg"></img>

## Other Cool Things to Note

* Using VMWare, I didn't have to mess around with wireless networking! I booted up the Arch iso, typed **ping www.google.com**, and received responses back! Hooray! It all just worked as a virtual wired connection via the pass through network adapter VMWare sets up on the machine.
    * Tinkering with finicky wireless network connections is hands down the single one thing I have spent the most time on across all Linux distributions. I'm not sure if I'm alone in this, but I have seen other users complain too... so I'm guessing not. The fact I didn't have to mess around with it was a huge win for using VMWare Fusion vs. setting up a Dual Boot strategy.
* Take a look at the base Arch system you get (you can whittle it down further if you want):

<img src="/static/img/blog_posts/adventures_in_arch_linux/basic-arch-packages.jpg"></img>

* Pretty minimal, right?

## Required Maintenance
Arch Linux is not a fire and forget sort of OS. Because of its [rolling release cycle](), new core changes are pushed out all the time, and if you don't regularly upgrade and deal with potential problems, you will most likely try to install a package at some point, and then be left with a massive upgrade that will likely cause issues. For a reference, see my experience just trying to install xorg-init above. I had setup the base system, maybe two days before I attempted to install the package, and I was already out of date!

For a developer machine, managing weekly upgrades is probably OK... especially if I utilize VMWare's snapshotting functionality, or potentially even [Docker]() (preferred in my mind at the moment due to being able to isolate system changes similar to a version control system). I'm probably going to try getting Docker going next and see how that goes. And of course, after the first couple manual Arch upgrades, I'll probably just automate it.

## Next Steps
I am concerned about the AUR driver installed on my system communicating with X, but with this OS, I suppose it is something I'll need to get used to, in addition to watching for general notes about big upgrades from the [news feeds](https://www.archlinux.org/feeds/).

In regards to emacs usage, I'm definitely not a purist. I actually like that once I got the GUI installed, I could use the emacs menus and such. They are there for a reason. In addition, once I get emacs down really well and can use it as my standard hacking / notepad environment, I'll probably install fully-fledged IDEs onto the system such as PyCharm because those have a ton of value too in terms of enabling rapid development. Use the right tool for the job.

From a general Arch perspective, I'm going to continue configuring / reading the wiki and potentially try to start contributing; this is a great OS, but because it is so bleeding edge and frequent updates are required on the part of the user, it is not for the faint of heart. Despite that, you get to use all of the latest and greatest tools in a stable, fully-customizable environment; which for me, is just what I am looking for.
