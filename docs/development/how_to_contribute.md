## How to Contribute to Blackbirds
This is an in-progress guide to how to develop for the game Blackbirds. As of the time of writing, this guide assumes you are using a Windows platform and have a basic understanding of Git. Linux users will have to adapt, unfortunately - but hey, you're using Linux, you're good at that.

### Install Evennia
Evennia is the engine on which Blackbirds runs. You'll need to install and set it up first. A detailed guide can be found on the Evennia wiki here: https://github.com/evennia/evennia/wiki/Getting-Started.

**NOTICE:** You're going to want to stop just before it tells you to set up a new game ("mygame"). We'll take it from here.

### Set up Blackbirds
Assuming you've followed the Evennia setup guide with no issues, you're ready to create and clone the game for your own modification.


#### Create and initialize the folder
 - Navigate to the folder where you installed Evennia and set up your virtual environment. You did that, right? Don't DM me on Discord. Go read the guide again, and then come back.

 - Either open up a terminal in VS Code or your editor of choice, or open Powershell at this location.

 - Enter `evennia --init blackbirds`
 
 - Enter `cd blackbirds`

 - Enter `evennia migrate`

#### Establish the folder as a Git repo
 - Back out into your base installation folder. Make a new directory there. It doesn't matter what you name it; you don't need it when you're done.

 - Navigate to that new folder, and clone the Blackbirds repo: `git clone https://github.com/Earthcrusher/Blackbirds.git`

 - This folder has a hidden directory, called `.git`. This needs to be put into the `blackbirds` folder.

 - You can delete your temporary directory.

 - In the `blackbirds` folder, from the terminal, enter: `git reset --hard HEAD`

 - Check the directory. It should now match the structure of the repo.

#### Obtain the database
The final step in setting up Blackbirds for development is grabbing a copy of the game's database. This is not strictly necessary for advanced Evennia users, but unless you feel like altering the settings file so it won't scream about missing rooms and the like, this is highly recommended.

You can download the latest database dump at https://www.mercymyqueen.com/blackbirds/evennia.db3.

I try to keep this database up to date. If you suspect it's missing something, let me (Earthcrusher) know and I'll upload a fresh copy.

Once you've obtained it, `evennia.db3`, the database file, needs to go into your `<installation dir>/blackbirds/server` folder. Overwrite the existing one.

#### Start and log into the game
This part of the guide assumes you're using a 3rd party MUD client. Although Evennia ships with a web client, I do not care for it and won't be providing support for it. I highly recommend Mudlet, found at http://www.mudlet.org.

 - Set up a new profile for Blackbirds, with the address `127.0.0.1` and port `4000`.

 - Open a terminal at `<install folder>/blackbirds`.

 - Enter `evennia start`.

 - Once the startup procedure is finished, you're free to log into the game.

#### Modifying the game
Modifying the game is just like writing code elsewhere. Open up a file and go wild on it. This is where I highly recommend a good, powerful editor like VS Code, especially one that can work with your Python virtual environment, integrate with Git, and even keep a tidy workspace.

**Tips:**

 - If you need access to a command allowed only to admin/developers, simply comment out the "locks" attribute of that command. It's highly recommended you do this with `CmdReload` so that you can restart the game without having to return to the console every time.

 - Be logged in while making changes. Use the RELOAD command in-game to load alterations to the code. Getting used to this workflow keeps things easy and streamlines.

 - Don't be afraid to tweak things and even break the game. You can always revert your changes and start from a clean slate.

 - If you try to RELOAD and the game is frozen, type `evennia reload` into the terminal instead. It means you have a Python error, and the game will resume after you fix it. Type `evennia reload` once more when you're done.