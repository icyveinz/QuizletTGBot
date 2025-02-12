from unittest.mock import MagicMock, AsyncMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from repository_layer.seen_cards_repository import SeenCardsRepository
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.asyncio
async def test_mark_card_as_seen_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    seen_cards_repo = SeenCardsRepository(mock_db)

    # Mock the insert operation
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute

    # Test the method
    result = await seen_cards_repo.mark_card_as_seen("123", 1)

    # Assert the result
    assert result is True
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_mark_card_as_seen_failure():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    seen_cards_repo = SeenCardsRepository(mock_db)

    # Simulate an error during the execute
    mock_db.execute = AsyncMock(side_effect=SQLAlchemyError)

    # Test the method
    result = await seen_cards_repo.mark_card_as_seen("123", 1)

    # Assert the result
    assert result is False
    mock_db.execute.assert_called_once()
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_get_list_of_related_and_seen_cards_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    seen_cards_repo = SeenCardsRepository(mock_db)

    # Mock the query execution and return mock data
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [1, 2, 3]
    mock_db.execute.return_value = mock_result

    # Test the method
    result = await seen_cards_repo.get_list_of_related_and_seen_cards("123")

    # Assert the result
    assert result == [1, 2, 3]
    mock_db.execute.assert_called_once()
    mock_result.scalars.return_value.all.assert_called_once()


@pytest.mark.asyncio
async def test_get_list_of_related_and_seen_cards_failure():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    seen_cards_repo = SeenCardsRepository(mock_db)

    # Simulate an error during the execute
    mock_db.execute = AsyncMock(side_effect=SQLAlchemyError)

    # Test the method
    result = await seen_cards_repo.get_list_of_related_and_seen_cards("123")

    # Assert the result
    assert result == []
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_clean_seen_cards_by_user_id_success():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    seen_cards_repo = SeenCardsRepository(mock_db)

    # Mock the delete operation
    mock_execute = AsyncMock()
    mock_db.execute = mock_execute

    # Test the method
    result = await seen_cards_repo.clean_seen_cards_by_user_id("123")

    # Assert the result
    assert result is True
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_clean_seen_cards_by_user_id_failure():
    # Mock the AsyncSession
    mock_db = MagicMock(spec=AsyncSession)
    seen_cards_repo = SeenCardsRepository(mock_db)

    # Simulate an error during the execute
    mock_db.execute = AsyncMock(side_effect=SQLAlchemyError)

    # Test the method
    result = await seen_cards_repo.clean_seen_cards_by_user_id("123")

    # Assert the result
    assert result is False
    mock_db.execute.assert_called_once()
    mock_db.rollback.assert_called_once()
