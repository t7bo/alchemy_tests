from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from source.bank import Account, Transaction
from unittest.mock import MagicMock

''' - Effectuer un dépôt avec un montant positif.
- Vérifier que le solde du compte est correctement mis à jour.
- Vérifier que la transaction est correctement ajoutée avec le type "deposit".
- Vérifier que le timestamp de la transaction est correctement enregistré.
- Vérifier que le **`session.commit()`** a été appelé. '''

def test_normal_deposit(my_session, account_factory):
    account = account_factory(1)

    # Configurer le retour pour session.get
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)

    transaction = Transaction()
    positive_deposit = transaction.deposit(my_session, 1, 100)  # dépôt de 100$

    assert positive_deposit.amount > 0
    assert positive_deposit.transaction_type == 'deposit'
    assert my_session.query(Transaction).count() == 1
    assert positive_deposit.transaction_date is not None
    assert my_session.commit.called
    
''' - Tenter de déposer un montant négatif.
- Vérifier que le solde du compte n'a pas changé.
- Vérifier qu'aucune transaction n'est créée.
- Vérifier que le **`session.commit()`** n'a pas été appelé. '''

def test_negative_deposit(my_session, account_factory):
    account = account_factory(2)
    
    # Configurer le retour pour session.get
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    
    transaction = Transaction()
    negative_deposit = transaction.deposit(my_session, 2, -20)
    
    assert account.balance == 0
    assert negative_deposit == "Deposit failed. Please enter a valid number."
    # my_session.commit.assert_not_called()
    assert my_session.query(Transaction).count() == 0
    assert my_session.commit.called
    

''' - Tenter de déposer un montant nul.
- Vérifier que le solde reste inchangé.
- Vérifier qu'aucune transaction n'est créée.
- Vérifier que le **`session.commit()`** n'a pas été appelé. '''

def test_zero_deposit(my_session, account_factory):
    account = account_factory(3)
    
    # Configurer le retour pour session.get
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    
    transaction = Transaction()
    negative_deposit = transaction.deposit(my_session, 3, 0)
    
    assert account.balance == 0
    assert negative_deposit == "Deposit failed. Please enter a valid number."
    # my_session.commit.assert_not_called()
    assert my_session.query(Transaction).count() == 0
    assert my_session.commit.called


''' - **test_withdraw_normal**:
    - Effectuer un retrait avec un solde suffisant.
    - Vérifier que le solde est correctement déduit.
    - Vérifier que la transaction est correctement ajoutée avec le type "withdraw".
    - Vérifier que le **`session.commit()`** a été appelé. '''
    
def test_normal_withdraw(my_session, account_factory):
    
    account = account_factory(4)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    transaction = Transaction()
    deposit = transaction.deposit(my_session, 4, 100)
    withdraw = transaction.withdraw(my_session, 4, 50)
    
    assert account.balance == 50
    assert withdraw.transaction_type == "withdraw"
    assert my_session.query(Transaction).count() == 2
    assert my_session.commit.called
    
''' - **test_withdraw_insufficient_funds**:
- Tenter de retirer un montant supérieur au solde disponible.
- Vérifier que le solde reste inchangé.
- Vérifier qu'aucune transaction n'est ajoutée.
- Vérifier que le **`session.commit()`** n'a pas été appelé. '''
    
def test_insufficient_funds_withdraw(my_session, account_factory):
    
    account = account_factory(5)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    transaction = Transaction()
    withdraw = transaction.withdraw(my_session, 5, 50)
    
    assert account.balance == 0
    assert withdraw == "Withdraw failed because of insufficient funds."
    assert my_session.query(Transaction).count() == 0
    assert my_session.commit.called
    
''' - **test_withdraw_negative_amount**:
- Tenter de retirer un montant négatif.
- Vérifier que le solde reste inchangé.
- Vérifier qu'aucune transaction n'est créée.
- Vérifier que le **`session.commit()`** n'a pas été appelé. '''

def test_negative_withdraw(my_session, account_factory):
    
    account = account_factory(6)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    
    transaction = Transaction()
    deposit = transaction.deposit(my_session, 6, 100)
    withdraw = transaction.withdraw(my_session, 6, -50)
    
    assert account.balance == 100
    assert withdraw == "Withdraw failed. Please enter a valid number."
    assert my_session.commit.called
    assert my_session.query(Transaction).count() == 1 # 1 parce que deposit

''' - **test_withdraw_zero_amount**:
- Tenter de retirer un montant nul.
- Vérifier que le solde reste inchangé.
- Vérifier qu'aucune transaction n'est créée.
- Vérifier que le **`session.commit()`** n'a pas été appelé. '''

