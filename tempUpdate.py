import subprocess as cmd

cp = cmd.call("git add .", shell=True)
cp = cmd.call("git commit -m 'update repository'", shell=True)
cp = cmd.call("git push -u origin -f", shell=True)
