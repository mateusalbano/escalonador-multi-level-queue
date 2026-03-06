from __future__ import annotations

from typing import Protocol, Tuple, Optional

from process.process import Process


class SchedulerInterface(Protocol):

    def context_switch(self, process: Optional[Process]) -> Tuple[Optional[Process], int]:
        ...