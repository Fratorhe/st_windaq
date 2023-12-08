import pathlib

import plotly.graph_objects as go
import streamlit as st
from plot_python_vki import generator_colors
from plotly.subplots import make_subplots
from streamlit_plotly_events import plotly_events

from st_windaq.windaq import get_data_WDH_from_binary, read_data_CSV

st.set_page_config(page_title="DAQ explorer")  # , layout="wide")


def get_data_WDH(uploaded_file):
    df = get_data_WDH_from_binary(uploaded_file.getvalue())
    return df


@st.cache_data
def read_data(uploaded_file):
    extension_file = pathlib.Path(uploaded_file.name).suffix.lower()[1:]
    reader_dispatch = {"csv": read_data_CSV, "wdh": get_data_WDH}

    df = reader_dispatch[extension_file](uploaded_file)
    clist = df.columns.tolist()

    return df, clist


color = generator_colors()


def update_layout(fig):
    font_size = 24

    fig.update_layout(
        font=dict(
            size=font_size + 2,  # Set the font size here
        ),
        xaxis_title_font_size=font_size + 2,
        yaxis_title_font_size=font_size + 2,
        xaxis_tickfont_size=font_size - 2,
        yaxis_tickfont_size=font_size - 2,
        hoverlabel_font_size=font_size - 2,
        legend_font_size=font_size - 10,
        xaxis_title=dict(text="Time, s", font=dict(size=16)),
    )
    return fig


st.sidebar.title("Select File:")
uploaded_file = st.sidebar.file_uploader(
    "Choose a WDH or CSV file:", accept_multiple_files=False
)

if uploaded_file is not None:
    df_input, channel_names = read_data(uploaded_file)

    diff_channel_name = "comp. press. diff."
    compute_difference = st.sidebar.checkbox(
        f"Compute difference absolute pressures? Will show as {diff_channel_name} in channel names."
    )

    if compute_difference:
        df_input[diff_channel_name] = (
            df_input["ABS Gauge Downstream 1000 Torr"]
            - df_input["ABS Gauge Upstream 1000 Torr"]
        )
        channel_names.append(diff_channel_name)

    st.sidebar.title("Graph #1:")

    # variables on first y axis.
    variables = st.sidebar.multiselect("Select lines for y1", channel_names)
    dfs = {variable: df_input[["Time", variable]] for variable in variables}

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for variable, df in dfs.items():
        fig = fig.add_trace(
            go.Scatter(x=df["Time"], y=df[variable], name=variable), secondary_y=False
        )

    # variables on second y axis.
    variables = st.sidebar.multiselect("Select lines for y2", channel_names)
    dfs = {variable: df_input[["Time", variable]] for variable in variables}

    for variable, df in dfs.items():
        fig = fig.add_trace(
            go.Scatter(x=df["Time"], y=df[variable], name=variable), secondary_y=True
        )

    point_selector = st.sidebar.checkbox("Do you want to select points on graph?")

    fig = update_layout(fig)

    if point_selector:
        selected_points = plotly_events(fig)
        print(selected_points)
    else:
        st.plotly_chart(fig)

    st.sidebar.title("Graph #2:")

    # adding an extra graph to analyze other variables if needed.
    variables = st.sidebar.multiselect("Select lines for graph:", channel_names)
    dfs = {variable: df_input[["Time", variable]] for variable in variables}
    fig2 = make_subplots()

    for variable, df in dfs.items():
        fig2 = fig2.add_trace(go.Scatter(x=df["Time"], y=df[variable], name=variable))

    fig2 = update_layout(fig2)

    st.plotly_chart(fig2)
