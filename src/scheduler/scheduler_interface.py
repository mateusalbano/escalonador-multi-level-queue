from __future__ import annotations

from typing import Protocol, Tuple, Optional

from process.process import Process


class SchedulerInterface(Protocol):
    """Minimal interface a CPU expects from a scheduler.

    This allows :class:`Cpu` to depend on an abstract contract instead of the
    concrete :class:`Scheduler` implementation, breaking the circular import
    and making the modules easier to test or substitute later.
    """

    def context_switch(
        self, current: Optional[Process]
    ) -> Tuple[Optional[Process], int]:
        """Return a (next_process, time_slice) pair when a core needs work."""
        ...