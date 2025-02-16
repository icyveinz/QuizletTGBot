import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from entity_layer.db_models.user_state import UserStateEntity
from entity_layer.enums.states_enum import StatesEnum
from repository_layer.user_repository import (
    UserRepository,
)  # Replace with the actual module path


@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def user_repo(mock_db):
    return UserRepository(mock_db)


@pytest.mark.asyncio
async def test_get_user(user_repo, mock_db):
    # Arrange
    user_id = "123"
    mock_user = UserStateEntity(user_id=user_id)

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_user
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Act
    result = await user_repo.get_user(user_id)

    # Assert
    mock_db.execute.assert_called_once()
    assert result == mock_user


@pytest.mark.asyncio
async def test_get_user_not_found(user_repo, mock_db):
    # Arrange
    user_id = "123"

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Act
    result = await user_repo.get_user(user_id)

    # Assert
    mock_db.execute.assert_called_once()
    assert result is None


@pytest.mark.asyncio
async def test_create_user(user_repo, mock_db):
    # Arrange
    user_id = "123"
    is_card_flipped = False
    mock_db.commit = AsyncMock()

    # Act
    result = await user_repo.create_user(user_id, is_card_flipped)

    # Assert
    # Check that add was called with an object that has the expected attributes
    mock_db.add.assert_called_once()
    added_user = mock_db.add.call_args[0][0]  # Get the first argument passed to add
    assert isinstance(added_user, UserStateEntity)
    assert added_user.user_id == user_id
    assert added_user.is_card_flipped == is_card_flipped

    mock_db.commit.assert_called_once()
    assert result == added_user


@pytest.mark.asyncio
async def test_create_user_database_error(user_repo, mock_db):
    # Arrange
    user_id = "123"
    is_card_flipped = False
    mock_db.commit.side_effect = SQLAlchemyError("Database error")
    mock_db.rollback = AsyncMock()

    # Act
    result = await user_repo.create_user(user_id, is_card_flipped)

    # Assert
    mock_db.rollback.assert_called_once()
    assert result is None


@pytest.mark.asyncio
async def test_reset_user(user_repo, mock_db):
    # Arrange
    user_id = "123"
    mock_user = UserStateEntity(
        user_id=user_id, state="some_state", front_side="some_front"
    )

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_user
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    mock_db.commit = AsyncMock()

    # Act
    result = await user_repo.reset_user(user_id)

    # Assert
    assert result is True
    assert mock_user.state is None
    assert mock_user.front_side is None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_reset_user_not_found(user_repo, mock_db):
    # Arrange
    user_id = "123"

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Act
    result = await user_repo.reset_user(user_id)

    # Assert
    assert result is False


@pytest.mark.asyncio
async def test_update_user_state(user_repo, mock_db):
    # Arrange
    user_id = "123"
    new_state = "new_state"
    mock_user = UserStateEntity(user_id=user_id)

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_user
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    mock_db.commit = AsyncMock()

    # Act
    result = await user_repo.update_user_state(user_id, new_state)

    # Assert
    assert result is True
    assert mock_user.state == new_state
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_state_not_found(user_repo, mock_db):
    # Arrange
    user_id = "123"
    new_state = "new_state"

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Act
    result = await user_repo.update_user_state(user_id, new_state)

    # Assert
    assert result is False


@pytest.mark.asyncio
async def test_toggle_user_is_card_flipped(user_repo, mock_db):
    # Arrange
    user_id = "123"
    mock_user = UserStateEntity(user_id=user_id, is_card_flipped=False)

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_user
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    mock_db.commit = AsyncMock()

    # Act
    result = await user_repo.toggle_user_is_card_flipped(user_id)

    # Assert
    assert result is True
    assert mock_user.is_card_flipped is True
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_user_is_card_flipped_not_found(user_repo, mock_db):
    # Arrange
    user_id = "123"

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Act
    result = await user_repo.toggle_user_is_card_flipped(user_id)

    # Assert
    assert result is False


@pytest.mark.asyncio
async def test_update_user_with_front_card(user_repo, mock_db):
    # Arrange
    user_id = "123"
    front = "new_front"
    mock_user = UserStateEntity(user_id=user_id)

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_user
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    mock_db.commit = AsyncMock()

    # Act
    result = await user_repo.update_user_with_front_card(user_id, front)

    # Assert
    assert result is True
    assert mock_user.front_side == front
    assert mock_user.state == StatesEnum.AWAITING_BACK.value
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_with_front_card_not_found(user_repo, mock_db):
    # Arrange
    user_id = "123"
    front = "new_front"

    # Mock the result of execute().scalars().first()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Act
    result = await user_repo.update_user_with_front_card(user_id, front)

    # Assert
    assert result is False
