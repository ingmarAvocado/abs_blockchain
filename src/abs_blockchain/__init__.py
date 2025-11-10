"""
abs_blockchain - Mock blockchain integration for abs_notary

This package provides MOCK implementations for:
- Ethereum/Web3 smart contract interactions (hash registry & NFT minting)
- Arweave file storage
- Transaction signing and gas estimation
- Wallet management

IMPORTANT: All functions are MOCKED for development.
Replace with real implementations when ready for production.
"""

from abs_blockchain.client import BlockchainClient
from abs_blockchain.contract_manager import ContractManager
from abs_blockchain.models import (
    NotarizationResult,
    NotarizationType,
    TransactionStatus,
    ArweaveUploadResult,
)
from abs_blockchain.config import BlockchainConfig

__version__ = "0.1.0"

__all__ = [
    "BlockchainClient",
    "ContractManager",
    "NotarizationResult",
    "NotarizationType",
    "TransactionStatus",
    "ArweaveUploadResult",
    "BlockchainConfig",
]
