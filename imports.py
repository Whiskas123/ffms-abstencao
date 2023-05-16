import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import seaborn as sns
from unidecode import unidecode

corr_xlsx = pd.read_excel('dados/corr/correspondencias.xlsx', converters={'cod_old':str,'cod_new':str})
corr = dict(zip(corr_xlsx.cod_old,corr_xlsx.cod_new))
cod_to_dsg = dict(zip(corr_xlsx.cod_new, corr_xlsx.dsg_new))
corr_concelhos_xlsx = pd.read_excel('dados/corr/correspondencias_old.xlsx', sheet_name = "concelhos", converters={'DICO':str,'Concelho':str})
corr_concelhos = dict(zip(corr_concelhos_xlsx.DICO, corr_concelhos_xlsx.Concelho))

portugal_districts = {
    '01': 'Aveiro',
    '02': 'Beja',
    '03': 'Braga',
    '04': 'Bragança',
    '05': 'Castelo Branco',
    '06': 'Coimbra',
    '07': 'Évora',
    '08': 'Faro',
    '09': 'Guarda',
    '10': 'Leiria',
    '11': 'Lisboa',
    '12': 'Portalegre',
    '13': 'Porto',
    '14': 'Santarém',
    '15': 'Setúbal',
    '16': 'Viana do Castelo',
    '17': 'Vila Real',
    '18': 'Viseu',
    '31': 'Madeira',
    '32': 'Madeira',
    '41': 'Açores',
    '42': 'Açores',
    '43': 'Açores',
    '44': 'Açores',
    '45': 'Açores',
    '46': 'Açores',
    '47': 'Açores',
    '48': 'Açores',
    '49': 'Açores'
}

def read_mai_year(ano):
    if ano >= 2009:
        df = pd.read_excel("dados/MAI/BDRE_Contagem_Eleitores_" + str(ano) + ".xls", sheet_name="Freguesia_Consulado", converters={"Codigo":str, 'Código':str, "Nac":int, "UE": int, "ER":int,"TOTAL":int})
        rename_dict = {"Codigo":"FREGUESIA", "Código":"FREGUESIA", "Nac":"NAC", "Distrito/Ilha/Continente > Concelho/País > Freguesia/Consulado":"Nome"}

        for old_col, new_col in rename_dict.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
                
        df = df[["FREGUESIA", "Nome", "NAC"]]
        df = df[~df["FREGUESIA"].isna()]
        df = df.loc[df["FREGUESIA"].map(lambda x: int(str(x)[:2])) < 50]
        if ano == 2013:
            df["FREGUESIA"] = df["FREGUESIA"].apply(lambda x: x.replace('  ',''))
        df["FREGUESIA"] = df["FREGUESIA"].map(corr)
        df = df.groupby('FREGUESIA').agg({'Nome': 'first', 'NAC': 'sum'})
        df = df.rename(columns={"NAC": "PT_MAI_" + str(ano)[2:]})
    else:
        df = pd.read_excel("dados/MAI/BDRE_Contagem_Eleitores_" + str(ano) + ".xls", converters={"Codigo":str, 'Código': str, "Nac":int, "UE": int, "ER":int,"TOTAL":int}, skiprows=1)
        if ano == 2002:
            df = df.drop(columns=["Unnamed: 0", "AVEIRO"])
        else:  
            df = df.drop(columns=["CONTINENTE E REGIÕES AUTÓNOMAS", "Unnamed: 1"])
        df = df.rename(columns = {"Unnamed: 2" : "Concelho", "Unnamed: 3":"Nome"})

        column_names = df.columns.tolist()
        column_names[-1] = 'NAC'
        df.columns = column_names

        df['Concelho'] = df['Concelho'].fillna(method='ffill')
        df = df[df['Nome'].notna()]

        # create a list of values to keep
        concelhos = corr_xlsx["Concelho"].unique().tolist()
        mask = df['Concelho'].isin(concelhos)
        df = df.loc[mask].reset_index(drop=True)

        df['Nome'] = df['Nome'].str.upper()
        df["FREGUESIA"] = np.nan
        
        df["Nome"] = df["Nome"].apply(lambda x: unidecode(x))
        df["Concelho"] = df["Concelho"].apply(lambda x: unidecode(x))
        #compare_xlsx = corr_xlsx
        #compare_xlsx["Nome"] = df["Nome"].apply(lambda x: unidecode(x))
        #compare_xlsx["Concelho"] = df["Concelho"].apply(lambda x: unidecode(x))

        for idx, row in df.iterrows():
            select_df = corr_xlsx.loc[(corr_xlsx['Concelho'] == row["Concelho"]) & (corr_xlsx['dsg_old'] == row["Nome"])]
            if not select_df.empty:
                df.loc[idx, "FREGUESIA"] = select_df.iloc[0]["cod_new"]
                df.loc[idx, "Nome"] = select_df.iloc[0]["dsg_new"]

        df = df[df["Nome"] != "HAVANA"]
        df = df.groupby('FREGUESIA').agg({'Nome': 'first', 'NAC': 'sum'})
        df = df.rename(columns={"NAC": "PT_MAI_" + str(ano)[2:]})
        
    return df

