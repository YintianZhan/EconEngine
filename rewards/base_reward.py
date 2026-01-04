"""
Base reward calculator interface for EconEngine.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np


class BaseRewardCalculator(ABC):
    """
    Abstract base class for reward calculators.

    Reward calculators determine how agent actions are rewarded,
    enabling different learning objectives and economic behaviors.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize reward calculator.

        Args:
            config: Configuration dictionary with hyperparameters
        """
        self.config = config or {}

    @abstractmethod
    def calculate_reward(self,
                        action_type: str,
                        action_details: Dict[str, Any],
                        old_state: Dict[str, Any],
                        new_state: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate reward for an action.

        Args:
            action_type: Type of action ('move', 'produce', 'consume')
            action_details: Details about the action (e.g., resource produced)
            old_state: Agent state before action
            new_state: Agent state after action

        Returns:
            Tuple of (total_reward, reward_breakdown)
            - total_reward: Single float reward value
            - reward_breakdown: Dict mapping component names to values
        """
        pass

    def get_config(self) -> Dict[str, Any]:
        """Get reward calculator configuration."""
        return self.config.copy()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config})"
