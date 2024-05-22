from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from bank import Base 

''' Fonction pour initialiser la base de données '''
def initialize_db(debug=False):
    # Crée un moteur de base de données SQLite avec un fichier nommé "bank.db"
    # Le paramètre `echo=debug` permet de contrôler l'affichage des requêtes SQL dans le terminal pour le débogage (ex: ALTER TABLE, INSERT INTO, etc.)
    engine = create_engine("sqlite:///bank.db", echo=debug)
    
    # Crée toutes les tables définies dans les classes héritant de Base
    # La méthode `create_all` vérifie toujours si les tables existent déjà avant de les créer
    Base.metadata.create_all(engine)  
    
    # Retourne l'objet engine (moteur de la BDD) et une fabrique de sessions
    # La fabrique de sessions (sessionmaker) lie les sessions à l'objet engine
    # La session est un élément clé dans SQLAlchemy qui gère toutes les opérations pour les objets de votre application.
    # Elle assure la coordination/relation entre l'application et la base de données. 
    return engine, sessionmaker(bind=engine)