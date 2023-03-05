from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly


def draw(T_z, T_0, m_total, P_max, m_in, kp, Td):
    time_step = 1 #sekunda
    simulation_time = 10 * 60 * 60 #godzina
    N = int(simulation_time / time_step) + 1
    k_Cw = 4200 #ciepło właściwe wody
    m_in = m_in /360000
    T_in = 30
    #temperatury
    T = [T_0]

    #moc
    P = [0]
    
    #uchyb
    E = [0]

    time = [0.0]

    for i in range(1 , 36000):
        time.append(i * time_step/3600)        
        E.append(T_z - T[-1])
        P.append(min(P_max, max(0, kp * (E[-1] + Td/time_step * (E[-1] - E[-2])))))
    
        T.append(T[-1] + (time_step / (k_Cw * m_total) * P[-1] - m_in * T[-1] + m_in * T_in))
        if(T[-1] - T[-2] < 0.00001):
            break
        
        
    fig = make_subplots(rows = 1, cols = 1, subplot_titles = ("Wykres zależności temperatury wody w bojlerze od czasu"))
    fig.add_trace(go.Scatter(x = time, y = T), row = 1, col = 1)
    fig.update_xaxes(title_text = "Czas [godzina]", row = 1, col = 1)
    fig.update_yaxes(title_text = "Temperatura [\N{DEGREE SIGN}C]", row = 1, col = 1)
    fig.add_hline(y=T_z, line_width=2, line_dash="dash", line_color="red", row = 1, col = 1)
    fig.update_layout(showlegend = False)
    fig.show()
    return fig

draw(40, 20, 80, 4000, 1, 400, 20)
