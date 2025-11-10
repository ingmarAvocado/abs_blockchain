# abs_blockchain

**Mock blockchain integration for abs_notary - gasless notarization service**

⚠️ **IMPORTANT: All blockchain operations are currently MOCKED for development.**

This module provides the API interface for blockchain operations. Developers can build against this interface while the real Web3 integration is being implemented.

## Features

- **Hash Registry Notarization** - Lightweight on-chain proof (50k gas)
- **NFT Minting** - Full ownership token with metadata (150k gas)
- **Arweave Integration** - Permanent file storage
- **Gasless Service** - Server pays all gas fees
- **Mock Implementation** - All operations return realistic test data

## Quick Start

```python
from abs_blockchain import BlockchainClient, NotarizationType

# Initialize client
client = BlockchainClient()

# Hash registry (simple)
result = await client.notarize_hash(
    file_hash="0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
)

# NFT minting (premium)
arweave_result = await client.upload_to_arweave(
    file_path="/path/to/file.pdf",
    file_hash="0x..."
)

nft_result = await client.mint_nft(
    file_hash="0x...",
    arweave_url=arweave_result.arweave_url,
    metadata={"name": "My Document", "description": "..."}
)
```

## Examples

See `examples/` directory for comprehensive examples:

1. **01_basic_notarization.py** - Hash registry workflow
2. **02_nft_minting.py** - NFT minting with Arweave
3. **03_complete_workflow.py** - Integration with abs_orm

```bash
poetry run python examples/01_basic_notarization.py
```

## Installation

```bash
# Development mode
poetry install

# With abs_utils integration
poetry install --extras dev
```

## Configuration

```bash
# .env file
BLOCKCHAIN_RPC_URL=http://localhost:8545
BLOCKCHAIN_CHAIN_ID=1337
BLOCKCHAIN_PRIVATE_KEY=0x...
BLOCKCHAIN_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_NFT_CONTRACT_ADDRESS=0x...
```

## API Reference

### BlockchainClient

```python
client = BlockchainClient(config=None)

# Notarization
await client.notarize_hash(file_hash, metadata=None)
await client.mint_nft(file_hash, arweave_url, metadata)

# Arweave
await client.upload_to_arweave(file_path, file_hash)

# Utilities
await client.estimate_gas(notarization_type)
await client.get_transaction_status(tx_hash)
await client.get_wallet_balance()
client.get_wallet_address()
```

## Mock vs Real Implementation

**Current (Mock):**
- Returns fake transaction hashes
- Instant "confirmation"
- No actual blockchain interaction
- Perfect for development

**Future (Real):**
- Web3.py integration
- Real smart contract calls
- Arweave file uploads
- Transaction confirmation waiting

## Integration

### With abs_orm

```python
from abs_blockchain import BlockchainClient
from abs_orm import get_session, DocumentRepository

client = BlockchainClient()

async with get_session() as session:
    repo = DocumentRepository(session)
    result = await client.notarize_hash(doc.file_hash)

    await repo.mark_as_on_chain(
        doc_id,
        transaction_hash=result.transaction_hash
    )
    await session.commit()
```

### With abs_utils

```python
from abs_blockchain import BlockchainClient
from abs_utils.crypto import hash_file_async
from abs_utils.logger import get_logger

logger = get_logger(__name__)
client = BlockchainClient()

file_hash = await hash_file_async(file_path)
result = await client.notarize_hash(file_hash)
logger.info("Notarized", extra={"tx_hash": result.transaction_hash})
```

## Development Workflow

1. Build your application using the mock client
2. All blockchain operations return realistic test data
3. Focus on application logic and UX
4. When ready, replace with real implementation
5. No code changes needed - same API interface

## License

MIT
