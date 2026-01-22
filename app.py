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
    
    with col_ctrl:
        st.subheader("Controls")
        pop_options = [
            "Normal", 
            "Uniform", 
            "Right Skewed (Income)", 
            "Left Skewed (Easy Test)", 
            "Bimodal (Two Species)", 
            "U-Shape (Polarized)"
        ]
        
        l_pop_type = st.selectbox("Pick a World Shape", pop_options, key="l_pop")
        l_n = st.slider("Sample Size (n)", min_value=1, max_value=100, value=2, key="l_n")
        
        st.info("**Vibe Check:** Notice how averaging acts as a filter for the 'ugliness' of the parent population.")

    l_data = get_pop_data(l_pop_type)
    l_means = np.mean(np.random.choice(l_data, size=(2000, l_n)), axis=1)

    with col_plot:
        # Population Plot - FIXED: removed singular 'color', added plural 'colors'
        fig1 = ff.create_distplot([l_data], ["Population"], show_hist=True, show_rug=False, colors=['#3366CC'])
        fig1.update_layout(height=300, title="The Population (The 'True' World)", margin=dict(t=30, b=0))
        # FIXED: use_container_width=True replaced with width='stretch'
        st.plotly_chart(fig1, width='stretch')
        
        # Sampling Distribution Plot - FIXED: plural 'colors' only
        fig2 = ff.create_distplot([l_means], ["Sampling Dist"], show_hist=True, colors=['#109618'])
        fig2.update_layout(height=400, title=f"The Sampling Distribution (n={l_n})", margin=dict(t=30, b=0))
        # FIXED: width='stretch'
        st.plotly_chart(fig2, width='stretch')
        
        st.write(f"**$\mu$:** {np.mean(l_data):.2f} | **$\mu_{\\bar{x}}$:** {np.mean(l_means):.2f} | **$SD_{\\bar{x}}$:** {np.std(l_means):.2f}")

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
        # Mystery Plot - FIXED: plural 'colors'
        fig_g = ff.create_distplot([g_means], ["Mystery Dist"], show_hist=True, colors=['#FF9900'])
        fig_g.update_layout(height=450, title=f"Testing Sampling Distribution with n={g_n}")
        # FIXED: width='stretch'
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
