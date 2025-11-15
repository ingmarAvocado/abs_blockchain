"""
MOCK Blockchain Client - For development purposes

All methods return mock data. Replace with real implementations for production.
"""

import asyncio
import time
from typing import Optional
from abs_blockchain.models import (
    NotarizationResult,
    NotarizationType,
    TransactionStatus,
    ArweaveUploadResult,
)
from abs_blockchain.config import BlockchainConfig, get_blockchain_config


class BlockchainClient:
    """
    MOCK Blockchain client for development.

    This client simulates:
    - Hash registry notarization
    - NFT minting with metadata
    - Arweave file uploads
    - Transaction status checking

    All operations are MOCKED and return fake data.
    """

    def __init__(self, config: Optional[BlockchainConfig] = None):
        """Initialize blockchain client"""
        self.config = config or get_blockchain_config()
        self._mock_tx_counter = 0
        self._mock_token_counter = 0

    async def notarize_hash(self, file_hash: str, metadata: Optional[dict] = None) -> NotarizationResult:
        """
        MOCK: Notarize a file hash on-chain (simple hash registry)

        Args:
            file_hash: SHA-256 hash of file (0x-prefixed)
            metadata: Optional metadata to store

        Returns:
            NotarizationResult with transaction details
        """
        # Simulate network delay
        await asyncio.sleep(0.1)

        self._mock_tx_counter += 1
        mock_tx_hash = f"0x{'a' * 63}{self._mock_tx_counter}"

        return NotarizationResult(
            transaction_hash=mock_tx_hash,
            status=TransactionStatus.CONFIRMED,
            notarization_type=NotarizationType.HASH,
            block_number=1000 + self._mock_tx_counter,
            gas_used=50000,
            timestamp=int(time.time()),
        )

    async def mint_nft(
        self,
        file_hash: str,
        arweave_url: str,
        metadata: dict,
    ) -> NotarizationResult:
        """
        MOCK: Mint an NFT with file metadata

        Args:
            file_hash: SHA-256 hash of file (0x-prefixed)
            arweave_url: Arweave URL where file is stored
            metadata: NFT metadata (name, description, etc.)

        Returns:
            NotarizationResult with NFT token ID
        """
        # Simulate network delay
        await asyncio.sleep(0.15)

        self._mock_tx_counter += 1
        self._mock_token_counter += 1

        mock_tx_hash = f"0x{'b' * 63}{self._mock_tx_counter}"

        return NotarizationResult(
            transaction_hash=mock_tx_hash,
            status=TransactionStatus.CONFIRMED,
            notarization_type=NotarizationType.NFT,
            block_number=1000 + self._mock_tx_counter,
            gas_used=150000,
            token_id=self._mock_token_counter,
            arweave_url=arweave_url,
            timestamp=int(time.time()),
        )

    async def mint_nft_from_file(
        self,
        file_path: str,
        file_hash: str,
        metadata: dict,
    ) -> NotarizationResult:
        """
        MOCK: Convenience method - Upload to Arweave and mint NFT in one call

        This is the recommended method for standard NFT minting workflows.
        For advanced use cases (existing Arweave URLs, retry logic), use
        upload_to_arweave() and mint_nft() separately.

        Args:
            file_path: Path to file to upload
            file_hash: SHA-256 hash of file (0x-prefixed)
            metadata: NFT metadata (name, description, attributes, etc.)

        Returns:
            NotarizationResult with NFT token ID and Arweave URL
        """
        # Step 1: Upload to Arweave
        arweave_result = await self.upload_to_arweave(file_path, file_hash)

        # Step 2: Mint NFT with Arweave URL
        return await self.mint_nft(
            file_hash=file_hash,
            arweave_url=arweave_result.arweave_url,
            metadata=metadata,
        )

    async def upload_to_arweave(self, file_path: str, file_hash: str) -> ArweaveUploadResult:
        """
        MOCK: Upload file to Arweave permanent storage

        Args:
            file_path: Path to file to upload
            file_hash: SHA-256 hash of file

        Returns:
            ArweaveUploadResult with Arweave URL
        """
        # Simulate upload delay
        await asyncio.sleep(0.2)

        # Mock Arweave ID
        mock_ar_id = f"{'c' * 43}"
        mock_url = f"{self.config.arweave_gateway}/{mock_ar_id}"

        # Mock file size (in real implementation, read from file)
        mock_file_size = 1024 * 100  # 100 KB

        return ArweaveUploadResult(
            arweave_id=mock_ar_id,
            arweave_url=mock_url,
            file_hash=file_hash,
            file_size=mock_file_size,
            cost_ar=0.001,  # Mock cost in AR tokens
        )

    async def get_transaction_status(self, tx_hash: str) -> TransactionStatus:
        """
        MOCK: Get transaction status

        Args:
            tx_hash: Transaction hash to check

        Returns:
            TransactionStatus
        """
        # Simulate network delay
        await asyncio.sleep(0.05)

        # Mock: All transactions are confirmed
        return TransactionStatus.CONFIRMED

    async def get_nft_metadata(self, token_id: int) -> dict:
        """
        MOCK: Get NFT metadata

        Args:
            token_id: NFT token ID

        Returns:
            NFT metadata dictionary
        """
        # Simulate network delay
        await asyncio.sleep(0.05)

        return {
            "token_id": token_id,
            "name": f"Notarized Document #{token_id}",
            "description": "Mock NFT metadata",
            "attributes": [
                {"trait_type": "Notarization Type", "value": "NFT"},
                {"trait_type": "Network", "value": "Mock Network"},
            ],
        }

    async def estimate_gas(self, notarization_type: NotarizationType) -> int:
        """
        MOCK: Estimate gas cost for notarization

        Args:
            notarization_type: Type of notarization

        Returns:
            Estimated gas units
        """
        if notarization_type == NotarizationType.HASH:
            return 50000
        else:  # NFT
            return 150000

    def get_wallet_address(self) -> str:
        """
        MOCK: Get server wallet address

        Returns:
            Ethereum address (0x-prefixed)
        """
        return "0x" + "1" * 40

    async def get_wallet_balance(self) -> float:
        """
        MOCK: Get server wallet balance in ETH

        Returns:
            Balance in ETH
        """
        # Simulate network delay
        await asyncio.sleep(0.05)

        return 10.5  # Mock balance
