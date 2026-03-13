# Sistema de Gestão de Frota (ORM SQLAlchemy)
Este projeto implementa uma camada de ORM (Object-Relational Mapping) em Python para gerenciar uma frota de veículos, motoristas, viagens e manutenções. O projeto utiliza o SQLAlchemy para mapear tabelas do PostgreSQL em classes Python, realizando operações CRUD e consultas complexas com relacionamentos.

# 🚀 Como Executar (Passo a Passo)
1. Pré-requisitos
Python 3.8+ instalado.

PostgreSQL instalado e em execução.

Um banco de dados criado (ex: gestao_frota).

2. Clonar ou Criar o Diretório
Crie uma pasta para o projeto e salve o arquivo principal (ex: main.py).

3. Criar Ambiente Virtual (Recomendado)
No terminal, dentro da pasta do projeto:

Bash
python -m venv venv
# No Windows:
venv\Scripts\activate

4. Instalar Dependências
Instale o SQLAlchemy e o driver do PostgreSQL:

```Bash
pip install sqlalchemy psycopg2
```

⚙️ Configuração do Banco de Dados
Em vez de deixar senhas expostas, o projeto utiliza uma string de conexão. Você deve configurar as variáveis de ambiente ou editar a linha de conexão no código:

Variáveis de Conexão
No arquivo main.py, localize a variável DATABASE_URL e substitua pelos seus dados:

Python
# Estrutura: postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
DATABASE_URL = "postgresql://postgres:suasenha@localhost:5432/gestao_frota"
Nota: O script está configurado com Base.metadata.create_all(engine), o que significa que as tabelas serão criadas automaticamente na primeira execução caso ainda não existam no seu banco de dados.

💻 Comandos de Execução
Para rodar o projeto e executar as operações de CRUD e Consultas:

```Bash
python main.py
```

📊 Exemplos de Uso (Saída do Console)
Ao executar o script, você verá uma saída similar a esta no seu terminal, demonstrando as fases do projeto:

1. Operações CRUD (Create, Read, Update, Delete)
Plaintext
--- Iniciando Operações CRUD ---
CREATE: 3 Motoristas inseridos.
READ: Motoristas cadastrados (Ordenados por nome):
 - Ana Paula (CNH: D)
 - Carlos Alberto (CNH: E)
 - Roberto Souza (CNH: B)
UPDATE: Experiência de Carlos Alberto atualizada.
DELETE: Registro removido com sucesso.

2. Consultas Avançadas (Relacionamentos e Joins)
Plaintext
--- Iniciando Consultas Avançadas ---

1. Viagens e Motoristas (Relacionamento Join):
Origem: São Paulo -> Destino: Rio de Janeiro | Motorista: Carlos Alberto

2. Custo Total de Manutenção por Veículo (Agregação):
Veículo: ABC-1234 | Gasto Total: R$ 1500.00
Veículo: XYZ-9876 | Gasto Total: R$ 450.00

3. Top 5 Veículos com mais KM (Filtro + Ordenação):
Placa: BRA2E19 | KM: 15400.50
Placa: ABC-1234 | KM: 1200.00
🛠️ Tecnologias Utilizadas
Linguagem: Python

ORM: SQLAlchemy

Banco de Dados: PostgreSQL

Driver: Psycopg2
