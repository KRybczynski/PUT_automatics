from flask import Flask, render_template, request
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import plotly

app = Flask(__name__)


def draw(T_z = 45, T_0 = 20, m_total = 80, P_max = 5000, m_in = 1, kp = 60, Td = 20):
    time_step = 60 #sekunda
    k_Cw = 4200 #ciepło właściwe wody
    
    m_in /= 6000

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
    return fig


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        #Temp_max = request.form['temp_max']
        to_draw = list(map(float, request.form.getlist('vals')))
        to_draw = request.form.getlist('vals')
        print(to_draw)
        #fig = draw(to_draw[0], to_draw[1], to_draw[2], to_draw[3] * 1000, to_draw[4], to_draw[5], to_draw[6])
        #fig = draw()
        #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        #return render_template('index.html', graphJSON=graphJSON, temp_max=to_draw[0], temp_init=to_draw[1], V=to_draw[2], P=to_draw[3], m_in=to_draw[4], kp=to_draw[5], Tp=to_draw[6])
        return render_template('index.html', temp_max=to_draw[0], temp_init=to_draw[1], V=to_draw[2], P=to_draw[3], m_in=to_draw[4], kp=to_draw[5], Tp=to_draw[6])
    else:
        #graphJSON = json.dumps(draw(40, 20, 80, 4000, 1, 400, 20), cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('index.html', temp_max=60, temp_init=20, V=80, P=2, m_in=1, kp=500, Tp = 1)
        #return render_template('index.html', graphJSON=graphJSON, temp_max=60, temp_init=20, V=80, P=2, m_in=1, kp=500, Tp = 1)

if __name__ == "__main__":
    app.run(debug=True)

