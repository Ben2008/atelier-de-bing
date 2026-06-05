import streamlit as st

from modules.mechanical_design.bend_allowance import (
    bend_allowance
)

st.set_page_config(
    page_title="L'Atelier de Bing",
    layout="wide"
)

menu = st.sidebar.selectbox(
    "Module",
    [
        "Mechanical Design",
        "Utilities",
        "MyWork"
    ]
)

if menu == "Mechanical Design":

    st.title("Sheet Metal")

    angle = st.number_input(
        "Angle (deg)",
        value=90.0
    )

    radius = st.number_input(
        "Inside Radius (mm)",
        value=1.5
    )

    thickness = st.number_input(
        "Thickness (mm)",
        value=1.0
    )

    k = st.number_input(
        "K-Factor",
        value=0.33
    )

    if st.button("Calculate"):

        ba = bend_allowance(
            angle,
            radius,
            thickness,
            k
        )

        st.success(
            f"Bend Allowance = {ba:.3f} mm"
        )

elif menu == "Utilities":

    st.title("Utilities")

    st.write(
        "Unit Converter coming next"
    )

else:

    st.title("MyWork")

    st.write(
        "Engineering Notes coming next"
    )