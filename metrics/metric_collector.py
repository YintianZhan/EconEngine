"""
Metric collector for tracking agent behavior and learning dynamics.
"""

from typing import Dict, List, Any, Optional
import numpy as np


class MetricCollector:
    """
    Collects metrics during agent training and episodes.

    Tracks step-level and episode-level metrics for analysis and visualization.
    """

    def __init__(self):
        """Initialize metric collector."""
        self.reset_episode()
        self.episode_metrics = []

    def reset_episode(self):
        """Reset metrics for new episode."""
        self.step_data = []
        self.current_episode = {
            'episode_number': 0,
            'total_reward': 0.0,
            'total_utility': 0.0,
            'steps': 0,
            'actions_taken': [],
            'locations_visited': [],
            'inventory_history': [],
        }

    def log_step(self,
                 step: int,
                 state: np.ndarray,
                 action: np.ndarray,
                 reward: float,
                 next_state: np.ndarray,
                 done: bool,
                 agent_data: Optional[Dict[str, Any]] = None):
        """
        Log data for a single step.

        Args:
            step: Step number in episode
            state: State vector before action
            action: Action taken (one-hot encoded)
            reward: Reward received
            next_state: State vector after action
            done: Whether episode ended
            agent_data: Additional agent data (location, inventory, hp, etc.)
        """
        # Extract action index
        if isinstance(action, np.ndarray):
            action_idx = int(np.argmax(action))
            action_array = action.tolist()
        elif isinstance(action, (list, tuple)):
            action_idx = int(np.argmax(action))
            action_array = list(action)
        else:
            action_idx = int(action)
            action_array = action

        step_record = {
            'step': step,
            'state': state.tolist() if isinstance(state, np.ndarray) else state,
            'action': action_array,
            'action_index': action_idx,
            'reward': float(reward),
            'next_state': next_state.tolist() if isinstance(next_state, np.ndarray) else next_state,
            'done': done,
        }

        # Add agent-specific data if provided
        if agent_data:
            step_record.update(agent_data)

        self.step_data.append(step_record)

        # Update episode aggregates
        self.current_episode['total_reward'] += reward
        self.current_episode['steps'] += 1
        self.current_episode['actions_taken'].append(action_idx)

        if agent_data:
            if 'location' in agent_data:
                self.current_episode['locations_visited'].append(agent_data['location'])
            if 'inventory' in agent_data:
                self.current_episode['inventory_history'].append(agent_data['inventory'].copy())
            if 'utilities' in agent_data:
                self.current_episode['total_utility'] = agent_data['utilities']

    def end_episode(self, episode_number: int) -> Dict[str, Any]:
        """
        Finalize episode and return episode summary.

        Args:
            episode_number: Episode number

        Returns:
            Dictionary with episode metrics
        """
        self.current_episode['episode_number'] = episode_number

        # Calculate action distribution
        action_counts = {}
        for action_idx in self.current_episode['actions_taken']:
            action_counts[action_idx] = action_counts.get(action_idx, 0) + 1

        total_actions = len(self.current_episode['actions_taken'])
        action_distribution = {
            action_idx: count / total_actions
            for action_idx, count in action_counts.items()
        } if total_actions > 0 else {}

        self.current_episode['action_distribution'] = action_distribution
        self.current_episode['action_counts'] = action_counts

        # Store episode data
        episode_summary = self.current_episode.copy()
        episode_summary['step_data'] = self.step_data.copy()

        self.episode_metrics.append(episode_summary)

        return episode_summary

    def get_episode_summary(self, episode_number: int) -> Optional[Dict[str, Any]]:
        """
        Get summary for a specific episode.

        Args:
            episode_number: Episode number to retrieve

        Returns:
            Episode summary dictionary or None if not found
        """
        for episode in self.episode_metrics:
            if episode['episode_number'] == episode_number:
                return episode
        return None

    def get_recent_episodes(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get summaries for the n most recent episodes.

        Args:
            n: Number of recent episodes to return

        Returns:
            List of episode summary dictionaries
        """
        return self.episode_metrics[-n:] if len(self.episode_metrics) >= n else self.episode_metrics

    def get_action_name(self, action_index: int) -> str:
        """
        Convert action index to human-readable name.

        Args:
            action_index: Index of action (0-8)

        Returns:
            Action name string
        """
        action_names = {
            0: 'move_right',
            1: 'move_down',
            2: 'move_left',
            3: 'move_up',
            4: 'produce_local',
            5: 'cook',
            6: 'consume_apple',
            7: 'consume_fish',
            8: 'consume_cooked_fish',
        }
        return action_names.get(action_index, f'unknown_{action_index}')

    def get_training_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics across all episodes.

        Returns:
            Dictionary with training-level metrics
        """
        if not self.episode_metrics:
            return {}

        utilities = [ep['total_utility'] for ep in self.episode_metrics]
        rewards = [ep['total_reward'] for ep in self.episode_metrics]
        steps = [ep['steps'] for ep in self.episode_metrics]

        return {
            'total_episodes': len(self.episode_metrics),
            'mean_utility': np.mean(utilities) if utilities else 0,
            'std_utility': np.std(utilities) if utilities else 0,
            'max_utility': max(utilities) if utilities else 0,
            'mean_reward': np.mean(rewards) if rewards else 0,
            'mean_steps': np.mean(steps) if steps else 0,
            'utility_trend': utilities,
            'reward_trend': rewards,
        }
