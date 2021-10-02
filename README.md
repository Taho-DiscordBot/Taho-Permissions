# slash-commands-recuperator
Python script to get the slash commands of a discord bot structured in a toml file. The structure is not the one given in the official Discord documentation but it is close to it, it is intended to be more easily readable and to be able to retrieve any information easily.

In the `config.toml` file, you must enter :

- The id of your bot
- The token of your bot

- The name of the file that will be created with your slash commands
- The version of the discord api at the time you are using the program (v9 by default)

- (A guild id if you want to get the commands of a particular guild)

**Don't forget to install the tool dependencies listed in `requirements.txt ` on your python for the tool to work properly.**
