#!/bin/bash

# Script: Ops Challenge: Class 02
# Goal: Automatize the copying of the file /var/log/syslog and manipulate a variable in bash to append the current date and time to the filename.
# Why: Getting used to bash scripting and using variables to get the most out of the process of automatization.

# Preparing variables for the script: This includes two timestamp variables, one with time and date and one with just the time. The time only variable is for the stretch goal.
append=$(date +%d-%m-%Y_%H-%M-%S)
timestamp=$(date +%H:%M:%S)

# Copy target file to the current working directory
echo "($timestamp) Copying target file to the current working directory."
cp /var/log/syslog .

# Append $append variable above to the filename of the copied file
echo "($timestamp) Adding current time and date to filename..."
mv syslog syslog_$append