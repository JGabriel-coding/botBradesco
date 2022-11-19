from playwright.sync_api import sync_playwright, Playwright,expect
import time,requests,os,urllib.request,re
from bs4 import BeautifulSoup
import pandas as pd
import csv


#Bot boleto Bradesco
def run(playwright:Playwright)-> None:
    
    with open('login.csv', encoding='utf-8') as arquivo_referencia:

    # 2. ler a tabela
        tabela = csv.reader(arquivo_referencia, delimiter=';')
        cnpj = []
        
    # 3. navegar pela tabela
        for l in tabela:
            cnpj.append(l[0:2])
        #senha.append(l[1])
   
    for login,senha in cnpj:
        print(login,senha)
    #Abrindo a pagina
        navegador = playwright.chromium.launch(headless=False)
        contexto = navegador.new_context()
        pagina=contexto.new_page()
        #logando na pagina
        pagina.goto("https://wwws.bradescosaude.com.br/PCBS-LoginSaude/td/inicioLoginEmpresaSaude.do")
        time.sleep(10)#esperando a pagina carregar
        pagina.fill("#ceicnpjcaepf", login)#user
        pagina.fill('#senha', senha)#Senha de Login
        time.sleep(5)
        pagina.get_by_role("button", name="Acessar").click()#Da o Click de Botão
        #Fecha os popups de propaganda
        pagina.locator('//*[@id="modal_reembolso_estipulante"]/div/div/img').click() 
        pagina.locator('//*[@id="modal_pos_covid"]/div/div/img').click()
        pagina.locator('//*[@id="modal_logada_estipulante"]/div/div/img').click()
        pagina.locator('//*[@id="modal_coronavirus"]/div/div/img').click()
        pagina.locator('//*[@id="modal_SaudeDigital_1ano"]/div/div/img').click()
        pagina.locator('//*[@id="fraude_boletos"]/div/div/img[2]').click()
        #pagina de apolices
        pagina.get_by_role("link", name="Impressão do Carnê de Pagamento").click()
        #pega a posição do ifram e abre o novo html
        url = pagina.url
        url_get = requests.get(url)
        soup = BeautifulSoup(url_get.content, 'html.parser')
        soup1 = soup.find('iframe', {"id":"fatura_acesso"})
        link = soup1.get('src')
        #with pagina.expect_navigation():   
        pagina.goto(link)
        time.sleep(5)
        apolice = pagina.locator('#apolices').all_text_contents()
        #apolice = pagina.locator('//*[@id="913832"]').all_text_contents()
        print(len(apolice))# seleciona o numero da apolice
        for i in range(len(apolice)):#seleciona a apolice correta.
            n = (apolice[i].strip())#//1000000
            print(n)
            print(len(n))
            #lista_n = []
            var = n[0:6]
            print(var)  
        #Click na apolice correta.      
        pagina.get_by_role("row", name="Selecione uma apólice. {}".format(var)).get_by_role("radio", name="Selecione uma apólice.").check()
        pagina.get_by_role("button", name="Confirmar").click()
        time.sleep(2)
        #donwload da apolice.
        with pagina.expect_download() as download_info:
            nameDown = str(pagina.locator('//*[@id="1"]/td[12]/a').all_text_contents())
            pagina.locator('//*[@id="1"]/td[12]/a').click()
            download = download_info.value
            teste_pdf = download.suggested_filename
            download.save_as(os.path.join( teste_pdf))     
        #time.sleep(5)
        contexto.close()
        navegador.close()



with sync_playwright() as playwright:
    run(playwright) 


#autentique('cliente.csv',",")









