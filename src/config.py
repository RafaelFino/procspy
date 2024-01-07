import json
from typing import Any
from proc import Proc   
class Config:
    def __init__(self) -> None:
        self.interval = 5
        self.interval = 60  
        self.database = "data/"
        self.log_name = "procspy.log"
        self.targets = {}         

    def default_targets(self) -> None:
        self.targets["chrome"] = Proc("chrome")
        self.targets["firefox"] = Proc("firefox")
        self.targets["steam"] = Proc("steam")                

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 
    
    def from_json(self, data: str) -> None:
        self.__dict__ = json.loads(data)
        for name, item in self.targets.items():
            self.targets[name] = Proc(name, item["limit"])  

    def load(self, path: str) -> None:
        with open(path, "r") as f:
            self.from_json(f.read()) 

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.to_json())

    def __str__(self) -> str:
        return self.to_json()
