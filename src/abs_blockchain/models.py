"""
Data models for blockchain operations
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class NotarizationType(str, Enum):
    """Type of notarization"""
    HASH = "hash"  # Simple hash registry
    NFT = "nft"    # NFT minting with metadata


class TransactionStatus(str, Enum):
    """Transaction status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class NotarizationResult(BaseModel):
    """Result of a notarization operation"""
    transaction_hash: str = Field(..., description="Blockchain transaction hash (0x-prefixed)")
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    notarization_type: NotarizationType
    block_number: Optional[int] = Field(None, description="Block number where tx was included")
    gas_used: Optional[int] = Field(None, description="Gas used for transaction")

    # NFT-specific fields
    token_id: Optional[int] = Field(None, description="NFT token ID (if type=NFT)")
    arweave_url: Optional[str] = Field(None, description="Arweave storage URL (if type=NFT)")

    # Timestamps
    timestamp: Optional[int] = Field(None, description="Unix timestamp of block")


class ArweaveUploadResult(BaseModel):
    """Result of Arweave file upload"""
    arweave_id: str = Field(..., description="Arweave transaction ID")
    arweave_url: str = Field(..., description="Full Arweave URL (https://arweave.net/...)")
    file_hash: str = Field(..., description="SHA-256 hash of uploaded file")
    file_size: int = Field(..., description="File size in bytes")
    cost_ar: float = Field(..., description="Cost in AR tokens")
