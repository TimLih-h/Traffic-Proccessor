**Speaker 1**
Hello, to begin with, we probably need to show you what's called this. Do you know what this is?

**Speaker 2**
Yes, of course.

**Speaker 1**
Well, should I send it to the chat now, will that be fine, or is the TV better for you?

**Speaker 2**
Well, firstly, Telegram is better, and secondly, if you have them.

**Speaker 1**
When?

**Speaker 2**
Can you open it on the screen?

**Speaker 1**
Well, let's do it that way then. If it works, of course. It seems to be fine like this. Can you see it?

**Speaker 2**
Yes.

**Speaker 1**
Well, here we have this, yes.

**Speaker 2**
Aha.

**Speaker 1**
Here we have... so it turns out the court's action is 1, yes, and the zones are only for the place or talent, Toushin, Tottenham in the park, Swish End, and we'll sweep our computer 7 traffic, segment, internet mask. Agreed?

**Speaker 2**
Yes, okay. So you even have "board umyu" for what? Who is "home user"? Who is "home"?

**Speaker 1**
Well, by the way, it's more likely just a person who uses it purely for their own purposes, maybe for projects. Well, you mentioned reservations, yes? There will be.

**Speaker 2**
Falling under the category of this administrator, or just an administrator in general? Not a 'Administrator' but just an administrator.

**Speaker 1**
Hmm.

**Speaker 2**
Managerial staff.

**Speaker 1**
Well, probably yes, not 'home user note'.

**Speaker 2**
Well, that is, we can say that if we recall the diagram I showed you personally, there we have computers, routers that provide regular users with internet access. And naturally, there is traffic, processor, and the entire platform, the entire framework used by administrators – conditionally speaking, controllers.

**Speaker 1**
Uh-huh, well, yes.

**Speaker 2**
And accordingly, for regular users – 'regular user' or 'home user' – they practically do not interact with this platform at all. That is, the observed user, or the user being observed, or being monitored.

**Speaker 1**
Uh-huh.

**Speaker 2**
In principle, does not interact with the platform at all. The main interaction, or at least real-time observation of the packet count, is needed by the administrator or controller.

**Speaker 1**
But.

**Speaker 2**
The other group, the researchers, will combine 2 roles. The researcher will be both a regular user and an administrator simultaneously.

**Speaker 1**
Uh-huh, understood. So.

**Speaker 2**
For a regular user, the only requirement is that integrating the system into the connection does not affect the connection in any way.

**Speaker 1**
Ah, aha, okay.

**Speaker 2**
Having a web interface is more of an administrator story. Uh-huh. So then, if the web interface is an administrator story, I have a clarification about story number 1.

**Speaker 1**
So.

**Speaker 2**
If one can open... and the administrator, the administrator uses it to see the packets. What is meant by 'to see'? That is, where should the administrator look to see this number? These packets. This could be clarified.

**Speaker 1**
Well, from this side, well, you could say. It can be shown in different ways – the correct number of packets can be shown purely through the online interface, yes, but.

**Speaker 2**
Can.

**Speaker 1**
Through.

**Speaker 2**
The question is, where, which component of the platform?

**Speaker 1**
Hello.

**Speaker 2**
Will distract? There's traffic processor, note, controller server, for the web interface, more precisely the management user interface. If you recall, this is a separate component. If you are struggling with the frontend, you can make it text-based, via command line or just text in the terminal.

**Speaker 1**
Uh-huh, understood, yes. So, here's 3, yes.

**Speaker 2**
Are you recording? Are you taking notes, yes?

**Speaker 1**
Well, we have the recording, so to speak.

**Speaker 2**
Well, you can leave real-time notes so you don't have to re-watch the recording, whichever is more convenient for you.

**Speaker 1**
Uh-huh.

**Speaker 2**
Regarding the diplomat – that's also for the administrator, actually.

**Speaker 1**
Uh-huh.

**Speaker 2**
This is either for all users, i.e., all groups, or for the administrator. In general, this is the administrator's task, area of responsibility, and main pain point. In what way will the null platform analyzer be put into operation?

**Speaker 1**
Uh-huh, well, okay, I agree on that. As for the rest.

