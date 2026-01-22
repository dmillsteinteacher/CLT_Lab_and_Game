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

# --- TAB 1: SINGLE LAB (BASELINE) ---
pop_options = ["Normal", "Uniform", "Right Skewed", "Left Skewed", "Bimodal", "U-Shape"]

with tab1:
    st.header("Deep Dive: The 'Normalizer' in Action")
    col_ctrl, col_plot = st.columns([1, 3])
    with col_ctrl:
        l_pop_type = st.selectbox("Pick a World Shape", pop_options, key="l_pop")
        l_n = st.slider("Sample Size (n)", min_value=1, max_value=100, value=2, key="l_n")
    
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
        st.write(fr"**Stats:** $\mu = {mu:.2f}$ | $\sigma = {sigma:.2f}$ | Simulated $SE = {np.std(l_means):.2f}$ | Theoretical $SE = {sigma/np.sqrt(l_n):.2f}$")

# --- TAB 2: COMPARATIVE LAB ---
with tab2:
    st.header("The Race to Normality")
    st.write("How quickly does each population 'forget' its shape? Enter a sample size to see all six worlds converge at once.")

    c_n = st.number_input("Enter Sample Size (n):", min_value=1, max_value=100, value=1, step=1)
    
    st.divider()

    # Create 3 columns x 2 rows for the 6 populations
    cols = st.columns(3)
    
    for idx, p_type in enumerate(pop_options):
        with cols[idx % 3]:
            # Generate data
            c_data = get_pop_data(p_type)
            c_means = np.mean(np.random.choice(c_data, size=(1500, c_n)), axis=1)
            
            # Create plot
            # Color logic: Change color as it gets more "Normal" based on n
            color = '#FF9900' if c_n < 30 else '#109618'
            
            fig_c = ff.create_distplot([c_means], [p_type], show_hist=True, show_curve=False, show_rug=False, colors=[color])
            fig_c.update_layout(
                height=300, 
                title=f"{p_type} (n={c_n})", 
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False,
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False)
            )
            st.plotly_chart(fig_c, key=f"comp_{p_type}", use_container_width=True)

    st.info("""
    **Pedagogical Observation:** * At **n=1**, you see the raw parent populations.
    * At **n=10**, notice how 'Uniform' is already looking Normal, but 'Bimodal' and 'U-Shape' are still fighting it.
    * At **n=30**, almost every shape has lost its unique identity.
    """)
