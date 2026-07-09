# Meeting Transcript

**Date:** 2026-07-05  
**Language:** English (translated from Russian)

---

### 00:00:01 – Speaker 1
Are we okay with the recording?

### 00:00:03 – Customer
Yes, fine.

### 00:00:07 – Speaker 1
Alright, let me show you now.

### 00:00:11 – Speaker 2
Go ahead.

### 00:00:12 – Speaker 3
Yes. So, within this sprint, we had the following task. Since we decided to stick with Docker, we needed to rework the application architecture. Because before, since everything was in Docker, we couldn't properly monitor all the traffic — only the traffic that went into the container itself.

### 00:00:38 – Speaker 3
And now we've reworked the entire software so that we have a target container (some application or server), and around it we have our traffic processor. In front of the application, we have a container with a gate. All traffic going to it first goes to the gate. There, if the IP is not on the list, it is forwarded to the target container. But if the IP *is* on the list (the blocklist), then the traffic doesn't reach the target and is redirected instead.

### 00:01:53 – Speaker 3
Accordingly, to make it easier to understand what to block, the element that scans the traffic has been improved. Now it shows data by IP. There is a separate page where you can see general statistics for incoming and outgoing traffic. There is a page showing the top 20 most active IPs with their statistics — incoming, outgoing, and the ports they correspond to, and so on.

### 00:02:50 – Speaker 3
As part of the first test, I'll show that it simply works in general. So, I build the container, and we wait for everything to spin up.

### 00:03:19 – Speaker 2
Right.

### 00:03:22 – Speaker 1
I don't get it yet.

### 00:03:24 – Speaker 3
It takes about 10 seconds to start. Okay, you can see — the backend isn't up yet, it hasn't started. There we go, it's ready. You can see that the components are connected, but there's nothing here yet because no traffic is flowing.

### 00:04:02 – Speaker 3
If we send a request to localhost on the target itself (which, at the moment, is just a dummy that returns one line) — we go in, and there's already some activity, and we're still executing the request itself. We can see that everything works, everything is received.

### 00:04:42 – Speaker 2
So, we have ping...

### 00:04:46 – Speaker 3
Wrong command. Crru. Anyway, yes — on the graph you can see incoming and outgoing traffic over time, with separate counters. And here is the IP page, where you can see: 0.0.0.1 is us, 0.0.0.2 is the target container that responds. Statistically speaking, the edge buttons don't work right now — they will be implemented in the future. Everything else displays as is. For correct statistics, the IP list refreshes every 60 seconds — so if they remain inactive for a minute, they will disappear from this list.

### 00:06:13 – Speaker 3
So, yes, it works. And now I'll show that our gate works. Basically...

### 00:06:18 – Speaker 2
Well, or we could just show the video.

### 00:06:18 – Speaker 3
We need to... with all this functionality. Hold on a minute.

### 00:06:37 – Speaker 2
Okay.

### 00:06:37 – Speaker 3
Right, in the gate's code itself, I add our IP to the blacklist.

### 00:06:46 – Speaker 2
Blacklist.

### 00:06:46 – Speaker 3
And now I rebuild our container.

### 00:06:56 – Speaker 2
Alright, it's rebuilding.

### 00:07:14 – Customer
And what exactly are you monitoring? Activity inside the Docker container?

### 00:07:21 – Speaker 3
The traffic processor now monitors everything that goes to and from this container. So if there is some application that actively interacts with the outside world, then all that traffic will be monitored.

### 00:07:43 – Customer
Uh-huh.

### 00:07:45 – Speaker 3
Okay, it's all up. Now I select the same command to test connectivity to our localhost.

### 00:08:09 – Customer
Next time it would be better to do this kind of project differently.

### 00:08:12 – Speaker 3
Yes.

### 00:08:12 – Speaker 2
Alright.

### 00:08:13 – Customer
I can't see anything.

### 00:08:17 – Speaker 2
Well, it seems visible, isn't it? No, it's visible?

### 00:08:20 – Customer
Actually, yes.

### 00:08:22 – Speaker 1
But maybe...

