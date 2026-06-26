import tkinter as tk
from tkinter import ttk
import subprocess,threading,time,csv,os,platform
from datetime import datetime
TARGET="";running=False
os.makedirs("Logs",exist_ok=True)
def log(ts,status,rt,reply):
 f=os.path.join("Logs","Ping_Report_"+datetime.now().strftime("%Y-%m-%d")+".csv")
 new=not os.path.exists(f)
 with open(f,"a",newline="",encoding="utf-8") as h:
  w=csv.writer(h)
  if new:w.writerow(["Timestamp","Status","ResponseTime","Reply"])
  w.writerow([ts,status,rt,reply])
def ping_once():
 cmd=["ping","-n","1",TARGET] if platform.system()=="Windows" else ["ping","-c","1",TARGET]
 p=subprocess.run(cmd,capture_output=True,text=True)
 txt=(p.stdout or "")+(p.stderr or "")
 lines=[l for l in txt.splitlines() if l.strip()]
 reply=""
 for l in lines:
  if "Reply from" in l or "Request timed out" in l or "bytes from" in l:
   reply=l;break
 if not reply and lines: reply=lines[-1]
 rt=""
 if "time=" in reply.lower():
  rt=reply.lower().split("time=")[1].split()[0]
 return p.returncode==0,rt,reply
def worker():
 global running
 out.delete("1.0","end")
 out.insert("end",f"Pinging {TARGET} with 32 bytes of data:\n\n")
 while running:
  ok,rt,reply=ping_once();ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  status="SUCCESS" if ok else "FAILED"
  log(ts,status,rt,reply)
  root.after(0,lambda t=ts,s=status,r=rt,rep=reply:(tree.insert("",0,values=(t,s,r)),out.insert("end",rep+"\n"),out.see("end")))
  time.sleep(1)
def start():
 global running,TARGET
 TARGET=ip_var.get().strip()
 if not TARGET:return
 if not running:
  running=True
  ip_entry.config(state="disabled")
  threading.Thread(target=worker,daemon=True).start()
def stop():
 global running
 running=False
 ip_entry.config(state="normal")
root=tk.Tk();root.title("Ping Monitor")
top=ttk.Frame(root);top.pack(fill="x",padx=10,pady=5)
ttk.Label(top,text="IP Address:").pack(side="left")
ip_var=tk.StringVar(value="4.2.2.2")
ip_entry=ttk.Entry(top,textvariable=ip_var,width=20)
ip_entry.pack(side="left",padx=5)

ttk.Button(root,text="Start",command=start).pack(side="left")
ttk.Button(root,text="Stop",command=stop).pack(side="left")
nb=ttk.Notebook(root);nb.pack(fill="both",expand=True)
f1=ttk.Frame(nb);f2=ttk.Frame(nb);nb.add(f1,text="Ping Report");nb.add(f2,text="Live Ping Output")
tree=ttk.Treeview(f1,columns=("Timestamp","Status","RT"),show="headings")
for c in ("Timestamp","Status","RT"): tree.heading(c,text=c)
tree.pack(fill="both",expand=True)
out=tk.Text(f2);out.pack(fill="both",expand=True)
root.mainloop()