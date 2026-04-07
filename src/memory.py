import json
import os
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Memory:
    max_messages: int = 12
    storage_path: str = "logs/conversation_history.json"
    _msgs: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.load()

    def add(self, user: str, assistant: str) -> None:
        self._msgs.append({"role": "user", "content": user})
        self._msgs.append({"role": "assistant", "content": assistant})
        if len(self._msgs) > self.max_messages:
            self._msgs = self._msgs[-self.max_messages:]
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self._msgs, f, indent=2)

    def load(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self._msgs = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._msgs = []

    def messages(self) -> List[Dict[str, str]]:
        return list(self._msgs)
    
    def clear(self) -> None:
        self._msgs = []
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
