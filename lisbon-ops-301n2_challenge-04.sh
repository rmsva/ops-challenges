#!/bin/bash

# Script: Ops Challenge: Class 04
# Goal: Create a bash script that launches a menu system with the listed options in the challenge.
# Why: Further bash scripting practice with what I learned about conditionals and menu systems.

while true; do # Sets up the main menu and a way for it to loop back to the starter screen if no valid open is chosen
	clear # Clears current terminal window
	echo "Hello world!" # All echo commands print to terminal
	echo "1. Ping self"
	echo "2. IP info"
	echo "e. Exit"
	read choice # Reads input from the user

	if [[ $choice = 1 ]]; then # What happens when option 1 from the menu above is picked. If option 1 is picked, then...
		ping -c 4 loopback # Pings host's loopback address 4 times and outputs results
		echo "Choose another option or press Enter to go back to main menu:"
		read choice # Reads input
	fi # Ends this condition

	if [[ $choice = 2 ]]; then # If option 2 (IP info) is picked, then...
		ip a # Shows network adapter information
		echo "Choose another option or press Enter to go back to main menu:"
		read choice # Reads input
	fi # Ends this condition

	if [[ $choice = e ]]; then # If e. is selected, then...
		echo "See you later!"
		exit 0 # Exits the program successfully
	fi # Ends this condition
done # Finalizes the script, looping back to line 7 since while remains true. Script won't end by itself unless you tell it to, or abort the script.