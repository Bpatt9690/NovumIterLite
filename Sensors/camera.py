import subprocess

# Command to execute
command = "libcamera-jpeg -t 5000 -o test.jpg"

# Call the command in the command line
subprocess.call(command, shell=True)