**Speaker 2**
It's all fine. Well, again, if you have planned to implement the system only inside a virtual machine, then yes, it's a good point. If you are planning... Well, we need to look – you have two separate discussions about whether you plan to run the traffic processor on real hardware, i.e., on a laptop, a dedicated separate laptop, or a microcontroller – well, Raspberry Pi, Arduino, why not? I think you yourself realize that if you plan to, then this user story can either be renamed, change its priority to 'should have', or leave the user story about running inside a virtual machine as a 'must have', and create a separate story about real hardware, i.e., a dedicated laptop or dedicated computer – laptop or microcomputer, like 'should have' or 'could have'?

**Speaker 1**
Uh-huh, understood.

**Speaker 2**
As far as I understand, you don't currently have separate user stories about a dedicated computer.

**Speaker 1**
Seems not, no. Uh-huh.

**Speaker 2**
Okay, well, we can note that and then finalize it.

**Speaker 1**
Uh-huh, okay.

**Speaker 2**
So, 'to see' – administrator, yes. And accordingly, the user – it's about the user, I already said. So that's even 3, like that. Story 4 – 'connection' – good. The only thing to clarify is 'to see' – where exactly to see? That is, management interface, graphic processor, or where? Currently, from this suggestion, it's unclear where the administrator will look.

**Speaker 1**
Well, in general, should we indicate that it's the management interface everywhere?

**Speaker 2**
Yes. Well, I don't know – everywhere or not everywhere, but if you imply that.

**Speaker 1**
Because.

**Speaker 2**
...looking at the management user interface with your eyes – this should not be implied, it's better to state it in the text.

**Speaker 1**
Well.

**Speaker 2**
...number 300.

**Speaker 1**
As I understand it, it's more about the functionality, the presence of such functionality. Where he sees it depends on the implementation.

**Speaker 2**
Such functionality can be implemented in any of the 4 system components. I would just clarify which component of the system is meant – whether it's only the management user interface, i.e., it's not about this information being duplicated across all 4 components. That is, 'to see' – meaning to see the counter information on all four components – on the traffic processor, on the communication node, on the server, and on the... I understand.

**Speaker 1**
What are you talking about?

**Speaker 2**
Well, like traffic... Okay, point 5 – good. The only thing, here are 2 comments. 1 – you can either split it into 2 separate user stories, or clarify it within this one about incoming and outgoing connections. That is, is it a list of IP addresses? It needs to be clarified – is this a list of IP addresses for incoming packets or for outgoing packets, is it common for both incoming and outgoing connections, or two separate lists? And I would classify this story as 'could have'. Well, let's say like this – uh-huh. 1 comment regarding clarifying this user story into separate incoming and outgoing – i.e., either 2 blocklists or one common blocklist. 2 comment regarding priority – since this falls under the functional description of the zero functional prototype or the 3rd functional prototype (which already modifies traffic), I would have it as 'could have' priority. I would do this in the 3rd iteration. In the first iteration, I would do just basic counters – this is the 'must have' – just 2 counters. In the 2nd iteration, 2nd functionality or 2nd prototype – advanced counters, i.e., pairs – counting IP addresses and ports. Advanced counters, advanced metrics, advanced statistics – that's a 'should have'. This functionality, which involves traffic modification, I would move to 'could have'.

**Speaker 1**
Aha.

**Speaker 2**
Okay, so that's about number 3. Next, story 6 – good. Well, here we need to look and discuss. This 'should have'/'could have' – this user story looks like advanced analytics functionality or advanced statistics collection. Formally, it belongs more to prototype version 2, uh-huh, but it might have non-trivial implementation, so we need to think, sit down, see how to do it, and it might be quite difficult to do. So I can agree with 'could have', i.e., the 3rd prototype, the 3rd version – 'could have'. And here I would indicate somewhere that 'view history of packets' – this might be about storage or a database – that all data is saved in storage or a database. So like, I would like the system to have a data storage where I can see the history of packets and connections with timestamps.

**Speaker 1**
Understood.

**Speaker 2**
So, here you can mention the storage right. From a functional point of view, this user story implies adding storage to the project. Without this user story, you can not use a database as such. That's the emphasis, uh-huh. Story 6 – understood, any questions?

**Speaker 1**
So, well, yes, understood.

**Speaker 2**
Okay. So story 7 – 'to tunnel traffic to a remote gateway for... buttons I know the wife.' Well, the wording is a bit complicated – it's as if written in Russian, in the Russian language manner, with a compound sentence with many... Well, okay. Here you can clarify the wording a bit – that traffic is encapsulated and forwarded here and there. 'Instagram Paris destination' – it's not entirely clear, because the final destination of the packet is still the original destination. The traffic is forwarded from there to the original destination using... so you can swap some parts and say that traffic is encapsulated and forwarded to the original destination or not?

