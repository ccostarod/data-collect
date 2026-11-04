# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not:A-Brand";v="8", "Chromium";v="156", "Microsoft Edge";v="156"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0',
        # 'cookie': '_ga=GA1.1.1618501782.1793629860; __gads=ID=837cf642b30c8eb8:T=1793629860:RT=1793643031:S=ALNI_MZQwN3CZnJbZiFZE4uk7opJ6EVPLw; __gpi=UID=0000167a2b407d75:T=1793629860:RT=1793643031:S=ALNI_MZ5CV3xuRIzW2Mg0dsahZjbno9HPA; __eoi=ID=6dfa6227b483bc7d:T=1793629860:RT=1793643031:S=AA-Afjauo2ms6FYaa_Tmz-_NKL1y; _ga_DJLCSW50SC=GS2.1.s1793643029$o3$g1$t1793643031$j59$l0$h0; _ga_D6NF5QC4QT=GS2.1.s1793643029$o3$g1$t1793643031$j59$l0$h0; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%227417df01-c6f4-4c0d-8024-31570877ceb1%5C%22%2C%5B1793629860%2C104000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol93QeY6yg9PU5ipXCPx4hguXHBjsv_tKprWTx2b4xjU-N65w1tq-3sY2__OzhKfvd1fLfXyyUwLnRwGRx2NV01o64CKew%3D%3D%22%5D%5D',
    }

def get_content(url):
    response = requests.get(url, headers=headers)
    return response

def get_basic_infos(soup):
    div_page = soup.find('div', class_ = 'td-page-content') 
    paragrafo = div_page.find_all('p')[1]
    ems = paragrafo.find_all('em')
    
    data = {}
    for em in ems:
        for texto in em.stripped_strings:
            if ":" in texto:
                chave, valor = texto.split(":", 1)
                data[chave.strip()] = valor.strip()

    return data

def get_aparicoes(soup):
    lis = (soup.find('div', class_ = 'td-page-content')
            .find("h4")
            .find_next()
            .find_all("li"))
    

    aparicoes = [i.text for i in lis]
    return aparicoes

def get_personagem_infos(url):
    response = get_content(url)

    if response.status_code != 200:
        print('Nao foi possivel obter a pagina')
        print(url)
        return {}

    else:
        soup = BeautifulSoup(response.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"

    response = requests.get(url, headers=headers)

    soup_personagens = BeautifulSoup(response.text)

    ancoras = (soup_personagens.find("div", class_="td-page-content")
                                .find_all("a"))

    links = [i["href"] for i in ancoras]
    return links

# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d["Link"] = i
    d["Nome"] = i.strip("/").split("/")[-1].replace("-", " ").title()

    data.append(d)


# %%

df = pd.DataFrame(data)
df

# %%

df.to_csv("dados_re.csv", index=False, sep=";")

df.to_parquet("dados_re.parquet", index=False, )

# %%

df_new = pd.read_parquet("dados_re.parquet")
df_new
# %%
