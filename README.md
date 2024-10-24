# Let's Snack - IA

O objetivo é consumir um modelo de Machine Learning para prever se um usuário é um potencial usuário do aplicativo, ou seja, se ele se alinha ao perfil do público-alvo.

## Funcionalidades

- Classificar possíveis usuários pelo: Peso e Altura;
- Guardar as classificações em um banco de dados;

## Rotas

Segue a documentação das rotas do projeto:

### Rota: /getResponse/

- Método: POST;
- Função: Classificar o usuário como: True ou False;
- Campos Obrigatórios (body): email, weight e height;
- Retorno: { "response": true }.

## Dependências

Para executar este projeto, você precisará instalar as seguintes bibliotecas e ferramentas:

### Python

- Python 3.12 ou superior
- flask
- psycopg2
- pickle
- pandas
- os
- python-dotenv 1.0.0

Você pode instalar as dependências Python com o seguinte comando:

```bash
pip install -r requirements.txt
```

### Banco de Dados

PostgreSQL

#### Criar banco de dados

Para criar os bancos de dados, execute os arquivo DDL2.sql no seu SGBD.
Observação: Scripts SQL estão nesse repositório: https://github.com/Let-s-Snack/RPAs/blob/main/README.md

### Outras Ferramentas

- Git
- Render

## Autores

- [@EnzoHino](https://www.github.com/EnzoHino)
- [@ArthurMicarelli](https://github.com/ArthurMicarelli)