def test_zero_withdraw(my_session, account_factory):

    account = account_factory(6)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    
    transaction = Transaction()
    deposit = transaction.deposit(my_session, 6, 100)
    withdraw = transaction.withdraw(my_session, 6, 0)
    
    assert account.balance == 100
    assert withdraw == "Withdraw failed. Please enter a valid number."
    assert my_session.query(Transaction).count() == 1 # 1 parce que deposit
    assert my_session.commit.called

''' - **test_transfer_normal**:
    - Effectuer un transfert entre deux comptes avec des soldes suffisants.
    - Vérifier que le montant est déduit du compte source.
    - Vérifier que le montant est ajouté au compte cible.
    - Vérifier que deux transactions sont créées avec les types appropriés.
    - Vérifier que le **`session.commit()`** a été appelé. '''
    
def test_transfer_normal(my_session, account_factory):
    
    account_from = account_factory(1)
    account_to = account_factory(2)
    
    # Configuration du retour pour session.get pour chaque compte
    def mock_get(cls, account_id):
        if account_id == 1:
            return account_from
        elif account_id == 2:
            return account_to
        return None
    
    my_session.get = MagicMock(side_effect=mock_get)
    
    transaction = Transaction()
    deposit = transaction.deposit(my_session, 1, 100)
    transfer = transaction.transfer(my_session, 1, 2, 50)
    
    assert account_from.balance == 50
    assert account_to.balance == 50
    assert my_session.query(Transaction).count() == 2 # deposit et transfer
    assert my_session.commit.called
    
''' - **test_transfer_insufficient_funds**:
    - Tenter un transfert avec un solde insuffisant sur le compte source.
    - Vérifier que le solde des deux comptes reste inchangé.
    - Vérifier qu'aucune transaction n'est ajoutée pour les deux comptes.
    - Vérifier que le **`session.commit()`** n'a pas été appelé. '''
    
def test_transfer_insufficient_funds(my_session, account_factory):
    
    account_from = account_factory(1)
    account_to = account_factory(2)
    
    # Configuration du retour pour session.get pour chaque compte
    def mock_get(cls, account_id):
        if account_id == 1:
            return account_from
        elif account_id == 2:
            return account_to
        return None
    
    my_session.get = MagicMock(side_effect=mock_get)
    
    transaction = Transaction()
    transfer = transaction.transfer(my_session, 1, 2, 50)
    
    assert account_from.balance == 0
    assert account_to.balance == 0
    assert transfer == 'Transfer failed due to insufficient funds from account 1'
    assert my_session.query(Transaction).count() == 0 # 0 transaction
    assert my_session.commit.called
    
    ''' - **test_transfer_negative_amount**:
    - Tenter de transférer un montant négatif.
    - Vérifier que le solde des deux comptes reste inchangé.
    - Vérifier qu'aucune transaction n'est ajoutée pour les deux comptes.
    - Vérifier que le **`session.commit()`** n'a pas été appelé. '''
    
def test_transfer_negative_amount(my_session, account_factory):
    
    account_from = account_factory(1)
    account_to = account_factory(2)
    
    # Configuration du retour pour session.get pour chaque compte
    def mock_get(cls, account_id):
        if account_id == 1:
            return account_from
        elif account_id == 2:
            return account_to
        return None
    
    my_session.get = MagicMock(side_effect=mock_get)
    
    transaction = Transaction()
    transfer = transaction.transfer(my_session, 1, 2, -50)
    
    assert account_from.balance == 0
    assert account_to.balance == 0
    assert transfer == "Transfer failed. Please enter a valid number."
    assert my_session.query(Transaction).count() == 0 # 0 transaction
    assert my_session.commit.called
    
    ''' - Tenter de transférer un montant nul.
- Vérifier que le solde des deux comptes reste inchangé.
- Vérifier qu'aucune transaction n'est ajoutée pour les deux comptes.
- Vérifier que le **`session.commit()`** n'a pas été appelé. '''

def test_transfer_zero_amount(my_session, account_factory):
    
    account_from = account_factory(1)
    account_to = account_factory(2)
    
    # Configuration du retour pour session.get pour chaque compte
    def mock_get(cls, account_id):
        if account_id == 1:
            return account_from
        elif account_id == 2:
            return account_to
        return None
    
    my_session.get = MagicMock(side_effect=mock_get)
    
    transaction = Transaction()
    transfer = transaction.transfer(my_session, 1, 2, 0)
    
    assert account_from.balance == 0
    assert account_to.balance == 0
    assert transfer == "Transfer failed. Please enter a valid number."
    assert my_session.query(Transaction).count() == 0 # 0 transaction
    assert my_session.commit.called
    

