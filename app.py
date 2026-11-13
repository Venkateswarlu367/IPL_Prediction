import streamlit as st
import pandas as pd
import pickle
import time
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IPL Prediction System",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists("players.csv"):
    st.error("❌ players.csv not found. Please create the dataset first.")
    st.stop()

if not os.path.exists("ipl_prediction_model.pkl"):
    st.error("❌ ipl_prediction_model.pkl not found. Please create the model first.")
    st.stop()

try:
    players = pd.read_csv("players.csv")

    with open("ipl_prediction_model.pkl", "rb") as file:
        model = pickle.load(file)

except Exception as e:
    st.error(f"❌ Error loading files: {e}")
    st.stop()

# ============================================================
# TEAM DATA
# ============================================================

teams = players["Team"].unique().tolist()

strengths = (
    players
    .groupby("Team")["Performance_Percentage"]
    .mean()
    .to_dict()
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ============================================================
   BACKGROUND
============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(255, 0, 102, 0.12),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(0, 119, 255, 0.12),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #f8faff,
            #eef3ff,
            #fff5fb
        );
}


/* ============================================================
   TEXT
============================================================ */

.stApp p {
    color: #252a48;
}

h1, h2, h3 {
    color: #171a3f !important;
}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #160b42,
            #302078,
            #56105f
        );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* ============================================================
   SIDEBAR TITLE
============================================================ */

.sidebar-title {
    text-align: center;
    font-size: 29px;
    font-weight: 900;
    padding: 18px;
    color: white !important;
}


/* ============================================================
   MAIN TITLE
============================================================ */

.main-title {
    font-size: 48px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #e6005c,
            #7928ca,
            #0077d9
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {

    0% {
        filter:
            drop-shadow(
                0 0 2px
                rgba(230,0,92,0.2)
            );
    }

    50% {
        filter:
            drop-shadow(
                0 0 18px
                rgba(121,40,202,0.4)
            );
    }

    100% {
        filter:
            drop-shadow(
                0 0 2px
                rgba(0,119,217,0.2)
            );
    }
}


/* ============================================================
   SUBTITLE
============================================================ */

.subtitle {
    color: #555b78 !important;
    font-size: 19px;
    margin-bottom: 20px;
}


/* ============================================================
   STAT CARDS
============================================================ */

.stat-card {
    min-height: 125px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #e6005c,
            #7928ca
        );

    box-shadow:
        0 10px 30px
        rgba(121,40,202,0.25);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;
}

.stat-card:hover {
    transform:
        translateY(-8px)
        scale(1.03);

    box-shadow:
        0 20px 45px
        rgba(121,40,202,0.4);
}

.stat-number {
    color: white !important;
    font-size: 38px;
    font-weight: 900;
}

.stat-label {
    color: white !important;
    font-size: 16px;
    font-weight: 700;
}


/* ============================================================
   WELCOME CARD
============================================================ */

.welcome-card {
    padding: 30px;
    border-radius: 22px;

    background: white;

    border:
        1px solid #dfe3f1;

    box-shadow:
        0 10px 30px
        rgba(30,40,80,0.10);

    transition: 0.3s;
}

.welcome-card:hover {
    transform:
        translateY(-5px);

    box-shadow:
        0 18px 40px
        rgba(30,40,80,0.18);
}

.welcome-title {
    color: #171a3f !important;
    font-size: 28px;
    font-weight: 800;
}

.welcome-text {
    color: #444b69 !important;
    font-size: 17px;
    line-height: 1.7;
}


/* ============================================================
   TEAM CARDS
============================================================ */

.team-card {
    min-height: 165px;

    padding: 20px 10px;

    border-radius: 20px;

    background: white;

    border:
        2px solid #e2e6f2;

    box-shadow:
        0 8px 25px
        rgba(30,40,80,0.10);

    text-align: center;

    transition:
        all 0.35s ease;
}

.team-card:hover {
    transform:
        translateY(-8px)
        scale(1.03);

    border-color:
        #7928ca;

    box-shadow:
        0 18px 40px
        rgba(121,40,202,0.25);
}

.team-name {
    color: #202052 !important;
    font-size: 18px;
    font-weight: 800;
}

