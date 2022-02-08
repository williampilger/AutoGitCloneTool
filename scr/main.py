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


def download_allRepos(eh_organizacao, repositorio, token):
    if(eh_organizacao):
        tipo = "orgs"
    else:
        tipo = "users"
    url = "https://api.github.com/" + tipo + "/" + repositorio + "/repos"
    print("Obtendo lista de repositórios", end="")
    resposta = downloadString(url, token)
    if(resposta):
        print(" - OK")
        repos_list = []
        mp.mkdir('down')
        while True:
            #Obter nome do repositório
            find_text = "\"name\":\""
            desloc = resposta.find(find_text)
            if(desloc == -1):
                break
            resposta = resposta[desloc+len(find_text):]
            nome = resposta[0:resposta.find("\"")]
            repos_list.append(nome)
            #Obter Clone URL
            find_text = "\"clone_url\":\""
            desloc = resposta.find(find_text)
            if(desloc == -1):
                break
            resposta = resposta[desloc+len(find_text):]
            cloneurl = resposta[0:resposta.find("\"")]
            print("\n ",nome," (", cloneurl, ")")
            os.system("git clone "+cloneurl.replace("ps://","ps://"+token+"@")+" "+mp.dirConvert("down/"+nome))
        return repos_list
    else:
        print(" - FALHA")

def compact(list_diretorios, prefixo, arqUnico):
    if(arqUnico):
        arqNome = prefixo
        mp.delfile(arqNome+".zip")
    else:
        arqNome = prefixo + datetime.today().strftime('%Y%m%d%H%M%S')
    make_archive(arqNome, 'zip', 'down')
    print("Aguardando exclusão dos arquivos compactados.")
    ok = False
    for i in range(10):
        print(".", end="")
        mp.rmdir("down")
        if( not os.path.isdir('down')):
            ok = True
            break
        time.sleep(2000)
    return ok


if (__name__ == "__main__"):
    #print("CONSULTE https://developer.github.com/changes/2020-02-10-deprecating-auth-through-query-param/")
    #input()#A função atualmente não funciona mais. é possível obter apenas os repositórios públicos.
    #sair(1)
    be.registra_log_geral("Lendo arquivo de configuração")
    arquivo = open("config", "rt")
    for linha in arquivo:
        linha = linha.replace("\n","").split(sep=";")
        be.registra_log_geral(f"Iniciando Download de repositórios: {linha[1]}")
        print(f"Iniciando Download de repositórios: {linha[1]}")
        rep_list = download_allRepos(linha[0] == 'org', linha[1], linha[2])
        if(rep_list):
            be.registra_log_geral("Compactando dados baixados. Isso pode demorar vários minutos.")
            print("Compactando dados baixados.")
            if( not compact(rep_list, f"Github_{linha[1]}_BACK", False)):
                print("Falha ao compactar dados do repositório atual. Operação abortada.")
                be.registra_log_geral("Falha ao compactar dados do repositório atual. Operação abortada.")
                break;
    be.registra_log_geral("Fim do programa.")
    print("FIM DO PROGRAMA!")
    #input()
