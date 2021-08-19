import streamlit as st
import flash as fd
from stream import Stream
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Flash Drum Simulator", page_icon="🔥", initial_sidebar_state="expanded", layout = "wide")

header = st.container()
mixture = st.container()
calculations = st.container()
simulations = st.container()
diagrams = st.container()
footer = st.container()

compounds = ["benzene", "toluene", "chlorobenzene", "p-xylene",  "styrene"]

with header:
    st.title("FLASH DRUM 🔥!")
    st.markdown("Make calculations, simulate a flash drum unit and generate phase diagrams for ideal mixtures!")
    colH = st.columns([50,1])
    with colH[0]:
        st.image("./media/main_flash.png", use_column_width = True)

with mixture:
    st.header("Prepare your mixture!")
    st.markdown("Choose at leats two comoponents and introduce its molar composition.  \n"
        "**NOTE:** _the sum of the mole fractions must be equals to **ONE** (1.0). If it is greater molar, compositions will be normalized._")


    components = st.multiselect(label="Choose the components", options= compounds)
    fraction = {}    
   
    for i in components:
        
        fraction[i] = st.number_input(label=i, key="Component_" + i, min_value=0.0000, max_value=1.0000, step=0.0001, format = "%.4f", value = 0.0)

    current_mixture = [key for key in fraction.keys()]
    components = fd.parameters(current_mixture)  
    nonZero = sum([z for z in fraction.values()])
    if nonZero > 0:
        feed_Stream = Stream(mComposition = fraction)
        feed_Stream.normalize()
        option = st.selectbox("Select an option", ["Calculations", "Simulations", "Diagrams"])

