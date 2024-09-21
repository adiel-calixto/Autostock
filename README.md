
![Logo](https://github.com/adiel-calixto/Autostock/blob/main/assets/logo_horizontal_i.png?raw=true)


# Autostock

Sistema de auto-atendimento e controle de estoque para pequenos negócios


## Instalação

**Requisito**: Python 3.12

**Instale o Pipenv**: Primeiro, você precisa ter o `pipenv` instalado. Caso não tenha, instale-o com o seguinte comando:

```bash  
  pip install pipenv
```

**Instale as dependências**: No diretório do projeto, execute:

```bash  
  pipenv install
```

**Ative o Ambiente Virtual**: Para ativar o ambiente virtual, use:

```bash  
  pipenv shell
```

**Inicie o banco de dados**: Para criar o banco de dados, execute:

```bash  
  alembic upgrade head
```

**Executar o Projeto**:

```bash  
  python main.py
```
## Bibliotecas usadas

- CustomTkinter - Interface gráfica
- SqlAlchemy - ORM
- Alembic - Versionamento da estrutura do banco de dados

## Autores

- [@adiel-calixto](https://www.github.com/adiel-calixto)
- [@JhonatanLobo](https://www.github.com/JhonatanLobo)
