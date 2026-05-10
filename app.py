import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="ProjectLamine ⚽", page_icon="⚽")

# Title
st.title("⚽ ProjectLamine")
st.markdown("*Before the big clubs. Before the headlines.*")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("players_data.csv", low_memory=False)
    stat_cols = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    for col in stat_cols:
        df[col] = df[col].fillna(df[col].median())
    df = df.dropna(subset=['overall', 'potential', 'age', 'league_name'])
    df['gem_score'] = df['potential'] - df['overall']
    df['youth_bonus'] = df['age'].apply(lambda x: 5 if x <= 23 else 0)
    df['final_gem_score'] = df['gem_score'] + df['youth_bonus']
    return df

df = load_data()

# Filters
st.sidebar.header("🔍 Scout Filters")
max_age = st.sidebar.slider("Maximum Age", 16, 30, 23)
min_overall = st.sidebar.slider("Minimum Overall", 40, 80, 60)
max_overall = st.sidebar.slider("Maximum Overall", 50, 90, 75)
min_score = st.sidebar.slider("Minimum Gem Score", 1, 20, 8)

# Filter data
gems = df[
    (df['age'] <= max_age) &
    (df['overall'] >= min_overall) &
    (df['overall'] <= max_overall) &
    (df['final_gem_score'] >= min_score)
].sort_values('final_gem_score', ascending=False)

# Results
st.subheader(f"🌟 {len(gems)} Hidden Gems Found")

st.dataframe(
    gems[['short_name', 'age', 'nationality_name', 'league_name',
          'club_name', 'overall', 'potential', 'final_gem_score']
    ].head(50).reset_index(drop=True),
    use_container_width=True
)

st.markdown("---")
st.caption("Built with ❤️ using FIFA 23 data | ProjectLamine")