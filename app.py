
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Foot Predict",
    page_icon="⚽",
    layout="wide"
)

DATA = Path(__file__).parent / "data"

teams = pd.read_csv(DATA / "teams_demo.csv")
players = pd.read_csv(DATA / "players_demo.csv")

st.title("⚽ Foot Predict")
st.caption("Football Analytics — Saison 2026–2027")

st.warning(
    "Prototype éducatif : les données sont fictives "
    "et les estimations ne sont pas des prédictions fiables."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Vue d’ensemble",
        "Analyse d’un match",
        "Analyse des joueurs",
        "Données"
    ]
)

if page == "Vue d’ensemble":

    st.header("Tableau de bord")

    col1, col2, col3 = st.columns(3)

    col1.metric("Équipes", len(teams))
    col2.metric("Joueurs", len(players))
    col3.metric("Saison", "2026–2027")

    st.subheader("Équipes")
    st.dataframe(teams, use_container_width=True)

elif page == "Analyse d’un match":

    st.header("Analyse comparative")

    names = teams["team"].tolist()

    col1, col2 = st.columns(2)

    home_name = col1.selectbox(
        "Équipe à domicile",
        names,
        index=0
    )

    away_name = col2.selectbox(
        "Équipe à l’extérieur",
        names,
        index=1
    )

    if home_name == away_name:
        st.error("Choisis deux équipes différentes.")

    else:
        home = teams[teams.team == home_name].iloc[0]
        away = teams[teams.team == away_name].iloc[0]

        home_est = max(
            0.2,
            (home.goals_for + away.goals_against) / 2 + 0.15
        )

        away_est = max(
            0.2,
            (away.goals_for + home.goals_against) / 2
        )

        a, b, c = st.columns(3)

        a.metric(
            f"Buts estimés — {home_name}",
            f"{home_est:.2f}"
        )

        b.metric(
            f"Buts estimés — {away_name}",
            f"{away_est:.2f}"
        )

        c.metric(
            "Total estimé",
            f"{home_est + away_est:.2f}"
        )

        st.caption(
            "Calcul heuristique de démonstration, "
            "non entraîné et non calibré."
        )

elif page == "Analyse des joueurs":

    st.header("Statistiques individuelles")

    selected = st.selectbox(
        "Filtrer par équipe",
        ["Toutes"] + sorted(players.team.unique().tolist())
    )

    view = (
        players
        if selected == "Toutes"
        else players[players.team == selected]
    )

    st.dataframe(view, use_container_width=True)

    if not view.empty:

        name = st.selectbox(
            "Choisir un joueur",
            view.player.tolist()
        )

        player = view[view.player == name].iloc[0]

        a, b, c = st.columns(3)

        a.metric("Buts", int(player.goals))
        b.metric("Passes décisives", int(player.assists))
        c.metric("Tirs cadrés", int(player.shots_on_target))

else:

    st.header("Jeux de données")

    st.subheader("Équipes")
    st.dataframe(teams, use_container_width=True)

    st.subheader("Joueurs")
    st.dataframe(players, use_container_width=True)