''' - **test_get_balance_initial**:
    - Vérifier le solde initial lorsqu'un nouveau compte est créé.
    - Créer un nouveau compte avec un solde initial spécifique.
    - Utiliser **`get_balance`** pour vérifier que le solde retourné correspond au solde initial.
    - Assurer que le résultat est exact sans avoir effectué de transactions. '''
    
def test_get_balance(my_session, account_factory):
    
    account = account_factory(1)
    balance = Account.get_balance(account) # le solde initial est défini à 0 dans source/bank.py
    
    assert balance == "Account 1's balance is 0 $"
    # Aucune transaction effectuée -> pas d'objet transaction créé
    
''' - **test_get_balance_after_deposit**:
    - Vérifier le solde après un dépôt.
    - Effectuer un dépôt sur un compte.
    - Utiliser **`get_balance`** pour vérifier que le solde retourné inclut le montant déposé.
    - Vérifier que le solde retourné est égal au solde initial plus le montant du dépôt. '''
    
def test_get_balance_after_deposit(my_session, account_factory):
    
    account = account_factory(1)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    transaction = Transaction()
    deposit = transaction.deposit(my_session, account, 50)
    balance = Account.get_balance(account)
    
    assert balance == "Account 1's balance is 50 $"
    assert my_session.query(Transaction).count() == 1 # 1 car déposit
    
''' - **test_get_balance_after_withdrawal**:
    - Vérifier le solde après un retrait.
    - Effectuer un retrait sur un compte avec un solde suffisant.
    - Utiliser **`get_balance`** pour vérifier que le solde retourné a été correctement déduit du montant retiré.
    - Vérifier que le solde retourné est égal au solde initial moins le montant du retrait'''
    
def test_get_balance_after_withdraw(my_session, account_factory):
    
    account = account_factory(1)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    transaction = Transaction()
    deposit = transaction.deposit(my_session, account, 50)
    withdraw = transaction.withdraw(my_session, account, 30)
    balance = Account.get_balance(account)
    
    assert balance == "Account 1's balance is 20 $"
    assert my_session.query(Transaction).count() == 2 # 2 car déposit + withdraw
    
''' test_get_balance_after_failed_withdrawal:
- Vérifier le solde après une tentative de retrait échouée due à un solde insuffisant.
- Tenter de retirer un montant supérieur au solde disponible.
- Utiliser **`get_balance`** pour vérifier que le solde n'a pas changé.
- Vérifier que le solde retourné est toujours égal au solde initial avant la tentative de retrait.  '''

def test_get_balance_after_failed_withdraw(my_session, account_factory):
    
    account = account_factory(1)
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)
    transaction = Transaction()
    deposit = transaction.deposit(my_session, account, 50)
    withdraw = transaction.withdraw(my_session, account, -30)
    balance = Account.get_balance(account)
    
    assert balance == "Account 1's balance is 50 $"
    assert my_session.query(Transaction).count() == 1 # 1 car déposit + failed withdraw
    
''' - **test_get_balance_after_transfer**:
    - Vérifier le solde après un transfert entre deux comptes.
    - Effectuer un transfert d'un montant spécifique d'un compte à un autre.
    - Utiliser **`get_balance`** pour vérifier les soldes des deux comptes après le transfert.
    - Pour le compte source, vérifier que le solde a diminué du montant transféré.
    - Pour le compte cible, vérifier que le solde a augmenté du montant transféré.'''
    
def test_get_balance_after_transfer(my_session, account_factory):
    
    account1 = account_factory(1)
    account2 = account_factory(2)
    
    # Configuration du retour pour session.get pour chaque compte
    def mock_get(cls, account_id):
        if account_id == 1:
            return account1
        elif account_id == 2:
            return account2
        return None
    
    my_session.get = MagicMock(side_effect=mock_get)
    
    transaction = Transaction()
    transaction.deposit(my_session, 1, 100)
    transaction.transfer(session=my_session, account_from=1, account_to=2, amount=30)
    
    balance_account1 = Account.get_balance(account1)
    balance_account2 = Account.get_balance(account2)
    
    assert balance_account1 == "Account 1's balance is 70 $"
    assert balance_account2 == "Account 2's balance is 30 $"
    assert my_session.query(Transaction).count() == 2 # deposit + transfer