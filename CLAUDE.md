# CLAUDE.md - abs_blockchain

**5-Minute Quick Start for LLMs**

## What is abs_blockchain?

Mock blockchain integration for the abs_notary gasless notarization service. Provides two notarization methods:
1. **Hash Registry** - Simple on-chain proof (50k gas)
2. **NFT Minting** - Full ownership token with Arweave storage (150k gas)

**⚠️ Currently 100% MOCKED** - Returns fake data for development. Real Web3 integration to be implemented by developers.

## Architecture: Two-Wallet Model

**1. Browser Wallet (Owner)**
- Deploys smart contracts (one-time)
- Grants/revokes roles
- Emergency controls
- Kept offline when possible

**2. Server Wallet (Notary)**
- Signs ALL user transactions
- Pays ALL gas fees (gasless service)
- Hot wallet running 24/7
- Users identified by metadata (user_id in abs_orm), not by wallet

## Core Concepts

### Gasless Service
- Server pays all gas fees (users never need crypto wallets)
- Web2 UX with Web3 proofs
- Server wallet configured in environment

### Two Notarization Types

**HASH (Simple):**
- Store file hash in smart contract
- Cheap (50k gas)
- Fast
- Good for: Free tier, high-volume, simple proof-of-existence

**NFT (Premium):**
- Upload file to Arweave
- Mint NFT with metadata
- Transferable ownership token
- Expensive (150k gas + Arweave fees)
- Good for: Premium tier, important documents, transferable certificates

## Quick Usage

```python
from abs_blockchain import BlockchainClient, NotarizationType

client = BlockchainClient()

# Hash registry (simple proof)
result = await client.notarize_hash("0xABCD...")
# Returns: NotarizationResult(tx_hash, block_number, gas_used)

# NFT minting - RECOMMENDED (automatic Arweave upload)
nft = await client.mint_nft_from_file(
    file_path="/path/to/file",
    file_hash="0xABCD...",
    metadata={"name": "Document", "description": "..."}
)
# Returns: NotarizationResult(tx_hash, token_id, arweave_url)

# NFT minting - ADVANCED (manual control)
arweave = await client.upload_to_arweave("/path/to/file", "0xABCD...")
nft = await client.mint_nft("0xABCD...", arweave.arweave_url, metadata)
# Returns: NotarizationResult(tx_hash, token_id, arweave_url)
```

## File Structure

```
abs_blockchain/
├── src/abs_blockchain/
│   ├── __init__.py          # Public API exports
│   ├── client.py            # BlockchainClient (MOCK)
│   ├── models.py            # Pydantic models
│   └── config.py            # Configuration
└── examples/                # Comprehensive examples
    ├── 01_basic_notarization.py
    ├── 02_nft_minting.py
    └── 03_complete_workflow.py
```

## Models

### NotarizationResult
```python
{
    "transaction_hash": "0x...",  # 66 chars
    "status": "confirmed",         # pending/confirmed/failed
    "notarization_type": "hash",   # hash/nft
    "block_number": 1001,
    "gas_used": 50000,
    "token_id": 1,                 # NFT only
    "arweave_url": "https://...",  # NFT only
}
```

### ArweaveUploadResult
```python
{
    "arweave_id": "...",
    "arweave_url": "https://arweave.net/...",
    "file_hash": "0x...",
    "file_size": 102400,
    "cost_ar": 0.001
}
```

## Integration with abs_orm

```python
# Worker processing document
from abs_blockchain import BlockchainClient
from abs_orm import get_session, DocumentRepository, DocStatus

client = BlockchainClient()

async with get_session() as session:
    repo = DocumentRepository(session)

    # Get pending document
    doc = await repo.get(doc_id)

    # Blockchain notarization
    result = await client.notarize_hash(doc.file_hash)

    # Update database
    await repo.mark_as_on_chain(
        doc_id,
        transaction_hash=result.transaction_hash,
        signed_json_path="/certs/cert.json",
        signed_pdf_path="/certs/cert.pdf"
    )

    await session.commit()
```

## Configuration

```python
# Environment variables
BLOCKCHAIN_RPC_URL=http://localhost:8545
BLOCKCHAIN_CHAIN_ID=1337
BLOCKCHAIN_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_NFT_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_PRIVATE_KEY=0x...
BLOCKCHAIN_GAS_LIMIT=300000
BLOCKCHAIN_GAS_PRICE_GWEI=20.0
```

## Mock Behavior

All methods are MOCKED:
- `notarize_hash()` returns fake tx hash (0xaaa...001, 0xaaa...002, etc.)
- `mint_nft()` returns fake token IDs (1, 2, 3...)
- `upload_to_arweave()` returns fake Arweave URLs
- `get_transaction_status()` always returns "confirmed"
- No actual blockchain interaction

## Common Patterns

### Gas Estimation
```python
gas = await client.estimate_gas(NotarizationType.HASH)  # 50000
gas = await client.estimate_gas(NotarizationType.NFT)   # 150000
```

### Wallet Info
```python
address = client.get_wallet_address()  # 0x1111...
balance = await client.get_wallet_balance()  # 10.5 ETH
```

### Batch Processing
```python
tasks = [client.notarize_hash(h) for h in hashes]
results = await asyncio.gather(*tasks)
```

## NFT API: Which Method to Use?

**Use `mint_nft_from_file()` (RECOMMENDED) when:**
- Standard NFT workflow (most use cases)
- You have the file path and want one-call simplicity
- You don't need separate error handling for upload vs mint
- You want clean, simple code

**Use `upload_to_arweave()` + `mint_nft()` (ADVANCED) when:**
- You already have an Arweave URL
- You need separate error handling/retry logic
- You want to mint multiple NFTs from same upload
- You need custom upload behavior

```python
# RECOMMENDED: One-call simplicity
result = await client.mint_nft_from_file(file_path, hash, metadata)

# ADVANCED: Manual control
arweave = await client.upload_to_arweave(file_path, hash)
result = await client.mint_nft(hash, arweave.arweave_url, metadata)
```

## When to Use What

**Use HASH when:**
- Free tier / basic notarization
- High volume processing
- Cost is primary concern
- Simple proof-of-existence is enough

**Use NFT when:**
- Premium tier / important documents
- User wants transferable certificate
- Permanent file storage needed
- Rich metadata desired

## TODOs for Real Implementation

1. Add Web3.py smart contract integration
2. Implement actual Arweave uploads
3. Add transaction confirmation waiting
4. Implement retry logic with exponential backoff
5. Add comprehensive error handling
6. Deploy smart contracts (HashRegistry + NFT)
7. Create contract ABIs
8. Add event listening for confirmations

## Examples

Run the examples to see complete workflows:
```bash
poetry run python examples/01_basic_notarization.py
poetry run python examples/02_nft_minting.py
poetry run python examples/03_complete_workflow.py
```

All examples demonstrate realistic usage patterns with mock data.
