# Let's Snack - IA

Este projeto utiliza um modelo de Machine Learning para prever se um usuário se alinha ao perfil do público-alvo do aplicativo **Let's Snack**, identificando potenciais usuários.

## Funcionalidades

- Classificar usuários potenciais com base em Peso e Altura.
- Armazenar as classificações em um banco de dados PostgreSQL.

## Classificações

### Tabela de Obesidade

Abaixo estão as categorias de obesidade e os scores associados:

| Tipo                | Score |
| ------------------- | ----- |
| Insufficient Weight | 2     |
| Normal Weight       | 3     |
| Overweight Level I  | 1     |
| Overweight Level II | -1    |
| Obesity Type I      | -2    |
| Obesity Type II     | -3    |
| Obesity Type III    | -4    |

### Tabela de Clusters de Hábitos

Os clusters e scores para o perfil de hábitos estão listados abaixo:

| Cluster | Descrição              | Score |
| ------- | ---------------------- | ----- |
| 1       | Muito Saudável         | 4     |
| 4       | Moderadamente Saudável | 1     |
| 2       | Mediano                | 0     |
| 3       | Pouco Saudável         | -4    |
| 0       | Muito Pouco Saudável   | -4    |

## Rotas

### Classificação de Usuário

**URL**: `http://ec2-54-175-111-241.compute-1.amazonaws.com:8080/getResponse/`

**Método**: `POST`

**Descrição**: Classifica o usuário como potencialmente interessado (`True`) ou não (`False`).

**Campos Obrigatórios (Body)**:A requisição deve incluir os seguintes campos:

```json
{
  "email": "string", // Email do usuário.
  "weight": "float", // Peso em quilogramas.
  "height": "float", // Altura em metros.
  "exercise": "int", // Frequência de atividades físicas nos últimos 7 dias (1 a 40).
  "self": "int", // Autoavaliação da saúde física (1 a 5, onde 1 é Excelente e 5 é Ruim).
  "fast_food": "int", // Frequência de fast food nos últimos 7 dias (1 a 30).
  "soda": "int" // Tipo de refrigerante (0: Não consome, 1: Diet, 2: Normal, 3: Ambos).
}
```

**Exemplo de Retorno**:

```json
{
  "is_possible_user": true,
  "score": 3 // Quando o score for maior ou igual a 0, o 'is_possible_user' é TRUE
}
```

## Dependências

### Python

- **Versão**: Python 3.12 ou superior
- **Bibliotecas**:
  - flask
  - psycopg2
  - pickle
  - pandas
  - os
  - python-dotenv (versão 1.0.0)

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```

### Banco de Dados

- **Sistema Gerenciador**: PostgreSQL
- **Script de Criação**: Para criar o banco de dados, execute o arquivo `DDL2.sql` no seu SGBD.

Observação: Scripts SQL estão disponíveis neste repositório: [GitHub - Let's Snack RPAs](https://github.com/Let-s-Snack/RPAs/blob/main/README.md)

### Outras Ferramentas

- Git
- EC2 AWS

## Autores

- [Enzo Hino](https://www.github.com/EnzoHino)
- [Arthur Micarelli](https://github.com/ArthurMicarelli)
