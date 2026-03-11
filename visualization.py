import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def render_visualization(fig):
    """Renders a Plotly or Matplotlib figure in Streamlit."""
    if fig is None:
        return
        
    if isinstance(fig, (go.Figure, go.FigureWidget)):
        st.plotly_chart(fig, use_container_width=True)
    elif hasattr(fig, 'axes'): # Simple check for matplotlib
        st.pyplot(fig)
    else:
        st.write("Retrieved a visualization object but could not render it natively.")
