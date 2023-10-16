import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Brasile-real-estate-dataset.csv', encoding='Windows-1254', index_col=0)
#print(f'{df}\n')
colunas = {'property_type': 'tipo_propriedade', 'state' : 'estado', 'region' : 'região', 'price_brl' : 'preco_brl'}
df.rename(columns=colunas, inplace=True)
renomear = {'apartment': 'apartamento', 'house': 'casa'}
df['tipo_propriedade'] = df['tipo_propriedade'].apply(lambda x: renomear[x] if x in renomear else x)
print(f'{df}\n')
print(f'{df.info()}\n')
print(f'{df.describe()}\n')

#Retirar os Nan
print(f'Quantidade de valores nulos:\n{df.isna().sum()}\n')
df.dropna(axis=0, inplace=True)

#Qual o preço por m^2?
df['preco_m2'] = df['preco_brl']/df['area_m2']
print(f'{df}\n')

#qual o estado com o imóvelcom maior valor por metro quadrado?
indice = df['area_m2'].idxmax()
estado_max = df.loc[indice, 'estado']
print(f'O imóvel com maior valor por metro por quadrado fica em {estado_max}\n')

#qual o estado com o imóvel com menor valor por metro quadrado?
indice = df['area_m2'].idxmin()
estado_min = df.loc[indice, 'estado']
print(f'O imóvel com menor valor por metro por quadrado fica em {estado_min}\n')
#Qual a média de preço por estado?
df_semregiao = df.drop('região', axis=1)
estados = df_semregiao.groupby(['estado', 'tipo_propriedade'])['preco_m2'].mean()
print(f'Média dos preços por estados e tipos de imóvel {estados}\n')
#Qual estado possuí maior média do preço do m2 e o tipo de imóvel
estado_imovel = estados.idxmax()
print(f'O estado e o tipo de imóvel com maior médio do preço do m2 é:{estado_imovel}\n')

#O valor do metro quadrado representa quantos por cento da média para o estado?
df_media = df.merge(estados, on=['estado', 'tipo_propriedade'], how='left')
df_media.rename(columns={ 'preco_m2_x' : 'preco_m2','preco_m2_y': 'media_preco'}, inplace=True)
df_media['pct_media'] = 100*df_media['preco_m2']/df_media['media_preco']
print(f'O valor do metro quadrado representa a porcentagem da média para o estado {df_media}\n')

# Quais os imóveis com valores menores que a média do preço/m2?
imoveis_valores_inferiores = df_media.where(df_media['pct_media'].apply(lambda row: row < 100))
imoveis_valores_inferiores.dropna(inplace=True)
print(f'Os imóveis abaixo do valor médio do estado são:\n {imoveis_valores_inferiores}\n')

#Classificaros imóveis de acordo com a representação da porcentagem do valor com o valor medio/m^2
bins = [33.33, 66.66, 100, 500]
rotulos = ['desvalorizado', 'valorizado', 'supervalorizado']

# Usar pd.cut com rótulos personalizados
df_media['classificacao'] = pd.cut(df_media['pct_media'], bins=bins, labels=rotulos)
print(f'Classificação dos imóveis\n{df_media}\n')

# Criar um boxplot com base no preço para cada classificação
plt.boxplot([df_media[df_media['classificacao'] == 'desvalorizado']['preco_brl'],
             df_media[df_media['classificacao'] == 'valorizado']['preco_brl'],
             df_media[df_media['classificacao'] == 'supervalorizado']['preco_brl']],
            labels=['Desvalorizado', 'Valorizado', 'Supervalorizado'], patch_artist=True)
# Configurações do gráfico
plt.xlabel('Classificação')
plt.ylabel('Preço (BRL)')
plt.title('Boxplot por Classificação de Preço')
# Exibir o gráfico
plt.show()

df_media.to_csv('Tabela valores por m2.csv')
