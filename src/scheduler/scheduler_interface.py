from __future__ import annotations

from typing import Protocol, Tuple, Optional

from process.process import Process


class SchedulerInterface(Protocol):

    def context_switch(
        self, current: Optional[Process]
    ) -> Tuple[Optional[Process], int]:
        """Return a (next_process, time_slice) pair when a core needs work."""
        ...