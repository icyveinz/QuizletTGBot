import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from db_core_layer.db_config import init_db, get_db  # Updated import path

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/applications_db"


# Test for the get_db function
@pytest.mark.asyncio
async def test_get_db():
    # Mock the SessionLocal to return a mock session
    with patch("db_core_layer.db_config.SessionLocal") as mock_session_local:
        mock_session = MagicMock(spec=AsyncSession)
        mock_session_local.return_value.__aenter__.return_value = mock_session

        # Use the get_db function to get the mock session
        async for session in get_db():
            # Assert that the session is the mock session
            assert session == mock_session
            # Ensure that __aenter__ method was called
            mock_session_local.return_value.__aenter__.assert_called_once()