def read_mai():
    ele21 = read_mai_year(2021)
    ele11 = read_mai_year(2011)
    ele01 = read_mai_year(2001)

    mai = ele21.merge(ele11,left_index=True, right_index=True).merge(ele01, left_index=True, right_index = True)
    return mai

def read_censos():
    nac21 = pd.read_excel('dados/dados_INE.xlsx', sheet_name="Nacionalidade2021", converters={'MUNICIPIO':str,'FREGUESIA':str}, skiprows=[0])
    nac11 = pd.read_excel('dados/dados_INE.xlsx', sheet_name="Nacionalidade2011", converters={'MUNICIPIO_CAOP2013':str,'FREGUESIA_CAOP2013':str}, skiprows=[0])
    nac01 = pd.read_excel('dados/dados_INE.xlsx', sheet_name="Nacionalidade2001", converters={'CONCELHO_EU02':str,'FREGUESIA_EU02':str}, skiprows=[0])
    tipologias2014 = pd.read_excel('dados/tipologias2014.xlsx', dtype={"Código": str}).rename(columns={"Código": "FREGUESIA"}).set_index("FREGUESIA")


    nac21 = nac21[(nac21["FREGUESIA"] != '000000') & (nac21["GRUPO ETÁRIO"] == "2 18 ou mais anos")]
    nac21 = nac21.rename(columns={"Designação CAOP2013": "FF_DSG", "Portuguesa":"PT", "Estrangeira":"EST", "Apátrida":"APA", "Total":"TOTAL"})
    nac21 = nac21[["CC_DSG", "FREGUESIA", "FF_DSG", "PT", "TOTAL"]]
    nac21["FREGUESIA"] = nac21["FREGUESIA"].map(corr)
    nac21['FF_DSG'] = nac21['FREGUESIA'].map(cod_to_dsg)
    nac21 = nac21.groupby('FREGUESIA').agg({'CC_DSG': 'first', 'FF_DSG': 'first', 'PT': 'sum', "TOTAL": "sum"})

    nac11 = nac11[(nac11["FREGUESIA_CAOP2013"] != '000000') & (nac11["GRUPO ETÁRIO"] == "2 18 ou mais anos")]
    nac11 = nac11.rename(columns={"Designação CAOP2013": "FF_DSG", "FREGUESIA_CAOP2013": "FREGUESIA", "Portuguesa":"PT", "Estrangeira":"EST", "Apátrida":"APA", "Total":"TOTAL"})
    nac11 = nac11[["CC_DSG", "FREGUESIA", "FF_DSG", "PT", "TOTAL"]]
    nac11["FREGUESIA"] = nac11["FREGUESIA"].map(corr)
    nac11['FF_DSG'] = nac11['FREGUESIA'].map(cod_to_dsg)
    nac11 = nac11.groupby('FREGUESIA').agg({'CC_DSG': 'first', 'FF_DSG': 'first', 'PT': 'sum', "TOTAL":"sum"})

    nac01 = nac01[(nac01["FREGUESIA_EU02"] != '000000') & (nac01["GRUPO ETÁRIO"] == "2 18 ou mais anos")]
    nac01 = nac01.rename(columns={"FREGUESIA_EU02": "FREGUESIA", "Portuguesa":"PT", "Estrangeira":"EST", "Apátrida":"APA", "Total":"TOTAL"})
    nac01["FREGUESIA"] = nac01["FREGUESIA"].map(corr)
    nac01['FF_DSG'] = nac01['FREGUESIA'].map(cod_to_dsg)
    nac01 = nac01.groupby('FREGUESIA').agg({'CC_DSG': 'first', 'FF_DSG': 'first', 'PT': 'sum', "TOTAL": 'sum'})

    nac11 = nac11.drop(['FF_DSG', 'CC_DSG'], axis=1)
    nac01 = nac01.drop(['FF_DSG', 'CC_DSG'], axis=1)
    nac21 = nac21.rename(columns={"TOTAL":"TOTAL_INE_21", "PT":"PT_INE_21"})
    nac11 = nac11.add_suffix('_INE_11')
    nac01 = nac01.add_suffix('_INE_01')

    tipologias2014 = tipologias2014.drop("Designação", axis=1)
    tipologias2014["Distrito"] = tipologias2014.index.map(lambda x: portugal_districts.get(x[:2], 'Unknown'))

    educacao21 = pd.read_excel('dados/educacao2021.xlsx').rename(columns={"cod": "FREGUESIA"}).set_index("FREGUESIA")
    educacao21 = remover_nao_freguesias(educacao21)
    educacao21 = educacao21.reset_index()
    educacao21["FREGUESIA"] = educacao21["FREGUESIA"].map(corr)
    educacao21 = educacao21.groupby("FREGUESIA").agg({"sec+":'sum', "superior":"sum"})
    educacao21 = educacao21.add_suffix("_INE_21")

    envelhecimento21 = pd.read_excel('dados/65+_2021.xlsx').set_index("FREGUESIA")
    envelhecimento21 = remover_nao_freguesias(envelhecimento21)
    envelhecimento21 = envelhecimento21.reset_index()
    envelhecimento21["FREGUESIA"] = envelhecimento21["FREGUESIA"].map(corr)
    envelhecimento21 = envelhecimento21.groupby("FREGUESIA").agg({"65+":'sum'})
    envelhecimento21 = envelhecimento21.add_suffix("_INE_21")

    envelhecimento11 = pd.read_excel('dados/65+_2011.xlsx').set_index("FREGUESIA")
    envelhecimento11 = remover_nao_freguesias(envelhecimento11)
    envelhecimento11 = envelhecimento11.reset_index()
    envelhecimento11["FREGUESIA"] = envelhecimento11["FREGUESIA"].map(corr)
    envelhecimento11 = envelhecimento11.groupby("FREGUESIA").agg({"65+":'sum'})
    envelhecimento11 = envelhecimento11.add_suffix("_INE_11")

    envelhecimento01 = pd.read_excel('dados/65+_2001.xlsx').set_index("FREGUESIA")
    envelhecimento01 = remover_nao_freguesias(envelhecimento01)
    envelhecimento01 = envelhecimento01.reset_index()
    envelhecimento01["FREGUESIA"] = envelhecimento01["FREGUESIA"].map(corr)
    envelhecimento01 = envelhecimento01.groupby("FREGUESIA").agg({"65+":'sum'})
    envelhecimento01 = envelhecimento01.add_suffix("_INE_01")

    desemprego21 = pd.read_excel('dados/desempregados_2021.xlsx').set_index("FREGUESIA")
    desemprego21 = remover_nao_freguesias(desemprego21)
    desemprego21 = desemprego21.reset_index()
    desemprego21["FREGUESIA"] = desemprego21["FREGUESIA"].map(corr)
    desemprego21 = desemprego21.groupby("FREGUESIA").agg({"desemprego":'sum'})
    desemprego21 = desemprego21.add_suffix("_INE_21")

    desemprego11 = pd.read_excel('dados/desempregados_2011.xlsx').set_index("FREGUESIA")
    desemprego11 = remover_nao_freguesias(desemprego11)
    desemprego11 = desemprego11.reset_index()
    desemprego11["FREGUESIA"] = desemprego11["FREGUESIA"].map(corr)
    desemprego11 = desemprego11.groupby("FREGUESIA").agg({"desemprego":'sum'})
    desemprego11 = desemprego11.add_suffix("_INE_11")

    populacao = tipologias2014.merge(nac21, left_index=True, right_index=True).merge(nac11, left_index=True, right_index=True).merge(nac01, left_index=True, right_index=True).merge(educacao21, left_index=True, right_index=True).merge(envelhecimento21, left_index=True, right_index=True).merge(envelhecimento11, left_index=True, right_index=True).merge(envelhecimento01, left_index=True, right_index=True).merge(desemprego21, left_index=True, right_index=True).merge(desemprego11, left_index=True, right_index=True)
    populacao["sec+_INE_21"] = populacao["sec+_INE_21"] / populacao["TOTAL_INE_21"] * 100
    populacao["superior_INE_21"] = populacao["superior_INE_21"] / populacao["TOTAL_INE_21"] * 100
    populacao["65+_INE_21"] = populacao["65+_INE_21"] / populacao["TOTAL_INE_21"] * 100
    populacao["65+_INE_11"] = populacao["65+_INE_11"] / populacao["TOTAL_INE_11"] * 100
    populacao["65+_INE_01"] = populacao["65+_INE_01"] / populacao["TOTAL_INE_01"] * 100
    populacao["desemprego_INE_21"] = populacao["desemprego_INE_21"] / populacao["TOTAL_INE_21"] * 100
    populacao["desemprego_INE_11"] = populacao["desemprego_INE_11"] / populacao["TOTAL_INE_11"] * 100

    populacao["sec+_INE_21"] = populacao["sec+_INE_21"].astype(float).round(1)
    populacao["superior_INE_21"] = populacao["superior_INE_21"].astype(float).round(1)
    populacao["65+_INE_21"] = populacao["65+_INE_21"].astype(float).round(1)
    populacao["65+_INE_11"] = populacao["65+_INE_11"].astype(float).round(1)
    populacao["65+_INE_01"] = populacao["65+_INE_01"].astype(float).round(1)
    populacao["desemprego_INE_21"] = populacao["desemprego_INE_21"].astype(float).round(1)
    populacao["desemprego_INE_11"] = populacao["desemprego_INE_11"].astype(float).round(1)

    populacao["VAR_PT_21_11_rel"] = (populacao["PT_INE_21"] - populacao["PT_INE_11"]) / populacao["PT_INE_11"] * 100

    return populacao

