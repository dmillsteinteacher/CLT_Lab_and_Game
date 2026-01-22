import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import scipy.stats as stats

# Set page to wide mode for side-by-side comparison
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
    elif ptype == "Skewed (Exponential)":
        return np.random.exponential(20, size)
    elif ptype == "Bimodal":
        return np.concatenate([np.random.normal(25, 5, size//2), np.random.normal(75, 5, size//2)])
    elif ptype == "U-Shape":
        # Beta distribution with alpha, beta < 1 creates a U-shape
        return np.random.beta(0.2, 0.2, size) * 100
    return np.random.normal(50, 15, size)

# --- TABS SETUP ---
tab1, tab2 = st.tabs(["🔬 Tab 1: The Lab", "🎮 Tab 2: The Permission Slip Game"])

# --- TAB 1: THE LAB ---
with tab1:
    st.header("Exploration: The 'Normalizer' in Action")
    
    # Layout for controls and plots
    col_ctrl, col_plot = st.columns([1, 3])
    
    with col_ctrl:
        st.subheader("Controls")
        l_pop_type = st.selectbox(
            "Pick a World Shape (Population)", 
            ["Normal", "Uniform", "Skewed (Exponential)", "Bimodal", "U-Shape"], 
            key="l_pop"
        )
        l_n = st.slider("Sample Size (n)", min_value=1, max_value=100, value=2, key="l_n")
        
        st.info("""
        **What to watch:**
        1. Does the center of the means match the center of the world?
        2. How large does **n** need to be before the bottom graph looks like a Bell Curve?
        """)

    # Generate Data
    l_data = get_pop_data(l_pop_type)
    # Take 2000 samples of size n and find their means
    l_means = np.mean(np.random.choice(l_data, size=(2000, l_n)), axis=1)

    with col_plot:
        # Top Plot: Population
        fig1 = ff.create_distplot([l_data], ["Population Distribution"], show_hist=True, show_rug=False)
        fig1.update_layout(height=300, title="The Population (The 'True' World)", margin=dict(t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)
        
        # Bottom Plot: Sampling Distribution
        fig2 = ff.create_distplot([l_means], ["Sampling Distribution of Means"], show_hist=True, color='green')
        fig2.update_layout(height=400, title=f"The Sampling Distribution (n={l_n})", margin=dict(t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)
        
        st.write(f"**Population Mean:** {np.mean(l_data):.2f} | **Mean of Sample Means:** {np.mean(l_means):.2f}")

# --- TAB 2: THE GAME ---
with tab2:
    st.header("The 'Permission Slip' Challenge")
    st.write("A mystery population has been generated. Can you find the **minimum n** required to use Normal Inference?")

    # Initialize Mystery Population in Session State so it persists
    if 'mystery_type' not in st.session_state:
        st.session_state.mystery_type = np.random.choice(["Uniform", "Skewed (Exponential)", "Bimodal", "U-Shape"])
    
    g_n = st.number_input("Test a Sample Size (n):", min_value=1, max_value=100, value=2)
    
    g_data = get_pop_data(st.session_state.mystery_type)
    g_means = np.mean(np.random.choice(g_data, size=(1000, g_n)), axis=1)
    
    # Normality Test (Shapiro-Wilk)
    # We test a subset of 500 for the p-value calculation
    _, p_val = stats.shapiro(g_means[:500])
    
    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g1:
        fig_g = ff.create_distplot([g_means], ["Mystery Distribution"], show_hist=True, color='orange')
        fig_g.update_layout(height=450, title=f"Testing Sampling Distribution with n={g_n}")
        st.plotly_chart(fig_g, use_container_width=True)
        
    with col_g2:
        st.subheader("Normality Meter")
        if p_val > 0.05:
            st.success("✅ PERMISSION GRANTED")
            st.balloons()
            st.write(f"At n={g_n}, this distribution is **Normal enough** for our Z-test math to work.")
            
            if st.button("Reveal Mystery Population"):
                st.info(f"The population shape was: **{st.session_state.mystery_type}**")
                if st.button("Play Again / New Mystery"):
                    del st.session_state.mystery_type
                    st.rerun()
        else:
            st.error("❌ PERMISSION DENIED")
            st.write("The distribution is still too 'Ugly' or skewed. The Normal model would be inaccurate here.")
            st.warning("Increase **n** and try again!")

    st.divider()
    st.caption("Note: We use the Shapiro-Wilk test (p > 0.05) to mathematically 'verify' normality for this game.")