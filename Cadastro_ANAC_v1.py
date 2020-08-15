#Python 3.7-------
#Aerodromos_ANAC_v1----
#15/ago/2020 - Evandro Jose da Silva (evandro@ita.br)
#Aceita dados em CSV retirados deste site: https://www.anac.gov.br/assuntos/setor-regulado/aerodromos/cadastro-de-aerodromos-civis
#Salva Arquivo CSV consolidado com os aerodromos e seus atributos, que podem ser lido no QGIS
#Obs.: pistas secundarias nao sao consideradas
#------------------------------------------------------------------------------------------------------------------------------

def main():
	from pathlib import Path
	print ('1. Visite: https://www.anac.gov.br/assuntos/setor-regulado/aerodromos/cadastro-de-aerodromos-civis')
	print ('2. Faça download dos arquivos CSV relacionados aos aerodromos brasileiros. Pode-se analisar mais de um arquivo ao mesmo tempo')
	print ('3. Crie uma pasta, adicione estes arquivos e e troque a extensão .csv por .entrada')
	folder= str(input("4.Cole aqui o diretorio criado:"))
	
	
	#----Leitura de arquivos de entrada-------------------------------
	Files=[]
	p = Path(folder)
	csv_files = [csvfile for csvfile in p.iterdir() if csvfile.is_file() and csvfile.suffix == '.entrada']
	for filename in csv_files:
	    Files.append(filename)
	    print ('OK. Será lido: ',filename)
	
	if len(Files)==0:
	    print ('--->ERRO: a pasta fornecida não contém os arquivos de entrada no padrão .entrada')
	    input('Finalizar e corrigir a pasta')
	    exit()
	
	LATD_0,LONGT_0= -13.,-48.77 #Centro
	Delta=100.#graus  #empregue valores menores para filtrar aerodromos em raio de Delta graus em relação ao centro
	
	import csv
	import pandas as pd
	LOG=[]
	
	ICAO,TIPO,NOME,MUNICIPIO,UF,LATD,LONGT,DIST,COMPRIMENTO,LARGURA,APROXIMCAO,SUPERFICIE,ORIENTACAO=[],[],[],[],[],[],[],[],[],[],[],[],[]
	
	def grad(x):
	    signal=-1.
	    for j in range(0,len(x)):
	        if x[j]=="S" or x[j]=="W":
	            pass
	        if x[j]=="N" or x[j]=="E":
	            signal=+1
	    size=len(x)
	    num=[]
	    result=[]
	    j=0
	    contin=True
	    while contin==True:
	        char=x[j]
	        try:
	            int(char)
	            #print(char)
	            num.append(int(char))
	        except:
	            #print('simb',char)
	            result.append(num)
	            num=[]
	        if j==(size-1):
	            contin=False
	        else:
	            j=j+1
	    vetor=[]
	    for j in range(0,len(result)):
	        a=result[j]
	        if len(a)>0:
	            vetor.append(a)
	    valor=0
	    for j in range(0,len(vetor)):
	        line=vetor[j]
	        if j==0:
	            if len(line)==1:
	                valor=line[0]
	            if len(line)==2:
	                valor=line[0]*10+line[1]
	        if j==1:
	            if len(line)==1:
	                valor=valor+line[0]/60.
	            if len(line)==2:
	                valor=valor+(line[0]*10+line[1])/60.
	        if j==2:
	            if len(line)==1:
	                valor=valor+line[0]/3600.
	            if len(line)==2:
	                valor=valor+(line[0]*10+line[1])/3600.
	            
	    return valor*signal
	            
	    
	
	#x="12° 4' 17"" E" #testes da funcao grad
	#print('-->',grad(x))
	
	def get_numb(x,sep='.',label=''):
	    'pega numero inteiro antes de m'
	    w=0
	    try:
	        V=[]
	        direita,k,dec=False,1,0
	        for j in range(0,len(x)):
	            #input('j= '+str(j))
	            try:
	                if direita==False:
	                    V.append(int(x[j]))
	                if direita==True:
	                    y=int(x[j])
	                    dec=dec+y/(10*k)
	                    k=k*10
	            except:
	                if (x[j]==sep):
	                    direita=True
	                
	            j=j+1
	        if len(V)==1:
	            resp=V[0]
	        elif len(V)==2:
	            resp=V[0]*10+V[1]
	        elif len(V)==3:
	            resp=V[0]*100+V[1]*10+V[2]
	        elif len(V)==4:
	            resp=V[0]*1000+V[1]*100+V[2]*10+V[3]
	        elif len(V)==5:
	            resp=V[0]*10000+V[1]*1000+V[2]*100+V[3]*10+V[4]
	        else:
	            print(ERROR, x)
	        
	        w=resp+dec
	    except:
	        mesg=str(label)+ ' '+'sem dados de comprimento/largura da PPD'
	        LOG.append(mesg)
	    return w
	
	
	        
	def get_orient(x,label=''):
	    '''orientacao magn em graus'''
	    #print (label)
	    #print ('x',x)
	    #print ('x[1]',x[1])
	    #input('nova orient')
	    resp=0.0001
	    try:
	        resp=int(x[1])*10+int(x[2])
	    except:
	        try: #exemplo 8L ao inves de 08L
	            resp=int(x[1])*10
	        except:
	            mesg=str(label)+ ' '+'sem dados de orientacao da PPD'
	            LOG.append(mesg)
	    return resp*10
	        
	#x=' 10/28'
	#print(';;;;;;',get_orient(x))
	
	
	for i in range(0,len(Files)):
	    with open(Files[i], 'r') as file:
	        print('       ...                    ....                     ')
	        print ('Analisando ',Files[i])
	        LOG.append('       ...                    ....                     ')
	        LOG.append(Files[i])
	        input("Pressione quaqluer tecla pa continuar")
	        a=csv.reader(file, delimiter=';')
	        linha=0
	        for row in a:
	            linha=linha+1
	            try:
	                if row[0][0]=="S" and len(row[0])==4:
	                    
	                    ICAO.append(row[0])
	                    if i==0:
	                        TIPO.append('Privado')
	                    if i==1:
	                        TIPO.append('Publico')
	                  
	                    NOME.append(row[2])
	                    MUNICIPIO.append(row[3])
	                    UF.append(row[4])
	                    #input('normal')
	                    lat,long=grad(row[5]),grad(row[6])
	                    
	                    distt=((lat-LATD_0)**2+(long-LONGT_0)**2)**0.5
	                    #input('normal1')
	                    LATD.append(lat)
	                    LONGT.append(long)
	                    DIST.append(distt)
	                    APROXIMCAO.append(row[8])
	                    SUPERFICIE.append(row[13])
	                    
	                    COMPRIMENTO.append(get_numb(row[10],label=row[0]))
	                    LARGURA.append(get_numb(row[11],label=row[0]))
	                    ORIENTACAO.append(get_orient(row[9],label=row[0]))
	
	                        
	                
	                    
	            except:
	                try:
	                        int(grad(row[5])) #para as linhas sem codigo icao
	                        ICAO.append('indefinido')
	                        if i==0:
	                            TIPO.append('Privado')
	                        if i==1:
	                            TIPO.append('Publico')
	                  
	                        NOME.append(row[2])
	                        MUNICIPIO.append(row[3])
	                        UF.append(row[4])
	                        lat,long=grad(row[5]),grad(row[6])
	                        distt=((lat-LATD_0)**2+(long-LONGT_0)**2)**0.5
	                        LATD.append(lat)
	                        LONGT.append(long)
	                        DIST.append(distt)
	                        APROXIMCAO.append(row[8])
	                        SUPERFICIE.append(row[13])
	                        
	                        COMPRIMENTO.append(get_numb(row[10],label=row[1]))
	                        LARGURA.append(get_numb(row[11],label=row[1]))
	                        ORIENTACAO.append(get_orient(row[9],label=row[1]))
	                     
	                except:
	                        mesg=("Ignorada linha "+str(linha)+' '+str(row))
	                        LOG.append(mesg)
	                        
	             
	            #print(ICAO,TIPO,NOME,MUNICIPIO,UF,LATD,LONGT)
	            #input('novo')
	
	cols =['ICAO','TIPO','NOME','MUNICIPIO','UF','LATD','LONGT','DIST','APROXIMCAO','SUPERFICIE','COMPRIMENTO','LARGURA','ORIENTACAO']
	
	df = pd.DataFrame(list(zip(ICAO,TIPO,NOME,MUNICIPIO,UF,LATD,LONGT,DIST,APROXIMCAO,SUPERFICIE,COMPRIMENTO,LARGURA,ORIENTACAO)), columns =cols )
	
	
	print (df)
	
	
	
	
	df_filtered=df[df['DIST'] <Delta]
	
	print (df_filtered)
	df_filtered.to_csv ('OUTPUT_Aerodromos_Consolidado.csv', index = None, header=True)
	print('             ......                             ....                                         ')
	print ('Arquivo CSV Salvo. Ele pode ser lido no QGIS, por exemplo')
	print ('Ha um arquivo de log para os erros na mesma pasta dos arquivos')
	            
	print('             ......                             ....                                         ')
	with open("log.txt", 'w') as output:
	    for row in LOG:
	        output.write(str(row) + '\n')
	
	input('Pressione qualquer tecla para finalizar')
	exit()