def get_comp():

    populacao = read_censos()
    mai = read_mai()
    comp = populacao.merge(mai, left_index=True, right_index=True)

    comp = comp.drop(columns=["Nome_y", "Nome"])
    comp["diff_abs_21"] = comp["PT_MAI_21"] - comp["PT_INE_21"]
    comp["diff_abs_21"] = comp["diff_abs_21"].astype(float)
    comp["diff_abs_11"] = comp["PT_MAI_11"] - comp["PT_INE_11"]
    comp["diff_abs_01"] = comp["PT_MAI_01"] - comp["PT_INE_01"]
    comp["diff_rel_21"] = comp["diff_abs_21"] / comp["PT_INE_21"] * 100
    comp["diff_rel_11"] = comp["diff_abs_11"] / comp["PT_INE_11"] * 100
    comp["diff_rel_01"] = comp["diff_abs_01"] / comp["PT_INE_01"] * 100
    comp['diff_rel_21'] = comp['diff_rel_21'].astype(float).round(1)
    comp['diff_rel_11'] = comp['diff_rel_11'].astype(float).round(1)
    comp['diff_rel_01'] = comp['diff_rel_01'].astype(float).round(1)
    comp["VAR_diff_rel_21_11"] = comp["diff_rel_21"] - comp["diff_rel_11"]

    return comp



