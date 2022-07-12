try:
    import os
    import time
    from datetime import datetime
    import shutil
    from shutil import make_archive
    import backend as be
    import multiplat as mp
except:
    print("Biblioteca necessária não disponível.\n\nEstamos finalizando.")
    quit()

try:
    import requests
except:
    mp.install_lib('requests')
    mp.restart_program()

#Função responsável por baixar a string do servidor
def downloadString(url, token):
    pload = { 'Authorization' : 'token ' + token }
    resp = requests.get(url, headers = pload ).text
    return resp


def download_allRepos(eh_organizacao, repositorio, token, eh_progressivo):
    if(eh_organizacao):
        tipo = "orgs"
    else:
        tipo = "users"
    page = 1
    while True:
        reposCont = 0
        url = f"https://api.github.com/{tipo}/{repositorio}/repos?per_page=100&page={page}"
        print("Obtendo lista de repositórios", end="")
        resposta = downloadString(url, token)
        if(resposta):
            print(" - OK")
            repos_list = []
            filedir = 'down'
            if eh_progressivo:
                filedir = filedir + '/' + repositorio
            mp.mkdir(filedir)
            while True:
                #Obter nome do repositório
                find_text = "\"name\":\""
                desloc = resposta.find(find_text)
                if(desloc == -1):
                    break
                resposta = resposta[desloc+len(find_text):]
                nome = resposta[0:resposta.find("\"")]
                #Obter Clone URL
                find_text = "\"clone_url\":\""
                desloc = resposta.find(find_text)
                if(desloc == -1):
                    break
                resposta = resposta[desloc+len(find_text):]
                cloneurl = resposta[0:resposta.find("\"")]
                print("\n ",nome," (", cloneurl, ")")
                if eh_progressivo and os.path.isdir(f"{filedir}/{nome}"):
                    os.system(f"cd {filedir}/{nome} & git pull")
                else:
                    os.system("git clone "+cloneurl.replace("ps://","ps://"+token+"@")+" "+mp.dirConvert(f"{filedir}/{nome}"))
                repos_list.append(nome)
                reposCont += 1
        else:
            print(" - FALHA")
        if(reposCont < 100):
            break #Aqui, se há 100, significa que há uma página seguinte.
        else:
            page += 1
    return repos_list

def compact(list_diretorios, prefixo, arqUnico, notRemove):
    if(arqUnico):
        arqNome = prefixo
        mp.delfile(arqNome+".zip")
    else:
        arqNome = prefixo + datetime.today().strftime('%Y%m%d%H%M%S')
    make_archive(arqNome, 'zip', 'down')
    print("Aguardando exclusão dos arquivos compactados.")
    if not notRemove:
        ok = False
        for i in range(30):#tenta excluir por 60 segundos
            print(".", end="")
            mp.rmdir("down")
            if( not os.path.isdir('down')):
                ok = True
                break
            time.sleep(2)
        return ok
    return True


if (__name__ == "__main__"):
    be.registra_log_geral("Lendo arquivo de configuração")
    arquivo = open("config", "rt")
    for linha in arquivo:
        linha = linha.replace("\n","").split(sep=";")
        if len(linha) > 3:
            progressive = len(linha) > 3 and linha[3] == 'Progressive'
            onefile = linha[3] == 'OneFile' or progressive
        be.registra_log_geral(f"Iniciando Download de repositórios: {linha[1]}")
        print(f"Iniciando Download de repositórios: {linha[1]}")
        rep_list = download_allRepos(linha[0] == 'org', linha[1], linha[2], progressive)
        if(rep_list):
            be.registra_log_geral("Compactando dados baixados. Isso pode demorar vários minutos.")
            print("Compactando dados baixados.")
            if( not compact(rep_list, f"Github_{linha[1]}_BACK", onefile, progressive)):
                print("Falha ao compactar dados do repositório atual. Operação abortada.")
                be.registra_log_geral("Falha ao compactar dados do repositório atual. Operação abortada.")
                break
    be.registra_log_geral("Fim do programa.")
    print("FIM DO PROGRAMA!")
    #input()
