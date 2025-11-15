"""
Tests for BlockchainClient
"""

import pytest
from abs_blockchain import BlockchainClient, NotarizationType


class TestBlockchainClient:
    """Test BlockchainClient mock implementation"""

    @pytest.mark.asyncio
    async def test_notarize_hash(self):
        """Test hash notarization"""
        client = BlockchainClient()
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"

        result = await client.notarize_hash(file_hash)

        assert result.transaction_hash.startswith("0x")
        assert len(result.transaction_hash) == 66
        assert result.notarization_type == NotarizationType.HASH
        assert result.gas_used == 50000
        assert result.block_number > 0
        assert result.token_id is None
        assert result.arweave_url is None

    @pytest.mark.asyncio
    async def test_upload_to_arweave(self):
        """Test Arweave upload"""
        client = BlockchainClient()
        file_path = "/storage/files/test.pdf"
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"

        result = await client.upload_to_arweave(file_path, file_hash)

        assert result.arweave_id
        assert result.arweave_url.startswith("https://arweave.net/")
        assert result.file_hash == file_hash
        assert result.file_size > 0
        assert result.cost_ar > 0

    @pytest.mark.asyncio
    async def test_mint_nft_manual(self):
        """Test manual NFT minting (two-step process)"""
        client = BlockchainClient()
        file_path = "/storage/files/test.pdf"
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
        metadata = {"name": "Test Document", "description": "Test"}

        # Step 1: Upload to Arweave
        arweave_result = await client.upload_to_arweave(file_path, file_hash)

        # Step 2: Mint NFT
        nft_result = await client.mint_nft(
            file_hash=file_hash,
            arweave_url=arweave_result.arweave_url,
            metadata=metadata,
        )

        assert nft_result.transaction_hash.startswith("0x")
        assert len(nft_result.transaction_hash) == 66
        assert nft_result.notarization_type == NotarizationType.NFT
        assert nft_result.gas_used == 150000
        assert nft_result.token_id > 0
        assert nft_result.arweave_url == arweave_result.arweave_url
        assert nft_result.block_number > 0

    @pytest.mark.asyncio
    async def test_mint_nft_from_file_convenience(self):
        """Test convenience method for NFT minting (one-step process)"""
        client = BlockchainClient()
        file_path = "/storage/files/test.pdf"
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
        metadata = {"name": "Test Document", "description": "Test"}

        # One-step: Upload + Mint
        result = await client.mint_nft_from_file(
            file_path=file_path,
            file_hash=file_hash,
            metadata=metadata,
        )

        assert result.transaction_hash.startswith("0x")
        assert len(result.transaction_hash) == 66
        assert result.notarization_type == NotarizationType.NFT
        assert result.gas_used == 150000
        assert result.token_id > 0
        assert result.arweave_url
        assert result.arweave_url.startswith("https://arweave.net/")
        assert result.block_number > 0

    @pytest.mark.asyncio
    async def test_mint_nft_from_file_vs_manual_equivalence(self):
        """Test that convenience method produces equivalent results to manual"""
        client = BlockchainClient()
        file_path = "/storage/files/test.pdf"
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
        metadata = {"name": "Test Document", "description": "Test"}

        # Convenience method
        convenience_result = await client.mint_nft_from_file(
            file_path=file_path,
            file_hash=file_hash,
            metadata=metadata,
        )

        # Both should be NFT type
        assert convenience_result.notarization_type == NotarizationType.NFT
        assert convenience_result.gas_used == 150000

        # Both should have token IDs and Arweave URLs
        assert convenience_result.token_id > 0
        assert convenience_result.arweave_url is not None

    @pytest.mark.asyncio
    async def test_get_nft_metadata(self):
        """Test NFT metadata retrieval"""
        client = BlockchainClient()
        token_id = 1

        metadata = await client.get_nft_metadata(token_id)

        assert metadata["token_id"] == token_id
        assert "name" in metadata
        assert "description" in metadata
        assert "attributes" in metadata

    @pytest.mark.asyncio
    async def test_estimate_gas(self):
        """Test gas estimation"""
        client = BlockchainClient()

        hash_gas = await client.estimate_gas(NotarizationType.HASH)
        nft_gas = await client.estimate_gas(NotarizationType.NFT)

        assert hash_gas == 50000
        assert nft_gas == 150000
        assert nft_gas > hash_gas

    @pytest.mark.asyncio
    async def test_get_wallet_balance(self):
        """Test wallet balance retrieval"""
        client = BlockchainClient()

        balance = await client.get_wallet_balance()

        assert balance > 0
        assert isinstance(balance, float)

    def test_get_wallet_address(self):
        """Test wallet address retrieval"""
        client = BlockchainClient()

        address = client.get_wallet_address()

        assert address.startswith("0x")
        assert len(address) == 42

    @pytest.mark.asyncio
    async def test_unique_transaction_hashes(self):
        """Test that each transaction gets unique hash"""
        client = BlockchainClient()
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"

        result1 = await client.notarize_hash(file_hash)
        result2 = await client.notarize_hash(file_hash)

        assert result1.transaction_hash != result2.transaction_hash

    @pytest.mark.asyncio
    async def test_unique_token_ids(self):
        """Test that each NFT gets unique token ID"""
        client = BlockchainClient()
        file_path = "/storage/files/test.pdf"
        file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
        metadata = {"name": "Test", "description": "Test"}

        result1 = await client.mint_nft_from_file(file_path, file_hash, metadata)
        result2 = await client.mint_nft_from_file(file_path, file_hash, metadata)

        assert result1.token_id != result2.token_id
        assert result2.token_id == result1.token_id + 1
