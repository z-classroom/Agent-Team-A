from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Memory:
    enabled: bool = True
    max_messages: int = 12

    def __post_init__(self) -> None:
        self._msgs: List[Dict[str, str]] = []

    def add(self, user: str, assistant: str) -> None:
        if not self.enabled: return
        self._msgs.append({"role": "user", "content": user})
        self._msgs.append({"role": "assistant", "content": assistant})
        if len(self._msgs) > self.max_messages:
            self._msgs = self._msgs[-self.max_messages :]

    def messages(self) -> List[Dict[str, str]]:
        return list(self._msgs)