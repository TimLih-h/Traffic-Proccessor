### Sprint review transcript

**00:00:00 Speaker 1**
Okay.

**00:00:00 Speaker 2**
Well, we have here, so to speak, a test. Well, even two tests. This is simply a traffic generator, you see, for a completely new domain.

**00:00:16 Customer**
Uh-huh.

**00:00:17 Speaker 2**
If we take it, if we add this topic, yes, now, if we take, say, this domain, it should start showing up very heavily in the traffic, so that there are about 1,200 packets, right?

**00:00:34 Customer**
Uh-huh.

**00:00:35 Speaker 2**
And I wrote something like that and sent it.

**00:00:39 Customer**
Uh-huh.

**00:00:40 Speaker 2**
But this is for this case, right? Are there any questions on your side?

**00:00:54 Customer**
Yes, the only question is to clarify: there it's 63–64 Mbit or Mbyte?

**00:00:59 Speaker 1**
Megabits.

**00:01:00 Speaker 2**
Megabytes.

**00:01:03 Customer**
Okay.

**00:01:05 Speaker 2**
But there is one problem, right? We need to reassemble it a little differently. We have this, yes. If we try to test it on some torrent, right? Wait a moment. There is still, okay. So. Well, here, let's say, she's writing now, I'll show this now, well, and here it goes, it's working.

**00:01:34 Speaker 2**
Uh-huh. Let's say, let's take Torrent, right? Uh-huh. How it's now, the traffic is passing through, yes, and Torrent, here's my container on the Torrent host, and now, hopefully, it will start, I don't know anymore. Okay, well, but it, well, you know, it's, well, yes.

**00:02:12 Speaker 2**
So, as we can see, it shows here 20–20 Mbit per second, right? But the traffic processor itself, as it were, as if it can't hold that much, and on the contrary, its speed drops.

**00:02:28 Speaker 3**
Uh-huh. Show the table with IPs? Oh, well, yes, so, there's a lot there. I'll be right there, they're all writing. Okay.

**00:02:44 Speaker 2**
And well, the problem is that, well, yes, the main task is that first it works normally, it handles speeds up to 1 Mbyte. Then further on, on the contrary, its speed starts to drop. Well, this is, as it were, our question here, right? Maybe then, well, go ahead, you say it.

**00:03:05 Speaker 3**
When we check the throughput of the module using a direct test, often with TCP packets or just UDP, it works stably. With TCP you saw, it shows very large values in volume, and in packets, 1,200.

**00:03:39 Speaker 2**
By the way, right now it's working on TCP.

**00:03:42 Speaker 3**
Got it. UDP is also counted there, and there are just more of them, because well, in short, with UDP, since it counts about 2,000 packets per second, and in memory, this amounts to a volume of a solid 20 Mbit per second. But when we run this with a large application, where the traffic is very diverse and heavy, apparently, it cannot fully withstand all the patches and starts losing packets very heavily. That is, the main thing is that the traffic, specifically in this example, should be no more than 2 Mbytes per second.

**00:04:48 Speaker 3**
So our question is rather this: does this speed limitation suit you for internet speed?

**00:05:04 Customer**
Well, 16 Mbit.

**00:05:05 Speaker 3**
Yes.

**00:05:07 Customer**
Well, overall it's fine. The only thing is, if there is such a limitation, then we need to figure out, in a more or less plausible way, a more or less realistic reason for why this is happening. That is, where exactly, at what specific stage does this shortfall in packets occur? Is it specifically the traffic processor, or some specific library that monitors the network and can't count everything, or specifically the traffic processor can't count everything, or specifically, well, the traffic processor and the library, and the traffic processor all manage to do things in real time, it just doesn't have time to send the data to the server. That is, even if there is such a limitation, then it's okay. Well, it might be fine. But if this limitation remains, then we need to understand for what specific reason it appears, what the bottleneck is there.

**00:06:11 Speaker 3**
Yes, this is in the process, we'll fix it — this is not mandatory, but at least to know what specifically is the problem.

**00:06:21 Customer**
That's good, yes, good. And here you are currently testing on the example of a torrent, correct?

**00:06:27 Speaker 3**
Yes.

**00:06:27 Customer**
So you can, for example, pause it?

**00:06:33 Speaker 2**
Yes. All right, yes.

**00:06:37 Customer**
And here, can you, right-click or somehow set a limit on the download speed, the upload speed?

**00:06:42 Speaker 2**
Well, here I set a limit. Well, here, 1 MB. Uh-huh. It seems so, yes, but I don't know how. Ah, yes, I'll pause it now.

