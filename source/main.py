from init_db import initialize_db
from bank import Account, Transaction

def main():
    ''' Initialisation de la BDD avec la création d'une session '''
    engine, Session = initialize_db()
    
    with Session() as session:

        # Création de comptes
        def create_account(account_id):
            # Verifier si le compte n'est pas déjà créé
            account = session.query(Account).filter_by(account_id=account_id).first()
            if not account:
                account = Account(account_id=account_id)
                session.add(account)
                session.commit()
            return account
        
        create_account(1)
        create_account(2)

        # Création de transactions
        transaction = Transaction()
        first_deposit = transaction.deposit(session, 1, 100) # dépôt de 100$
        second_deposit = transaction.deposit(session, 2, 50) # retrait de 50$
        transfer = transaction.transfer(session, 1, 2, 50) # transfer de 50$ du compte 1 au compte 2
        # Ajout de plusieurs transactions
        session.add_all([first_deposit, second_deposit, transfer])
        # Validation
        session.commit()
        
        session.close()
        engine.dispose()
    
if __name__ == "__main__":
    main()
