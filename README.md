# Let's Snack - IA

O objetivo é consumir um modelo de Machine Learning para prever se um usuário é um potencial usuário do aplicativo, ou seja, se ele se alinha ao perfil do público-alvo.

## Funcionalidades

- Classificar possíveis usuários pelo: Peso e Altura;
- Guardar as classificações em um banco de dados;

## Rotas

### EndPoint: http://ec2-54-175-111-241.compute-1.amazonaws.com:8080/getResponse/

- **Método**: `POST`
- **Função**: Classificar o usuário como um possível usuário: `True` ou `False`.
- **Retorno:** { "response": bool }.
- **Campos Obrigatórios** (Body):

```json
{
  "email": "string", // Email do usuário.
  "weight": "float", // Peso do usuário em quilogramas.
  "height": "float", // Altura do usuário em metros.
  "exercise": "int", // Frequência de atividades físicas nos últimos 7 dias (1 a 40).
  "self": "int", // Autoavaliação da saúde física (1 a 5, onde 1 é Excelente e 5 é Ruim).
  "fast_food": "int", // Frequência de compras de fast food nos últimos 7 dias (1 a 30).
  "soda": "int" // Tipo de refrigerante consumido (0 para "Não consome", 1 para "Diet", 2 para "Normal", 3 para "Ambos").
}
```

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
- EC2 AWS

## Autores

- [@EnzoHino](https://www.github.com/EnzoHino)
- [@ArthurMicarelli](https://github.com/ArthurMicarelli)
