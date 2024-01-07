import json
from datetime import datetime
class Proc:
    def __init__(self, name: str, limit: float = 60*60*2) -> None:
        self.elapsed = []
        self.name = name        
        self.limit = limit

    def add(self, elapsed:float) -> None:
        self.elapsed.append(elapsed)

    def get_elapsed(self) -> float:
        return sum(self.elapsed)
    
    def is_expired(self) -> bool:
        elapsed = self.get_elapsed()
                    
        if elapsed >= self.limit:
            return True
        
        return False
    
    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def from_json(self, data: str) -> None:
        self.__dict__ = json.loads(data)
        
    def __str__(self) -> str:
        return self.to_json()