import tkinter as tk
from tkinter import ttk,messagebox
import threading,subprocess,platform,time,csv,os
from datetime import datetime
running=False
TARGET="4.2.2.2"
def logfile():
 os.makedirs("Logs",exist_ok=True);return os.path.join("Logs","Ping_Report_"+datetime.now().strftime("%Y-%m-%d")+".csv")
def log(ts,st,rt,reply):
 f=logfile();new=not os.path.exists(f)
 with open(f,"a",newline="",encoding="utf-8") as h:
  w=csv.writer(h)
  if new:w.writerow(["Timestamp","Status","ResponseTime","Reply"])
  w.writerow([ts,st,rt,reply])
def ping():
 cmd=["ping","-n","1",TARGET] if platform.system()=="Windows" else ["ping","-c","1",TARGET]
 p=subprocess.run(cmd,capture_output=True,text=True)
 out=p.stdout+p.stderr
 st="SUCCESS" if p.returncode==0 else "FAILED";rt=""
 for part in out.replace("<","=").split():
  if part.lower().startswith("time="): rt=part.split("=")[1]
 return st,rt,out.strip()
def loop():
 global running
 while running:
  ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  st,rt,r=ping();log(ts,st,rt,r)
  root.after(0,lambda t=ts,s=st,x=rt: tree.insert("",0,values=(t,s,x)))
  time.sleep(1)
def start():
 global running
 if not running:
  running=True;threading.Thread(target=loop,daemon=True).start();lbl.config(text="Running")
def stop():
 global running
 running=False;lbl.config(text="Stopped")
root=tk.Tk();root.title("Ping Monitor")
ttk.Button(root,text="Start",command=start).pack()
ttk.Button(root,text="Stop",command=stop).pack()
lbl=ttk.Label(root,text="Stopped");lbl.pack()
tree=ttk.Treeview(root,columns=("Time","Status","RT"),show="headings")
for c in ("Time","Status","RT"): tree.heading(c,text=c)
tree.pack(fill="both",expand=True)
root.protocol("WM_DELETE_WINDOW",lambda:(stop(),root.destroy()))
root.mainloop()
