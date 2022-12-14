import pandas as pd

def replace_mails(user, type_vacancy):
  name= f'{user}_{type_vacancy}.cvs'
    #Lendo dataframe (df)
  df = pd.read_csv('emails.csv',encoding='utf-8', delimiter=',')
    # Ordenando na ordem crescente e excluindo os repetidos e as outras colunas
  df = df.sort_values('Email', ascending=True)
  df = df.drop_duplicates(subset='Email', keep='first')
  df = df['Email']
  df_= dict(df)

    # Criando outro dataframe com os dados tratados
  df_second = pd.DataFrame(df)
  df_second.to_csv(name)
  df_second = pd.read_csv(name,encoding='utf-8', delimiter=',')
  print('Converted!')