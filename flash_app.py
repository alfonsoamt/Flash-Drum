import streamlit as st
import flash as fd
from stream import Stream
import plotly.graph_objects as go
import numpy as np

@st.cache(show_spinner = False)
def showBubbleT(flash_item, P, c):

    return flash_item.bubbleT(P, c)

@st.cache(show_spinner = False)
def showBubbleP(flash_item, T, c):

    return flash_item.bubbleP(T, c)

@st.cache(show_spinner = False)
def showDewT(flash_item, P, c):

    return flash_item.dewT(P, c)

@st.cache(show_spinner = False)
def showDewP(flash_item, T, c):

    return flash_item.dewP(T, c)

@st.cache(show_spinner = False)
def showIsothermal(flash_item, T, P, c, energy):
    flash_item.isothermal(T, P, c, energy)
    return flash_item.Streams(energy)

@st.cache(show_spinner = False)
def showAdiabatic(flash_item, P, c):
    flash_item.adiabatic(P, c)
    return flash_item.Streams(True)

@st.cache(show_spinner = False)
def Txy_diagram(flash_item, C1, C2, P, c, n):

    x = np.linspace(0.0, 1.0, num = int(n))
    T_b = []
    T_d = []

    for xi in x:

        fraction_d = {C1: xi, C2: 1 - xi}        
        flash_item.setFeedStream(Stream(mComposition = fraction_d))
        T_b.append(flash_item.bubbleT(P, c))
        T_d.append(flash_item.dewT(P, c))

    figTxy = go.Figure()
    figTxy.add_trace(go.Scatter(x = x, y = T_b, mode = "lines+markers", name = "Bubble points", line = {'color': '#3D78FD', 'width': 3.5}, marker = {'color': '#3D78FD', 'symbol': 0, 'size': 10}))
    figTxy.add_trace(go.Scatter(x = x, y = T_d, mode = "lines+markers", name = "Dew points", line = {'color': '#3DFDB2', 'width': 3.5}, marker = {'color': '#3DFDB2', 'symbol': 0, 'size': 10}))
    figTxy.update_layout(  legend = {'yanchor': "bottom", 'xanchor': "right", "orientation": 'h', 'x': 1, 'y': 1},
                        xaxis = {'range': [0,1],
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
                    title = {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 25},
                     'text' : "Phase equilibrium of {} and {} at {} kPa".format(C1, C2, P)},
                    )

    return figTxy

@st.cache(show_spinner = False)
def Pxy_diagram(flash_item, C1, C2, T, c, n):

    x = np.linspace(0.0, 1.0, num = int(n))
    P_b = []
    P_d = []

    for xi in x:

        fraction_d = {C1: xi, C2: 1 - xi}        
        flash_item.setFeedStream(Stream(mComposition = fraction_d))
        P_b.append(flash_item.bubbleP(T, c))
        P_d.append(flash_item.dewP(T, c))
    
    figPxy = go.Figure()
    figPxy.add_trace(go.Scatter(x = x, y = P_b, mode = "lines+markers", name = "Bubble points", line = {'color': '#3D78FD', 'width': 3.5}, marker = {'color': '#3D78FD', 'symbol': 0, 'size': 10}))
    figPxy.add_trace(go.Scatter(x = x, y = P_d, mode = "lines+markers", name = "Dew points", line = {'color': '#3DFDB2', 'width': 3.5}, marker = {'color': '#3DFDB2', 'symbol': 0, 'size': 10}))
    figPxy.update_layout(legend = {'yanchor': "bottom", 'xanchor': "right", "orientation": 'h', 'x': 1, 'y': 1},
            xaxis = {'range': [0,1],
                    'linecolor': "#0238B2",
                    'linewidth': 5,
                    'showgrid': False,
                    'title': {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 16},
                    'text': 'x,y {}'.format(C1)},
                    'dtick': 0.1,
                    'tick0': 0.0},
            yaxis = {'linecolor': "#0238B2",
                    'linewidth': 5,
                    'showgrid': False,
                    'title': {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 16},
                    'text': 'Pressure (kPa)'}},
        plot_bgcolor = '#01143D',
        title = {'font': {'family': 'Bahnschrift SemiBold Condensed,Impact,Overpass,Droid Sans,Raleway,Arial', 'size': 25},
        'text' : "Phase equilibrium of {} and {} at {} K".format(C1, C2, T)},
        )

    return figPxy

