#!/usr/bin/env python3

###################################################################################
# Desenvolvido por Daniel Pereira
# Versão: 1.2
###################################################################################

from bs4 import BeautifulSoup
import requests
import json
import re

URL = "https://status.ix.br"


def request(url):
    return requests.get(url)


def parse_result(html):
    bs = BeautifulSoup(html, 'html.parser')
    ixlist = bs.find_all('ul', {'class': 'list-group components'})

    data = []
    for ix in ixlist:
        name = ix.find('strong').text.strip()
        items = ix.find('div', {'class': 'group-items'}).find_all('li', {'class': 'list-group-item'})
        for item in items:
            status_div = item.find('div', {'class': 'pull-right'})
            status = status_div.text.strip()
            status_div.decompose()
            item_name = item.text.strip()
            if name == 'IX-br - Outras Localidades':
                ix_grupo = re.sub('.*- ', '', name)
                ix_nome = re.sub('IX.br ', '', item_name)
                ix_localizacao = ix_nome
            else:
                ix_grupo = re.sub('IX.br ', '', name)
                ix_nome = re.sub(' -.*', '', item_name)
                ix_localizacao = re.sub('.*- IX.br ', '', item_name)

            ix_data = {"IX_GRUPO": ix_grupo, "IX_LOCALIZACAO": ix_localizacao, "IX_NOME": ix_nome, "IX_STATUS": status}
            data.append(ix_data)

    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    response = request(URL)
    parse_result(response.text)
