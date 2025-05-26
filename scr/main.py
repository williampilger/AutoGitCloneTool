try:
    import os
    import time
    from datetime import datetime
    from shutil import make_archive
    import backend as be
    import multiplat as mp
    import subprocess
except:
    print("Biblioteca necessária não disponível.\n\nEstamos finalizando.")
    quit()

try:
    import requests
except:
    mp.install_lib('requests')
    mp.restart_program()

def runOsCommand(cmd):
    print(f"{os.getcwd()}:$ {cmd}")
    os.system(cmd)

#Função responsável por baixar a string do servidor
def downloadString(url, token):
    pload = { 'Authorization' : 'token ' + token }
    resp = requests.get(url, headers = pload ).json()
    return resp

def download_allRepos(eh_organizacao, repositorio, token, eh_progressivo, inifiledir, includeStars=False):
    if(eh_organizacao):
        tipo = "orgs"
    else:
        tipo = "users"
    repos_list = []
    page = 1
    while True:
        reposCont = 0
        url = f"https://api.github.com/{tipo}/{repositorio}/repos?per_page=100&page={page}"
        print("Obtendo lista de repositórios", end="")
        repos = downloadString(url, token)
        if(repos):
            print(" - OK")
            filedir = inifiledir
            if eh_progressivo:
                filedir = mp.dirConvert(f"{filedir}/{repositorio}")
            mp.mkdir(filedir)
            for repo in repos:
                nome = repo.get("name")
                cloneurl = repo.get("clone_url")
                print("\n ", nome, " (", cloneurl, ")")
                target_dir = mp.dirConvert(f"{filedir}/{nome}")
                if eh_progressivo and os.path.isdir(target_dir):
                    subprocess.run(['git', 'pull'], cwd=target_dir) # runOsCommand(f'cd "{target_dir}" & git pull')
                else:
                    runOsCommand(f'git clone {cloneurl.replace('ps://', 'ps://'+token+'@')} "{target_dir}"')
                repos_list.append(nome)
                reposCont += 1
        else:
            print(" - FALHA")
        if(reposCont < 100):
            break #Aqui, se há 100, significa que há uma página seguinte.
        else:
            page += 1
    if includeStars and tipo == "users":
        print("Obtendo repositórios marcados como favoritos (stars)")
        page = 1
        while True:
            reposCont = 0
            url = f"https://api.github.com/users/{repositorio}/starred?per_page=100&page={page}"
            print("Obtendo lista de repositórios", end="")
            repos = downloadString(url, token)
            if(repos):
                print(" - OK")
                filedir = inifiledir
                if eh_progressivo:
                    filedir = mp.dirConvert(f"{filedir}/{repositorio}/_stared")
                mp.mkdir(filedir)
                for repo in repos:
                    owner = repo.get("owner").get("login")
                    nome = repo.get("name")
                    cloneurl = repo.get("clone_url")
                    print("\n ", nome, " (", cloneurl, ")")
                    target_dir = mp.dirConvert(f"{filedir}/{owner}/{nome}")
                    if eh_progressivo and os.path.isdir(target_dir):
                        subprocess.run(['git', 'pull'], cwd=target_dir) # runOsCommand(f'cd "{target_dir}" & git pull')
                    else:
                        runOsCommand(f'git clone {cloneurl.replace('ps://', 'ps://'+token+'@')} "{target_dir}"')
                    repos_list.append(nome)
                    reposCont += 1
            else:
                print(" - FALHA")
            if(reposCont < 100):
                break #Aqui, se há 100, significa que há uma página seguinte.
            else:
                page += 1
    return repos_list

def compact(dir, prefixo, arqUnico, notRemove):
    dir = mp.dirConvert(dir)
    if(arqUnico):
        arqNome = prefixo
        mp.delfile(arqNome+".zip")
    else:
        arqNome = prefixo + datetime.today().strftime('%Y%m%d%H%M%S')
    make_archive(arqNome, 'zip', dir)
    print("Aguardando exclusão dos arquivos compactados.")
    if not notRemove:
        ok = False
        for i in range(30):#tenta excluir por 60 segundos
            print(".", end="")
            mp.rmdir(dir)
            if( not os.path.isdir(dir)):
                ok = True
                break
            time.sleep(2)
        return ok
    return True


if (__name__ == "__main__"):
    be.registra_log_geral("Lendo arquivo de configuração")
    arquivo = open("config", "rt")
    for linha in arquivo:
        [conf_type, conf_profile, conf_hash, conf_dir, conf_mode] = linha.replace("\n","").split(sep=";")
        conf_dir = mp.replaceAmbientVars(conf_dir)

        progressive = conf_mode == 'Progressive'
        onefile = conf_mode == 'OneFile' or progressive
        dir = f'{conf_dir}'

        be.registra_log_geral(f"Iniciando Download de repositórios: {conf_profile}")
        print(f"Iniciando Download de repositórios: {conf_profile}")
        rep_list = download_allRepos(conf_type == 'org', conf_profile, conf_hash, progressive, dir, True)
        if(rep_list):
            be.registra_log_geral("Compactando dados baixados. Isso pode demorar vários minutos.")
            print("Compactando dados baixados.")
            if( not compact(f'{dir}/{conf_profile}', f"Github_{conf_profile}_BACK", onefile, progressive)):
                print("Falha ao compactar dados do repositório atual. Operação abortada.")
                be.registra_log_geral("Falha ao compactar dados do repositório atual. Operação abortada.")
                break
    be.registra_log_geral("Fim do programa.")
    print("FIM DO PROGRAMA!")

