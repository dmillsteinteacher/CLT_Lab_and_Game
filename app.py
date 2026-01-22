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
tab1, tab2 = st.tabs(["🔬 Tab 1: The Lab", "🎮 Tab 2: The Permission Slip Game"])

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
        
        st.markdown(f"""
        **Note:** As the sample size ($n$) increases, the sampling distribution 
        of the mean (x̄) will increasingly resemble a normal distribution, 
        regardless of the shape of the parent population.
        """)

    l_data = get_pop_data(l_pop_type)
    mu = np.mean(l_data)
    sigma = np.std(l_data)
    
    # Generate Sampling Distribution (2000 simulations)
    l_means = np.mean(np.random.choice(l_data, size=(2000, l_n)), axis=1)
    mu_x_bar = np.mean(l_means)
    sd_x_bar = np.std(l_means)
    theoretical_se = sigma / np.sqrt(l_n)

    with col_plot:
        # --- POPULATION PLOT ---
        fig1 = ff.create_distplot([l_data], ["Population"], show_hist=True, show_curve=False, show_rug=False, colors=['#3366CC'])
        fig1.update_layout(height=300, title="Parent Population Distribution", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig1, width='stretch')
        
        st.write(fr"**Population Parameters:** $\mu = {mu:.2f}$ | $\sigma = {sigma:.2f}$")
        
        st.divider()

        # --- SAMPLING DISTRIBUTION PLOT ---
        # Using Unicode x̄ in the title to ensure proper rendering in Plotly
        fig2 = ff.create_distplot([l_means], ["Sampling Dist"], show_hist=True, show_curve=False, show_rug=False, colors=['#109618'])
        fig2.update_layout(height=400, title=f"Sampling Distribution of x̄ (n={l_n})", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig2, width='stretch')
        
        # Display Stats with the SE formula comparison using raw LaTeX strings
        st.write(fr"**Sampling Distribution Statistics:** $\mu_{{\bar{{x}}}} = {mu_x_bar:.2f}$")
        st.write(fr"**Standard Error:** Simulated $SD_{{\bar{{x}}}} = {sd_x_bar:.2f}$ | Theoretical $\frac{{\sigma}}{{\sqrt{{n}}}} = \frac{{{sigma:.2f}}}{{\sqrt{{{l_n}}}}} = {theoretical_se:.2f}$")

# --- TAB 2: THE GAME ---
with tab2:
    st.header("The 'Permission Slip' Challenge")
    st.write("A mystery population has been generated. Find the **minimum n** required to use Normal Inference.")

    if 'mystery_type' not in st.session_state:
        st.session_state.mystery_type = np.random.choice(pop_options[1:])
    
    g_n = st.number_input("Test a Sample Size (n):", min_value=1, max_value=100, value=2)
    
    g_data = get_pop_data(st.session_state.mystery_type)
    g_means = np.mean(np.random.choice(g_data, size=(1000, g_n)), axis=1)
    
    try:
        _, p_val = stats.shapiro(g_means[:500])
    except:
        p_val = 0 

    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g1:
        fig_g = ff.create_distplot([g_means], ["Mystery Dist"], show_hist=True, show_curve=False, show_rug=False, colors=['#FF9900'])
        fig_g.update_layout(height=450, title=f"Testing Sampling Distribution with n={g_n}")
        st.plotly_chart(fig_g, width='stretch')
        
    with col_g2:
        st.subheader("Normality Meter")
        if p_val > 0.05:
            st.success("✅ PERMISSION GRANTED")
            st.balloons()
            st.write(f"At n={g_n}, this is **Normal enough** to use the Z-table safely.")
            
            if st.button("Reveal Mystery Population"):
                st.info(f"The world was: **{st.session_state.mystery_type}**")
                if st.button("New Game"):
                    del st.session_state.mystery_type
                    st.rerun()
        else:
            st.error("❌ PERMISSION DENIED")
            st.write("The CLT hasn't smoothed out the parent population's influence yet.")
            st.warning("Increase **n** and try again!")

    st.divider()
    st.caption("Verification Engine: Shapiro-Wilk Normality Test (Alpha=0.05)")

# --- PADDING ---
# .............................................................................
# .............................................................................
# END OF FILE
