Title: Outlook Big Inbox Cleaner
Date: 2014-05-26
Modified: 2014-05-26
Category: Programming
Tags: Microsoft, Outlook, VSTO, Exchange
Slug: outlook-big-inbox-cleaner
Authors: Chris Zacny
Summary: Struggling with thousands of messages in your Outlook Inbox that you can't delete due to Exchange Server errors? Read this.

## Current Release ##
To clone / fork the current release of the Outlook Big Inbox Cleaner, please go here:

- <a href="https://github.com/chriszacny/OutlookBigInboxCleaner">https://github.com/chriszacny/OutlookBigInboxCleaner</a>

Please see README.md on that page for information on installation and setup. 

----------

## Big Data in Your Outlook Inbox ##

One of the trending buzzwords you'll hear lately is "Big Data". The concept of petabytes of data, or even exabytes of data being transferred across the world on a daily basis is something that wasn't fathomable ten years ago, and yet, here we are.

Today I'm going to present a tool that helps with a "Big Data" problem that is fairly specialized in Outlook. It isn't on the scale of petabytes or exabytes, but still deals with lots of data in its own right.

<img src="/static/img/blog_posts/outlook_big_inbox_cleaner/inbox.jpg"></img>

As you can see in this screenshot, I have 47,967 unread e-mail messages sitting in a folder. Oops! Obviously, these e-mails could have been funneled to my **Deleted Items**, or some other folder via an automated rule, but I neglected to set that up; in this case, I was planning on monitoring these particular messages in a certain fashion for project X, but I was pulled into other projects, so I never ended up having to worry about project X.

When I noticed the folder getting very large (as in, tens of thousands of messages), I attempted to **Delete All**, but this led to an error: 

<img src="/static/img/blog_posts/outlook_big_inbox_cleaner/memory.jpg"></img>

I had some options in an attempt to fix this:

1. Contact my Exchange administrator and try to get them to help clean up my mailbox. 
2. Manually select batches of items and delete them.
3. Write an Outlook Addin that selects items in batches and deletes them for me. 

Naturally, I went with item 3. I didn't choose 1 because this was a non-critical issue not worth bothering our Exchange folks with; it was just annoying to see an ever-growing folder in my inbox getting bigger and bigger, and it was probably slowing my Exchange account down. 2 wasn't viable in terms of my time. 3 seemed like the best choice; indeed, it only took me an hour or so to put together.

Here is what I ended up with:

<img src="/static/img/blog_posts/outlook_big_inbox_cleaner/ui.jpg"></img>

As you can see, I created a new tab called **Cleanup**. In that tab, I defined a button called **Cleanup Selected Folder**, which effectively tosses up a prompt asking whether you want to continue. Then, it deletes items in the batch size you set in **Batch Size**, waits for 3 seconds, and does it again. You can also select **Delete Permanently** to delete the items forever; without this, the items just get sent to **Deleted Items** which wouldn't be all that great because you will just have moved x-number of messages to **Deleted Items**, in which you'd probably just get an out of memory error when you attempt to delete the messages like before. So when cleaning out big, useless folders, I usually tick this.

This is sort of a "fire and forget" Addin. You accept the prompt stating that you want to delete the mail items, and it starts running. I left it on overnight for two nights and by the second night, it had cleaned up the big 47,000 item folder. Woohoo!

## Technical Details ##
This really is a pretty simple addin, but it follows (and breaks) a few rules that go with developing Outlook Addins. 

To start, I created a new Visual C# Outlook 2010 Add-in project using Visual Studio 2012. This sets up the shell to automatically deploy the Addin at build time to Outlook. I then went ahead and jotted my UI down on some paper; I realized I wanted a Ribbon interface, but I didn't want to mess with the current predefined Microsoft one in order to try and stay isolated (for example, attempting to modify the Home tab). This meant I would need to set ControlIdType to Custom on my new Ribbon tab. One thing I struggled with for a few minutes, as it had been awhile since I'd written an Outlook Addin, was getting the actual new tab to **show up**. It is important to remember what type of Outlook item you are applying the ribbon to; by default I think it applied it to the Microsoft.Outlook.Mail.Compose Inspector. But I wanted it applied to the main Explorer window. So I had to do this:

