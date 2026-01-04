"""
Concrete reward calculator implementations for EconEngine.
"""

from typing import Dict, Any, Tuple
from .base_reward import BaseRewardCalculator


class SimpleUtilityReward(BaseRewardCalculator):
    """
    Simple utility-based reward calculator.

    Replicates current behavior:
    - Consumption: positive utility from resource
    - All other actions: -0.05 penalty

    This serves as baseline for comparison.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize simple utility reward calculator.

        Config options:
            action_penalty: Penalty for all actions (default: -0.05)
        """
        super().__init__(config)
        self.action_penalty = self.config.get('action_penalty', -0.05)

    def calculate_reward(self,
                        action_type: str,
                        action_details: Dict[str, Any],
                        old_state: Dict[str, Any],
                        new_state: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate reward using simple utility model.

        Args:
            action_type: 'move', 'produce', or 'consume'
            action_details: Dict with action info (e.g., 'resource', 'success')
            old_state: State before action
            new_state: State after action

        Returns:
            (total_reward, breakdown)
        """
        breakdown = {
            'consumption_utility': 0.0,
            'action_penalty': self.action_penalty,
        }

        # Consumption gives positive utility
        if action_type == 'consume' and action_details.get('success', False):
            utility_gained = action_details.get('utility_gained', 0.0)
            breakdown['consumption_utility'] = utility_gained
            breakdown['action_penalty'] = 0.0  # No penalty for successful consumption

        total_reward = sum(breakdown.values())

        return total_reward, breakdown


class OpportunityCostReward(BaseRewardCalculator):
    """
    Opportunity-cost aware reward calculator.

    Improved reward structure that captures:
    - Consumption utility (positive)
    - Time opportunity cost (variable penalty based on time spent)
    - Production value (reward for creating valuable goods)
    - Efficiency bonus (reward for efficient production chains)

    This enables learning of economic behaviors like production chains
    and optimal resource allocation.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize opportunity-cost reward calculator.

        Config options:
            opportunity_cost_rate: Cost per unit time (default: 0.03)
            production_value_weight: Fraction of utility rewarded at production (default: 0.3)
            efficiency_bonus: Bonus multiplier for efficient chains (default: 0.1)
            holding_cost: Cost per unit inventory (default: 0.0, disabled)
        """
        super().__init__(config)
        self.opportunity_cost_rate = self.config.get('opportunity_cost_rate', 0.03)
        self.production_value_weight = self.config.get('production_value_weight', 0.3)
        self.efficiency_bonus = self.config.get('efficiency_bonus', 0.1)
        self.holding_cost = self.config.get('holding_cost', 0.0)

    def calculate_reward(self,
                        action_type: str,
                        action_details: Dict[str, Any],
                        old_state: Dict[str, Any],
                        new_state: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate reward using opportunity-cost model.

        Args:
            action_type: 'move', 'produce', or 'consume'
            action_details: Dict with action info
            old_state: State before action
            new_state: State after action

        Returns:
            (total_reward, breakdown)
        """
        breakdown = {
            'consumption_utility': 0.0,
            'opportunity_cost': 0.0,
            'production_value': 0.0,
            'efficiency_bonus': 0.0,
            'holding_cost': 0.0,
        }

        # 1. Time opportunity cost (applies to all actions)
        time_cost = action_details.get('time_cost', 1.0)
        breakdown['opportunity_cost'] = -self.opportunity_cost_rate * time_cost

        # 2. Consumption utility (positive)
        if action_type == 'consume' and action_details.get('success', False):
            utility_gained = action_details.get('utility_gained', 0.0)
            breakdown['consumption_utility'] = utility_gained

            # Efficiency bonus: reward consuming high-value items
            # (cooked fish gives more utility per resource than raw fish)
            if self.efficiency_bonus > 0 and utility_gained > 0:
                # Simple heuristic: bonus for consuming high-utility items
                if utility_gained >= 2.0:  # Cooked fish (2.5) or bread (3.0)
                    breakdown['efficiency_bonus'] = self.efficiency_bonus * utility_gained

        # 3. Production value (reward creating valuable goods)
        elif action_type == 'produce' and action_details.get('success', False):
            resource_utility = action_details.get('resource_utility', 0.0)
            output_units = action_details.get('output_units', 1.0)

            # Reward a fraction of the final utility at production time
            production_value = self.production_value_weight * resource_utility * output_units
            breakdown['production_value'] = production_value

        # 4. Holding cost (penalty for large inventory - optional)
        if self.holding_cost > 0:
            total_inventory = sum(new_state.get('inventory', {}).values())
            breakdown['holding_cost'] = -self.holding_cost * total_inventory

        total_reward = sum(breakdown.values())

        return total_reward, breakdown
