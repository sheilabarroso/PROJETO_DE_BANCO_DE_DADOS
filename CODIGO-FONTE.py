import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, Date, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date

# ==========================================================
# PARTE 1 — A PONTE (Configuração e Conexão)
# ==========================================================
# Substitua os dados abaixo pelas credenciais do seu PostgreSQL
USER = 'postgres'
PASSWORD = 'sua_senha'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'gestao_frota'

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# ==========================================================
# PARTE 2 — O ESPELHO (Mapeamento ORM)
# ==========================================================

class Veiculo(Base):
    __tablename__ = 'VEÍCULO'
    
    pk_id_veicular = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String(10), unique=True, nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    tipo_veicular = Column(String(20), nullable=False)
    ano = Column(Integer, nullable=False)
    quilometragem = Column(Numeric(12, 2), default=0)
    status = Column(String(20), default='ATIVO')
    consumo_medio = Column(Numeric(5, 2))

    # Regras de integridade espelhadas do SQL
    __table_args__ = (
        CheckConstraint("tipo_veicular IN ('Carro', 'Moto', 'Caminhão')"),
        CheckConstraint("status IN ('ATIVO', 'MANUTENCAO', 'INATIVO')"),
        CheckConstraint("quilometragem >= 0"),
    )

    # Relacionamento 1-N: Um veículo tem várias manutenções
    manutencoes = relationship("Manutencao", back_populates="veiculo", cascade="all, delete-orphan")

class Motorista(Base):
    __tablename__ = 'MOTORISTA'
    
    pk_id_motorista = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    categoria_cnh = Column(String(2), nullable=False)
    tempo_experiencia = Column(Integer, default=0)
    disponivel = Column(Boolean, default=True)

    # Relacionamento 1-N: Um motorista tem várias viagens
    viagens = relationship("Viagem", back_populates="motorista")

class Manutencao(Base):
    __tablename__ = 'MANUTENÇÃO'
    
    pk_id_manutencao = Column(Integer, primary_key=True, autoincrement=True)
    fk_id_veicular = Column(Integer, ForeignKey('VEÍCULO.pk_id_veicular', ondelete='CASCADE'), nullable=False)
    data_manutencao = Column(Date, nullable=False)
    tipo_manutencao = Column(String(20), nullable=False)
    custo = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String)

    veiculo = relationship("Veiculo", back_populates="manutencoes")

class Viagem(Base):
    __tablename__ = 'VIAGEM'
    
    pk_id_viagem = Column(Integer, primary_key=True, autoincrement=True)
    fk_id_veicular = Column(Integer, ForeignKey('VEÍCULO.pk_id_veicular'), nullable=False)
    fk_id_motorista = Column(Integer, ForeignKey('MOTORISTA.pk_id_motorista'), nullable=False)
    data_viagem = Column(Date, nullable=False)
    origem = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    distancia_percorrida = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos N-1 (Many-to-One)
    veiculo = relationship("Veiculo")
    motorista = relationship("Motorista", back_populates="viagens")

# Criar as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(engine)

# ==========================================================
# PARTE 3 — OPERAÇÕES CRUD (Create, Read, Update, Delete)
# ==========================================================

def executar_crud():
    print("\n--- Iniciando Operações CRUD ---")
    
    # 1. CREATE: Inserir 3 registros
    m1 = Motorista(cpf='111.111.111-11', nome='Carlos Alberto', categoria_cnh='E')
    m2 = Motorista(cpf='222.222.222-22', nome='Ana Paula', categoria_cnh='D')
    m3 = Motorista(cpf='333.333.333-33', nome='Roberto Souza', categoria_cnh='B')
    session.add_all([m1, m2, m3])
    session.commit()
    print("CREATE: 3 Motoristas inseridos.")

    # 2. READ: Listagem com Ordenação
    motoristas = session.query(Motorista).order_by(Motorista.nome).all()
    print("READ: Motoristas cadastrados (Ordenados por nome):")
    for m in motoristas:
        print(f" - {m.nome} (CNH: {m.categoria_cnh})")

    # 3. UPDATE: Atualizar 1 registro
    motorista_update = session.query(Motorista).filter_by(cpf='111.111.111-11').first()
    if motorista_update:
        motorista_update.tempo_experiencia = 10
        session.commit()
        print(f"UPDATE: Experiência de {motorista_update.nome} atualizada.")

    # 4. DELETE: Remover 1 registro
    motorista_del = session.query(Motorista).filter_by(cpf='333.333.333-33').first()
    if motorista_del:
        session.delete(motorista_del)
        session.commit()
        print("DELETE: Registro removido com sucesso.")

# ==========================================================
# PARTE 4 — CONSULTAS COM RELACIONAMENTO
# ==========================================================

def executar_consultas_avancadas():
    print("\n--- Iniciando Consultas Avançadas ---")

    # Consulta 1: Relacionamento (Join) - Listar Viagens e seus Motoristas
    print("\n1. Viagens e Motoristas (Relacionamento):")
    viagens = session.query(Viagem).join(Motorista).all()
    for v in viagens:
        print(f"Origem: {v.origem} -> Destino: {v.destino} | Motorista: {v.motorista.nome}")

    # Consulta 2: Agregação por Relacionamento - Soma de Manutenções por Veículo
    print("\n2. Custo Total de Manutenção por Veículo (Agregação):")
    custos = session.query(
        Veiculo.placa, 
        func.sum(Manutencao.custo).label('total')
    ).join(Manutencao).group_by(Veiculo.placa).all()
    for placa, total in custos:
        print(f"Veículo: {placa} | Gasto Total: R$ {total}")

    # Consulta 3: Filtro + Ordenação - Veículos com alta quilometragem
    print("\n3. Top 5 Veículos com mais KM (Filtro + Ordenação):")
    veiculos = session.query(Veiculo).filter(Veiculo.quilometragem > 0).order_by(Veiculo.quilometragem.desc()).limit(5).all()
    for v in veiculos:
        print(f"Placa: {v.placa} | KM: {v.quilometragem}")

# Execução do Script
if __name__ == "__main__":
    try:
        executar_crud()
        executar_consultas_avancadas()
    except Exception as e:
        print(f"Erro na execução: {e}")
        session.rollback()
    finally:
        session.close()
