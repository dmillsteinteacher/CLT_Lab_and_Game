import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go

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
    elif ptype == "Right Skewed":
        return np.random.exponential(20, size)
    elif ptype == "Left Skewed":
        return 100 - np.random.exponential(20, size)
    elif ptype == "Bimodal":
        return np.concatenate([np.random.normal(25, 5, size//2), np.random.normal(75, 5, size//2)])
    elif ptype == "U-Shape":
        return np.random.beta(0.2, 0.2, size) * 100
    return np.random.normal(50, 15, size)

# --- TABS SETUP ---
tab1, tab2 = st.tabs(["🔬 Tab 1: Single Population Lab", "📊 Tab 2: Comparative Convergence Lab"])

pop_options = ["Normal", "Uniform", "Right Skewed", "Left Skewed", "Bimodal", "U-Shape"]

# --- TAB 1: SINGLE LAB (RETAINED AS BASELINE) ---
with tab1:
    st.header("Deep Dive: The 'Normalizer' in Action")
    col_ctrl, col_plot = st.columns([1, 3])
    with col_ctrl:
        l_pop_type = st.selectbox("Pick a World Shape", pop_options, key="l_pop")
        l_n = st.slider("Sample Size (n)", min_value=1, max_value=100, value=2, key="l_n_slider")
    
    l_data = get_pop_data(l_pop_type)
    mu, sigma = np.mean(l_data), np.std(l_data)
    l_means = np.mean(np.random.choice(l_data, size=(2000, l_n)), axis=1)
    
    with col_plot:
        fig1 = ff.create_distplot([l_data], ["Pop"], show_hist=True, show_curve=False, show_rug=False, colors=['#3366CC'])
        fig1.update_layout(height=250, title="Parent Population", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig1, key="l_fig1")
        
        fig2 = ff.create_distplot([l_means], ["Sampling"], show_hist=True, show_curve=False, show_rug=False, colors=['#109618'])
        fig2.update_layout(height=350, title=f"Sampling Distribution of x̄ (n={l_n})", margin=dict(t=30, b=0), showlegend=False)
        st.plotly_chart(fig2, key="l_fig2")
        st.write(fr"**Stats:** $\mu = {mu:.2f}$ | $\sigma = {sigma:.2f}$ | Sim $SE = {np.std(l_means):.2f}$ | Theo $SE = {sigma/np.sqrt(l_n):.2f}$")

# --- TAB 2: COMPARATIVE CONVERGENCE LAB ---
with tab2:
    st.header("The Universal Laws of Sampling")
    st.write("Scrub the slider to watch 6 different worlds obey the same statistical laws simultaneously.")

    # Using a slider for the 'Scrubbing' effect
    c_n = st.slider("Select Sample Size (n):", min_value=1, max_value=100, value=1, key="comp_n_slider")
    
    st.divider()

    # Create 3 columns x 2 rows
    cols = st.columns(3)
    
    for idx, p_type in enumerate(pop_options):
        with cols[idx % 3]:
            # Generate Population Data for Parameters
            c_data = get_pop_data(p_type)
            p_mu = np.mean(c_data)
            p_sigma = np.std(c_data)
            
            # Generate Sampling Distribution
            c_means = np.mean(np.random.choice(c_data, size=(1000, c_n)), axis=1)
            s_mu = np.mean(c_means)
            s_se = np.std(c_means)
            t_se = p_sigma / np.sqrt(c_n)
            
            # Color logic for visual feedback
            color = '#FF9900' if c_n < 30 else '#109618'
            
            # Plot
            fig_c = ff.create_distplot([c_means], [p_type], show_hist=True, show_curve=False, show_rug=False, colors=[color])
            fig_c.update_layout(
                height=250, 
                title=f"Source: {p_type}", 
                margin=dict(l=10, r=10, t=40, b=10),
                showlegend=False,
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False)
            )
            st.plotly_chart(fig_c, key=f"comp_plot_{p_type}", use_container_width=True)
            
            # Display the side-by-side math
            st.markdown(f"""
            **Pop:** $\mu={p_mu:.1f}, \sigma={p_sigma:.1f}$  
            **Sample x̄:** $\mu_{{\\bar{{x}}}}={s_mu:.1f}$  
            **SE:** Sim={s_se:.2f} | Theo={t_se:.2f}
            """)
            st.write("---")

    st.success(f"**Insight:** Notice how $\mu_{{\\bar{{x}}}}$ stays near {p_mu:.1f} regardless of $n$, while SE shrinks consistently.")

# --- PADDING ---
# .............................................................................
# END OF FILE
