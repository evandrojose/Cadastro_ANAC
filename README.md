# Cadastro_ANAC

A Agencia de Aviação Civil do Brasil mantém dados sobre os aeroportos do país em seu site, nos formatos CSV e Excel. No entanto, o CSV fornecido possui uma apresentação que dificulta sua importação em SIGs, como o QGIS, por exemplo.

O script Python (versão Python3) fornecido deve ser rodado e apresentará as seguintes instruções:
1. Visite: https://www.anac.gov.br/assuntos/setor-regulado/aerodromos/cadastro-de-aerodromos-civis
2. Faça download dos arquivos CSV relacionados aos aerodromos brasileiros. Pode-se analisar mais de um arquivo ao mesmo tempo
3. Crie uma pasta, adicione estes arquivos e e troque a extensão .csv por .entrada
4.Cole aqui o diretorio criado:

Será criado um arquivo OUTPUT em CSV com os dados consolidados, além de um log.txt com eventos de erros a afins.

O CSV resposta será útil para análises em planilha, Python, R, QGis, etc.
