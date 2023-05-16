def print_mapa(var1="diff_rel_21", var2 = "diff_rel_11", var3="diff_rel_01", ano1 = 2021, ano2 = 2011, ano3 = 2001):
    district_stats1 = comp.groupby('Distrito')[var1].apply(lambda x: pd.Series({'weighted_mean_diff': (x * comp.loc[x.index, 'PT_INE_21']).sum() / comp.loc[x.index, 'PT_INE_21'].sum()}))
    district_stats1 = pd.DataFrame(district_stats1).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats2 = comp.groupby('Distrito')[var2].apply(lambda x: pd.Series({'weighted_mean_diff': (x * comp.loc[x.index, 'PT_INE_11']).sum() / comp.loc[x.index, 'PT_INE_11'].sum()}))
    district_stats2 = pd.DataFrame(district_stats2).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats3 = comp.groupby('Distrito')[var3].apply(lambda x: pd.Series({'weighted_mean_diff': (x * comp.loc[x.index, 'PT_INE_01']).sum() / comp.loc[x.index, 'PT_INE_01'].sum()}))
    district_stats3 = pd.DataFrame(district_stats3).reset_index().drop(columns=["level_1"]).set_index("Distrito")

    district_stats = pd.concat([district_stats1, district_stats2, district_stats3], axis=1)
    min_val = district_stats.min().min()
    max_val = district_stats.max().max()
    
    mapa = gpd.read_file('mapa/PRT_adm1.shp')
    mapa = mapa.replace({"Azores":"Açores", 'Aveiro': 'X', 'Beja': 'X', 'Braga': 'X', 'Bragança': 'X', 'Castelo Branco': 'X', 'Coimbra': 'X', 'Évora': 'X', 'Faro': 'X', 'Guarda': 'X', 'Leiria': 'X', 'Lisboa': 'X', 'Portalegre': 'X', 'Porto': 'X', 'Santarém': 'X', 'Setúbal': 'X', 'Viana do Castelo': 'X', 'Vila Real': 'X', 'Viseu': 'X'}
)
    mapa = mapa.merge(district_stats1, left_on='NAME_1', right_index=True)
    mapa = mapa.merge(district_stats2, left_on='NAME_1', right_index=True, suffixes=('_'+var1, '_'+var2))
    mapa = mapa.merge(district_stats3, left_on='NAME_1', right_index=True, suffixes=('_'+var2, '_'+var3))

    fig, (ax3, ax2, ax1) = plt.subplots(ncols=3, figsize=(16, 14))
    mapa.plot(column=var1, cmap='OrRd', legend=True, ax=ax1, vmin=min_val, vmax=max_val)
    ax1.set_title(f"{ano1}", fontsize=16)
    ax1.set_axis_off()

    mapa.plot(column=var2, cmap='OrRd', legend=True, ax=ax2, vmin=min_val, vmax=max_val)
    ax2.set_title(f"{ano2}", fontsize=16)
    ax2.set_axis_off()
    
    mapa.plot(column=var3, cmap='OrRd', legend=True, ax=ax3, vmin=min_val, vmax=max_val)
    ax3.set_title(f"{ano3}", fontsize=16)
    ax3.set_axis_off()

    # Add labels to the map with the average population for each district
    for idx, row in mapa.iterrows():
        ax1.annotate(text=f"{row[var1]:.0f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax2.annotate(text=f"{row[var2]:.0f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax3.annotate(text=f"{row[var3]:.0f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
    plt.show()
    
#Distribuição dos excessos
def print_mapa2(var1="diff_abs_21", var2 = "diff_abs_11", var3="diff_abs_01", ano1 = 2021, ano2 = 2011, ano3 = 2001):
    district_stats1 = comp.groupby('Distrito')[var1].apply(lambda x: pd.Series({'excesso_percentagem': x.sum() / comp[var1].sum() * 100}))
    district_stats1 = pd.DataFrame(district_stats1).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats2 = comp.groupby('Distrito')[var2].apply(lambda x: pd.Series({'excesso_percentagem': x.sum() / comp[var2].sum() * 100}))
    district_stats2 = pd.DataFrame(district_stats2).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats3 = comp.groupby('Distrito')[var3].apply(lambda x: pd.Series({'excesso_percentagem': x.sum() / comp[var3].sum() * 100}))
    district_stats3 = pd.DataFrame(district_stats3).reset_index().drop(columns=["level_1"]).set_index("Distrito")

    district_stats = pd.concat([district_stats1, district_stats2, district_stats3], axis=1)
    min_val = district_stats.min().min()
    max_val = district_stats.max().max()
    
    mapa = gpd.read_file('mapa/PRT_adm1.shp')
    mapa = mapa.replace({"Azores":"Açores", "Madeira:":"X",'Aveiro': 'X', 'Beja': 'X', 'Braga': 'X', 'Bragança': 'X', 'Castelo Branco': 'X', 'Coimbra': 'X', 'Évora': 'X', 'Faro': 'X', 'Guarda': 'X', 'Leiria': 'X', 'Lisboa': 'X', 'Portalegre': 'X', 'Porto': 'X', 'Santarém': 'X', 'Setúbal': 'X', 'Viana do Castelo': 'X', 'Vila Real': 'X', 'Viseu': 'X'})
    
    mapa = mapa.merge(district_stats1, left_on='NAME_1', right_index=True)
    mapa = mapa.merge(district_stats2, left_on='NAME_1', right_index=True, suffixes=('_'+var1, '_'+var2))
    mapa = mapa.merge(district_stats3, left_on='NAME_1', right_index=True, suffixes=('_'+var2, '_'+var3))

    fig, (ax3, ax2, ax1) = plt.subplots(ncols=3, figsize=(16, 14))
    mapa.plot(column=var1, cmap='OrRd', legend=True, ax=ax1, vmin=min_val, vmax=max_val)
    ax1.set_title(f"{ano1}", fontsize=16)
    ax1.set_axis_off()

    mapa.plot(column=var2, cmap='OrRd', legend=True, ax=ax2, vmin=min_val, vmax=max_val)
    ax2.set_title(f"{ano2}", fontsize=16)
    ax2.set_axis_off()
    
    mapa.plot(column=var3, cmap='OrRd', legend=True, ax=ax3, vmin=min_val, vmax=max_val)
    ax3.set_title(f"{ano3}", fontsize=16)
    ax3.set_axis_off()

    # Add labels to the map with the average population for each district
    for idx, row in mapa.iterrows():
        ax1.annotate(text=f"{row[var1]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax2.annotate(text=f"{row[var2]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax3.annotate(text=f"{row[var3]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
    plt.show()
    
def print_mapa3(var1="diff_abs_21", var2 = "diff_abs_11", var3="diff_abs_01", ano1 = 2021, ano2 = 2011, ano3 = 2001):
    district_stats1 = comp.groupby('Distrito')[var1].apply(lambda x: pd.Series({'excesso_percentagem': (x.sum() / comp[var1].sum() * 100) - (comp.loc[x.index, "PT_INE_21"].sum() / comp["PT_INE_21"].sum() * 100)}))
    district_stats1 = pd.DataFrame(district_stats1).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats2 = comp.groupby('Distrito')[var2].apply(lambda x: pd.Series({'excesso_percentagem': (x.sum() / comp[var2].sum() * 100) - (comp.loc[x.index, "PT_INE_11"].sum() / comp["PT_INE_11"].sum() * 100)}))
    district_stats2 = pd.DataFrame(district_stats2).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats3 = comp.groupby('Distrito')[var3].apply(lambda x: pd.Series({'excesso_percentagem': (x.sum() / comp[var3].sum() * 100)- (comp.loc[x.index, "PT_INE_01"].sum() / comp["PT_INE_01"].sum() * 100)}))
    district_stats3 = pd.DataFrame(district_stats3).reset_index().drop(columns=["level_1"]).set_index("Distrito")

    district_stats = pd.concat([district_stats1, district_stats2, district_stats3], axis=1)
    min_val = district_stats.min().min()
    max_val = district_stats.max().max()
    
    mapa = gpd.read_file('mapa/PRT_adm1.shp')
    #mapa = mapa.replace({"Azores":"Açores", 'Aveiro': 'X', 'Beja': 'X', 'Braga': 'X', 'Bragança': 'X', 'Castelo Branco': 'X', 'Coimbra': 'X', 'Évora': 'X', 'Faro': 'X', 'Guarda': 'X', 'Leiria': 'X', 'Lisboa': 'X', 'Portalegre': 'X', 'Porto': 'X', 'Santarém': 'X', 'Setúbal': 'X', 'Viana do Castelo': 'X', 'Vila Real': 'X', 'Viseu': 'X'})
    
    mapa = mapa.replace({"Azores":"X", "Madeira":"X"})
    mapa = mapa.merge(district_stats1, left_on='NAME_1', right_index=True)
    mapa = mapa.merge(district_stats2, left_on='NAME_1', right_index=True, suffixes=('_'+var1, '_'+var2))
    mapa = mapa.merge(district_stats3, left_on='NAME_1', right_index=True, suffixes=('_'+var2, '_'+var3))

    fig, (ax3, ax2, ax1) = plt.subplots(ncols=3, figsize=(16, 14))
    mapa.plot(column=var1, cmap='OrRd', legend=True, ax=ax1, vmin=min_val, vmax=max_val)
    ax1.set_title(f"{ano1}", fontsize=16)
    ax1.set_axis_off()

    mapa.plot(column=var2, cmap='OrRd', legend=True, ax=ax2, vmin=min_val, vmax=max_val)
    ax2.set_title(f"{ano2}", fontsize=16)
    ax2.set_axis_off()
    
    mapa.plot(column=var3, cmap='OrRd', legend=True, ax=ax3, vmin=min_val, vmax=max_val)
    ax3.set_title(f"{ano3}", fontsize=16)
    ax3.set_axis_off()

    # Add labels to the map with the average population for each district
    for idx, row in mapa.iterrows():
        ax1.annotate(text=f"{row[var1]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax2.annotate(text=f"{row[var2]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax3.annotate(text=f"{row[var3]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
    plt.show()
    
def print_boxplot(var = "diff_rel_21", titulo = "Erro relativo p/TIPAU - 2021"):
    data = [comp[var], comp_APU[var], comp_AMU[var], comp_APR[var]]

    # Plot the boxplots
    fig, ax = plt.subplots()
    boxplots = ax.boxplot(data)

    # Add x-axis labels
    ax.set_title(titulo)
    ax.set_xticklabels(['Todas', "APU", "AMU", "APR"])
    ax.set_ylabel("%")
    ax.set_ylim([-80, 180])
    # Show the plot
    plt.show()
    
def print_mapa4(var1="PT_INE_21", var2 = "PT_INE_11", var3="PT_INE_01", ano1 = 2021, ano2 = 2011, ano3 = 2001):
    district_stats1 = comp.groupby('Distrito')[var1].apply(lambda x: pd.Series({'excesso_percentagem': (x.sum() / comp[var1].sum() * 100)}))
    district_stats1 = pd.DataFrame(district_stats1).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats2 = comp.groupby('Distrito')[var2].apply(lambda x: pd.Series({'excesso_percentagem': (x.sum() / comp[var2].sum() * 100)}))
    district_stats2 = pd.DataFrame(district_stats2).reset_index().drop(columns=["level_1"]).set_index("Distrito")
    
    district_stats3 = comp.groupby('Distrito')[var3].apply(lambda x: pd.Series({'excesso_percentagem': (x.sum() / comp[var3].sum() * 100)}))
    district_stats3 = pd.DataFrame(district_stats3).reset_index().drop(columns=["level_1"]).set_index("Distrito")

    district_stats = pd.concat([district_stats1, district_stats2, district_stats3], axis=1)
    min_val = district_stats.min().min()
    max_val = district_stats.max().max()
    
    mapa = gpd.read_file('mapa/PRT_adm1.shp')
    mapa = mapa.replace({"Azores":"Açores", 'Aveiro': 'X', 'Beja': 'X', 'Braga': 'X', 'Bragança': 'X', 'Castelo Branco': 'X', 'Coimbra': 'X', 'Évora': 'X', 'Faro': 'X', 'Guarda': 'X', 'Leiria': 'X', 'Lisboa': 'X', 'Portalegre': 'X', 'Porto': 'X', 'Santarém': 'X', 'Setúbal': 'X', 'Viana do Castelo': 'X', 'Vila Real': 'X', 'Viseu': 'X'})
    
    #mapa = mapa.replace({"Azores":"X", "Madeira":"X"})
    mapa = mapa.merge(district_stats1, left_on='NAME_1', right_index=True)
    mapa = mapa.merge(district_stats2, left_on='NAME_1', right_index=True, suffixes=('_'+var1, '_'+var2))
    mapa = mapa.merge(district_stats3, left_on='NAME_1', right_index=True, suffixes=('_'+var2, '_'+var3))

    fig, (ax3, ax2, ax1) = plt.subplots(ncols=3, figsize=(16, 14))
    mapa.plot(column=var1, cmap='OrRd', legend=True, ax=ax1, vmin=min_val, vmax=max_val)
    ax1.set_title(f"{ano1}", fontsize=16)
    ax1.set_axis_off()

    mapa.plot(column=var2, cmap='OrRd', legend=True, ax=ax2, vmin=min_val, vmax=max_val)
    ax2.set_title(f"{ano2}", fontsize=16)
    ax2.set_axis_off()
    
    mapa.plot(column=var3, cmap='OrRd', legend=True, ax=ax3, vmin=min_val, vmax=max_val)
    ax3.set_title(f"{ano3}", fontsize=16)
    ax3.set_axis_off()

    # Add labels to the map with the average population for each district
    for idx, row in mapa.iterrows():
        ax1.annotate(text=f"{row[var1]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax2.annotate(text=f"{row[var2]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
        ax3.annotate(text=f"{row[var3]:.1f}", xy=row['geometry'].centroid.coords[0], horizontalalignment='center', fontsize=15)
    plt.show()
    
#print(comp["diff_abs_21"].sum())
#print(comp["diff_abs_11"].sum())
#print(comp["diff_abs_01"].sum())
#district_stats1 = comp.groupby('Distrito')[var1].apply(lambda x: pd.Series({'excesso_percentagem': x / comp.loc[x.index, var1].sum() * 100}))
#district_stats1 = pd.DataFrame(district_stats1).reset_index().drop(columns=["level_1"]).set_index("Distrito")
#comp.groupby("Distrito").agg({'diff_abs_21': 'sum'})["diff_abs_21"] / comp["diff_abs_21"].sum() * 100 