"""
Metric logger for persisting training data to disk.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class MetricLogger:
    """
    Logs metrics to JSON Lines format for later analysis.

    Each line in the output file is a valid JSON object representing
    one episode's data.
    """

    def __init__(self, log_dir: str = './runs', experiment_name: Optional[str] = None):
        """
        Initialize metric logger.

        Args:
            log_dir: Base directory for logs
            experiment_name: Name of experiment (defaults to timestamp)
        """
        if experiment_name is None:
            experiment_name = f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.experiment_name = experiment_name
        self.log_dir = Path(log_dir) / experiment_name
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # File paths
        self.episodes_file = self.log_dir / 'episodes.jsonl'
        self.steps_file = self.log_dir / 'steps.jsonl'
        self.summary_file = self.log_dir / 'summary.json'
        self.config_file = self.log_dir / 'config.json'

        # Initialize files
        self.episodes_file.touch(exist_ok=True)
        self.steps_file.touch(exist_ok=True)

        print(f"Logging metrics to: {self.log_dir}")

    def log_config(self, config: Dict[str, Any]):
        """
        Save experiment configuration.

        Args:
            config: Configuration dictionary
        """
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def log_episode(self, episode_data: Dict[str, Any], include_steps: bool = True):
        """
        Log episode data to JSON Lines file.

        Args:
            episode_data: Dictionary with episode metrics
            include_steps: Whether to log individual steps to separate file
        """
        # Log episode summary
        episode_summary = episode_data.copy()

        # Extract step data if present
        step_data = episode_summary.pop('step_data', [])

        # Write episode summary
        with open(self.episodes_file, 'a') as f:
            f.write(json.dumps(episode_summary) + '\n')

        # Optionally write detailed step data
        if include_steps and step_data:
            with open(self.steps_file, 'a') as f:
                for step in step_data:
                    step_record = {
                        'episode': episode_data['episode_number'],
                        **step
                    }
                    f.write(json.dumps(step_record) + '\n')

    def log_training_summary(self, summary: Dict[str, Any]):
        """
        Save overall training summary.

        Args:
            summary: Training summary dictionary
        """
        with open(self.summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

    def get_log_dir(self) -> Path:
        """Get path to log directory."""
        return self.log_dir

    def load_episodes(self) -> list:
        """
        Load all episode data from log file.

        Returns:
            List of episode dictionaries
        """
        episodes = []
        if self.episodes_file.exists():
            with open(self.episodes_file, 'r') as f:
                for line in f:
                    if line.strip():
                        episodes.append(json.loads(line))
        return episodes

    def load_steps(self, episode_number: Optional[int] = None) -> list:
        """
        Load step data from log file.

        Args:
            episode_number: If specified, only load steps for this episode

        Returns:
            List of step dictionaries
        """
        steps = []
        if self.steps_file.exists():
            with open(self.steps_file, 'r') as f:
                for line in f:
                    if line.strip():
                        step = json.loads(line)
                        if episode_number is None or step.get('episode') == episode_number:
                            steps.append(step)
        return steps

    def __repr__(self) -> str:
        return f"MetricLogger(experiment='{self.experiment_name}', log_dir='{self.log_dir}')"
