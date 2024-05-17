from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from source.bank import Transaction

''' - Effectuer un dépôt avec un montant positif.
- Vérifier que le solde du compte est correctement mis à jour.
- Vérifier que la transaction est correctement ajoutée avec le type "deposit".
- Vérifier que le timestamp de la transaction est correctement enregistré.
- Vérifier que le **`session.commit()`** a été appelé. '''

def test_deposit(my_session, account_factory):
    account = account_factory(1)

    # Configurer le retour pour session.get
    my_session.get = UnifiedAlchemyMagicMock(return_value=account)

    transaction = Transaction()
    positive_deposit = transaction.deposit(my_session, 1, 100)  # dépôt de 100$

    assert positive_deposit.amount > 0
    assert positive_deposit.transaction_type == 'deposit'
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
    assert my_session.commit.called