2023/03/23
I'm probably REALLY going to regret this (hence the last commit name), but I think it would be kinda fun to see if I can get this working with either the console or the GUI window. This might have to be dropped eventually, because with the way I'm thinking about doing combat, it might not be possible unless I have full control over the cursor/insertion point, which I don't think you have with most terminals/consoles.
Either way, I think it will be a fun challenge for the time being.

2023/03/16
I've started to rethink having quests in custom files. I think it would work better as Python scripts, and I can supply functions to make quest writing easier. This is what the stuff in the "plugins" directory is for.

2023/03/10
I've decided to actually start fleshing this out. I'm finding it kind of enjoyable writing a bunch of systems that could support a sort of "modular" game where everything is loaded from files insteaded of baked into the code. Most the definitions for things like items, NPCs, and map data will be stored using JSON, but I give them custom file extensions because it's cool.

Other things like player saves and quest files will have their own formats, but again the idea is to make something where you could add content or completely change the game without ever having to change a line of code. That may not be entierly possible, but the idea excites me at least.

I am having a harder time coming up with how to handle quests, but I'm sure that will come as I think about it more. I still have a long ways to go in other areas, so I have a lot of time to think about it.

2023/03/08
Just a silly little text-based game I've been working on for years.