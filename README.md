# KenzieHouse (KH)
Este projeto é uma Api E-commerce de móveis, criada com o intuito de facilitar a compra de móveis na internet.

### 📋 Pré-requisitos

Para iniciar o projeto na sua máquina, é necessário que sua máquina tenha instalado python3+ e o git.

Começe clonando o repositório usando git clone:
 ```
 git clone 'link_do_clone'
 ```

### 🔧 Instalação

Começe criando um ambiente virtual:

```
python -m venv venv
```

Após isso entre no ambiente virtual e instale o requirements.txt:

```
source venv/bin/activate
pip install -r requirements.txt
```

Também é preciso criar um `.env` com as informações do banco de dados e outras informações necessárias conforme o `.env.example`

## ⚙️ Executando os testes

Para rodar os testes na sua máquina, basta executar o seguinte comando no seu terminal:
```
pytest tests/nome_do_arquivo_de_teste
```
obs: alguns testes foram feitos para rotas que estão protegidas, e para de eles funcionem será necessário comentar os decorators das funções no controller da rota.


## 📦 Desenvolvimento
Esta api foi hospedada em https://capstone-q3-heroku.herokuapp.com na plataforma [Heroku](https://www.heroku.com/home) em uma conta gratuita.
 
É possivel ver os endpoints da api na documentação [KenzieHouse](https://capstone-q3-insomnia-documentation.vercel.app/)

## 🛠️ Construído com

* [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Micro framework que utiliza a linguagem Python para criar aplicativos Web. 
* [JWT](https://jwt.io/introduction) - Usado para autenticação das rotas.
* [SQLAlchemy](https://www.sqlalchemy.org/) - Usado para criação do banco de dados.
## ✒️ Autores

* **Fernando Schneider** - *Tech Leader* - [Fernando Schneider](https://gitlab.com/FernandoSchneider)
* **Renato Moresche** - *Scrum Master* - [Renato Moresche](https://gitlab.com/moresche)
* **Calebe Navarro** - *Product Owner* - [Calebe Navarro](https://gitlab.com/CalebeNavarro)
* **Gustavo Silva** - *Dev* - [Gustavo Silva](https://gitlab.com/GustavoSil)
* **Wander Moreira** - *Dev* - [Wander Moreira](https://gitlab.com/trevius)

