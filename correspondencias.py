#Codigo correspondências

#novas_freguesias =  set(nac21["Designação CAOP2013"]) - set(nac01["FF_DSG"].unique())

#Correspondencias Código-Designacao
#corr_01 = nac01.groupby('FREGUESIA_EU02')['FF_DSG'].unique().reset_index()
#corr_01['FF_DSG'] = corr_01['FF_DSG'].apply(lambda x: list(x)[0])
#corr_01 = corr_01.iloc[1:]
#corr_01 = corr_01.set_index('FREGUESIA_EU02')['FF_DSG'].to_dict()
#corr_21 = nac21.groupby('FREGUESIA')['Designação CAOP2013'].unique().reset_index()
#corr_21 ['Designação CAOP2013'] = corr_21['Designação CAOP2013'].apply(lambda x: list(x)[0])
#corr_21 = corr_21.iloc[1:]
#corr_21 = corr_21.set_index('FREGUESIA')['Designação CAOP2013'].to_dict()

#corr = pd.DataFrame.from_dict(corr_01, orient='index', columns=['dsg_old'])
#corr.index.name = 'cod_old'
#corr['cod_new'] = None
#corr['dsg_new'] = None

#for index, row in corr.iterrows():
#    if index in corr_21:
#        corr.loc[index, "cod_new"] = index
#        corr.loc[index, "dsg_new"] = corr_21[index]

#for index, row in corr.iterrows():
#    if row["cod_new"] == None:
#        for key, value in corr_21.items():
#            if key[:4] == index[:4] and row["dsg_old"] in value:
#                corr.loc[index, "cod_new"] = key
#                corr.loc[index, "dsg_new"] = value
#corr.to_csv("correspondencias.csv")