import colorsys
import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
from statsmodels.nonparametric.smoothers_lowess import lowess
import plotly.express as px
import seaborn as sns
from unidecode import unidecode
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import numpy as np

cmap = {'APU': '#C7253D', 'AMU': '#53B2FF', 'APR': '#193E2E'}
cmap_grey = {'APU': '#E98695', 'AMU': '#5CB6FF', 'APR': '#40A075'}

def lighten_color(color_hex, factor):
    rgb = mcolors.hex2color(color_hex)
    h, s, v = colorsys.rgb_to_hsv(*rgb)
    v = min(1, v + factor)
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return mcolors.rgb2hex(rgb)

def print_scatter(comp, variableX, variableY, variableZ, variableXtitle, variableYtitle, name="test.html", division="TIPAU", hover_data=['FF_DSG', "PT_INE_21", "PT_MAI_21"], nbins = 5, frac=0.3):
    scaler = MinMaxScaler(feature_range=(1, 40))  # Adjust the feature range as needed
    pt_ine_21_scaled = scaler.fit_transform(comp['PT_INE_21'].values.reshape(-1, 1)).flatten()
    
    if division == "TIPAU":
        # Group the data and calculate conditional means
        grouped_data_APR = comp[comp["TIPAU"] == "APR"].groupby(variableX)[variableY].mean().reset_index()
        grouped_data_APU = comp[comp["TIPAU"] == "APU"].groupby(variableX)[variableY].mean().reset_index()
        grouped_data_AMU = comp[comp["TIPAU"] == "AMU"].groupby(variableX)[variableY].mean().reset_index()
        # Apply LOESS smoothing to the grouped data
        smoothed_data_APR = lowess(grouped_data_APR[variableY], grouped_data_APR[variableX], frac=frac)
        smoothed_data_APU = lowess(grouped_data_APU[variableY], grouped_data_APU[variableX], frac=frac)
        smoothed_data_AMU = lowess(grouped_data_AMU[variableY], grouped_data_AMU[variableX], frac=frac)
        colors = cmap_grey

    elif division == "population":
        comp["Tamanho"], cut_bin = pd.qcut(comp['PT_INE_21'], q = nbins, retbins = True)
        
        cmap_pop = sns.color_palette("rocket_r",n_colors=nbins)
   
        comp["Tamanho"] = comp["Tamanho"].apply(lambda x: pd.Interval(left=int(round(x.left)), right=int(round(x.right))))
        labels = comp["Tamanho"].unique()
        labels = labels.to_list()
        labels = labels[-1:] + labels[:-1]
        cmap_pop_hex = [mcolors.rgb2hex(color) for color in cmap_pop]
        colors_dict = {}
        i = 0
        
        for label in labels:
            colors_dict[label] = cmap_pop_hex[i]
            i+=1
            
        colors_dict_lighter = copy.deepcopy(colors_dict)
        lighten_factor = 0.2  # Adjust the factor as desired
        for key in colors_dict_lighter:
            color = colors_dict_lighter[key]
            lightened_color = lighten_color(color, lighten_factor)
            colors_dict_lighter[key] = lightened_color
            
        
        grouped_data_list = {}
        smoothed_data_list = {}
        for value in labels:
            grouped_data_list[value] = (comp[comp["Tamanho"] == value].groupby(variableX)[variableY].mean().reset_index())
            smoothed_data_list[value] = lowess(grouped_data_list[value][variableY], grouped_data_list[value][variableX], frac=frac)

        colors = colors_dict_lighter

    # Set up the scatter plot
    fig = px.scatter(comp, x=variableX, y=variableY,
                     labels={
                         variableY: variableYtitle,
                         variableX: variableXtitle
                     },
                     color=variableZ,
                     color_discrete_map=colors,
                     size=pt_ine_21_scaled,
                     size_max=40,
                     hover_data=hover_data,
                     category_orders={variableZ: np.sort(comp[variableZ].unique())})

    if division == "TIPAU":
        fig.add_trace(go.Scattergl(x=grouped_data_APR[variableX], y=smoothed_data_APR[:, 1],
                                 mode='lines', name='APR smoothed', line=dict(color=cmap["APR"], width=5)))
        fig.add_trace(go.Scattergl(x=grouped_data_APU[variableX], y=smoothed_data_APU[:, 1],
                                 mode='lines', name='APU smoothed', line=dict(color=cmap["APU"], width=5)))
        fig.add_trace(go.Scattergl(x=grouped_data_AMU[variableX], y=smoothed_data_AMU[:, 1],
                                 mode='lines', name='AMU smoothed', line=dict(color=cmap["AMU"], width=5)))
    elif division == "population":
        
        i = 0
        for value in labels:
            fig.add_trace(go.Scattergl(x=grouped_data_list[value][variableX], y=smoothed_data_list[value][:, 1],
                                 mode='lines', name= str(value) + " smoothed", line=dict(color=colors_dict[value], width=5)))
            i+=1

    fig.show()
    #fig.write_html("outputs/" + name, full_html=False, include_plotlyjs='cdn')
    print("Correlação geral: " + str(np.corrcoef(comp[variableX], comp[variableY])[0][1]))

    return fig
    
    