**00:07:19 Customer**
Well, overall it's fine. The only thing is, if there is such a limitation, then it's okay, well, it might be fine. But if this limitation remains, then we need to understand for what specific reason it appears, what the bottleneck is there. Well, here, yes, yes. Here, at 10. It seems. Well, I can't quite see, the font is really small there. And I can't quite see, do the torrent numbers match the numbers?

**00:07:27 Speaker 3**
Well, no, they don't match.

**00:07:30 Speaker 2**
Ah, well, they don't match. Well, here, well, 1,000, maybe there.

**00:07:32 Customer**
But there, look, in the torrent it's 1,000 of what, kilobits or megabits?

**00:07:35 Speaker 3**
Ah, yes, yes, it's 1,000 kilobits there.

**00:07:39 Customer**
Okay, try reducing it from megabits, from megabytes down to, say, 100?

**00:07:54 Speaker 2**
Yes.

**00:08:04 Speaker 3**
Well, here you go. Now it's 500.

**00:08:07 Customer**
Try reducing it to 100 more.

**00:08:11 Speaker 1**
Well, it's not a fact that Torrent adds, yes, I'm thinking about it.

**00:08:15 Customer**
Well, if it displays, well, at least.

**00:08:19 Speaker 1**
Here, on the screen, there's something like, say, 100, or

**00:08:23 Speaker 3**
Right now we have 182 here, well,

**00:08:32 Customer**
Well, what? Well, the good news is that there is a correlation between these numbers.

**00:08:39 Speaker 3**
Yes.

**00:08:41 Speaker 3**
And we spent a lot of private time trying to understand exactly where that bottleneck is. It's not entirely clear yet. Because not with the torrent, but with the point test, everything matches exactly, down to the units.

**00:09:10 Customer**
And another question, well, maybe then it's a feature of Torrent, that it uses some custom protocols there? Well. And another question: on video or audio streams, did you test not on torrent?

**00:09:27 Speaker 3**
No, we haven't had time yet. Well, we can run it this week and make a small video with this, or just report back.

**00:09:41 Customer**
Well, yes. Yes, that would be good. Okay. In video players, there is usually system statistics. That is, inside the video player settings, you can enable video statistics or administrative statistics, or statistics for system administrators, which just show, for the selected quality of that video or audio, what its bitrate is. That is, and there too, see if there is a correlation between the highest quality, the highest bitrate, what looks similar here, and the lowest. Because, well, classic streams, like video calls, or specifically video broadcasts of TV channels online, just video or online streams. They use more classic technologies, in the sense that they use more honest TCP, and it can perform better, unlike torrent. The fact that Torrent is fast—Torrent can use custom protocols for speed, which, well, yes, are poorly counted by you.

**00:11:05 Speaker 3**
Got it. So. Well, let's try. Well, we have, sorry, classic topics, to be sure for any user, and now there are four of them.

**00:11:20 Customer**
Well, great, great.

**00:11:22 Speaker 3**
So. And also an important clarification: before this, we showed you a gateway that can block traffic by IP. During this week in the course with FreeTA, we came to the conclusion that we cannot attach it to the Java-based paid applications so that it works correctly. Therefore, everything related to the proxy was removed, and at the moment it's simply scanning traffic with reflection and splitting by IP. That is also an important clarification. And in general, this entire functionality for changing the target is quite convenient; it's enough to just merge two configuration files and specify in three places the name of the target container, and everything works. So it's convenient and practical.

**00:13:02 Customer**
The main thing is not to clarify which definition of convenience we are using.

**00:13:06 Speaker 3**
Yes, yes. All right.

**00:13:07 Speaker 1**
Okay. Thank you.

**00:13:09 Customer**
Okay.

**00:13:10 Speaker 3**
So. Well, for the demonstration, yes. Those, about the Assembly.

**00:13:17 Speaker 1**
Yes. I'll send you what you need to ask. Yes, we need the customer-facing documentation repository.

**00:13:34 Speaker 3**
Documentation and its appearance were not a priority so far. The main efforts all went into development, so the README that greets us is not the full version; it will be finalized by the release.

**00:14:04 Speaker 2**
Well, as it were, the chief editor.

**00:14:06 Speaker 3**
Yes.

**00:14:06 Speaker 1**
Yes, so far it's very brief instructions, there shouldn't be any development ones, but well, in general, that's it for people.

**00:14:09 Speaker 2**
Well.

**00:14:18 Customer**
The most important question: have you run your own instructions on a clean machine? That is, if I take my own server or my own machine and repeat everything, will everything start up for me from the first time?