def remover_nao_freguesias(df):
    for index_value in df.index:
        # Check if the length of the index value is less than 6 characters
        if len(str(index_value)) < 6:
            # Delete the row with the corresponding index
            df = df.drop(index=index_value)
    return df

# ADICIONAR VARIÁVEIS (MÉDIA PONDERADA PARA AS UNIÕES DE FREGUESIAS (EX: EDUCAÇÃO))
#df = pd.DataFrame({
#    'Index': ['A', 'A', 'B', 'B', 'C'],
#    'A': [1, 2, 3, 4, 5],
#    'B': [10, 20, 30, 40, 50]
#})
#weighted_mean = lambda x: np.average(x, weights=df.loc[x.index, "A"])
#grouped_df = df.groupby('Index').agg(A=("A", "sum"),B_weighted=("B", weighted_mean))


#GRÁFICO COMPARAÇÃO POPULAÇÃO RECENSEADA 
#mai_list = []
#for year in range(2001, 2022):
#    df = read_mai(year)
#   mai = df["PT_MAI_" + str(year)[2:]].sum()
#   print(str(year) + ": " + str(mai))
#    mai_list.append(mai)
#ine_list = [8113427, 8166640,  8079525]
# create two series objects with different numbers of observations
#years_ine = ["2001", "2011", "2021"]
#years_mai = [str(x).zfill(2) for x in range(2001, 2022)]
#mai = pd.Series(mai_list, index=years_mai)
#ine = pd.Series(ine_list, index=years_ine)
# reindex both series to have a common index
#common_index = [str(x).zfill(2) for x in range(2001, 2022)]
#mai = mai.reindex(common_index)
#ine = ine.reindex(common_index)
#df = pd.concat([mai, ine], axis=1)
#df.columns = ['MAI', 'INE']
# plot both series using Seaborn
#lp = sns.lineplot(data=df)
#lp.set_xticklabels(lp.get_xticklabels(), rotation=90)
#lp.set_title("População Portuguesa +18 / Recenseada")
