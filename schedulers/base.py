"""Scheduler abstract interface."""

from abc import ABC, abstractmethod


class Scheduler(ABC):
    @abstractmethod
    def select(self, queue, banks, current_cycle):
        """Return selected MemoryRequest or None."""
        raise NotImplementedError


def bank_ready_for_request(bank, cycle):
    return bank.is_ready(cycle)