**00:14:35 Speaker 3**
Most likely, specifically for these questions, it won't happen right now. It needs some revision. Yes, which we will implement this week.

**00:14:51 Customer**
Well, can you open it on a phone if you have one?

**00:14:55 Speaker 2**
Ah, to you.

**00:14:58 Customer**
What do you mean? What are you? Let's share the screen, let's. What do you mean? Look, what we need to show in Telegram, show what we need on the screen.

**00:15:10 Speaker 2**
Ah. Okay, okay. So. Well, here we have this, I updated it. Okay, okay.

**00:15:36 Speaker 2**
Well, here. And what should be in this document?

**00:15:45 Speaker 1**
There should be the project readiness level, what we have, also what we need to do for the customer to accept our project, and also the instructions themselves, I remember.

**00:16:06 Speaker 2**
Yes, yes, but here it's all for the old version V2, which is in the history, but directly for the current one, it's not fully up to date, the latest changes are being made, so that also needs updating.

**00:16:33 Speaker 1**
Yes.

**00:16:37 Speaker 2**
Well, I can't really discuss it, right?

**00:16:42 Speaker 3**
Here, well. Without discussion, I suppose, what would you like to see?

**00:16:48 Speaker 1**
Well, okay, yes.

**00:16:52 Speaker 3**
What, are there any other functional details you would like to see that we can do during the time before the final release?

**00:17:05 Speaker 2**
Well, how long is it?

**00:17:12 Speaker 1**
One week.

**00:17:13 Speaker 2**
Well, one and a half.

**00:17:19 Customer**
Yes. Well, from what we discussed. We discussed quite a lot, I think. At the initial stages. From what we discussed there in a week and a half, what will be realistic to do.

**00:17:34 Customer**
The good thing is we need to finally identify the problematic area that is causing the problems. Perhaps the problematic area is the torrent. That is, we need to see how the processor, the traffic processor, behaves on other applications besides torrent. It will be possible to behave more adequately, well, more detailed. Yes. So. Further. Advanced statistics, there was that, correct?

**00:18:15 Speaker 2**
Database, data storage.

**00:18:17 Speaker 1**
Ah. So, yes?

**00:18:22 Speaker 1**
Well, there was historical data.

**00:18:30 Speaker 2**
Traffic modification.

**00:18:38 Speaker 1**
Traffic modifications or attacks. The gateway was exactly that.

**00:18:41 Customer**
Well, these are modifications, either blocking or allowing.

**00:18:44 Speaker 1**
Well, in reality.

**00:18:45 Speaker 3**
And for us, well, we will, in principle, make them, most likely, exactly everything related to, we, modifications, we won't be able to. But the history, the same database, I think we can manage to write during this time. For this, I will change the format of the data transmitted from the poster to the backend. And it will be able to keep a correct log by timestamps, what IPs, at what time, how much.

**00:19:32 Customer**
Why, yes? Needed. Well, yes, yes. We need to save the data when they arrive.

**00:19:38 Speaker 3**
Yes, in the current implementation, all global counters are maintained in the process itself. And if we save everything to a log now, every, say, 10 seconds, they won't be ready for analysis.

**00:20:09 Customer**
And do you have this directly with the processor? Does the frontend write?

**00:20:13 Speaker 3**
No, it transmits data to the backend, and the backend already outputs all values to the frontend. But roughly speaking, you could say so.

**00:20:30 Customer**
Well, you can compose it like this, well, that is, yes.

**00:20:32 Speaker 3**
Is there a specific or sample data format that should be entered into the database?

**00:20:44 Customer**
Yes, to store it for a long time, in general. Everything, everything we have now. The point is simply that when your frontend page refreshes, when you click here, all the data doesn't disappear. That is, it shouldn't reset to zero.

**00:21:02 Speaker 2**
Well, yes, of course, it gets saved, the rest

**00:21:05 Speaker 3**
For now, just, well, yes, it gets saved. It

**00:21:08 Customer**
Well, I understand. I mean that from the point of view of storing in the database, everything we have now is good to store. And there, well, from the frontend point of view, the first step will be to change nothing at all. Here. The next step, if you have time and you get to it, is to add a selection of the time window for which the information is displayed on the screen here. That is, in the first step, you don't change the frontend at all. Mmm, well, how much is it? 30 seconds? Right now, I understand, it's set to that.

**00:21:45 Customer**
Well, yes, yes. Well, so in the first step, we change nothing in the frontend. You query the database for a minute. Then, in the next step, you can slightly change the query so that what was 30 seconds, well, you know, a choice between 30 seconds, a minute, five minutes, ten, thirty, an hour, five hours, ten hours, twelve hours, well, that is, some kind of granularity.