if len(fraction) > 1 and nonZero > 0:

    if option == "Calculations":

        with calculations:
            st.header("1.- Mixture calculations 💥")
            st.markdown("Here you can find four type of calculations.")

            flash_c = fd.FlashDrum()
            stream_c = Stream(mComposition = feed_Stream.getmC())
            Calculation = st.selectbox("Choose the calculation type:", ["BubbleT point", "BubbleP point", "DewT point", "DewP point"] )
            if nonZero > 0:
                flash_c.setFeedStream(stream_c)

                if Calculation == "BubbleT point":

                    st.subheader("1.1- BubbleT point")

                    with st.form(key = "BubbleT"):
                        
                        st.markdown("**Temperature of the Bubble point given a pressure:**")
                        colBT1, colBT2 = st.columns([1, 1])

                        with colBT1:
                            
                            P1 = st.number_input(label = "Pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
                                                
                            buttonBT = st.form_submit_button("GO!")

                            if buttonBT:

                                with colBT2:
                                    st.markdown("__Temperature__")
                                    with st.spinner('Calculating...'):
                                        st.markdown("**{:.2f} K**".format(flash_c.bubbleT(P1, components)))
                                        st.success("Calculations complete!")


                elif Calculation == "BubbleP point":

                    st.subheader("1.2- BubbleP point")

                    with st.form(key = "BubbleP"):
                        st.markdown("**Pressure of the Bubble point given a temperature:**")
                        colBP1, colBP2 = st.columns([1, 1])
                        with colBP1:

                            T1 = st.number_input(label = "Temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                            buttonBP = st.form_submit_button("GO!")

                            if buttonBP:


                                with colBP2:
                                    st.markdown("__Pressure__")
                                    with st.spinner('Calculating...'):
                                        st.markdown("**{:.2f} kPa**".format(flash_c.bubbleP(T1, components)))
                                        st.success("Calculations complete!")


                elif Calculation == "DewT point":

                        st.subheader("1.3- DewT point")

                        with st.form(key = "DewT"):
                            
                            st.markdown("**Temperature of the Dew point given a pressure:**")
                            colDT1, colDT2 = st.columns([1, 1])
                            with colDT1:
                                
                                P2 = st.number_input(label = "Pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
                                                
                                buttonDT = st.form_submit_button("GO!")

                                if buttonDT:
                    

                                    with colDT2:
                                        st.markdown("__Temperature__")
                                        with st.spinner('Calculating...'):
                                            st.markdown("**{:.2f} K**".format(flash_c.dewT(P2, components)))
                                            st.success("Calculations complete!")


                elif Calculation == "DewP point":

                    st.subheader("1.4- DewP point")
                    
                    with st.form(key = "DewP"):
                        st.markdown("**Pressure of the Dew point given a temperature:**")
                        colDP1, colDP2 = st.columns([1, 1])
                        with colDP1:

                            T2 = st.number_input(label = "Temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                            buttonDP = st.form_submit_button("GO!")

                            if buttonDP:
        

                                with colDP2:
                                    st.markdown("__Pressure__")
                                    with st.spinner('Calculating...'):
                                        st.markdown("**{:.2f} kPa**".format(flash_c.dewP(T2, components)))
                                        st.success("Calculations complete!")
            
            else:
                st.error("Fracction values sum must be non-zero!")   

    elif option == "Simulations":          
        with simulations:
            st.header("2.- Flash Drum simulations 💻")
            st.markdown("In this section you can make flash drum simulations")
            flash_s = fd.FlashDrum()

            simulation = st.selectbox(label = "Choose simulation type", options=["Isothermal Flash Drum", "Adiabatic Flash Drum"])
            if nonZero > 0:
                
                
                if simulation == "Isothermal Flash Drum":

                    

                    st.subheader("2.1- Isothermal Flash Drum")        

                    with st.form(key = "IsothermalFlash"):

                        Tfeed = st.number_input(label = "Feedstream temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                        Pfeed = st.number_input(label = "Feedstream pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
                        mFfeed = st.number_input(label = "Feedstream molar flow in mol/h", min_value= 0.01, max_value=1000000.00, step = 0.01, format= "%.2f")
                        stream_s = Stream(name = "FEED", Temperature = Tfeed, Pressure = Pfeed, mComposition = feed_Stream.getmC(), molarFlow= mFfeed)
                        flash_s.setFeedStream(stream_s)
                        st.markdown("**Isothermal flash drum simulation given a temperature and pressure:**")
                        T3 = st.number_input(label = "Drum Temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                        P3 = st.number_input(label = "Drum Pressure in kPa",min_value= 10.0, max_value=1100.0, step = 10.0, format = "%.2f")
                        energyBalance = st.checkbox(label = "Energy balance")
                        buttonIF = st.form_submit_button("GO!")

                        if buttonIF:
                                
                            if energyBalance:

                                with st.spinner("Calculating..."):
                                    flash_s.isothermal(T3, P3, components, True)
                                    st.text(flash_s.Streams(True))
                                    st.success("Calculations complete!")
                            else:
                                with st.spinner("Calculating..."):
                                    flash_s.isothermal(T3, P3, components)
                                    st.text(flash_s.Streams())
                                    st.success("Calculations complete!")

                elif simulation == "Adiabatic Flash Drum":

                    st.subheader("2.2- Adiabatic Flash Drum")
                    with st.form(key = "AdiabaticFlash"):
                        
                        flash_s.setFeedStream(Stream(mComposition = feed_Stream.getmC()))
                        Pfeeda = st.number_input(label = "Feedstream pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
                        mFfeeda = st.number_input(label = "Feedstream molar flow in mol/h", min_value= 0.01, max_value=1000000.00, step = 0.01, format= "%.2f")
                        stream_sa = Stream(name = "FEED", Temperature = flash_s.bubbleT(Pfeeda, components), Pressure = Pfeeda, mComposition = feed_Stream.getmC(), molarFlow= mFfeeda)
                        flash_s.setFeedStream(stream_sa)
                        
                        st.markdown("**Adiabatic flash drum simulation given a pressure:**")


                        P4 = st.number_input(label = "Drum Pressure in kPa", min_value= 10.0, max_value=Pfeeda, step = 10.0, format="%.2f")
                        buttonAF = st.form_submit_button("GO!")

                        if buttonAF:

                            with st.spinner("Calculating..."):
                                flash_s.adiabatic(P4, components)
                                st.text(flash_s.Streams(True))
                                st.success("Calculations complete!")


            else: 
                st.error("Fracction values sum must be non-zero!") 

    else:
        with diagrams:
            st.header("3.- Binary phase diagrams ☁")
            flash_d = fd.FlashDrum()
            components_d = fd.parameters(current_mixture)
            

            colD1, colD2 = st.columns([1, 1])

            with colD1:

                C1 = st.selectbox(label="Compound 1", options = current_mixture)

            with colD2:

                C2 = st.selectbox(label="Compound 2", options = current_mixture)

            if C1 == C2:
                st.error("Compound 1 and Compound 2 must be different!")
            else:
                
                Diagram = st.selectbox(label="Phase Diagram", options = ["T vs xy Diagram", "P vs xy Diagram"])
                
                with st.form(key = "Diagrams"):

                    if Diagram == "T vs xy Diagram":

                        st.subheader("3.1- T vs xy Diagram")
                        P_d = st.number_input(label = "System pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
                        n = st.number_input(label = "Number of points", min_value = 3, max_value = 101, step= 1)
                        x = np.linspace(0.0, 1.0, num = n)
                        buttonDT = st.form_submit_button("Generate diagram!")

                        if buttonDT:

                            with st.spinner("Generating diagram..."):
                                
                                T_b = []
                                T_d = []
                                fig = go.Figure()
                                for xi in x:
                                    fraction_d = {C1: xi, C2: 1 - xi}
                                    
                                    stream_d = Stream(mComposition = fraction_d)
                                    flash_d.setFeedStream(stream_d)
                                    T_b.append(flash_d.bubbleT(P_d, components_d))
                                    T_d.append(flash_d.dewT(P_d, components_d))

                                fig.add_trace(go.Scatter(x = x, y = T_b, mode = "lines+markers", name = "Bubble points", line = {'color': '#3D78FD', 'width': 3.5}, marker = {'color': '#3D78FD', 'symbol': 0, 'size': 10}))
                                fig.add_trace(go.Scatter(x = x, y = T_d, mode = "lines+markers", name = "Dew points", line = {'color': '#3DFDB2', 'width': 3.5}, marker = {'color': '#3DFDB2', 'symbol': 0, 'size': 10}))
                                fig.update_layout(xaxis = {'range': [0,1],
                                                            'linecolor': "#0238B2",
                                                            'linewidth': 5,
                                                            'showgrid': False,
                                                            'title': {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 16},
                                                            'text': 'x,y {}'.format(C1)},
                                                            'dtick': 0.1,
                                                            'tick0': 0.0},
                                                    yaxis = {  'linecolor': "#0238B2",
                                                            'linewidth': 5,
                                                            'showgrid': False,
                                                            'title': {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 16},
                                                            'text': 'Temperature (K)'}},
                                                plot_bgcolor = '#01143D',
                                                title = {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 25}, 'text' : "Phase equilibrium of {} and {} at {} kPa".format(C1, C2, P_d)},
                                                )
                                st.plotly_chart(fig, use_container_width = True)

                    elif Diagram == "P vs xy Diagram":
                        
                        st.subheader("3.2- P vs xy Diagram")
                        T_d = st.number_input(label = "System temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                        n = st.number_input(label = "Number of points", min_value = 3, max_value = 101, step= 1)
                        x = np.linspace(0.0, 1.0, num = n)
                        buttonDT = st.form_submit_button("Generate diagram!")

                        if buttonDT:

                            with st.spinner("Generating diagram..."):
                                
                                P_b = []
                                P_d = []
                                fig = go.Figure()
                                for xi in x:
                                    fraction_d = {C1: xi, C2: 1 - xi}
                                    
                                    stream_d = Stream(mComposition = fraction_d)
                                    flash_d.setFeedStream(stream_d)
                                    P_b.append(flash_d.bubbleP(T_d, components_d))
                                    P_d.append(flash_d.dewP(T_d, components_d))

                                fig.add_trace(go.Scatter(x = x, y = P_b, mode = "lines+markers", name = "Bubble points", line = {'color': '#3D78FD', 'width': 3.5}, marker = {'color': '#3D78FD', 'symbol': 0, 'size': 10}))
                                fig.add_trace(go.Scatter(x = x, y = P_d, mode = "lines+markers", name = "Dew points", line = {'color': '#3DFDB2', 'width': 3.5}, marker = {'color': '#3DFDB2', 'symbol': 0, 'size': 10}))
                                fig.update_layout(xaxis = {'range': [0,1],
                                                            'linecolor': "#0238B2",
                                                            'linewidth': 5,
                                                            'showgrid': False,
                                                            'title': {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 16},
                                                            'text': 'x,y {}'.format(C1)},
                                                            'dtick': 0.1,
                                                            'tick0': 0.0},
                                                    yaxis = {  'linecolor': "#0238B2",
                                                            'linewidth': 5,
                                                            'showgrid': False,
                                                            'title': {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 16},
                                                            'text': 'Pressure (kPa)'}},
                                                plot_bgcolor = '#01143D',
                                                title = {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 25}, 'text' : "Phase equilibrium of {} and {} at {} K".format(C1, C2, T_d)},
                                                )
                                st.plotly_chart(fig, use_container_width = True)
                    

with footer:
    st.text("Here goes extra infromation about me or the app.")