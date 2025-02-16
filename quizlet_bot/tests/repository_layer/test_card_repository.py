from unittest.mock import MagicMock, AsyncMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.card_repository import CardRepository
from entity_layer.db_models.card import Card


@pytest.mark.asyncio
async def test_user_has_cards_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the query execution and return mock data
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = Card(
        user_id="123", front_side="Front", back_side="Back"
    )
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.user_has_cards("123")

    # Assert the result
    assert result is True
    mock_db.execute.assert_called_once()
    mock_result.scalars.return_value.first.assert_called_once()


@pytest.mark.asyncio
async def test_user_has_cards_no_cards():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the query execution and return None
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.user_has_cards("123")

    # Assert the result
    assert result is False
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_cards_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Create mock data
    mock_card = Card(user_id="123", front_side="Front", back_side="Back")

    # Create a mock for the result of the query chain
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()

    # Make sure that scalars().all() returns the list of mock cards
    mock_result.scalars.return_value.all.return_value = [mock_card]
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.get_user_cards("123")

    # Assert the result
    assert result == [mock_card]  # Expect the list with the mocked card
    mock_db.execute.assert_called_once()
    mock_result.scalars.return_value.all.assert_called_once()


@pytest.mark.asyncio
async def test_get_next_unstudied_card_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the query execution and return mock data
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = Card(
        user_id="123", front_side="Front", back_side="Back", is_studied=False
    )
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.get_next_unstudied_card("123")

    # Assert the result
    assert result == Card(
        user_id="123", front_side="Front", back_side="Back", is_studied=False
    )
    mock_db.execute.assert_called_once()
    mock_result.scalars.return_value.first.assert_called_once()


@pytest.mark.asyncio
async def test_get_next_unstudied_card_no_unstudied():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the query execution and return None
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.get_next_unstudied_card("123")

    # Assert the result
    assert result is None
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_reset_studied_cards_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the query execution and return mock data
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Card(user_id="123", front_side="Front", back_side="Back", is_studied=True)
    ]
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.reset_studied_cards("123")

    # Assert the result
    assert result == 1
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_card_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the card creation
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()

    # Test the method
    result = await card_repo.create_card("123", "Front", "Back")

    # Assert the result
    assert isinstance(result, Card)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_cards_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the card creation
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_db.add_all = MagicMock()
    mock_db.commit = MagicMock()

    # Test the method
    result = await card_repo.create_cards(
        "123", [("Front1", "Back1"), ("Front2", "Back2")]
    )

    # Assert the result
    assert result is True
    mock_db.add_all.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_card_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    card_repo = CardRepository(mock_db)

    # Mock the query execution and return mock data
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = Card(
        user_id="123", front_side="Front", back_side="Back"
    )
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await card_repo.get_card(1)

    # Assert the result
    assert result == Card(user_id="123", front_side="Front", back_side="Back")
    mock_db.execute.assert_called_once()
    mock_result.scalars.return_value.first.assert_called_once()
