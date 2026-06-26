
import tkinter as tk
from tkinter import ttk,filedialog
import config
def run():
    cfg=config.load()
    root=tk.Tk();root.title("Ping Monitor Professional - Phase 1");root.geometry("900x600")
    top=ttk.Frame(root,padding=8);top.pack(fill="x")
    vars={k:tk.StringVar(value=str(v)) for k,v in cfg.items()}
    for i,(lbl,key) in enumerate([("Target IP","target_ip"),("Interval","interval"),("Timeout","timeout"),("Packet Size","packet_size"),("Log Folder","log_folder")]):
        ttk.Label(top,text=lbl).grid(row=i,column=0,sticky="w")
        ttk.Entry(top,textvariable=vars[key],width=30).grid(row=i,column=1,sticky="w")
        if key=="log_folder":
            ttk.Button(top,text="Browse",command=lambda:vars[key].set(filedialog.askdirectory() or vars[key].get())).grid(row=i,column=2)
    def save():
        c={k:(int(v.get()) if k in ("interval","timeout","packet_size") else v.get()) for k,v in vars.items()}
        config.save(c); status.set("Settings saved")
    ttk.Button(top,text="Save Settings",command=save).grid(row=6,column=0,pady=8)
    ttk.Button(top,text="Start").grid(row=6,column=1)
    ttk.Button(top,text="Stop").grid(row=6,column=2)
    nb=ttk.Notebook(root);nb.pack(fill="both",expand=True)
    for name in ["Ping Report","Live Ping Output","Statistics","Log Files","Settings"]:
        f=ttk.Frame(nb); nb.add(f,text=name)
        ttk.Label(f,text=f"{name} - Phase 1").pack(pady=20)
    status=tk.StringVar(value="Ready")
    ttk.Label(root,textvariable=status,relief="sunken").pack(fill="x",side="bottom")
    root.mainloop()
