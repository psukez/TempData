import subprocess as cmd

cp = cmd.call("git add .", shell=True)
#print(cp)
message = "update the repository"

cp = cmd.call("git commit -m '{message}'", shell=True)
cp = cmd.call("git push -u origin -f", shell=True)
