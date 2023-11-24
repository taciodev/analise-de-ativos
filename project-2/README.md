# Análise de Ações

Este é um breve guia sobre como configurar o ambiente para o projeto.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados em sua máquina:

- Python (versão 3.12.0 ou superior): [Download Python](https://www.python.org/downloads/)

## Clonar o Repositório

Clone este repositório em sua máquina local:

```bash
git clone https://github.com/taciodev/analise-de-ativos.git
```

## Configurar Ambiente Virtual

```bash
python -m venv venv
```

Ative o ambiente virtual:

- No Windows:

```bash
.\venv\Scripts\activate
```

- No Linux/Mac:

```bash
source venv/bin/activate
```

Instale o pip-tools:

```bash
pip install pip-tools
```

## Configurar Dependências

Adicione ou remova dependências conforme necessário no arquivo `requirements.in`.

Atualizar o `requirements.txt`:

- Sempre que você adicionar ou remover dependências, execute o seguinte comando para atualizar o `requirements.txt`.

```bash
pip-compile requirements.in
```

## Instalar Dependências

```bash
./install_dependencies.sh
```

Certifique-se de que o script tem permissões de execução. Se não tiver, você pode conceder permissões de execução usando o comando:

```bash
chmod +x install_dependencies.sh
```

## Executar o Projeto

```bash
python main.py
```

## Desativar Ambiente Virtual

```bash
deactivate
```
