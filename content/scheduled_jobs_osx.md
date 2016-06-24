Title: Scheduled Jobs in OS X
Date: 2015-02-06
Modified: 2015-02-06
Category: Programming
Tags: OS X, Mac, Scheduled Jobs
Slug: scheduled-jobs-in-os-x
Authors: Chris Zacny
Summary: Interested in scheduling jobs in OS X using launchctl? Read this post.

<img src="/static/img/blog_posts/scheduled_jobs_osx/gear.png" class="blog-img-center"></img>

## Overview 
This past week, I wanted to schedule a simple shell script to run once a day at 12PM on my Mac. I was kind of surprised at how much was involved; I expected some sort of easy GUI method, but there did not appear to be one. Here is what I did to get it to work. I am going to demonstrate a toy script, but obviously you could run whatever you need via this method.

## Walkthrough
1. First, create your shell script: 

		:::text
		cd ~
		mkdir greetings_script
		cd greetings_script
		touch myscript.sh
	
2. In this case it could be something simple like:

		:::text
		#!/bin/bash
		touch ~/testingfile.txt
		echo "Greetings" >> ~/testingfile.txt

3. Using your text editor put that text into **myscript.sh**

4. Make the script executable: **chmod +x myscript.sh**

5. Make a file called com.example.GreetingsScript.plist: **touch com.example.GreetingsScript.plist**

6. Using your text editor, put the following into **com.example.GreetingsScript.plist**:

		:::xml
		<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
		<plist version="1.0">
		<dict>
			<key>Label</key>
			<string>com.example.GreetingsScript</string>
			<key>Program</key>
			<string>/Users/czacny/greetings_script/myscript.sh</string>
			<key>UserName</key>
			<string>czacny</string>
			<key>StartCalendarInterval</key>
			<array>
			  <dict>
			    <key>Minute</key>
			    <integer>0</integer>
			    <key>Hour</key>
			    <integer>12</integer>
			  </dict>
			</array> 
		</dict>
		</plist>


7. As you can see, this is effectively a control file for a scheduled task. **Label** is required, and in this case because we are running a program, **Program** is also required. As a note, **you will need to change the Program and UserName keys to match your environment**.

8. Copy this xml file to /Library/LaunchDaemons: **sudo cp com.example.GreetingsScript.plist /Library/LaunchDaemons/**

9. Run launchctl to "load" the plist file into the list of scheduled jobs: **sudo launchctl load /Library/LaunchDaemons/com.example.GreetingsScript.plist**

10. You will receive no output from the 'launchctl load' command, but you can verify that it loaded the file by running the same command again. In this case you will receive "Already loaded" in your output.

11. Now, wait until 12PM. At that time you should see a ~/testingfile.txt file get created, with the output "Greetings" in it. 

## Notes and Explanations
1. There are actually several ways to run shell scripts on a scheduled basis. You apparently can still use cron, which is my normal perferred method on nix-based machines, but note that cron apparently uses launchd behind the scenes. You can also use the Automator app to create a workflow, and then load that into the Calendar app as an alarm action based on a time, but I personally kind of hated that after trying it.

2. If you modify your plist file after it has been loaded; you will need to use launchctl to **unload** and then **load** it again for your changes to take effect. At least, that was my experience when I tested it.

3. If you want to test your job immediately when you run **launchctl load**, you can put this in your plist file:

		:::text
		<key>RunAtLoad</key>
		<true/>

4. The options for StartCalendarInterval are a lot like cron. One annoying thing however, is that if you only want to run a job on Sunday, Monday and Tuesday, you'll need to do something like this (hence the array):

		:::xml
		<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
		<plist version="1.0">
		<dict>
			<key>Label</key>
			<string>com.example.GreetingsScript</string>
			<key>Program</key>
			<string>/Users/czacny/greetings_script/myscript.sh</string>
			<key>UserName</key>
			<string>czacny</string>
			<key>StartCalendarInterval</key>
			<array>
			  <dict>
			    <key>Minute</key>
			    <integer>0</integer>
			    <key>Hour</key>
			    <integer>12</integer>
			    <key>Weekday</key>
			    <integer>0</integer>
			  </dict>
			  <dict>
			    <key>Minute</key>
			    <integer>0</integer>
			    <key>Hour</key>
			    <integer>12</integer>
			    <key>Weekday</key>
			    <integer>1</integer>
			  </dict>
			  <dict>
			    <key>Minute</key>
			    <integer>0</integer>
			    <key>Hour</key>
			    <integer>12</integer>
			    <key>Weekday</key>
			    <integer>2</integer>
			  </dict>
			</array> 
		</dict>
		</plist>


## Helpful Links
* <a href="https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/launchctl.1.html" target="_blank">launchctl reference</a>
* <a href="https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html" target="_blank">plist file reference (helpful when you need to construct your own plist files)</a> 
* <a href="http://apple.stackexchange.com/questions/46368/whats-wrong-with-my-launchctl-config" target="_blank">Reference to plutil, which can be used to debug errors in plist files</a>
* <a href="http://alvinalexander.com/mac-os-x/launchd-plist-examples-startinterval-startcalendarinterval" target="_blank">StartCalendarInterval examples</a>
* <a href="http://nathangrigg.net/2012/07/schedule-jobs-using-launchd/#quick-start" target="_blank">Another tutorial</a>
