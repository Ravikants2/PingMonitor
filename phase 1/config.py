
import json
from pathlib import Path
CFG=Path("Config/settings.json")
DEFAULT={"target_ip":"4.2.2.2","interval":1,"timeout":1000,"packet_size":32,"log_folder":"Logs"}
def load():
    CFG.parent.mkdir(exist_ok=True)
    if CFG.exists():
        return {**DEFAULT,**json.loads(CFG.read_text())}
    save(DEFAULT); return DEFAULT.copy()
def save(cfg):
    CFG.write_text(json.dumps(cfg,indent=2))
