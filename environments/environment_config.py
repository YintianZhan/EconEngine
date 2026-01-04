"""
Environment configuration loader for EconEngine.

Loads YAML configuration files to create economic environments.
"""

import yaml
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path


class EnvironmentConfig:
    """
    Configuration for an economic environment.

    Attributes:
        name: Environment name
        grid_size: (width, length) tuple
        episode_length: Number of time steps per episode
        resources: Dict mapping resource names to their properties
        agent_start: Starting location (x, y) for agent
        optimal_utility: Expected optimal utility (for validation)
        optimal_strategy: Description of optimal strategy (for documentation)
    """

    def __init__(self, config_dict: Dict[str, Any]):
        """Initialize environment config from dictionary."""
        self.name = config_dict.get('environment_name', 'unnamed')
        self.grid_size = tuple(config_dict.get('grid_size', [2, 2]))
        self.episode_length = config_dict.get('episode_length', 24)
        self.resources = config_dict.get('resources', {})
        self.agent_start = tuple(config_dict.get('agent_start', [0, 0]))
        self.optimal_utility = config_dict.get('optimal_utility', None)
        self.optimal_strategy = config_dict.get('optimal_strategy', None)

        # Production chains (for moderate environments)
        self.production_chains = config_dict.get('production_chains', [])

    def get_resource_locations(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Extract resource locations from config.

        Returns:
            Dict mapping resource names to list of (x, y) locations
        """
        locations = {}
        for resource_name, properties in self.resources.items():
            if isinstance(properties, dict) and 'locations' in properties:
                locations[resource_name] = [tuple(loc) for loc in properties['locations']]
            elif isinstance(properties, dict) and 'location' in properties:
                locations[resource_name] = [tuple(properties['location'])]
        return locations

    def get_resource_regeneration(self, resource_name: str) -> Optional[float]:
        """
        Get regeneration rate for a resource.

        Args:
            resource_name: Name of the resource

        Returns:
            Regeneration rate (None means infinite/instant regeneration)
        """
        if resource_name not in self.resources:
            return None

        properties = self.resources[resource_name]
        if isinstance(properties, dict):
            regen = properties.get('regeneration_rate', properties.get('regeneration', None))
            if regen == 'inf' or regen == float('inf'):
                return None  # Infinite regeneration
            return regen
        return None

    def get_resource_capacity(self, resource_name: str) -> Optional[int]:
        """
        Get maximum capacity for a resource at a location.

        Args:
            resource_name: Name of the resource

        Returns:
            Maximum capacity (None means unlimited)
        """
        if resource_name not in self.resources:
            return None

        properties = self.resources[resource_name]
        if isinstance(properties, dict):
            return properties.get('max_capacity', None)
        return None

    def __repr__(self) -> str:
        return f"EnvironmentConfig(name='{self.name}', grid={self.grid_size}, episode_length={self.episode_length})"


def load_environment(config_path: str) -> EnvironmentConfig:
    """
    Load environment configuration from YAML file.

    Args:
        config_path: Path to YAML config file

    Returns:
        EnvironmentConfig object

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Environment config not found: {config_path}")

    with open(path, 'r') as f:
        config_dict = yaml.safe_load(f)

    return EnvironmentConfig(config_dict)


def get_preset_config(preset_name: str) -> EnvironmentConfig:
    """
    Load a preset environment configuration.

    Args:
        preset_name: Name of preset (e.g., 'simple_2x2', 'moderate_5x5')

    Returns:
        EnvironmentConfig object

    Raises:
        FileNotFoundError: If preset doesn't exist
    """
    # Get the directory where this file lives
    module_dir = Path(__file__).parent
    config_path = module_dir / 'configs' / f'{preset_name}.yaml'

    return load_environment(str(config_path))
