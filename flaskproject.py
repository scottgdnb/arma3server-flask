# ~/flaskproject/flaskproject.py
from flask import Flask, request, render_template, flash, url_for, redirect, jsonify
import subprocess
import os
import time
import re

app = Flask(__name__)
app.secret_key = 'secretkeylol'

# Server functions below here...
# Compare the 2 folders for differences
# modlist = current mods.cfg
# modlistcurrent = directories in 'mods/'
# modslistdiff = mods not in mods.cfg

# App Routes

@app.route("/")
def index():
   return render_template('status.html', status=subprocess.run(["scripts/status.sh"], stdout=subprocess.PIPE).stdout.decode())

@app.route("/reboot", methods=['GET', 'POST'])
def reboot():
   if "stop" in request.form:
      flash('Stopping.')
      subprocess.Popen(["/usr/bin/sudo", "scripts/stop.sh"])
      return render_template('reboot.html', status=subprocess.run(["scripts/status.sh"], stdout=subprocess.PIPE).stdout.decode())
   elif "start" in request.form:
      flash('Starting.')
      subprocess.Popen(["/usr/bin/sudo", "scripts/start.sh"])
      return render_template('reboot.html', status=subprocess.run(["scripts/status.sh"], stdout=subprocess.PIPE).stdout.decode())
   elif "restart" in request.form:
      flash('Restarting.')
      subprocess.Popen(["/usr/bin/sudo", "scripts/restart.sh"])
      return render_template('reboot.html', status=subprocess.run(["scripts/status.sh"], stdout=subprocess.PIPE).stdout.decode())
   else:
      return render_template('reboot.html', status=subprocess.run(["scripts/status.sh"], stdout=subprocess.PIPE).stdout.decode())

@app.route("/diagnostics")
def diagnostics():
   return render_template('diagnostics.html', status=subprocess.run(['scripts/status.sh'], stdout=subprocess.PIPE).stdout.decode())

@app.route("/mods", methods=['GET', 'POST'])
def mods():
   if "refreshlist" in request.form:
      modscfg = open("/home/steam/arma3/mods.cfg")
      modlist = modscfg.read().splitlines()
      modsdir = "/home/steam/arma3/mods/"
      modlistcurrent = [ item for item in os.listdir(modsdir) if os.path.isdir(os.path.join(modsdir, item)) ]
      s= set(modlist)
      modlistdiff = [x for x in modlistcurrent if x not in s]
      flash('Refreshing.')
      return render_template('mods.html', mods=modlist, newmods=modlistdiff, status=subprocess.run(['scripts/status.sh'], stdout=subprocess.PIPE).stdout.decode())
   elif "applychanges" in request.form:
      modscfg = open("/home/steam/arma3/mods.cfg")
      modlist = modscfg.read().splitlines()
      modsdir = "/home/steam/arma3/mods/"
      modlistcurrent = [ item for item in os.listdir(modsdir) if os.path.isdir(os.path.join(modsdir, item)) ]
      s= set(modlist)
      modlistdiff = [x for x in modlistcurrent if x not in s]
      flash('Updating - Please restart the server.')
      data = request.form
      f = open("/home/steam/arma3/mods.cfg", "w")
      f.write("\n".join(data))
      f.close()
      with open("/home/steam/arma3/mods.cfg", "r") as f:
         lines = f.readlines()
      with open("/home/steam/arma3/mods.cfg", "w") as f:
         for line in lines:
            if line.strip("\n") != "applychanges":
               f.write(line)
      return render_template('mods.html', mods=modlist, newmods=modlistdiff, status=subprocess.run(['scripts/status.sh'], stdout=subprocess.PIPE).stdout.decode())
   else:
      modscfg = open("/home/steam/arma3/mods.cfg")
      modlist = modscfg.read().splitlines()
      modsdir = "/home/steam/arma3/mods/"
      modlistcurrent = [ item for item in os.listdir(modsdir) if os.path.isdir(os.path.join(modsdir, item)) ]
      s= set(modlist)
      modlistdiff = [x for x in modlistcurrent if x not in s]
      return render_template('mods.html', mods=modlist, newmods=modlistdiff, status=subprocess.run(['scripts/status.sh'], stdout=subprocess.PIPE).stdout.decode())


if __name__ == "__main__":
   app.run(host='0.0.0.0')