**00:22:16 Speaker 2**
Probably, it's also worth adding the ability to, well, scroll the graph, right?

**00:22:22 Customer**
Well, that's the third stage, that's like advanced level.

**00:22:26 Speaker 2**
Yes.

**00:22:29 Customer**
Well, that is, yes. Initially, you have a fixed window for the last 10 minutes, well, current, for the last minute from the current point in time. The next is that from the current point in time, you vary the boundary that determines the size of the window. And the third stage is, indeed, when you detach the second boundary from the current point in time, and you can vary the window itself, both in size and in.

**00:23:03 Speaker 2**
Yes.

**00:23:05 Speaker 3**
What details are here? Is everything around it enough for now, or can we add more details about the traffic here and in the IP section separately?

**00:23:29 Customer**
Well, I think more details are not needed.

**00:23:36 Speaker 1**
Okay.

**00:23:37 Speaker 3**
So. When is the question? We also need to ask, are you using the product?

**00:23:59 Customer**
Well, already in the current one, yes.

**00:24:02 Speaker 3**
Well, yes.

**00:24:11 Customer**
Well, as it were, yes, but it never worked. They gave it to us, but we couldn't. Unfortunately. We have our own private VM, but it doesn't run 24/7. We don't have one for the report.

**00:24:21 Customer**
Well, okay. Maybe we could still get one?

**00:24:30 Speaker 3**
Well, yes.

**00:24:30 Speaker 2**
So, by the way.

**00:24:32 Speaker 3**
How can we increase the chance that our product will remain useful after the final test?

**00:24:33 Customer**
Well, at a minimum, figure out what the problem is with the torrent—well, not with the torrent, but with the traffic. So it's clear how much it's wrong and for what reason. Is it wrong at all, or is it just torrent glitches.

**00:24:54 Speaker 1**
So, feedback on the documentation.

**00:25:02 Customer**
Well, the documentation exists.

**00:25:05 Speaker 2**
Uh-huh.

**00:25:06 Speaker 3**
Requires refinement, okay.

**00:25:07 Speaker 1**
Yes.

**00:25:12 Customer**
So, we need to record: have you confirmed that our product is ready for independent use?

**00:25:27 Speaker 3**
Well, I think it's been three times already.

**00:25:28 Speaker 1**
If we do everything we need, well, everything we can plan for the next week and a half, will it be a finished product?

**00:25:38 Speaker 3**
Well, overall, I think yes.

**00:25:42 Customer**
The only thing is also regarding the traffic processor, take a look there. Probably even with this database, okay, I think probably even with this database, the less priority things, the more priority things, so that everything works exactly, starts up. Well, here. Using two commands: git clone and then docker compose up. For me, everything starts with two commands. The next point is specifically regarding connecting the traffic processor to different parts, to different other parts of the system, so that I could, for example, monitor activity of containers on two different machines. That is, the main server and frontend would run on the server, while the traffic processor would attach to different containers on different machines, and it would be relatively easy to change the data source. Ideally, it should change with one line.

**00:29:05 Speaker 1**
Theoretically, as an option, we can add arguments to the docker-compose, where one argument is the IP of the server somewhere there, and the second argument is the name of the container.

**00:29:17 Customer**
Well, in an ideal world, really in an ideal world, if the traffic processor has two things set. The first is how the traffic processor identifies itself, well, its name or its ID, something like that. And the second is indeed where it sends, I don't know what your model is. Which direction the data goes. Here. But if your traffic processor sends data to the server, then yes. The second thing is the address of the server to send the data to. Well, the sending address. And if this works so that I run on the server, well, on one dedicated machine that's online on the internet, I run all containers except the traffic processor, and then on the target machine, a single traffic processor is launched, where two lines are changed, that would be a good use scenario, the only thing is that it should work.

**00:30:19 Speaker 2**
Uh-huh.

**00:30:20 Speaker 3**
That is, this is above the database, this is in the gradation after figuring out the display problem, this is the second thing we should, in principle, do.

**00:30:31 Customer**
Well, because this falls under the scenario that the product works.

**00:30:37 Speaker 3**
Yes.

**00:30:38 Customer**
Without this, the product would be hard to call working, because it would be difficult to use in practice. The fact that data gets deleted there, but that's like it works until you press F5.

**00:30:56 Speaker 1**
Okay.

**00:30:58 Speaker 2**
We, by the way, need to add security to the server.

**00:31:04 Speaker 1**
Well, ideally, this server should be deployed on a VM, remote.

