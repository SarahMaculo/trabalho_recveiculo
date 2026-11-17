import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


try:
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1' )
    df_recveiculos = df_ocorrencias[['cisp','recuperacao_veiculos']]
    df_recveiculos = df_recveiculos.groupby('cisp', as_index=False)['recuperacao_veiculos'].sum()
    df_recveiculos = df_recveiculos.sort_values(
        by='cisp',
        ascending=False
    )
    # print(df_recveiculos)

except Exception as e:
    print(f'O erro foi: {e}')

try:
    array_recuperacao = np.array(df_recveiculos['recuperacao_veiculos'])
    media_recuperacao = np.mean(array_recuperacao)
    mediana_recuperacao = np.median(array_recuperacao)
    distancia = abs (
        media_recuperacao - mediana_recuperacao / mediana_recuperacao * 100
    )
    q1 = np.quantile(array_recuperacao, .25)
    q2 = np.quantile(array_recuperacao, .50)
    q3 = np.quantile(array_recuperacao, .75)

    iqr = q3 - q1
    limite_sup = q3 + (1.5*iqr)
    limite_inf = q1 - (1.5*iqr)

    # 25% menores
    df_rec_maiores = df_recveiculos[df_recveiculos['recuperacao_veiculos']>q3]
    df_rec_menores = df_recveiculos[df_recveiculos['recuperacao_veiculos']<q1]

    # Outliers
    df_rec_outliers_maiores = (
        df_recveiculos[df_recveiculos['recuperacao_veiculos']>limite_sup]
    )

    df_rec_outliers_menores = (
        df_recveiculos[df_recveiculos['recuperacao_veiculos']<limite_inf]
    )

    max = np.max(array_recuperacao)
    min = np.min(array_recuperacao)

    amplitude = max - min
    variancia = np.var(array_recuperacao)
    distancia_variancia = variancia / (media_recuperacao**2) * 100
    desvio_padrao = np.std(array_recuperacao)
    coef_variacao = (desvio_padrao / media_recuperacao) * 100 

except Exception as e:
    print(f'O erro foi: {e}')

try:
    print('TAXAS DE RECUPERAÇÃO DE VEÍCULOS')
    print()
    print('M A I O R E S')
    print(f'{df_rec_maiores.sort_values(by='recuperacao_veiculos', ascending=False)}')
    print()
    print('M E N O R E S')
    print(f'{df_rec_menores.sort_values(by='recuperacao_veiculos', ascending=True)}')
    print()
    print('O U T L I E R S')
    print()
    print('O U T L I E R S  M A I O R E S')
    if len(df_rec_outliers_maiores) == 0:
        print('Não há outliers.')
    else:
        print(df_rec_outliers_maiores)

    print()
    print('O U T L I E R S   M E N O R E S')
    if len(df_rec_outliers_menores) == 0:
        print('Não há outliers.')
    else: 
        print(df_rec_outliers_menores)

    print('MOSTRANDO VALORES')
    print()
    print(f'''
    Mínimo: {min}
    Máximo: {max}

    Limite inferior: {limite_inf}

    Q1: {q1}
    Q2: {q2}
    Q3: {q3}

    Limite Superior: {limite_sup}
    
    MEDIDAS DE TENDÊNCIA CENTRAL
    
    Média: {media_recuperacao}
    Mediana: {mediana_recuperacao}
    Distância entre a média e mediana: {distancia}
    Amplitude Total: {amplitude}
    IQR: {iqr}
    Variância: {variancia}
    Coeficiência da Variância: {coef_variacao}
    ''')
except Exception as e:
    print(f'O erro feito: {e}')

try:
    plt.figure(figsize=(16, 10))
    plt.subplot(2,2,1)
    plt.boxplot(df_recveiculos['recuperacao_veiculos'], orientation='horizontal', showmeans=True)
    plt.title('Distribuição dos dados - Recuperação de Veículos')

    plt.subplot(2, 2, 2)
    plt.text(0.1, 1.50, f'Limite Inferior: {limite_inf},', fontsize=12)
    plt.text(0.1, 1.40, f'Mínimo: {min},', fontsize=12)
    plt.text(0.1, 1.30, f'Q1: {q1},', fontsize=12)
    plt.text(0.1, 1.20, f'Q2: {q2},', fontsize=12)
    plt.text(0.1, 1.10, f'Q3: {q3},', fontsize=12)
    plt.text(0.1, 1.00, f'Máximo: {max},', fontsize=12)
    plt.text(0.1, 0.90, f'Limite Superior: {limite_sup},', fontsize=12)

    plt.text(0.1, 0.70, f'Mediana: {mediana_recuperacao},', fontsize=12)
    plt.text(0.1, 0.60, f'Média: {media_recuperacao},', fontsize=12)
    plt.text(0.1, 0.50, f'IQR: {iqr},', fontsize=12)
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude},', fontsize=12)
    plt.text(0.1, 0.30, f'Distância: {distancia},', fontsize=12)
    plt.axis('off')

    # Gráfico de barras das delegacias que registraram mais e menos recuperações
    plt.subplot(2,2,3)
    plt.barh(df_rec_maiores['cisp'], df_rec_maiores['recuperacao_veiculos'], color='#800020')
    
    plt.title('Delegacias com maiores registros de recuperação de veículos')
    plt.xlabel('Recuperação de Veículos')
    plt.ylabel('Delegacias')

    plt.subplot(2,2,4)
    plt.barh(df_rec_menores['cisp'], df_rec_menores['recuperacao_veiculos'], color='#800020')
    plt.title('Delegacias com menores registros de recuperação de veículos')
    plt.xlabel('Recuperação de Veículos')
    plt.ylabel('Delegacias')

    plt.show()
except Exception as e:
    print(f'Erro: {e}')