.team-label {
    color: #626985 !important;
    font-size: 14px;
    margin-top: 10px;
}

.team-strength {
    color: #e6005c !important;
    font-size: 30px;
    font-weight: 900;
    margin-top: 8px;
}


/* ============================================================
   PREDICTION CARD
============================================================ */

.prediction-card {
    padding: 40px;
    margin-top: 25px;

    border-radius: 28px;

    text-align: center;

    background:
        linear-gradient(
            120deg,
            #e6005c,
            #7928ca,
            #0077d9,
            #7928ca
        );

    background-size:
        300% 300%;

    animation:
        gradientMove 5s ease infinite;

    box-shadow:
        0 20px 60px
        rgba(121,40,202,0.35);
}

@keyframes gradientMove {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.prediction-title {
    color: white !important;
    font-size: 25px;
    font-weight: 800;
}

.prediction-winner {
    color: white !important;
    font-size: 42px;
    font-weight: 900;
    margin: 12px;
}

.prediction-confidence {
    color: white !important;
    font-size: 20px;
}


/* ============================================================
   BUTTON
============================================================ */

.stButton > button {

    width: 100%;

    min-height: 52px;

    border: none;

    border-radius: 15px;

    font-size: 18px;

    font-weight: 800;

    color: white !important;

    background:
        linear-gradient(
            90deg,
            #e6005c,
            #7928ca,
            #0077d9
        );

    transition:
        all 0.3s ease;
}

.stButton > button:hover {

    transform:
        translateY(-3px)
        scale(1.02);

    box-shadow:
        0 8px 30px
        rgba(121,40,202,0.4);
}


/* ============================================================
   SELECT BOX
============================================================ */

div[data-baseweb="select"] > div {

    background-color:
        white !important;

    border:
        2px solid #d7dcef !important;

    border-radius:
        12px !important;
}

div[data-baseweb="select"] span {

    color:
        #171a3f !important;
}

.stSelectbox label {

    color:
        #202052 !important;

    font-weight:
        700 !important;
}


/* ============================================================
   METRICS
============================================================ */

[data-testid="stMetric"] {

    background:
        white;

    border:
        1px solid #dfe3f1;

    border-radius:
        18px;

    padding:
        18px;

    box-shadow:
        0 8px 25px
        rgba(30,40,80,0.10);
}

[data-testid="stMetricLabel"] * {

    color:
        #555d7a !important;
}

[data-testid="stMetricValue"] * {

    color:
        #171a3f !important;

    font-weight:
        900 !important;
}


/* ============================================================
   PROGRESS BAR
============================================================ */

.stProgress > div > div > div > div {

    background:
        linear-gradient(
            90deg,
            #e6005c,
            #7928ca,
            #0077d9
        );
}


/* ============================================================
   FOOTER
============================================================ */

.footer-box {

    margin-top:
        50px;

    padding:
        25px;

    text-align:
        center;

    border-top:
        1px solid #dce1ee;
}

.footer-title {

    color:
        #202052 !important;

    font-size:
        20px;

    font-weight:
        800;
}

.footer-text {

    color:
        #656c86 !important;

    font-size:
        14px;
}


/* ============================================================
   FLOATING BALL
============================================================ */

.floating-ball {

    position:
        fixed;

    right:
        25px;

    bottom:
        25px;

    font-size:
        45px;

    z-index:
        999;

    animation:
        ballBounce 2s ease-in-out infinite;
}

@keyframes ballBounce {

    0% {
        transform:
            translateY(0)
            rotate(0deg);
    }

    50% {
        transform:
            translateY(-20px)
            rotate(10deg);
    }

    100% {
        transform:
            translateY(0)
            rotate(0deg);
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FLOATING BALL
# ============================================================

st.markdown(
    '<div class="floating-ball">🏏</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    '<div class="sidebar-title">🏏 IPL PREDICTOR</div>',
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "🚀 Navigation",
    [
        "🏠 Home",
        "🔮 Match Prediction",
        "👤 Player Performance",
        "⚔️ Team Comparison",
        "📊 Statistics",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🤖 Machine Learning")
st.sidebar.write("Random Forest Classifier")

st.sidebar.markdown("### 📊 Dataset")
st.sidebar.write(f"🏆 Teams: {len(teams)}")
st.sidebar.write(f"👤 Players: {len(players)}")
st.sidebar.write("🏏 Matches: 5000")

st.sidebar.markdown("---")

st.sidebar.caption(
    "IPL Data Science Project"
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">'
        '🏏 IPL Prediction System'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '⚡ Machine Learning • Player Analytics • Match Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-number">10</div>'
            '<div class="stat-label">🏆 IPL Teams</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-number">180</div>'
            '<div class="stat-label">👤 Players</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-number">5000</div>'
            '<div class="stat-label">🏏 Matches</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            '<div class="stat-card">'
            '<div class="stat-number">RF</div>'
            '<div class="stat-label">🤖 ML Model</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.write("")

    # --------------------------------------------------------
    # WELCOME
    # --------------------------------------------------------

    st.markdown(
        '<div class="welcome-card">'
        '<div class="welcome-title">'
        '🔥 Welcome to IPL Analytics'
        '</div>'
        '<div class="welcome-text">'
        'Welcome to the IPL Prediction System. '
        'This project combines Machine Learning, '
        'player statistics and team analysis to '
        'predict the likely winner of an IPL match.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # TEAMS
    # --------------------------------------------------------

    st.subheader("🏆 IPL Teams")

    for start in range(0, len(teams), 5):

        current_teams = teams[start:start + 5]

        columns = st.columns(5)

        for index, team in enumerate(current_teams):

            with columns[index]:

                st.markdown(
                    f'<div class="team-card">'
                    f'<div class="team-name">'
                    f'{team}'
                    f'</div>'
                    f'<div class="team-label">'
                    f'💪 Average Strength'
                    f'</div>'
                    f'<div class="team-strength">'
                    f'{strengths[team]:.1f}%'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.write("")


# ============================================================
# MATCH PREDICTION
# ============================================================

elif page == "🔮 Match Prediction":

    st.markdown(
        '<div class="main-title">'
        '🔮 Match Winner Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '🤖 AI powered IPL match prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # Team selection

    col1, col2 = st.columns(2)

    with col1:

        team1 = st.selectbox(
            "🏏 Select Team 1",
            teams,
            key="team1"
        )

    with col2:

        team2_list = [
            team
            for team in teams
            if team != team1
        ]

        team2 = st.selectbox(
            "🏏 Select Team 2",
            team2_list,
            key="team2"
        )

    strength1 = strengths[team1]
    strength2 = strengths[team2]

    st.write("")

    # Strength display

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            f"💪 {team1}",
            f"{strength1:.1f}%"
        )

    with col2:

        st.metric(
            f"💪 {team2}",
            f"{strength2:.1f}%"
        )

    st.write("")

    # Venue and toss

    col1, col2 = st.columns(2)

    with col1:

        venue = st.selectbox(
            "🏟️ Venue",
            [
                "Neutral",
                "Team 1 Home",
                "Team 2 Home"
            ]
        )

    with col2:

        toss_winner = st.selectbox(
            "🪙 Toss Winner",
            [
                team1,
                team2
            ]
        )

    # Factors

    if venue == "Team 1 Home":

        venue_factor = 3.0

    elif venue == "Team 2 Home":

        venue_factor = -3.0

    else:

        venue_factor = 0.0

    if toss_winner == team1:

        toss_advantage = 2.0

    else:

        toss_advantage = -2.0

    st.write("")

    # Prediction

    if st.button(
        "🚀 PREDICT WINNER",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 AI is analyzing the match..."
        ):

            time.sleep(1)

            input_data = pd.DataFrame(
                [[
                    strength1,
                    strength2,
                    toss_advantage,
                    venue_factor
                ]],
                columns=[
                    "Team1_Strength",
                    "Team2_Strength",
                    "Toss_Advantage",
                    "Venue_Factor"
                ]
            )

            probabilities = model.predict_proba(
                input_data
            )[0]

            team1_probability = float(
                probabilities[1]
            )

            team2_probability = float(
                probabilities[0]
            )

            if team1_probability >= team2_probability:

                winner = team1
                confidence = team1_probability

            else:

                winner = team2
                confidence = team2_probability

        st.balloons()

        st.markdown(
            f'<div class="prediction-card">'
            f'<div class="prediction-title">'
            f'🏆 PREDICTED WINNER'
            f'</div>'
            f'<div class="prediction-winner">'
            f'{winner}'
            f'</div>'
            f'<div class="prediction-confidence">'
            f'🤖 Model Confidence: '
            f'{confidence * 100:.1f}%'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                f"🏏 {team1}",
                f"{team1_probability * 100:.1f}%"
            )

            st.progress(
                team1_probability
            )

        with col2:

            st.metric(
                f"🏏 {team2}",
                f"{team2_probability * 100:.1f}%"
            )

            st.progress(
                team2_probability
            )


# ============================================================
# PLAYER PERFORMANCE
# ============================================================

elif page == "👤 Player Performance":

    st.markdown(
        '<div class="main-title">'
        '👤 Player Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '🔥 Player statistics and performance analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    selected_team = st.selectbox(
        "🏏 Select Team",
        teams
    )

    team_players = players[
        players["Team"] == selected_team
    ].copy()

    team_players = team_players.sort_values(
        "Performance_Percentage",
        ascending=False
    )

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Players",
            len(team_players)
        )

    with col2:

        st.metric(
            "🔥 Best Rating",
            f"{team_players['Performance_Percentage'].max():.1f}%"
        )

    with col3:

        st.metric(
            "📊 Average Rating",
            f"{team_players['Performance_Percentage'].mean():.1f}%"
        )

    with col4:

        st.metric(
            "🏏 Total Runs",
            f"{team_players['Runs'].sum():,}"
        )

    st.write("")

    # Table

    st.subheader(
        "📋 Player Statistics"
    )

    columns_to_show = [
        "Player_Name",
        "Role",
        "Matches",
        "Runs",
        "Wickets",
        "Strike_Rate",
        "Economy",
        "Performance_Percentage"
    ]

    st.dataframe(
        team_players[columns_to_show],
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    # Top 5

    st.subheader(
        "🔥 Top 5 Players"
    )

    top5 = (
        team_players
        .nlargest(
            5,
            "Performance_Percentage"
        )
        [
            [
                "Player_Name",
                "Performance_Percentage"
            ]
        ]
        .set_index("Player_Name")
    )

    st.bar_chart(top5)

    st.write("")

    # Individual player

    st.subheader(
        "🔍 Individual Player"
    )

    selected_player = st.selectbox(
        "Select Player",
        team_players["Player_Name"].tolist()
    )

    player = team_players[
        team_players["Player_Name"] == selected_player
    ].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏏 Runs",
            int(player["Runs"])
        )

    with col2:

        st.metric(
            "🎯 Wickets",
            int(player["Wickets"])
        )

    with col3:

        st.metric(
            "⚡ Strike Rate",
            f"{player['Strike_Rate']:.2f}"
        )

    with col4:

        st.metric(
            "🔥 Performance",
            f"{player['Performance_Percentage']:.1f}%"
        )


# ============================================================
# TEAM COMPARISON
# ============================================================

elif page == "⚔️ Team Comparison":

    st.markdown(
        '<div class="main-title">'
        '⚔️ Team Comparison'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '💪 Compare two IPL teams'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        comparison_team1 = st.selectbox(
            "🏏 Team 1",
            teams,
            key="comparison1"
        )

    with col2:

        comparison_team2 = st.selectbox(
            "🏏 Team 2",
            [
                team
                for team in teams
                if team != comparison_team1
            ],
            key="comparison2"
        )

    strength_team1 = strengths[
        comparison_team1
    ]

    strength_team2 = strengths[
        comparison_team2
    ]

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f'<div class="team-card">'
            f'<div class="team-name">'
            f'{comparison_team1}'
            f'</div>'
            f'<div class="team-label">'
            f'💪 Team Strength'
            f'</div>'
            f'<div class="team-strength">'
            f'{strength_team1:.1f}%'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f'<div class="team-card">'
            f'<div class="team-name">'
            f'{comparison_team2}'
            f'</div>'
            f'<div class="team-label">'
            f'💪 Team Strength'
            f'</div>'
            f'<div class="team-strength">'
            f'{strength_team2:.1f}%'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.write("")

    comparison_data = pd.DataFrame(
        {
            "Team Strength": [
                strength_team1,
                strength_team2
            ]
        },
        index=[
            comparison_team1,
            comparison_team2
        ]
    )

    st.subheader(
        "📊 Strength Comparison"
    )

    st.bar_chart(
        comparison_data
    )

    if strength_team1 > strength_team2:

        st.success(
            f"🏆 {comparison_team1} has the higher "
            f"project team-strength rating."
        )

    elif strength_team2 > strength_team1:

        st.success(
            f"🏆 {comparison_team2} has the higher "
            f"project team-strength rating."
        )

    else:

        st.info(
            "⚖️ Both teams have the same strength."
        )


# ============================================================
# STATISTICS
# ============================================================

elif page == "📊 Statistics":

    st.markdown(
        '<div class="main-title">'
        '📊 IPL Statistics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '📈 Explore project statistics and rankings'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🔥 Highest Rating",
            f"{players['Performance_Percentage'].max():.1f}%"
        )

    with col2:

        st.metric(
            "📊 Average Rating",
            f"{players['Performance_Percentage'].mean():.1f}%"
        )

    with col3:

        st.metric(
            "👤 Players",
            len(players)
        )

    with col4:

        st.metric(
            "🏆 Teams",
            players["Team"].nunique()
        )

    st.write("")

    # Team ranking

    st.subheader(
        "🏆 Team Strength Ranking"
    )

    ranking = pd.DataFrame(
        list(strengths.items()),
        columns=[
            "Team",
            "Team Strength"
        ]
    )

    ranking = ranking.sort_values(
        "Team Strength",
        ascending=False
    )

    ranking["Rank"] = range(
        1,
        len(ranking) + 1
    )

    ranking["Team Strength"] = (
        ranking["Team Strength"]
        .round(2)
    )

    st.dataframe(
        ranking[
            [
                "Rank",
                "Team",
                "Team Strength"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        ranking[
            [
                "Team",
                "Team Strength"
            ]
        ].set_index("Team")
    )

    st.write("")

    # Role distribution

    st.subheader(
        "👤 Player Role Distribution"
    )

    role_data = (
        players["Role"]
        .value_counts()
        .rename_axis("Role")
        .reset_index(
            name="Players"
        )
    )

    st.dataframe(
        role_data,
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    # Top players

    st.subheader(
        "🌟 Top 10 Players"
    )

    top10 = (
        players
        .nlargest(
            10,
            "Performance_Percentage"
        )
        [
            [
                "Player_Name",
                "Team",
                "Role",
                "Runs",
                "Wickets",
                "Performance_Percentage"
            ]
        ]
    )

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">'
        'ℹ️ About Project'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '🏏 IPL Prediction Machine Learning Project'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        ### 🏏 IPL Prediction System

        This is an educational Data Science and
        Machine Learning project designed to analyze
        IPL teams and players.

        ### 🤖 Machine Learning

        **Algorithm:** Random Forest Classifier

        The prediction model uses:

        - Team 1 Strength
        - Team 2 Strength
        - Toss Advantage
        - Venue Factor

        ### 📊 Dataset

        - 🏆 10 IPL Teams
        - 👤 180 Players
        - 🏏 5000 Match Records

        ### 📈 Player Performance

        Player performance is a project-generated
        metric based on batting, bowling, fielding
        and recent-form ratings.
        """
    )

    st.warning(
        "⚠️ This project uses synthetic/project-generated "
        "data. The predictions are for educational purposes "
        "and are not official IPL predictions."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-box">'
    '<div class="footer-title">'
    '🏏 IPL Prediction System'
    '</div>'
    '<div class="footer-text">'
    '🤖 Machine Learning &nbsp; • &nbsp; '
    '📊 Data Science &nbsp; • &nbsp; '
    '🏆 IPL Analytics'
    '</div>'
    '<div class="footer-text">'
    'Made for educational purposes ❤️'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)