# IPL Prediction System

A Streamlit-based IPL analytics website that combines a machine-learning match prediction model with player performance statistics and team comparisons.

## Features

- **Home dashboard:** Overview of the project, team list, and team-strength ratings.
- **Match prediction:** Select two teams, a venue condition, and the toss winner to estimate each team's winning probability.
- **Player performance:** View player statistics by team, explore the top five players, and inspect an individual player's metrics.
- **Team comparison:** Compare the project-generated strength ratings of two teams.
- **Statistics:** Explore team rankings, player-role distribution, and the top ten players.
- **About:** Project and model information, including the limitations of the predictions.

## Technology

- Python
- Streamlit
- Pandas
- NumPy
- scikit-learn
- Pickle (for loading the saved model)

## Project structure

```text
IPL_Prediction_Website/
├── app.py
├── ipl_prediction_model.pkl
├── matches.csv
├── players.csv
└── requirements.txt
```

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application and user interface |
| `ipl_prediction_model.pkl` | Saved machine-learning model loaded by the application |
| `players.csv` | Player records used for team strengths, player statistics, and dashboard metrics |
| `matches.csv` | Match dataset included with the project |
| `requirements.txt` | Python package dependencies |

> The current `app.py` loads `players.csv` and `ipl_prediction_model.pkl` directly. The bundled `matches.csv` is not read by the current application code.

## Requirements

- Python 3.9 or later (use a Python version compatible with the installed package versions)
- pip

## Installation

1. Download or clone this project and open a terminal in the project directory:

   ```bash
   cd IPL_Prediction_Website
   ```

2. (Recommended) Create and activate a virtual environment.

   **Windows:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the application

Make sure `app.py`, `players.csv`, and `ipl_prediction_model.pkl` are in the same directory. Then run:

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal (normally `http://localhost:8501`). Open that URL in your browser.

## How match prediction works

On the **Match Prediction** page:

1. Choose Team 1 and Team 2.
2. Select the venue condition: neutral, Team 1 home, or Team 2 home.
3. Select the toss winner.
4. Click **PREDICT WINNER**.

The application calculates each team's strength as the mean of `Performance_Percentage` for that team's players. It then supplies four features to the saved classifier:

- `Team1_Strength`
- `Team2_Strength`
- `Toss_Advantage`
- `Venue_Factor`

The app uses these project-defined adjustments:

- Toss advantage: `+2.0` when Team 1 wins the toss; otherwise `-2.0`.
- Venue factor: `+3.0` for Team 1 home, `-3.0` for Team 2 home, and `0.0` for a neutral venue.

The model's `predict_proba()` output is displayed as the two teams' estimated probabilities. The team with the higher probability is shown as the predicted winner.

## Expected player data

The application expects `players.csv` to contain at least these columns:

- `Team`
- `Player_Name`
- `Role`
- `Matches`
- `Runs`
- `Wickets`
- `Strike_Rate`
- `Economy`
- `Performance_Percentage`

The saved model must accept a four-feature input with the feature names and order shown above, and support `predict_proba()`.

## Notes and limitations

- This is an educational project, not an official IPL prediction service.
- The project describes its player and match data as synthetic/project-generated. Results should not be treated as real-world forecasts.
- The prediction depends on the included pre-trained model and the data in `players.csv`; this application does not train the model when it starts.
- The displayed toss and venue adjustments are fixed rules in the application, not live match information.
- `matches.csv` is included in the project archive but is not currently used by `app.py`.
- Keep the CSV files and model file in the same directory as `app.py`, or update the file paths in the code.
- Only load `.pkl` files from sources you trust. Pickle files can execute code when loaded.

## Troubleshooting

**`players.csv not found` or `ipl_prediction_model.pkl not found`**

Confirm that both files are in the same directory from which you run `streamlit run app.py`.

**`ModuleNotFoundError`**

Activate your virtual environment and run:

```bash
pip install -r requirements.txt
```

**Model loading or prediction error**

Check that the model file is valid and compatible with the scikit-learn version in your environment. Confirm that it was trained with the four expected features and supports probability predictions.

**CSV column error**

Check that `players.csv` contains all the required column names listed above, including the exact spelling and capitalization.

## License

No license file was included in the supplied project archive. Add a `LICENSE` file if you intend to distribute or reuse this project under a specific license.
