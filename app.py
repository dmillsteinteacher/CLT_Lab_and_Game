import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import scipy.stats as stats

# Set page to wide mode
st.set_page_config(page_title="The CLT Experience", layout="wide")

st.title("The CLT Experience: From Chaos to Predictability")

# --- POPULATION GENERATOR ---
@st.cache_data
def get_pop_data(ptype):
    size = 100000
    if ptype == "Normal":
        return np.random.normal(50, 15, size)
    elif ptype == "Uniform":
        return np.random.uniform(0, 100, size)
    elif ptype == "Right Skewed (Income)":
        return np.random.exponential(20, size)
    elif ptype == "Left Skewed (Easy Test)":
        return 100 - np.random.exponential(20, size)
    elif ptype == "Bimodal (Two Species)":
        return np.concatenate([np.random.normal(25, 5, size//2), np.random.normal(75, 5, size//2)])
    elif ptype == "U-Shape (Polarized)":
        return np.random.beta(0.2, 0.2, size) * 100
    return np.random.normal(50, 15, size)

# --- TABS SETUP ---
tab1, tab2 = st.tabs(["🔬 Tab 1: The Lab", "🎮 Tab 2: Name That Population"])

# --- TAB 1: THE LAB (UNCHANGED) ---
pop_options = ["Normal", "Uniform", "Right Skewed (Income)", "Left Skewed (Easy Test)", "Bimodal (Two Species)", "U-Shape (Polarized)"]

with tab1:
    st.header("Exploration: The 'Normalizer' in Action")
    col_ctrl, col_plot = st.columns([1, 3])
    with col_ctrl:
        st.subheader("Controls")
        l_pop_type = st.selectbox("Pick a World Shape", pop_options, key="l_pop")
        l_n = st.slider("Sample Size (n)", min_value=1, max_value=100, value=2, key="l_n")
        st.markdown(f"**Note:** As $n$ increases, the sampling distribution of x̄ increasingly resembles a normal distribution.")
    l_data = get_pop_data(l_pop_type)
    mu, sigma = np.mean(l_data), np.std(l_data)
    l_means = np.mean(np.random.choice(l_data, size=(2000, l_n)), axis=1)
    with col_plot:
        fig1 = ff.create_distplot([l_data], ["Population"], show_hist=True, show_curve=False, show_rug=False, colors=['#3366CC'])
        fig1.update_layout(height=300, title="Parent Population Distribution", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig1, key="lab_pop")
        st.write(fr"**Population Parameters:** $\mu = {mu:.2f}$ | $\sigma = {sigma:.2f}$")
        st.divider()
        fig2 = ff.create_distplot([l_means], ["Sampling Dist"], show_hist=True, show_curve=False, show_rug=False, colors=['#109618'])
        fig2.update_layout(height=400, title=f"Sampling Distribution of x̄ (n={l_n})", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig2, key="lab_samp")
        st.write(fr"**Standard Error:** Simulated $SD_{{\bar{{x}}}} = {np.std(l_means):.2f}$ | Theoretical $\frac{{\sigma}}{{\sqrt{{n}}}} = {sigma/np.sqrt(l_n):.2f}$")

# --- TAB 2: NAME THAT POPULATION ---
with tab2:
    st.header("Challenge: Name That Population")
    
    if 'mystery_type' not in st.session_state:
        st.session_state.mystery_type = np.random.choice(pop_options)
    if 'game_stage' not in st.session_state:
        st.session_state.game_stage = "input" # Stages: input -> guess -> reveal

    # PHASE 1: INPUT
    if st.session_state.game_stage == "input":
        st.write("### Step 1: Design your experiment.")
        st.write("Choose a sample size ($n$). If $n$ is too small, you see the population's chaos. If $n$ is too large, the CLT hides the truth.")
        n_input = st.number_input("Enter n to generate the Sampling Distribution:", min_value=1, max_value=100, value=1)
        if st.button("Generate Data"):
            st.session_state.current_n = n_input
            st.session_state.game_stage = "guess"
            st.rerun()

    # PHASE 2: GUESS
    elif st.session_state.game_stage == "guess":
        col_g1, col_g2 = st.columns([2, 1])
        
        g_data = get_pop_data(st.session_state.mystery_type)
        g_means = np.mean(np.random.choice(g_data, size=(1500, st.session_state.current_n)), axis=1)
        
        with col_g1:
            fig_g = ff.create_distplot([g_means], ["Mystery"], show_hist=True, show_curve=False, show_rug=False, colors=['#FF9900'])
            fig_g.update_layout(height=500, title=f"Sampling Distribution (n={st.session_state.current_n})", showlegend=False)
            st.plotly_chart(fig_g, key="game_plot")
            
        with col_g2:
            st.subheader("Step 2: Make Your Guess")
            st.write(f"Based on this distribution for $n={st.session_state.current_n}$, what is the parent shape?")
            user_guess = st.radio("Select Shape:", pop_options)
            if st.button("Submit Guess"):
                st.session_state.user_guess = user_guess
                st.session_state.game_stage = "reveal"
                st.rerun()

    # PHASE 3: REVEAL
    elif st.session_state.game_stage == "reveal":
        st.subheader("Step 3: The Reveal")
        if st.session_state.user_guess == st.session_state.mystery_type:
            st.success(f"🎯 **Correct!** It was **{st.session_state.mystery_type}**.")
            st.balloons()
        else:
            st.error(f"❌ **Incorrect.** You guessed {st.session_state.user_guess}, but it was **{st.session_state.mystery_type}**.")
        
        # Display the "Why" - show the parent population
        p_data = get_pop_data(st.session_state.mystery_type)
        fig_reveal = ff.create_distplot([p_data], ["Parent"], show_hist=True, show_curve=False, show_rug=False, colors=['#3366CC'])
        fig_reveal.update_layout(height=300, title=f"Actual Parent Population: {st.session_state.mystery_type}", showlegend=False)
        st.plotly_chart(fig_reveal, key="reveal_plot")
        
        if st.button("Start New Round"):
            st.session_state.mystery_type = np.random.choice(pop_options)
            st.session_state.game_stage = "input"
            st.rerun()

    st.divider()
    st.caption("Pedagogical Goal: Develop an intuition for how much information is lost at various values of n.")

# --- PADDING ---
# .............................................................................
# END OF FILE
