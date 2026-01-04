"""
Streamlit Dashboard for EconEngine Agent Visualization

Visualizes agent learning behavior, actions, inventory, and spatial movement patterns.

Usage:
    streamlit run streamlit_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="EconEngine Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Action name mapping
ACTION_NAMES = {
    0: 'Move Right',
    1: 'Move Down',
    2: 'Move Left',
    3: 'Move Up',
    4: 'Produce Local',
    5: 'Cook',
    6: 'Consume Apple',
    7: 'Consume Fish',
    8: 'Consume Cooked Fish',
}

ACTION_CATEGORIES = {
    0: 'Move', 1: 'Move', 2: 'Move', 3: 'Move',
    4: 'Produce', 5: 'Produce',
    6: 'Consume', 7: 'Consume', 8: 'Consume',
}


@st.cache_data
def load_experiment_list():
    """Load list of available experiments from runs directory."""
    runs_dir = Path('./runs')
    if not runs_dir.exists():
        return []

    experiments = []
    for exp_dir in runs_dir.iterdir():
        if exp_dir.is_dir():
            config_file = exp_dir / 'config.json'
            if config_file.exists():
                experiments.append({
                    'name': exp_dir.name,
                    'path': str(exp_dir)
                })

    return sorted(experiments, key=lambda x: x['name'], reverse=True)


@st.cache_data
def load_experiment_data(experiment_path):
    """Load all data for an experiment."""
    exp_dir = Path(experiment_path)

    # Load config
    with open(exp_dir / 'config.json', 'r') as f:
        config = json.load(f)

    # Load episodes
    episodes = []
    episodes_file = exp_dir / 'episodes.jsonl'
    if episodes_file.exists():
        with open(episodes_file, 'r') as f:
            for line in f:
                if line.strip():
                    episodes.append(json.loads(line))

    # Load steps (if available)
    steps = []
    steps_file = exp_dir / 'steps.jsonl'
    if steps_file.exists():
        with open(steps_file, 'r') as f:
            for line in f:
                if line.strip():
                    steps.append(json.loads(line))

    # Load summary (if available)
    summary = None
    summary_file = exp_dir / 'summary.json'
    if summary_file.exists():
        with open(summary_file, 'r') as f:
            summary = json.load(f)

    return {
        'config': config,
        'episodes': episodes,
        'steps': steps,
        'summary': summary
    }


def plot_training_progress(episodes):
    """Plot training progress over episodes."""
    if not episodes:
        st.warning("No episode data available")
        return

    df = pd.DataFrame(episodes)

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Total utility
    fig.add_trace(go.Scatter(
        x=df['episode_number'],
        y=df['total_utility'],
        mode='lines+markers',
        name='Total Utility',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))

    # Moving average
    if len(df) >= 10:
        window = min(20, len(df) // 2)
        moving_avg = df['total_utility'].rolling(window=window, center=True).mean()
        fig.add_trace(go.Scatter(
            x=df['episode_number'],
            y=moving_avg,
            mode='lines',
            name=f'Moving Avg ({window} eps)',
            line=dict(color='#ff7f0e', width=3, dash='dash')
        ))

    fig.update_layout(
        title='Training Progress: Total Utility per Episode',
        xaxis_title='Episode Number',
        yaxis_title='Total Utility',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_action_distribution(episode_data):
    """Plot action distribution for an episode."""
    action_counts = episode_data.get('action_counts', {})

    if not action_counts:
        st.warning("No action data available for this episode")
        return

    # Convert action indices to names
    action_labels = [ACTION_NAMES.get(int(k), f'Action {k}') for k in action_counts.keys()]
    action_values = list(action_counts.values())

    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=action_labels,
        values=action_values,
        hole=0.3,
        marker=dict(colors=px.colors.qualitative.Set3)
    )])

    fig.update_layout(
        title='Action Distribution',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_action_category_distribution(episode_data):
    """Plot action distribution by category (Move/Produce/Consume)."""
    actions_taken = episode_data.get('actions_taken', [])

    if not actions_taken:
        st.warning("No action data available")
        return

    # Categorize actions
    categories = [ACTION_CATEGORIES.get(a, 'Unknown') for a in actions_taken]
    category_counts = pd.Series(categories).value_counts()

    # Create bar chart
    fig = go.Figure(data=[go.Bar(
        x=category_counts.index,
        y=category_counts.values,
        marker=dict(color=['#2ecc71', '#e74c3c', '#3498db'])
    )])

    fig.update_layout(
        title='Action Category Distribution',
        xaxis_title='Action Category',
        yaxis_title='Count',
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_inventory_trajectory(episode_data):
    """Plot inventory levels over time."""
    inventory_history = episode_data.get('inventory_history', [])

    if not inventory_history:
        st.warning("No inventory data available")
        return

    # Convert to DataFrame
    df = pd.DataFrame(inventory_history)

    # Create line chart
    fig = go.Figure()

    colors = {
        'apple': '#e74c3c',
        'fish': '#3498db',
        'wood': '#95a5a6',
        'cooked fish': '#f39c12'
    }

    for resource in df.columns:
        if resource in colors:
            fig.add_trace(go.Scatter(
                x=list(range(len(df))),
                y=df[resource],
                mode='lines+markers',
                name=resource.title(),
                line=dict(color=colors.get(resource, '#000'), width=2),
                marker=dict(size=4)
            ))

    fig.update_layout(
        title='Inventory Levels Over Time',
        xaxis_title='Time Step',
        yaxis_title='Quantity',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_spatial_heatmap(episode_data, grid_size):
    """Plot spatial heatmap showing where agent spent time."""
    locations_visited = episode_data.get('locations_visited', [])

    if not locations_visited:
        st.warning("No location data available")
        return

    # Count time at each location
    location_counts = {}
    for loc in locations_visited:
        loc_tuple = tuple(loc) if isinstance(loc, list) else loc
        location_counts[loc_tuple] = location_counts.get(loc_tuple, 0) + 1

    # Create grid
    width, height = grid_size
    grid = np.zeros((height, width))

    for (x, y), count in location_counts.items():
        if 0 <= x < height and 0 <= y < width:
            grid[x][y] = count

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=grid,
        colorscale='YlOrRd',
        text=grid.astype(int),
        texttemplate='%{text}',
        textfont={"size": 16},
        hovertemplate='Location (%{x}, %{y})<br>Time Spent: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title='Spatial Heatmap: Time Spent at Each Location',
        xaxis_title='Y Coordinate',
        yaxis_title='X Coordinate',
        height=400,
        xaxis=dict(side='bottom'),
        yaxis=dict(autorange='reversed')
    )

    st.plotly_chart(fig, use_container_width=True)


def show_episode_replay(steps_data):
    """Show step-by-step episode replay."""
    if not steps_data:
        st.warning("No step data available. Steps are only logged every 10 episodes.")
        return

    st.subheader("📽️ Episode Replay")

    # Step selector
    step_num = st.slider(
        "Select Step",
        min_value=0,
        max_value=len(steps_data) - 1,
        value=0,
        key='step_slider'
    )

    step = steps_data[step_num]

    # Display step info
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Step", step['step'])
        st.metric("Action", ACTION_NAMES.get(step['action_index'], 'Unknown'))

    with col2:
        st.metric("Reward", f"{step['reward']:.3f}")
        st.metric("Done", "Yes" if step.get('done', False) else "No")

    with col3:
        if 'hp' in step:
            st.metric("HP", step['hp'])
        if 'utilities' in step:
            st.metric("Total Utility", f"{step['utilities']:.2f}")

    # Show inventory if available
    if 'inventory' in step:
        st.write("**Inventory:**")
        inv_df = pd.DataFrame([step['inventory']])
        st.dataframe(inv_df, use_container_width=True)

    # Show location if available
    if 'location' in step:
        st.write(f"**Location:** {step['location']}")


def create_animated_map(steps_data, grid_size, step_num):
    """
    Create an animated map showing agent position and resources.

    Args:
        steps_data: List of step dictionaries
        grid_size: Tuple of (width, height)
        step_num: Current step number to display

    Returns:
        Plotly figure with agent on map
    """
    import plotly.graph_objects as go

    width, height = grid_size
    step = steps_data[step_num]

    # Get agent location
    agent_loc = step.get('location', [0, 0])
    agent_x = agent_loc[1] if isinstance(agent_loc, (list, tuple)) else 0
    agent_y = agent_loc[0] if isinstance(agent_loc, (list, tuple)) else 0

    # Create resource map (hardcoded for simple_2x2, can be made dynamic later)
    resource_map = {
        (0, 0): '🐟 Fish',
        (0, 1): '🍎 Apple',
        (1, 0): '💧 Water',
        (1, 1): '🪵 Wood'
    }

    # Create grid data for heatmap background
    grid_data = []
    annotations = []

    for x in range(height):
        row = []
        for y in range(width):
            # Base color (light gray)
            row.append(0.2)

            # Add resource labels
            if (x, y) in resource_map:
                annotations.append(
                    dict(
                        x=y,
                        y=x,
                        text=resource_map[(x, y)],
                        showarrow=False,
                        font=dict(size=20, color='#333'),
                        xanchor='center',
                        yanchor='middle'
                    )
                )
        grid_data.append(row)

    # Highlight agent's current location
    grid_data[agent_y][agent_x] = 1.0

    # Create figure
    fig = go.Figure()

    # Add grid heatmap
    fig.add_trace(go.Heatmap(
        z=grid_data,
        colorscale=[
            [0, '#f0f0f0'],      # Light gray for empty cells
            [0.5, '#fff3cd'],    # Light yellow for resources
            [1, '#28a745']       # Green for agent location
        ],
        showscale=False,
        hoverinfo='skip'
    ))

    # Add agent marker
    fig.add_trace(go.Scatter(
        x=[agent_x],
        y=[agent_y],
        mode='markers+text',
        marker=dict(
            size=40,
            color='#ff6b6b',
            symbol='star',
            line=dict(color='white', width=2)
        ),
        text=['🤖'],
        textfont=dict(size=30),
        textposition='middle center',
        hoverinfo='skip',
        showlegend=False
    ))

    # Update layout
    fig.update_layout(
        title=f'Agent Location - Step {step["step"]}',
        xaxis=dict(
            title='Y Coordinate',
            tickmode='linear',
            tick0=0,
            dtick=1,
            range=[-0.5, width - 0.5],
            showgrid=False
        ),
        yaxis=dict(
            title='X Coordinate',
            tickmode='linear',
            tick0=0,
            dtick=1,
            range=[-0.5, height - 0.5],
            showgrid=False,
            autorange='reversed'
        ),
        width=500,
        height=500,
        annotations=annotations,
        plot_bgcolor='white'
    )

    return fig


def show_animated_replay(steps_data, grid_size):
    """Show animated episode replay with map visualization."""
    if not steps_data:
        st.warning("No step data available. Steps are only logged every 10 episodes.")
        return

    st.subheader("📽️ Animated Episode Replay")

    # Animation controls
    col1, col2 = st.columns([3, 1])

    with col1:
        step_num = st.slider(
            "Select Step",
            min_value=0,
            max_value=len(steps_data) - 1,
            value=0,
            key='animated_step_slider'
        )

    with col2:
        # Auto-play toggle (future enhancement)
        st.write("")  # Spacer

    step = steps_data[step_num]

    # Two column layout: Map on left, details on right
    col_map, col_details = st.columns([1, 1])

    with col_map:
        # Show animated map
        map_fig = create_animated_map(steps_data, grid_size, step_num)
        st.plotly_chart(map_fig, use_container_width=True)

        # Show trajectory (path taken so far)
        if step_num > 0:
            trajectory = [s.get('location', [0, 0]) for s in steps_data[:step_num + 1]]
            trajectory_str = " → ".join([f"({loc[0]},{loc[1]})" for loc in trajectory if loc])
            st.caption(f"**Path:** {trajectory_str}")

    with col_details:
        st.subheader("Step Details")

        # Metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Step", step['step'])
            st.metric("Reward", f"{step['reward']:.3f}")
            if 'hp' in step:
                st.metric("HP", step['hp'])

        with col_b:
            st.metric("Action", ACTION_NAMES.get(step['action_index'], 'Unknown'))
            st.metric("Done", "Yes" if step.get('done', False) else "No")
            if 'utilities' in step:
                st.metric("Utility", f"{step['utilities']:.2f}")

        # Inventory
        if 'inventory' in step:
            st.write("**Inventory:**")
            inv_data = step['inventory']
            inv_cols = st.columns(4)
            resources = ['apple', 'fish', 'wood', 'cooked fish']
            emojis = ['🍎', '🐟', '🪵', '🍳']

            for idx, (res, emoji) in enumerate(zip(resources, emojis)):
                with inv_cols[idx]:
                    st.metric(
                        emoji,
                        f"{inv_data.get(res, 0):.0f}",
                        label_visibility="visible"
                    )


# Main Dashboard
def main():
    st.title("📊 EconEngine Agent Dashboard")
    st.markdown("Visualize agent learning behavior, actions, and spatial movement patterns")

    # Sidebar - Experiment selection
    st.sidebar.header("🔬 Experiment Selection")

    experiments = load_experiment_list()

    if not experiments:
        st.error("No experiments found in ./runs/ directory. Run training first!")
        st.info("Run: `python agent.py` to generate training data")
        return

    # Select experiment
    experiment_names = [exp['name'] for exp in experiments]
    selected_name = st.sidebar.selectbox(
        "Select Experiment",
        experiment_names,
        index=0
    )

    selected_exp = next(exp for exp in experiments if exp['name'] == selected_name)

    # Load experiment data
    data = load_experiment_data(selected_exp['path'])

    # Display config
    st.sidebar.subheader("⚙️ Configuration")
    st.sidebar.json(data['config'])

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Training Progress",
        "🎬 Episode Analysis",
        "📊 Statistics",
        "🎮 Episode Replay",
        "🚀 New Training"
    ])

    # Tab 1: Training Progress
    with tab1:
        st.header("Training Progress")

        if data['episodes']:
            plot_training_progress(data['episodes'])

            # Summary stats
            st.subheader("Summary Statistics")
            df = pd.DataFrame(data['episodes'])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Episodes", len(df))
            with col2:
                st.metric("Max Utility", f"{df['total_utility'].max():.2f}")
            with col3:
                st.metric("Mean Utility", f"{df['total_utility'].mean():.2f}")
            with col4:
                st.metric("Final Utility", f"{df['total_utility'].iloc[-1]:.2f}")
        else:
            st.warning("No episode data available")

    # Tab 2: Episode Analysis
    with tab2:
        st.header("Episode Analysis")

        if data['episodes']:
            # Episode selector
            episode_num = st.selectbox(
                "Select Episode",
                range(len(data['episodes'])),
                index=len(data['episodes']) - 1,  # Default to last episode
                format_func=lambda x: f"Episode {x} (Utility: {data['episodes'][x]['total_utility']:.2f})"
            )

            episode = data['episodes'][episode_num]

            # Episode overview
            st.subheader(f"Episode {episode_num} Overview")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Utility", f"{episode['total_utility']:.2f}")
            with col2:
                st.metric("Total Reward", f"{episode['total_reward']:.2f}")
            with col3:
                st.metric("Steps Taken", episode['steps'])
            with col4:
                actions_taken = len(episode.get('actions_taken', []))
                st.metric("Actions", actions_taken)

            # Visualizations
            col1, col2 = st.columns(2)

            with col1:
                plot_action_distribution(episode)
                plot_action_category_distribution(episode)

            with col2:
                plot_inventory_trajectory(episode)

                # Spatial heatmap
                grid_size = data['config'].get('grid_size', [2, 2])
                plot_spatial_heatmap(episode, grid_size)
        else:
            st.warning("No episode data available")

    # Tab 3: Statistics
    with tab3:
        st.header("Training Statistics")

        if data['episodes']:
            df = pd.DataFrame(data['episodes'])

            # Overall statistics
            st.subheader("Overall Statistics")

            stats_df = pd.DataFrame({
                'Metric': ['Mean Utility', 'Std Utility', 'Max Utility', 'Min Utility', 'Total Episodes'],
                'Value': [
                    f"{df['total_utility'].mean():.2f}",
                    f"{df['total_utility'].std():.2f}",
                    f"{df['total_utility'].max():.2f}",
                    f"{df['total_utility'].min():.2f}",
                    len(df)
                ]
            })
            st.dataframe(stats_df, use_container_width=True)

            # Learning progression
            st.subheader("Learning Progression")

            # Split into phases
            n_episodes = len(df)
            phase_size = max(1, n_episodes // 3)

            early = df.iloc[:phase_size]
            mid = df.iloc[phase_size:2*phase_size]
            late = df.iloc[2*phase_size:]

            phase_stats = pd.DataFrame({
                'Phase': ['Early', 'Middle', 'Late'],
                'Episodes': [f"0-{phase_size-1}", f"{phase_size}-{2*phase_size-1}", f"{2*phase_size}-{n_episodes-1}"],
                'Mean Utility': [
                    f"{early['total_utility'].mean():.2f}",
                    f"{mid['total_utility'].mean():.2f}",
                    f"{late['total_utility'].mean():.2f}"
                ],
                'Max Utility': [
                    f"{early['total_utility'].max():.2f}",
                    f"{mid['total_utility'].max():.2f}",
                    f"{late['total_utility'].max():.2f}"
                ]
            })
            st.dataframe(phase_stats, use_container_width=True)

            # Display summary if available
            if data['summary']:
                st.subheader("Training Summary")
                st.json(data['summary'])
        else:
            st.warning("No episode data available")

    # Tab 4: Episode Replay
    with tab4:
        if data['episodes']:
            # Select episode for replay
            episode_num_replay = st.selectbox(
                "Select Episode for Replay",
                range(len(data['episodes'])),
                index=len(data['episodes']) - 1,
                format_func=lambda x: f"Episode {x}",
                key='replay_episode_selector'
            )

            # Get steps for this episode
            episode_steps = [s for s in data['steps'] if s.get('episode') == episode_num_replay]

            if episode_steps:
                # Get grid size from config
                grid_size = tuple(data['config'].get('grid_size', [2, 2]))

                # Show animated replay with map visualization
                show_animated_replay(episode_steps, grid_size)
            else:
                st.info(f"No detailed step data for Episode {episode_num_replay}. Steps are logged every 10 episodes. Try selecting a multiple of 10.")
        else:
            st.warning("No episode data available")

    # Tab 5: New Training
    with tab5:
        st.header("🚀 Start New Training Session")

        st.markdown("""
        Configure and launch a new training session. The agent will train with the specified
        parameters and results will be saved to a new experiment directory.
        """)

        # Training configuration form
        with st.form("training_config"):
            st.subheader("Training Configuration")

            col1, col2 = st.columns(2)

            with col1:
                # Environment selection
                env_configs = ['simple_2x2', 'simple_fish_cooking']
                environment = st.selectbox(
                    "Environment",
                    env_configs,
                    help="Select the environment configuration"
                )

                # Reward type selection
                reward_type = st.selectbox(
                    "Reward Type",
                    ['simple', 'opportunity_cost'],
                    help="Select the reward calculation method"
                )

                # Number of training episodes
                num_episodes = st.number_input(
                    "Training Episodes",
                    min_value=10,
                    max_value=10000,
                    value=400,
                    step=10,
                    help="Number of episodes for training"
                )

            with col2:
                # Number of test episodes
                num_test_episodes = st.number_input(
                    "Test Episodes",
                    min_value=0,
                    max_value=1000,
                    value=100,
                    step=10,
                    help="Number of test episodes (no learning)"
                )

                # Verbose output
                verbose = st.checkbox(
                    "Verbose Output",
                    value=True,
                    help="Print detailed training progress"
                )

                # Auto-open after training
                auto_open = st.checkbox(
                    "Auto-select after training",
                    value=True,
                    help="Automatically select new experiment when complete"
                )

            # Submit button
            submitted = st.form_submit_button("🎯 Start Training", use_container_width=True)

            if submitted:
                import subprocess
                import time
                from pathlib import Path

                st.success(f"Starting training with {num_episodes} training episodes + {num_test_episodes} test episodes...")
                st.info(f"Environment: {environment} | Reward: {reward_type}")

                # Create progress placeholder
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Build command
                cmd = [
                    'python3', 'agent.py',
                    '--config', environment, reward_type, str(num_episodes), str(num_test_episodes)
                ]

                status_text.text("Launching training process...")

                try:
                    # Start training process
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1
                    )

                    # Monitor progress
                    episode_count = 0
                    total_episodes = num_episodes + num_test_episodes

                    status_text.text("Training in progress...")

                    # Read output line by line
                    for line in process.stdout:
                        if 'Episode' in line and 'complete' in line:
                            episode_count += 1
                            progress = min(episode_count / total_episodes, 1.0)
                            progress_bar.progress(progress)
                            status_text.text(f"Progress: {episode_count}/{total_episodes} episodes | {line.strip()}")
                        elif 'Test Episode' in line:
                            episode_count += 1
                            progress = min(episode_count / total_episodes, 1.0)
                            progress_bar.progress(progress)
                            status_text.text(f"Testing: {episode_count - num_episodes}/{num_test_episodes} | {line.strip()}")

                    # Wait for completion
                    process.wait()

                    if process.returncode == 0:
                        progress_bar.progress(1.0)
                        status_text.text("✅ Training complete!")
                        st.success("Training finished successfully!")

                        # Find the latest experiment
                        runs_dir = Path('./runs')
                        experiments = sorted(runs_dir.glob('experiment_*'), key=lambda p: p.stat().st_mtime, reverse=True)
                        if experiments:
                            latest_exp = experiments[0].name
                            st.info(f"Results saved to: {latest_exp}")

                            if auto_open:
                                st.info("Rerun the dashboard to view the new experiment")
                                st.button("🔄 Refresh Dashboard", on_click=lambda: st.rerun())
                    else:
                        error_output = process.stderr.read()
                        st.error(f"Training failed with error code {process.returncode}")
                        st.code(error_output, language='text')

                except Exception as e:
                    st.error(f"Error starting training: {e}")
                    import traceback
                    st.code(traceback.format_exc(), language='text')


if __name__ == "__main__":
    main()