<img src="/static/img/blog_posts/outlook_big_inbox_cleaner/set_to_explorer.jpg"></img>

At that point, when I compiled and built the project, it started showing up in the place I expected it to; namely, the main Outlook Explorer window.

After I got that working, it was just figuring out how to get the proper folders and such to do the deletion of the appropriate MailItem objects.

The code is fairly self-explanatory, so if you clone it via GitHub, it should be easy to follow along. However, as mentioned, I follow and break a few rules of Outlook Addin development.

## Rules I Follow ##

One good practice to follow when working with large numbers of COM objects in Outlook Addins is "release them" using [Marshal.ReleaseComObject()](http://msdn.microsoft.com/en-us/library/system.runtime.interopservices.marshal.releasecomobject.aspx). Effectively, every time you reference one of these objects, its reference count is increased via a Runtime Callable Wrapper (RCW) associated with it, and once finished working with the object, you need to manually decrement the reference count in order to properly trigger garbage collection on it. There are varying opinions on this. Whenever you start messing around with reference counts and such, you can end up screwing yourself over; for example, when working on our InterAction Outlook Addin back at LexisNexis, I specifically remember one case in which I released the primary Explorer COM object; when I subsequently attempted to access it again from another part of the Addin, I received an exception (can't remember which at the moment; the documentation indicates either NullReferenceException or InvaidComObjectException), but effectively, I had rendered the entire Addin invalid at that point. Luckily this was in development / debugging. So you need to be cautious about what COM objects you are going to release. In my case, I release almost all of them because I'm deleting them in one big loop. If I didn't, I'd imagine memory would balloon up fairly quickly; especially in an Addin like this one, in which we are referencing tens of thousands of COM objects. Actually, that would be a good experiment to run when I have time; remove the [Marshal.ReleaseComObject()](http://msdn.microsoft.com/en-us/library/system.runtime.interopservices.marshal.releasecomobject.aspx) calls and see how it affects memory on a large folder. I should note - I *have* seen outlook.exe crash once when using this Addin after running for an extended period of time. I haven't had time to thoroughly diagnose yet; my suspicion is that it is because of:

1. Some sort of access violation due to calling [Marshal.ReleaseComObject()](http://msdn.microsoft.com/en-us/library/system.runtime.interopservices.marshal.releasecomobject.aspx). As mentioned in the documentation for that method, I am guessing something is attempting to access a COM object right as I am releasing it, as mentioned in the documentation. 
2. The rule that I break, which is mentioned in the next section.
3. A combination of 1 and 2.

At this point though, I've cleaned up my Inbox, so I am moving on to other things. Perhaps if I have more time in the future, I may come back to this.


## Rules I break ##

When developing Outlook Addins, one of the "rules" that you'll typically hear is to only access UI objects on the main thread. I've also heard that you should only access COM objects on the main thread. This means, that for most operations, you are restricted to the main thread for pretty much everything. Following on that, with an application like mine, you'll end up holding the UI thread pretty much continually, making Outlook unresponsive. If you don't follow this rule, and end up using multiple threads to access COM objects in Outlook, apparently, unpredictable Outlook crashes can occur. So I was kind of in a catch-22 - if I followed the advice stating to only use the UI thread, Outlook would become unresponsive because I only would have one thread to work with when deleting Outlook items (I know this because I tried it first, and that is what happened). If I didn't follow the advice, I could end up with unpredictable crashes. In this Addin, I decided to risk it in favor of still being able to control Outlook, and do all of the deleting of the Outlook MailItem objects from a background thread, which is probably why I crashed as mentioned earlier. 

## Conclusion ##
Hopefully if you ever end up in a situation like me with a giant Inbox, and you don't want to bug your Exchange admin for help, you can just load up this Addin and let it run overnight for a few nights. 

At the moment, you'll need Visual Studio to compile and build the Addin, but if you end up needing to deploy it, shoot me a message and I can attempt to come up with an installer, or at least a deployment process for the addin, in addition to some debugging.

And finally, **use caution** when using this Addin. It is *very* experimental, comes with no warranty, if it blows away all your data I am not responsible yada-yada... be careful!