#!/bin/zsh

# Directory to store collected data
DATA_DIR="./data/2"

# How many data I want to collect in each map
HOW_MANY=10

# Ensure the data directory exists
mkdir -p "$DATA_DIR"

# Iterate from map 1 to 10
for map in {1..10}
do
  echo "Running map $map"

  # Create or clear a directory for the current map's data
  MAP_DIR="$DATA_DIR/map_$map"
  mkdir -p "$MAP_DIR"

  # Run the game for 20 rounds
  for ((round=1; round<=HOW_MANY; round++))
  do
    echo "Round $round for map $map"
    export ROUND=$round

    # Start the Python game with the --one-shot flag
    python -m mlgame -f 60 --one-shot -i ./ml/ml_play_manual.py . --game_type PRACTICE --sensor_num 5 --sound off --time_to_play 2500 --map $map

    # Your game script should handle data collection and file writing per round
  done

  # After 20 rounds, process the collected data as needed
  echo "Completed 20 rounds for map $map."
  # Here, you might process or summarize the data collected in MAP_DIR
done

echo "Completed data collection."