### 00:08:22 – Speaker 2
We need to now, yes, let's do it.

### 00:08:31 – Speaker 1
Well, this...

### 00:08:47 – Customer
It's not certain it will work, but...

### 00:08:51 – Speaker 1
Hopefully.

### 00:08:54 – Speaker 2
It will work. So now, I'm bringing up the whole container.

### 00:09:03 – Speaker 3
You can see that our IP has been added.

### 00:09:08 – Speaker 2
Uh-huh, okay, while it's building.

### 00:09:38 – Speaker 2
Alright, waiting for the backend to start.

### 00:09:45 – Customer
For future reference: if you have some component that requires this kind of reconfiguration, you can run the whole system in two terminals. In one terminal, run all containers except one, so it stays running, and in the second terminal, run only the container you need to reconfigure. That way, after reconfiguration, it doesn't rebuild everything, and we don't have to wait. In the second terminal, you stop only what you need to change, modify it, and restart it — it will be much faster.

### 00:10:24 – Speaker 2
Good. So, now...

### 00:10:27 – Speaker 3
Here we sent a request to this server. You can see there was incoming traffic, but there was no response because the gate redirected everything. And here is the message from the server: "Your IP has been blocked."

### 00:10:54 – Speaker 2
So, there you go.

### 00:10:56 – Speaker 3
Yes, and here you can see that only our IP was present, while the target itself didn't respond at all.

### 00:11:12 – Customer
Well, what do you mean?

### 00:11:13 – Speaker 2
Right.

### 00:11:16 – Customer
Do you mean that the response from the server came to the traffic processor, but the traffic processor didn't forward it further? Right?

### 00:11:25 – Speaker 3
Yes.

### 00:11:26 – Customer
Why? Or why did you decide not to include it in the statistics?

### 00:11:31 – Speaker 2
What exactly? The...

### 00:11:32 – Customer
The response. The traffic processor saw it, blocked it, and then sent it further.

### 00:11:39 – Speaker 3
All the activity of the gate itself and other work that our software does is currently filtered so that only what is important for the application itself is shown. Where does it filter? It doesn't count it, but that can be removed, and then it will count everything — including how the gate forwards and how it checks whether the IP is alive and everything else. Right now it's just filtered out.

### 00:12:36 – Customer
Well, okay, fine, understood.

### 00:12:41 – Speaker 2
How?

### 00:12:42 – Speaker 3
That's the test plan — that's everything we wanted to demonstrate.

### 00:12:49 – Customer
Could you run, for example, a ping of 20 packets in the terminal?

### 00:12:55 – Speaker 3
Ping won't be able to get through, it doesn't work with ports. But I'll try now.

### 00:13:04 – Speaker 2
Just...

### 00:13:04 – Customer
Instead of a request.

### 00:13:07 – Speaker 3
What do you mean? Like this?

### 00:13:11 – Speaker 2
Ping it.

### 00:13:12 – Customer
And your filtering and everything — is it tied to ports or to containers?

### 00:13:28 – Speaker 3
The filtering is generally partly on ports and partly on containers.

### 00:13:43 – Customer
Uh-huh. Well, ping goes simply to the address. Ping goes to the whole machine and to the whole container. Ping is lower-level than ports — it works below the port level, in terms of network abstraction layers. Ping doesn't depend on ports.

### 00:14:11 – Speaker 1
You can't just go into some container and ping it like that.

### 00:14:17 – Speaker 3
Well, I probably could...

### 00:14:20 – Speaker 2
I have a feeling I don't...

### 00:14:21 – Speaker 3
I don't know, I could just spam actively so that the counters show more activity in the statistics.

### 00:14:36 – Customer
Look, or just write a `for` loop around this command — wrap it in a `for` that will... basically, you need to write a bash script, or more precisely, your command that does this. Or just a plain command string.

### 00:15:02 – Customer
Curl, it's built-in, right? Alright.

### 00:15:09 – Speaker 2
Got it.

### 00:15:11 – Customer
Well, see how to make a loop in PowerShell, and do it so that you have it right here in the command line.