st.set_page_config(page_title="Flash Drum Simulator", page_icon="🔥", initial_sidebar_state="expanded", layout = "wide")

header = st.container()
mixture = st.container()
calculations = st.container()
simulations = st.container()
diagrams = st.container()
footer = st.container()
compounds = ["benzene", "toluene", "chlorobenzene", "p-xylene",  "styrene"]
flash_c = fd.FlashDrum()
flash_s = fd.FlashDrum()
flash_d = fd.FlashDrum()

with header:
    st.title("FLASH DRUM 🔥!")
    st.markdown("Make calculations, simulate a flash drum unit and generate phase diagrams for ideal mixtures!")
    colH = st.columns([50,1])
    with colH[0]:
        st.image("./media/main_flash.png", use_column_width = True)
    st.markdown("A flash drum is an unit operation where a feed stream $F$ (with $z$ composition)\
         is separated into a vapor stream $V$ (with $y$ composition), and a liquid stream $L$ (with $x$ composition).\
        This is a single-equilibrium separation-stage, that means that the temperature and pressure in the outlet streams are the same \
        $T_{V}=T_{L}$, $P_{V}=P_{L}$. Through **Rachford–Rice** procedures you can: \n"
    " * do bubble and dew point calcuations  \n"
    " * model an isothermal or adiabatic flash")
    st.latex(r'''f(\Psi)= \sum_{i=1}^{C}\frac{z_{i}(1 - K_{i})}{1 + \Psi(K_{i} - 1)} = 0''')
    st.caption("Rachford–Rice equation")
    st.markdown("Where:  \n""* $\Psi$ is the vapor-feed ratio $V/F$    \n"\
        "* $K_{i}$ is the vapor-liquid equilibrum ratio $y_{i}/x_{i}$ for the $i$ component, and it is a function of $T$ and $P$   \n"\
        "* $z_{i}$ is the molar composition for the $i$ component")

with mixture:
    st.header("Prepare your mixture!")
    st.markdown("Choose at leats two comoponents and set molar composition $z_{i}$.  \n"
        "**NOTE:** *the sum of the mole fractions must be equals to **ONE** (1.0). If it is greater molar, compositions will be normalized*.")

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

