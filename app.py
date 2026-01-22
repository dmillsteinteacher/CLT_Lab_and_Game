import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import scipy.stats as stats
import plotly.graph_objects as go

# Set page to wide mode
st.set_page_config(page_title="The CLT Experience", layout="wide")

st.title("The CLT Experience: From Chaos to Predictability")

# --- POPULATION GENERATOR ---
@st.cache_data
def get_pop_data(ptype):
    """Generates a large population based on the selected shape."""
    size = 100000
    if ptype == "Normal":
        return np.random.normal(50, 15, size)
    elif ptype == "Uniform":
        return np.random.uniform(0, 100, size)
    elif ptype == "Right Skedwed (Income)":
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

# --- TAB 1: THE LAB ---
with tab1:
    st.header("Exploration: The 'Normalizer' in Action")
    col_ctrl, col_plot = st.columns([1, 3])
    
    pop_options = [
        "Normal", 
        "Uniform", 
        "Right Skewed (Income)", 
        "Left Skewed (Easy Test)", 
        "Bimodal (Two Species)", 
        "U-Shape (Polarized)"
    ]

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
        st.plotly_chart(fig1, width='stretch')
        st.write(fr"**Population Parameters:** $\mu = {mu:.2f}$ | $\sigma = {sigma:.2f}$")
        st.divider()
        fig2 = ff.create_distplot([l_means], ["Sampling Dist"], show_hist=True, show_curve=False, show_rug=False, colors=['#109618'])
        fig2.update_layout(height=400, title=f"Sampling Distribution of x̄ (n={l_n})", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig2, width='stretch')
        st.write(fr"**Sampling Distribution Statistics:** $\mu_{{\bar{{x}}}} = {np.mean(l_means):.2f}$")
        st.write(fr"**Standard Error:** Simulated $SD_{{\bar{{x}}}} = {np.std(l_means):.2f}$ | Theoretical $\frac{{\sigma}}{{\sqrt{{n}}}} = {sigma/np.sqrt(l_n):.2f}$")

# --- TAB 2: NAME THAT POPULATION ---
with tab2:
    st.header("The Challenge: Name That Population")
    st.write("Commit to a sample size and make your guess. Remember: larger $n$ values make the parent's identity harder to see!")

    if 'mystery_type' not in st.session_state:
        st.session_state.mystery_type = np.random.choice(pop_options)
    if 'revealed' not in st.session_state:
        st.session_state.revealed = False

    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g2:
        st.subheader("The Challenge")
        # CHANGED: Replaced slider with number_input for suspense
        g_n = st.number_input(
            "Enter Sample Size (n):", 
            min_value=1, 
            max_value=100, 
            value=1, 
            step=1, 
            key="g_n_input"
        )
        
        show_normal = st.checkbox("Overlay Normal Reference", value=False)
        
        st.write("---")
        st.write("### Your Guess:")
        user_guess = st.radio("What was the source shape?", pop_options)
        
        if st.button("Final Answer"):
            st.session_state.revealed = True

    # Simulation with the manually entered n
    g_data = get_pop_data(st.session_state.mystery_type)
    g_means = np.mean(np.random.choice(g_data, size=(1500, g_n)), axis=1)

    with col_g1:
        fig_g = ff.create_distplot([g_means], ["Mystery Dist"], show_hist=True, show_curve=show_normal, show_rug=False, colors=['#FF9900'])
        fig_g.update_layout(height=500, title=f"Mystery Sampling Distribution (n={g_n})", showlegend=False)
        st.plotly_chart(fig_g, width='stretch')

    if st.session_state.revealed:
        if user_guess == st.session_state.mystery_type:
            st.success(f"🎯 **Correct!** It was **{st.session_state.mystery_type}**.")
            if g_n > 20:
                st.info(f"Statistics Master! You identified the shape even after the CLT smoothed it out with n={g_n}.")
            st.balloons()
        else:
            st.error(f"❌ **Incorrect.** You guessed {user_guess}, but it was actually **{st.session_state.mystery_type}**.")
        
        if st.button("Play Next Round"):
            st.session_state.mystery_type = np.random.choice(pop_options)
            st.session_state.revealed = False
            st.rerun()

    st.divider()
    st.caption("Pedagogical Goal: Notice how convergence speeds vary. Normal and Uniform shapes become indistinguishable quickly, while Bimodal and U-shapes persist longer.")

# --- PADDING ---
# .............................................................................
# END OF FILE
