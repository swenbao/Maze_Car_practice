#!/bin/zsh

# Directory to store collected data
DATA_DIR="./data/1

# how many data I want to collect in each level
HOW_MANY = 20

# Ensure the data directory exists
mkdir -p "$DATA_DIR"

# Iterate from map 1 to 24
for map in {1..10}
do
  echo "Running map $map"

  # Create or clear a directory for the current level's data
  LEVEL_DIR="$DATA_DIR/map_$level"
  mkdir -p "$LEVEL_DIR"
  > "$LEVEL_DIR/round_info.txt"  # Assuming you want to store some round-specific information here

  # Run the game for 20 rounds
  for ROUND in {1..$HOW_MANY}
  do
    echo "Round $ROUND for map $map"

    # Start the Python game with the --one-shot flag
    python -m mlgame --no-display -f 1000000 --one-shot -i ./ml/ml_play_template.py . --game_type PRACTICE --sensor_num 5 --sound off --time_to_play 2500 --map $map

    # Since the game terminates after one round, there's no need to monitor and kill the process
    # Your game script should handle data collection and file writing per round
  done

  # After 20 rounds, process the collected data as needed
  echo "Completed 20 rounds for map $map."
  # Here, you might process or summarize the data collected in LEVEL_DIR
done

echo "All levels completed."