**Speaker 1**
Uh-huh, yes, yes.

**Speaker 2**
That it passes through this gateway. Like this. In general, this is a good point, I like it. In terms of priorities – after the 'could have' priorities... Well, you can think about it – this 3rd priority 'could have'.

**Speaker 1**
Well, yes.

**Speaker 2**
This user story is borderline between 3rd and 4th priority – in terms of complexity and functionality, it's either 3rd or 4th. Either 'could have' or it will be...

**Speaker 1**
...starting.

**Speaker 2**
...there.

**Speaker 1**
Uh-huh.

**Speaker 2**
Export, naturally... I only...

**Speaker 1**
...met.

**Speaker 2**
Yes. Story 8 – excellent, excellent. Uh-huh. Monitoring – story 9 – also fine.

**Speaker 1**
In it, this...

**Speaker 2**
...a friend. At the moment, I have a poor idea of how this can be implemented. Well, okay, it's not entirely clear. This user story is tied to blocklists or whitelists. So it must go together with the blocklist. That is, it's a story about: if our blocklist is empty, we should allow everything; if our allowlist is empty, we should block everything. So I think the priority of this user story should be the same as that of the blocklists/allowlists. Uh-huh, that means it's 'could have' after all, because traffic modification is already version 3. Aha, good. So then you have story 10 – 'to have a device'. Story 10 – good. It implies, precisely, that story 10 implies the presence of a physical device. The story implies that the traffic processor is not a virtual machine but something physical. And story 10 should correspond with a new story, also like story 11 – about wanting to have the traffic processor as a physical device. And by priority, this is indeed 'should have' or 3rd priority. We'll see.

**Speaker 1**
Well, are you sure it's not suitable, or after all?

**Speaker 2**
No, remember? Yes, yes. But it's like a regular port.

**Speaker 1**
So, uh-huh, thank you. Probably then 2... Yes, we also have a bit of design, so to speak, the MVP zero. Let me try, hopefully it will work. Well, this is probably not the most important part – it's quite simple to run.

**Speaker 2**
The fact that it's simple or not simple does not relieve you of the need to agree on all this.

**Speaker 1**
Uh-huh. So, well, honestly, there are 2 tables at the very beginning. Just like a log of packets, packet details, and all that. It shows when it's working, when it's with Nancy, and when it's just not connected.

**Speaker 2**
Uh-huh.

**Speaker 1**
...not connected. And we also have a connection here – we have source, destination, protocol, packet. And here is just a table – you could say the current connection. So that's already MVP 2, yes?

**Speaker 2**
Well, a slightly more advanced analyzer.

**Speaker 1**
Well, and yes, the same error – so it turns out the same – when either it's not working with a database or TCP is not working, uh-huh, simply. That's all. Well.

**Speaker 2**
Okay, well, let's go through prototype 1, which is just counters. In principle, yes. The only thing, probably... Well, this column here – I don't know how you will actually implement all this.

**Speaker 1**
Well.

**Speaker 2**
But essentially, you have the right column – you have 2 central counters. The number displayed in these counters shows the system state – whether there are packets or no packets. And essentially, zero shows that we have no network activity; more than zero shows a working state – some activity is happening. And in the final design, you probably don't need these buttons on the right. Functionally, for the prototype.

**Speaker 1**
But these are just requirements.

**Speaker 2**
Regarding the design – you could make a row above these 2 counters, for example, about how the traffic processor is feeling. And there, conditionally speaking, an LED – a green light indicating the traffic processor is online, and below – the counter readings, uh-huh. If suddenly the connection to the traffic processor is lost, or it doesn't receive data for a long time, then this light changes to red and shows what you have written in the 'error' section. So I mean, the graphical interface for version 1 consists of 2 main elements – the top part of the screen (about 20% of the screen) is the status line: traffic processor online/offline. If it's online – a green light, like 'all good'. If it's offline – a red light, and what you have written in the 'error' section. Uh-huh, okay. And the 2nd part of the screen, the remaining 60-75% of the screen, is essentially these 2 counters.

**Speaker 1**
Yes, well. So it's all clear.

**Speaker 2**
I hope it's more or less clear.

**Speaker 1**
Uh-huh, so everything.

