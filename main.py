import requests
import re #regex
import csv
import data_mail

def get_issues(username, repo):
    """ nome de usuário e repo devem ser strings
    auth deve ser uma tupla de nome de usuário e senha.
    eventualmente, vamos trocá-lo para usar um token oauth"""

    tmpl = "https://api.github.com/repos/{username}/{repo}/issues?per_page=100"
    url = tmpl.format(username=username, repo=repo)
    return _getter(url)

def _getter(url):
    """  Pagination utility.  Obnoxious. """

    link = dict(next=url)
    while 'next' in link:
        response = requests.get(link['next'])

        # E .. se não obtivermos bons resultados, basta sair.
        if response.status_code != 200:
            raise IOError(
                "Non-200 status code %r; %r; %r" % (
                    response.status_code, url, response.json()))

        for result in response.json():
            yield result

        link = _link_field_to_dict(response.headers.get('link', None))


def _link_field_to_dict(field):
    """ Utilitário para separar o campo de cabeçalho Link do github.
    É meio feio."""

    if not field:
        return dict()

    return dict([
        (
            part.split('; ')[1][5:-1],
            part.split('; ')[0][1:-1],
        ) for part in field.split(', ')
    ])


def create_csv(user, repository, type_vacancy):
  with open('emails.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Título', 'Tags'])
        for count, issue in enumerate(get_issues(user, repository)):
            print(str(count) + ': ', end='')
            for label in issue['labels']:
                if(type_vacancy == label['name']):
                    text = issue['body']
                    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
                    if (match):
                        email = match[0]
                        title = (issue['title'])
                        tags = ''
                        for i, tag in enumerate(issue['labels']):
                            if(i != 0):
                                tags += ', '
                            tags += tag['name']
                        print('Título: ' + title + '\n e-mail: ' + email)
                        writer.writerow([email, title, tags])
                    break

def getLink():
  # coleta a fonte
  user = input('Qual o usuario? (ex: frontendbr, backend-br) \n')
  repository = input('Repositório: (ex: vagas) \n')
  type_vacancy = input('Qual o tipo da Vaga? (ex: Remoto) \n')

  #passa os dados como parametro
  create_csv(user, repository, type_vacancy)
  
  #faz um replace no emails
  data_mail.replace_mails(user, type_vacancy)

getLink()
