import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from source.bank import Account

# Fixture pour créer une session mock
@pytest.fixture
def my_session():
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

# Fonction pour créer des comptes
@pytest.fixture
def account_factory(my_session):
    def create_account(account_id):
        account = Account(account_id=account_id)
        my_session.add(account)
        my_session.commit()
        return account
    return create_account