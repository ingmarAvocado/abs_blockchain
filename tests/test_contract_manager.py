#!/usr/bin/env python3
"""
Test suite for ContractManager mock implementations.

Tests all 9 methods to ensure they:
1. Return valid mock data
2. Track state correctly
3. Use async with appropriate delays
4. Generate unique transaction hashes
5. Maintain consistency within sessions
"""

import asyncio
import re
import pytest
import pytest_asyncio
from typing import Dict, Set

from src.abs_blockchain.contract_manager import ContractManager


class TestContractManager:
    """Test suite for ContractManager mock methods."""

    @pytest_asyncio.fixture
    async def manager(self):
        """Create a ContractManager instance for testing."""
        return ContractManager(owner_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")

    @pytest.mark.asyncio
    async def test_deploy_hash_registry(self, manager):
        """Test HashRegistry deployment returns valid mock data."""
        result = await manager.deploy_hash_registry()

        # Check return structure
        assert isinstance(result, dict)
        assert "contract_address" in result
        assert "transaction_hash" in result
        assert "deployer" in result
        assert "contract_type" in result

        # Validate format
        assert result["contract_address"].startswith("0x")
        assert len(result["contract_address"]) == 42  # 0x + 40 hex chars
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66  # 0x + 64 hex chars
        assert result["deployer"] == manager.owner_address
        assert result["contract_type"] == "HashRegistry"

        # Check state tracking
        assert hasattr(manager, "_deployed_contracts")
        assert "hash_registry" in manager._deployed_contracts
        assert manager._deployed_contracts["hash_registry"] == result["contract_address"]

    @pytest.mark.asyncio
    async def test_deploy_nft_contract(self, manager):
        """Test NFT contract deployment with custom name/symbol."""
        result = await manager.deploy_nft_contract(
            name="TestNFT",
            symbol="TEST"
        )

        # Check return structure
        assert isinstance(result, dict)
        assert "contract_address" in result
        assert "transaction_hash" in result
        assert "deployer" in result
        assert "contract_type" in result
        assert "name" in result
        assert "symbol" in result

        # Validate format
        assert result["contract_address"].startswith("0x")
        assert len(result["contract_address"]) == 42
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["deployer"] == manager.owner_address
        assert result["contract_type"] == "NFT"
        assert result["name"] == "TestNFT"
        assert result["symbol"] == "TEST"

        # Check state tracking
        assert "nft_contract" in manager._deployed_contracts
        assert manager._deployed_contracts["nft_contract"] == result["contract_address"]

    @pytest.mark.asyncio
    async def test_grant_notary_role(self, manager):
        """Test granting NOTARY_ROLE to an address."""
        contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        notary_address = "0x1111111111111111111111111111111111111111"

        result = await manager.grant_notary_role(contract_address, notary_address)

        # Check return structure
        assert isinstance(result, dict)
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["contract_address"] == contract_address
        assert result["notary_address"] == notary_address
        assert result["role"] == "NOTARY_ROLE"

        # Check state tracking
        assert hasattr(manager, "_granted_roles")
        key = f"{contract_address}:NOTARY_ROLE"
        assert key in manager._granted_roles
        assert notary_address in manager._granted_roles[key]

        # Verify has_role works
        has_role = await manager.has_role(contract_address, "NOTARY_ROLE", notary_address)
        assert has_role is True

    @pytest.mark.asyncio
    async def test_grant_minter_role(self, manager):
        """Test granting MINTER_ROLE to an address."""
        contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
        minter_address = "0x2222222222222222222222222222222222222222"

        result = await manager.grant_minter_role(contract_address, minter_address)

        # Check return structure
        assert isinstance(result, dict)
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["contract_address"] == contract_address
        assert result["minter_address"] == minter_address
        assert result["role"] == "MINTER_ROLE"

        # Check state tracking
        key = f"{contract_address}:MINTER_ROLE"
        assert key in manager._granted_roles
        assert minter_address in manager._granted_roles[key]

        # Verify has_role works
        has_role = await manager.has_role(contract_address, "MINTER_ROLE", minter_address)
        assert has_role is True

    @pytest.mark.asyncio
    async def test_revoke_notary_role(self, manager):
        """Test revoking NOTARY_ROLE from an address."""
        contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        notary_address = "0x1111111111111111111111111111111111111111"

        # First grant the role
        await manager.grant_notary_role(contract_address, notary_address)
        assert await manager.has_role(contract_address, "NOTARY_ROLE", notary_address) is True

        # Then revoke it
        result = await manager.revoke_notary_role(contract_address, notary_address)

        # Check return structure
        assert isinstance(result, dict)
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["revoked_address"] == notary_address
        assert result["role"] == "NOTARY_ROLE"

        # Verify role was revoked
        has_role = await manager.has_role(contract_address, "NOTARY_ROLE", notary_address)
        assert has_role is False

    @pytest.mark.asyncio
    async def test_revoke_minter_role(self, manager):
        """Test revoking MINTER_ROLE from an address."""
        contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
        minter_address = "0x2222222222222222222222222222222222222222"

        # First grant the role
        await manager.grant_minter_role(contract_address, minter_address)
        assert await manager.has_role(contract_address, "MINTER_ROLE", minter_address) is True

        # Then revoke it
        result = await manager.revoke_minter_role(contract_address, minter_address)

        # Check return structure
        assert isinstance(result, dict)
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["revoked_address"] == minter_address
        assert result["role"] == "MINTER_ROLE"

        # Verify role was revoked
        has_role = await manager.has_role(contract_address, "MINTER_ROLE", minter_address)
        assert has_role is False

    @pytest.mark.asyncio
    async def test_pause_contract(self, manager):
        """Test pausing a contract."""
        contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

        result = await manager.pause_contract(contract_address)

        # Check return structure
        assert isinstance(result, dict)
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["contract_address"] == contract_address
        assert result["status"] == "paused"

        # Check state tracking
        assert hasattr(manager, "_paused_contracts")
        assert contract_address in manager._paused_contracts

    @pytest.mark.asyncio
    async def test_unpause_contract(self, manager):
        """Test unpausing a contract."""
        contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

        # First pause it
        await manager.pause_contract(contract_address)
        assert contract_address in manager._paused_contracts

        # Then unpause it
        result = await manager.unpause_contract(contract_address)

        # Check return structure
        assert isinstance(result, dict)
        assert result["transaction_hash"].startswith("0x")
        assert len(result["transaction_hash"]) == 66
        assert result["contract_address"] == contract_address
        assert result["status"] == "active"

        # Verify it was unpaused
        assert contract_address not in manager._paused_contracts

    @pytest.mark.asyncio
    async def test_has_role_without_grant(self, manager):
        """Test has_role returns False for ungrated roles."""
        result = await manager.has_role(
            "0x5FbDB2315678afecb367f032d93F642f64180aa3",
            "NOTARY_ROLE",
            "0x9999999999999999999999999999999999999999"
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_unique_transaction_hashes(self, manager):
        """Test that each operation generates unique transaction hashes."""
        hashes = set()

        # Deploy contracts
        result1 = await manager.deploy_hash_registry()
        hashes.add(result1["transaction_hash"])

        result2 = await manager.deploy_nft_contract()
        hashes.add(result2["transaction_hash"])

        # Grant roles
        result3 = await manager.grant_notary_role(
            "0x5FbDB2315678afecb367f032d93F642f64180aa3",
            "0x1111111111111111111111111111111111111111"
        )
        hashes.add(result3["transaction_hash"])

        result4 = await manager.grant_minter_role(
            "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
            "0x2222222222222222222222222222222222222222"
        )
        hashes.add(result4["transaction_hash"])

        # Pause/unpause
        result5 = await manager.pause_contract("0x5FbDB2315678afecb367f032d93F642f64180aa3")
        hashes.add(result5["transaction_hash"])

        result6 = await manager.unpause_contract("0x5FbDB2315678afecb367f032d93F642f64180aa3")
        hashes.add(result6["transaction_hash"])

        # All hashes should be unique
        assert len(hashes) == 6

        # All hashes should follow the format
        for tx_hash in hashes:
            assert tx_hash.startswith("0x")
            assert len(tx_hash) == 66
            assert re.match(r'^0x[a-f0-9]{64}$', tx_hash)

    @pytest.mark.asyncio
    async def test_transaction_counter_pattern(self, manager):
        """Test that transaction hashes use a counter pattern."""
        # Deploy a contract to start counter
        result1 = await manager.deploy_hash_registry()
        tx1 = result1["transaction_hash"]

        # Deploy another
        result2 = await manager.deploy_nft_contract()
        tx2 = result2["transaction_hash"]

        # Extract the counter part (last 3 hex digits)
        counter1 = int(tx1[-3:], 16)
        counter2 = int(tx2[-3:], 16)

        # Counter should increment
        assert counter2 == counter1 + 1

    @pytest.mark.asyncio
    async def test_methods_have_delays(self, manager):
        """Test that all methods have async delays to simulate network operations."""
        import time

        # Test deploy_hash_registry timing
        start = time.time()
        await manager.deploy_hash_registry()
        elapsed = time.time() - start
        assert elapsed >= 0.1  # Should have at least 0.1s delay

        # Test grant_notary_role timing
        start = time.time()
        await manager.grant_notary_role(
            "0x5FbDB2315678afecb367f032d93F642f64180aa3",
            "0x1111111111111111111111111111111111111111"
        )
        elapsed = time.time() - start
        assert elapsed >= 0.05  # Should have at least 0.05s delay

        # Test has_role timing
        start = time.time()
        await manager.has_role(
            "0x5FbDB2315678afecb367f032d93F642f64180aa3",
            "NOTARY_ROLE",
            "0x1111111111111111111111111111111111111111"
        )
        elapsed = time.time() - start
        assert elapsed >= 0.04  # Should have at least 0.04s delay

    @pytest.mark.asyncio
    async def test_multiple_roles_per_contract(self, manager):
        """Test that multiple addresses can have the same role."""
        contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        notary1 = "0x1111111111111111111111111111111111111111"
        notary2 = "0x2222222222222222222222222222222222222222"

        # Grant role to multiple addresses
        await manager.grant_notary_role(contract_address, notary1)
        await manager.grant_notary_role(contract_address, notary2)

        # Both should have the role
        assert await manager.has_role(contract_address, "NOTARY_ROLE", notary1) is True
        assert await manager.has_role(contract_address, "NOTARY_ROLE", notary2) is True

        # Revoke from one
        await manager.revoke_notary_role(contract_address, notary1)

        # Check states
        assert await manager.has_role(contract_address, "NOTARY_ROLE", notary1) is False
        assert await manager.has_role(contract_address, "NOTARY_ROLE", notary2) is True


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])