**00:31:09 Speaker 2**
Well, globally,

**00:31:10 Customer**
Well, globally no, because that's, well, in short, globally no. That is, it would be good to do, but it's not a priority. Because, again, when this is deployed inside the perimeter I need, I'll be setting it all up myself.

**00:31:39 Speaker 2**
Well, okay.

**00:31:42 Customer**
Good. For my own domains, in short.

**00:31:51 Speaker 3**
We'll have another one. This is the most important, this should be. Well, yes. Here, thank you.

**00:31:53 Speaker 1**
Another option is to let the customer play with it.

**00:31:58 Speaker 3**
Well, we've played with it. A lot. Do you want to play?

**00:32:00 Customer**
Here, can you open some stream in the container, audio or video. A live broadcast, there, through channels.

**00:32:11 Speaker 2**
Well, like, somehow

**00:32:13 Speaker 3**
Well, if you're ready to support it for 7–10 minutes. Well, we can, of course, do it differently, because right now we're connecting the product to a third-party project, in the form of

**00:32:31 Customer**
Well, okay. What is this called?

**00:32:39 Customer**
This is exactly what it is. The torrent that's running inside the container, and the traffic processor is monitoring this torrent client, correct?

**00:32:48 Speaker 3**
Yes.

**00:32:49 Speaker 2**
Well, the whole container, yes?

**00:32:50 Customer**
Yes. You can simply go inside the container and run a file download there via the console using wget or curl.

**00:33:01 Speaker 2**
This is Transmission, yes? So.

**00:33:05 Customer**
Well, find some one, this, well, type in the search there, Debian or Ubuntu ISO.

**00:33:13 Speaker 2**
Ubuntu ISO.

**00:33:16 Customer**
Make it bigger, so.

**00:33:17 Speaker 2**
And, ah, and, let's download it.

**00:33:21 Customer**
Copy the link.

**00:33:23 Speaker 2**
So.

**00:33:40 Customer**
No, well, click Downloads. And there, Other Downloads or something like that. Lower down. Some alternative downloads.

**00:33:53 Speaker 2**
Ah, ha-ha-ha. You could just clone some repo, for example, ours.

**00:33:56 Speaker 2**
Ah, well, let it be that.

**00:33:58 Customer**
Ah, it will take a long time.

**00:34:00 Speaker 2**
So. Maybe here?

**00:34:09 Customer**
Well, hover over it. It won't. Well, the green one, above the gray one.

**00:34:14 Speaker 2**
No. Well, let's say if it's a target, no, same thing,

**00:34:19 Customer**
Well, type Debian ISO.

**00:34:22 Speaker 2**
Debian ISO image. So, complete installation image.

**00:34:32 Speaker 2**
Here, this is a torrent, this is a regular one. If there is, here, that is, this is a regular one. This is a regular one.

**00:34:53 Customer**
Can you copy it, yes?

**00:34:58 Speaker 2**
Can you copy it? No, why? Ah, yes. So, copy it. Good.

**00:35:12 Speaker 1**
Well, now you'll open the terminal on one side and the interface on the other.

**00:35:15 Speaker 2**
Well, it's all working, yes.

**00:35:34 Speaker 2**
And wget, yes.

**00:35:41 Speaker 3**
How much is it, zero, or how much is it writing?

**00:35:47 Speaker 2**
Well, wget itself, well, well, about 10 Mbytes. Yes, 10, well, yes. Well, approximately the same, as with the torrent. Ah, well here. It's downloading, yes, and so on. It doesn't show the speed, right. It doesn't show the speed. Well, you can roughly guess that, well, yes, 10, roughly.

**00:36:04 Customer**
How many packets per second? 15.

**00:36:07 Speaker 2**
Yes. And if you check by IP? How much is there?

**00:36:09 Customer**
Switch it to, this, to megabytes per second.

**00:36:11 Speaker 2**
Well, yes, 500.

**00:36:13 Customer**
No, but if you put it on the full right part,

**00:36:17 Speaker 2**
Ah, 1,000 MB, yes?

**00:36:18 Customer**
Yes.

**00:36:19 Speaker 2**
Yes.

**00:36:25 Customer**
Well, at least it shows a deviation that matches the torrent. Well, that is, it deviates consistently, it makes an error, but the error is consistently learned. That's already not bad.

**00:36:43 Speaker 2**
Well, good.

**00:36:47 Customer**
Well, great. So. Well, I suppose we'll wrap up.

**00:36:49 Speaker 2**
Well, great, yes. Here, I suppose we'll wrap up.