**Speaker 2**
Okay. And regarding version 2 – well, properly speaking, besides the connection tracking, it would be good to add the functionality of displaying the history of counter readings as a graph. That is, without storing data on the backend, without any tricky manipulations – I mean without storing data in a database, uh-huh. Save, for example, the readings from the last 30 or last 100 readings from both counters. So, a small array of 30 or 100 measurements, constantly update it, and accordingly either store it simply as variables on the backend and do it via online connection through a websocket on the frontend. So that the frontend renders a graph – i.e., the frontend renders changes in counter readings in real time. And these readings are not stored anywhere. When you refresh the page, press F5, this graph resets and it's completely empty, then data comes in over time, the graph is drawn slowly until it remembers everything, and then it starts moving. Uh-huh. This would be... We need to see how difficult it is to make graphs and how difficult it is to send values online. This could be added to the user story with the 2nd priority – i.e., 'should have'.

**Speaker 1**
Uh-huh.

**Speaker 2**
About wanting to see such an online graph of counter changes. And we need to study how technically difficult it is to do. If it's not technically difficult – if it's quite simple or moderately difficult – it's worth doing first, and then this table. If it turns out that the online connection and rendering this graph in real time is too technically difficult for the frontend, then it's less priority. And version 2 can start with the table. If the graph doesn't work out?

**Speaker 1**
Understood, uh-huh. So instead of, not instead of.

**Speaker 2**
Well, these are 2 different...

**Speaker 1**
Yes.

**Speaker 2**
Yes, 2 different screens, 2 different displays.

**Speaker 1**
Yes, yes, aha. Okay, we'll try to do it.

**Speaker 2**
Yes.

**Speaker 1**
We'll see.

**Speaker 2**
We'll try.

**Speaker 1**
So, well, I think that's all.

**Speaker 2**
Aha, good.

**Speaker 1**
Right, thank you very much for finding the time.

**Speaker 2**
Yes, you're welcome. I hope you succeed.

**Speaker 1**
Uh-huh, well, goodbye for now. Not everything – I needed to ask about the assignment regarding MVP. What needed to be asked?

**Speaker 2**
The idea – what should be included in the first MVP version.

**Speaker 1**
Well, like a basic packet counting, yes. And you could say.

**Speaker 2**
How does it look on each of the 4 components?

**Speaker 1**
Well, what do we want to take on loan? As the most basic, yes?

**Speaker 2**
Aha.

**Speaker 1**
And well, yes, we will set up a web server – the simplest one. Perhaps as you can say, as you were shown, yes?

**Speaker 2**
Uh-huh.

**Speaker 1**
That's all, I think.

**Speaker 2**
Well, what will the web server do, what will the communication node do? Well, yes, it's all clear.

**Speaker 1**
Well, yes, well – the communication node forwards data to the backend. The backend, as they say, spontaneously shows what data it received.

**Speaker 2**
Well, okay, and.

**Speaker 1**
In general, I think it's all good.

**Speaker 2**
Do you already know who will handle the traffic processor and setting up virtual machines and that sort of thing?

**Speaker 1**
Well, I think Timur.

**Speaker 2**
Okay. Is there an understanding of how, actually, to make the first version of the traffic processor? What technologies are needed and how, for example, to make 2 virtual interfaces and connect them so that they forward packets from one to the other and back again? Uh-huh, well, okay. If any difficulties or questions arise, write. This task is truly non-trivial. Uh-huh. I'm interested to see if you'll find a solution. If you have difficulties with the solution or something isn't working out, write, I'll consult separately on this issue. Because honestly, this thing is a little bit complicated for you. But as they say, 'he who isn't afraid of difficulties – or rather, he who is afraid of difficulties doesn't drink champagne'.

**Speaker 1**
Well, there's probably enough documentation on the internet.

**Speaker 2**
Well, we need to see how far you get. In theory, it should be done with about 3 small Linux commands, small pieces of code. But that's in theory – there's no guarantee it will work. So try it, and if it works or if there are any difficulties, we'll meet separately for a consultation on this issue.

**Speaker 1**
Okay, uh-huh.

**Speaker 2**
Okay, thank you. That's all, thank you. No more questions from my side.

**Speaker 1**
Goodbye.

**Speaker 2**
All the best, goodbye, have a nice evening.

**Speaker 1**
Uh-huh.

**Speaker 2**
Goodbye.