if len(fraction) > 1 and nonZero > 0:

    with calculations:

        st.header("1.- Mixture calculations 💥")
        st.markdown("A mixture of a given composition $z$ has a ***bubble*** and a ***dew point***. ""If one variable is fixed, ***Pressure*** $P$ or ***Temperature*** $T$, \
            then you can find the another one. For a bubble point $\Psi = 0$ the **Rachford–Rice** equation is simplied to:")
        st.latex(r'''f(\Psi = 0) = \sum_{i}^{C}z_{i}K_{i} - 1 = 0''')
        st.markdown("And for a dew point  $\Psi = 1$ the ecuation is:")
        st.latex(r'''f(\Psi = 1) = \sum_{i}^{C}\frac{z_{i}}{K_{i}} - 1 = 0''')

        stream_c = Stream(mComposition = feed_Stream.getmC())
        flash_c.setFeedStream(stream_c)
        st.subheader("1.1- BubbleT point")

        with st.form(key = "BubbleT"):
        
            st.markdown("**Temperature of the Bubble point given a pressure:**")
            colBT1, colBT2 = st.columns([1, 1])

            with colBT1:

                P1 = st.number_input(label = "Pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")                                        
                buttonBT = st.form_submit_button("GO!")

                if buttonBT:

                    with colBT2:

                        st.markdown("**Temperature**")

                        with st.spinner('Calculating...'):
                            st.markdown("**{:.2f} K**".format(showBubbleT(flash_c, P1, components)))
                            st.success("Calculations complete!")

        st.subheader("1.2- BubbleP point")

        with st.form(key = "BubbleP"):

            st.markdown("**Pressure of the Bubble point given a temperature:**")
            colBP1, colBP2 = st.columns([1, 1])

            with colBP1:

                T1 = st.number_input(label = "Temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                buttonBP = st.form_submit_button("GO!")

                if buttonBP:

                    with colBP2:

                        st.markdown("**Pressure**")

                        with st.spinner('Calculating...'):

                            st.markdown("**{:.2f} kPa**".format(showBubbleP(flash_c, T1, components)))
                            st.success("Calculations complete!")

        st.subheader("1.3- DewT point")

        with st.form(key = "DewT"):
            
            st.markdown("**Temperature of the Dew point given a pressure:**")
            colDT1, colDT2 = st.columns([1, 1])

            with colDT1:
                
                P2 = st.number_input(label = "Pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")                                        
                buttonDT = st.form_submit_button("GO!")

                if buttonDT:            

                    with colDT2:

                        st.markdown("**Temperature**")

                        with st.spinner('Calculating...'):

                            st.markdown("**{:.2f} K**".format(showDewT(flash_c, P2, components)))
                            st.success("Calculations complete!")

        st.subheader("1.4- DewP point")
        
        with st.form(key = "DewP"):

            st.markdown("**Pressure of the Dew point given a temperature:**")
            colDP1, colDP2 = st.columns([1, 1])

            with colDP1:

                T2 = st.number_input(label = "Temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                buttonDP = st.form_submit_button("GO!")

                if buttonDP:

                    with colDP2:

                        st.markdown("**Pressure**")

                        with st.spinner('Calculating...'):

                            st.markdown("**{:.2f} kPa**".format(showDewP(flash_c, T2, components)))
                            st.success("Calculations complete!")
        
    with simulations:
        st.header("2.- Flash Drum simulations 💻")
        st.markdown("This app allow you perform two types of simulation:""\n1.- Isothermal\n2.- Adiabatic""\nBoth are in steady state and both requires the **Rachford–Rice** procedure \
            for solve the system.")
        st.subheader("2.1- Isothermal Flash Drum")  
        st.markdown("In the isothermal flash, a feed stream goes through the drum where you fix the temerature and pressure, to determinate the outlet compositions $x$ and $y$ and the outlet\
             streams $L$ and $V$. Also, if you want to know the heat $Q$ required for the drum, you must activate the energy balance option.") 
        st.markdown("The first step is to find the $\Psi$ ratio for the given pressure $P$ and temperature $T$ which makes the **Rachford–Rice** equation equals to $0$.\n"\
            "Then find the outlet molar flows by $V = F\Psi$ and $L = F - V$ and the molar compositions by:")
        st.latex(r'''x_{i} = \frac{z_{i}}{1 + \Psi(K_{i}-1)}''')
        st.latex(r'''y_{i} = \frac{z_{i}K_{i}}{1 + \Psi(K_{i}-1)}=x_{i}K_{i}''')
        st.markdown("And finally solve the energy balance:")
        st.latex(r'''Q + Fh_{F} = Vh_{V} + Lh_{L}''')

        with st.form(key = "IsothermalFlash"):

            Tfeed = st.number_input(label = "Feedstream temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
            Pfeed = st.number_input(label = "Feedstream pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
            mFfeed = st.number_input(label = "Feedstream molar flow in mol/h", min_value= 0.01, max_value=1000000.00, step = 0.01, format= "%.2f")
            stream_s = Stream(name = "FEED", Temperature = Tfeed, Pressure = Pfeed, mComposition = feed_Stream.getmC(), molarFlow= mFfeed)
            flash_s.setFeedStream(stream_s)
            T3 = st.number_input(label = "Drum Temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
            P3 = st.number_input(label = "Drum Pressure in kPa",min_value= 10.0, max_value=1100.0, step = 10.0, format = "%.2f")
            energyBalance = st.checkbox(label = "Energy balance")
            buttonIF = st.form_submit_button("GO!")

            if buttonIF:

                with st.spinner("Calculating..."):

                    ifd = showIsothermal(flash_s, T3, P3, components, energyBalance)
                    st.text(ifd)
                    st.success("Calculations complete!")
  
        st.subheader("2.2- Adiabatic Flash Drum")
        st.markdown("In the adiabatic flash, a saturated liquid vaporizes in a valve adiabatically ($Q = 0$) by a pressure reduction, and goes through the drum to be separated. Here you only fix the drum pressure."\
            "This procedure solves both, the **Rachford–Rice** equation and the energy balance simultaneously:")
        st.latex(r'''f(\Psi)= \sum_{i=1}^{C}\frac{z_{i}(1 - K_{i})}{1 + \Psi(K_{i} - 1)} = 0''')
        st.latex(r'''f(T) = Vh_{V} + Lh_{L} - Fh_{F} = 0''')
        with st.form(key = "AdiabaticFlash feed"):

            
            flash_s.setFeedStream(Stream(mComposition = feed_Stream.getmC()))
            Pfeeda = st.number_input(label = "Feedstream pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
            mFfeeda = st.number_input(label = "Feedstream molar flow in mol/h", min_value= 0.01, max_value=1000000.00, step = 0.01, format= "%.2f")
            stream_sa = Stream(name = "FEED", Temperature = flash_s.bubbleT(Pfeeda, components), Pressure = Pfeeda, mComposition = feed_Stream.getmC(), molarFlow= mFfeeda)
            buttonAFF = st.form_submit_button("Save feedstream!")
            flash_s.setFeedStream(stream_sa)

        with st.form(key = "AdiabaticFlash drum"):
            P4 = st.number_input(label = "Drum Pressure in kPa", min_value= 10.0, max_value=Pfeeda, step = 10.0, format="%.2f")
            buttonAF = st.form_submit_button("GO!")

            if buttonAF:

                with st.spinner("Calculating..."):

                    afd = showAdiabatic(flash_s, P4, components)
                    st.text(afd)
                    st.success("Calculations complete!")

    with diagrams:
        st.header("3.- Binary phase diagrams ☁")
        st.markdown("Phase diagrams are representations where two or more phases co-exist. \
            Here you can generate a binary phase diagrams for the liquid and vapor phase at a given pressure or temperature. \
            In order to generate this diagram bubble points and dew points are calculated changing the composition to obtain different points. \
                The more points you introduce the longer it will take for the diagram.")
        
        components_d = fd.parameters(current_mixture)
        
        colD1, colD2 = st.columns([1, 1])

        with colD1:

            C1 = st.selectbox(label="Compound 1", options = current_mixture)

        with colD2:

            C2 = st.selectbox(label="Compound 2", options = current_mixture)

        if C1 == C2:
            st.error("Compound 1 and Compound 2 must be different!")
            st.stop()
                        
        st.subheader("3.1- T vs xy Diagram")
        st.markdown("Given a pressure generate bubble and dew points in the composition range.")

        with st.form(key = "Diagram Txy"):

            colTxy1, colTxy2  =st.columns([1, 3])

            with colTxy1:
            
                P_dTxy = st.number_input(label = "System pressure in kPa", min_value= 10.0, max_value=1100.0, step = 10.0, format="%.2f")
                n = st.number_input(label = "Number of points", min_value = 3, max_value = 101, step= 1, key = "n_txy")
                buttonDT = st.form_submit_button(label = "Generate diagram Txy!")

            if buttonDT:

                with colTxy2:

                    with st.spinner("Generating diagram Txy..."):
                        
                        figTxy = Txy_diagram(flash_d, C1, C2, P_dTxy, components_d, n)                                
                        st.plotly_chart(figTxy, use_container_width = True)
                           
        st.subheader("3.2- P vs xy Diagram")
        st.markdown("Given a temperature generate bubble and dew points in the composition range.")

        with st.form(key = "Diagram Pxy"):

            colPxy1, colPxy2  =st.columns([1, 3])

            with colPxy1:

                T_dPxy = st.number_input(label = "System temperature in K", min_value=250.0, max_value=800.0, step=1.0, format = "%.2f")
                n = st.number_input(label = "Number of points", min_value = 3, max_value = 101, step= 1, key = "n_Txy")
                buttonDP = st.form_submit_button(label = "Generate diagram Pxy!")

            if buttonDP:                        

                with colPxy2:

                    with st.spinner("Generating diagram Pxy..."):

                        figPxy = Pxy_diagram(flash_d, C1, C2, T_dPxy, components_d, n)  
                        st.plotly_chart(figPxy, use_container_width = True)

with footer:
    st.header("About me!")
    st.markdown("Here goes extra infromation about me or the app.")