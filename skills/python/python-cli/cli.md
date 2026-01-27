# Command-line interface (CLI)

In addition to the usage of the package via API, a CLI app shall be created that allows to run most functionalities from the command line. 

The CLI shall be created with the package ´typer´. In addition, the following general guidelines and constraints apply:
- implement a user-friendly interface with clear instructions and help messages.
- include error handling for invalid inputs 
- implement logging for all CLI operations. Only use ´typer.echo´ if the output is meant for the user.
