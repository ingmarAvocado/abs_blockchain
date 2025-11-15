# abs_blockchain - Method Reference for LLMs

**Target Audience**: LLMs integrating abs_blockchain into code
**Purpose**: Quick reference for choosing the right methods and understanding the API

---

## Table of Contents

1. [Quick Decision Tree](#quick-decision-tree)
2. [Core Methods Reference](#core-methods-reference)
3. [Common Usage Patterns](#common-usage-patterns)
4. [Error Handling](#error-handling)
5. [Best Practices](#best-practices)

---

## Quick Decision Tree

### What does the user want to do?

```
┌─ User wants to notarize a file
│
├─ Simple proof-of-existence (free tier, high volume)?
│  └─> Use: notarize_hash()
│     Gas: 50k, No storage, Just blockchain proof
│
└─ Transferable certificate with permanent storage (premium tier)?
   │
   ├─ Standard workflow (have file path)?
   │  └─> Use: mint_nft_from_file() ⭐ RECOMMENDED
   │     Gas: 150k, Arweave storage, Automatic upload
   │
   └─ Advanced workflow (already have Arweave URL or need custom logic)?
      └─> Use: upload_to_arweave() + mint_nft()
         Gas: 150k, Manual control, Separate steps
```

---

## Core Methods Reference

### 1. Hash Registry Methods

#### `notarize_hash(file_hash, metadata=None)`
**When**: User wants simple, cheap proof-of-existence
**Use Case**: Free tier, high-volume, basic notarization

```python
from abs_blockchain import BlockchainClient

client = BlockchainClient()

# Simple notarization
result = await client.notarize_hash(
    file_hash="0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
    metadata={"user_id": "123", "doc_type": "contract"}  # Optional
)

# Returns: NotarizationResult
# - transaction_hash: "0xaaa...001"
# - status: "confirmed"
# - notarization_type: "hash"
# - block_number: 1001
# - gas_used: 50000
# - token_id: None (not NFT)
# - arweave_url: None (no storage)
```

**Characteristics**:
- ✅ Cheap (50k gas)
- ✅ Fast
- ✅ Simple on-chain proof
- ❌ No file storage
- ❌ No ownership token
- ❌ Not transferable

---

### 2. NFT Methods

#### `mint_nft_from_file(file_path, file_hash, metadata)` ⭐ RECOMMENDED
**When**: User wants NFT certificate (95% of NFT use cases)
**Use Case**: Standard NFT workflow, premium tier, transferable certificates

```python
from abs_blockchain import BlockchainClient

client = BlockchainClient()

# One-call NFT minting (automatic Arweave upload)
result = await client.mint_nft_from_file(
    file_path="/storage/files/contract.pdf",
    file_hash="0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
    metadata={
        "name": "Notarized Contract - Q4 2024",
        "description": "Official notarization certificate",
        "image": "https://abs-notary.com/preview.png",  # Certificate preview
        "external_url": "https://abs-notary.com/verify/0xd7a8...",
        "attributes": [
            {"trait_type": "Document Type", "value": "Contract"},
            {"trait_type": "File Hash", "value": "0xd7a8..."},
            {"trait_type": "Notarization Date", "value": "2024-11-15"},
        ]
    }
)

# Returns: NotarizationResult
# - transaction_hash: "0xbbb...001"
# - status: "confirmed"
# - notarization_type: "nft"
# - block_number: 1002
# - gas_used: 150000
# - token_id: 1 ⭐
# - arweave_url: "https://arweave.net/ccc..." ⭐
```

**Characteristics**:
- ✅ One method call (simple)
- ✅ Automatic Arweave upload
- ✅ Permanent file storage
- ✅ Transferable ownership token
- ✅ Rich metadata support
- ❌ Expensive (150k gas + Arweave fees)

**This is the RECOMMENDED method for standard NFT minting.**

---

#### `upload_to_arweave(file_path, file_hash)` + `mint_nft(file_hash, arweave_url, metadata)`
**When**: Advanced use cases requiring manual control
**Use Cases**:
- Already have an Arweave URL (re-minting)
- Need separate error handling for upload vs mint
- Want to mint multiple NFTs from same upload
- Custom retry logic required

```python
from abs_blockchain import BlockchainClient

client = BlockchainClient()

# Step 1: Upload to Arweave (with error handling)
try:
    arweave_result = await client.upload_to_arweave(
        file_path="/storage/files/contract.pdf",
        file_hash="0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
    )
    # Returns: ArweaveUploadResult
    # - arweave_id: "ccc..."
    # - arweave_url: "https://arweave.net/ccc..."
    # - file_hash: "0xd7a8..."
    # - file_size: 102400 (bytes)
    # - cost_ar: 0.001 (AR tokens)
except Exception as e:
    # Handle upload failure
    # Maybe retry with exponential backoff
    pass

# Step 2: Mint NFT with Arweave URL (separate error handling)
try:
    nft_result = await client.mint_nft(
        file_hash="0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
        arweave_url=arweave_result.arweave_url,
        metadata={
            "name": "Notarized Contract",
            "description": "Certificate",
            "document": arweave_result.arweave_url,  # Link to file
            "attributes": [...]
        }
    )
except Exception as e:
    # Handle minting failure
    # Maybe retry just the minting step
    pass
```

**Characteristics**:
- ✅ Separate error handling
- ✅ Can reuse Arweave URLs
- ✅ Fine-grained control
- ❌ More verbose (2 calls)
- ❌ Manual error handling required

**Use only when you need the extra control.**

---

### 3. Query Methods

#### `get_transaction_status(tx_hash)`
**When**: Check if transaction confirmed
**Returns**: `TransactionStatus.CONFIRMED | PENDING | FAILED`

```python
status = await client.get_transaction_status("0xaaa...001")
# Returns: TransactionStatus.CONFIRMED (in mock)
```

#### `get_nft_metadata(token_id)`
**When**: Retrieve NFT metadata on-chain
**Returns**: Dictionary with NFT metadata

```python
metadata = await client.get_nft_metadata(token_id=1)
# Returns: {
#   "token_id": 1,
#   "name": "Notarized Document #1",
#   "description": "...",
#   "attributes": [...]
# }
```

#### `estimate_gas(notarization_type)`
**When**: User wants to know cost before notarization
**Returns**: Estimated gas units

```python
from abs_blockchain import NotarizationType

hash_gas = await client.estimate_gas(NotarizationType.HASH)
# Returns: 50000

nft_gas = await client.estimate_gas(NotarizationType.NFT)
# Returns: 150000
```

#### `get_wallet_address()`
**When**: Display server wallet address
**Returns**: Ethereum address (0x-prefixed)

```python
address = client.get_wallet_address()
# Returns: "0x1111111111111111111111111111111111111111" (mock)
```

#### `get_wallet_balance()`
**When**: Check if server wallet has enough funds
**Returns**: Balance in ETH

```python
balance = await client.get_wallet_balance()
# Returns: 10.5 (ETH)
```

---

## Common Usage Patterns

### Pattern 1: Free Tier - Simple Notarization

```python
from abs_blockchain import BlockchainClient
from abs_orm import get_session, DocumentRepository

client = BlockchainClient()

async with get_session() as session:
    repo = DocumentRepository(session)

    # Get document from database
    doc = await repo.get(doc_id)

    # Notarize on blockchain (hash only)
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

---

### Pattern 2: Premium Tier - NFT Certificate

```python
from abs_blockchain import BlockchainClient
from abs_orm import get_session, DocumentRepository

client = BlockchainClient()

async with get_session() as session:
    repo = DocumentRepository(session)

    # Get document from database
    doc = await repo.get(doc_id)

    # Prepare NFT metadata
    metadata = {
        "name": f"Notarized {doc.filename}",
        "description": f"Official notarization certificate for {doc.filename}",
        "image": f"https://abs-notary.com/preview/{doc_id}.png",
        "external_url": f"https://abs-notary.com/verify/{doc.file_hash}",
        "attributes": [
            {"trait_type": "Document Type", "value": doc.doc_type or "Unknown"},
            {"trait_type": "File Hash", "value": doc.file_hash},
            {"trait_type": "Notarization Date", "value": str(doc.uploaded_at.date())},
            {"trait_type": "User ID", "value": str(doc.user_id)},
        ]
    }

    # Mint NFT (automatic Arweave upload)
    result = await client.mint_nft_from_file(
        file_path=doc.file_path,
        file_hash=doc.file_hash,
        metadata=metadata
    )

    # Update database with NFT details
    await repo.mark_as_on_chain(
        doc_id,
        transaction_hash=result.transaction_hash,
        signed_json_path="/certs/cert.json",
        signed_pdf_path="/certs/cert.pdf"
    )

    # Store additional NFT metadata in database
    # (token_id, arweave_url could be stored in a separate table)

    await session.commit()
```

---

### Pattern 3: Batch Processing

```python
from abs_blockchain import BlockchainClient
import asyncio

client = BlockchainClient()

# Get pending documents
pending_docs = await get_pending_documents()

# Batch notarize (hash registry)
tasks = [
    client.notarize_hash(doc.file_hash)
    for doc in pending_docs
]

results = await asyncio.gather(*tasks)

# Update database with results
for doc, result in zip(pending_docs, results):
    await update_document(doc.id, result.transaction_hash)
```

---

### Pattern 4: Gas Estimation Before Notarization

```python
from abs_blockchain import BlockchainClient, NotarizationType

client = BlockchainClient()

# User selects premium tier
if user.tier == "premium":
    # Estimate NFT cost
    gas_estimate = await client.estimate_gas(NotarizationType.NFT)
    cost_eth = gas_estimate * gas_price_gwei / 1e9

    # Show user the cost
    print(f"Cost: {gas_estimate:,} gas (~{cost_eth:.4f} ETH)")

    # Proceed with NFT minting
    result = await client.mint_nft_from_file(...)
else:
    # Free tier - hash only
    gas_estimate = await client.estimate_gas(NotarizationType.HASH)
    result = await client.notarize_hash(...)
```

---

### Pattern 5: Retry Logic for Advanced NFT Minting

```python
from abs_blockchain import BlockchainClient
import asyncio

client = BlockchainClient()

# Step 1: Upload to Arweave with retry
max_retries = 3
for attempt in range(max_retries):
    try:
        arweave_result = await client.upload_to_arweave(file_path, file_hash)
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        await asyncio.sleep(2 ** attempt)  # Exponential backoff

# Step 2: Mint NFT with retry
for attempt in range(max_retries):
    try:
        nft_result = await client.mint_nft(
            file_hash,
            arweave_result.arweave_url,
            metadata
        )
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        await asyncio.sleep(2 ** attempt)
```

---

## Error Handling

### Mock Implementation Notes

The current implementation is **100% MOCKED**:

```python
# All methods return fake data
result = await client.notarize_hash(...)
# Returns: NotarizationResult with fake tx_hash "0xaaa...001"

result = await client.mint_nft_from_file(...)
# Returns: NotarizationResult with fake token_id=1

arweave = await client.upload_to_arweave(...)
# Returns: ArweaveUploadResult with fake Arweave URL
```

### Real Implementation Error Handling (TODO)

When implementing real blockchain integration, handle these errors:

```python
from web3.exceptions import TimeExhausted, ContractLogicError

try:
    result = await client.notarize_hash(file_hash)
except TimeExhausted:
    # Transaction timed out waiting for confirmation
    # Retry or check status manually
    pass
except ContractLogicError as e:
    # Smart contract rejected transaction
    # (e.g., hash already notarized, insufficient permissions)
    pass
except ValueError as e:
    # Invalid input (e.g., malformed hash)
    pass
except Exception as e:
    # Network error, RPC error, etc.
    pass
```

---

## Best Practices

### 1. Choose the Right Method

**Decision Matrix**:

| User Needs | Method | Gas Cost | Storage | Certificate |
|------------|--------|----------|---------|-------------|
| Free tier, proof-of-existence | `notarize_hash()` | 50k | ❌ | ❌ |
| Premium tier, standard NFT | `mint_nft_from_file()` | 150k | ✅ | ✅ |
| Advanced NFT, custom logic | `upload_to_arweave()` + `mint_nft()` | 150k | ✅ | ✅ |

### 2. Metadata Best Practices

**Good NFT Metadata**:

```python
metadata = {
    # Required fields (OpenSea standard)
    "name": "Clear, descriptive name",
    "description": "Detailed description of the certificate",

    # Recommended fields
    "image": "https://...",  # Preview image URL
    "external_url": "https://...",  # Link to verification page

    # Custom attributes
    "attributes": [
        {"trait_type": "Document Type", "value": "Contract"},
        {"trait_type": "File Hash", "value": "0x..."},
        {"trait_type": "Notarization Date", "value": "2024-11-15"},
        {"trait_type": "Issuer", "value": "abs_notary"},
        # Add user_id or other metadata here (not sensitive data!)
    ],

    # Optional fields
    "animation_url": "https://...",  # For animated certificates
    "background_color": "FFFFFF",  # Hex color (no #)
}
```

**Avoid**:
- ❌ Sensitive user data (emails, addresses, SSN, etc.)
- ❌ Mutable data (store on-chain for permanence)
- ❌ Large binary data (use Arweave URL instead)

### 3. Gas Optimization

```python
# ❌ BAD: NFT for everything
for doc in documents:
    await client.mint_nft_from_file(...)  # Expensive!

# ✅ GOOD: Hash for bulk, NFT for premium
for doc in free_tier_docs:
    await client.notarize_hash(doc.file_hash)  # Cheap (50k gas)

for doc in premium_docs:
    await client.mint_nft_from_file(...)  # Premium (150k gas)
```

### 4. Integration with abs_orm

```python
from abs_blockchain import BlockchainClient
from abs_orm import get_session, DocumentRepository, DocStatus

async def process_document(doc_id: int):
    """Complete document processing workflow"""
    client = BlockchainClient()

    async with get_session() as session:
        repo = DocumentRepository(session)

        # 1. Get document
        doc = await repo.get(doc_id)

        # 2. Check status
        if doc.status != DocStatus.PENDING:
            return  # Already processed

        # 3. Determine notarization type
        if doc.user.tier == "premium":
            # NFT minting
            result = await client.mint_nft_from_file(
                file_path=doc.file_path,
                file_hash=doc.file_hash,
                metadata={...}
            )
        else:
            # Hash registry
            result = await client.notarize_hash(doc.file_hash)

        # 4. Update database
        await repo.mark_as_on_chain(
            doc_id,
            transaction_hash=result.transaction_hash,
            signed_json_path="/certs/cert.json",
            signed_pdf_path="/certs/cert.pdf"
        )

        await session.commit()
```

### 5. Async Best Practices

```python
# ✅ GOOD: Parallel processing
tasks = [
    client.notarize_hash(hash1),
    client.notarize_hash(hash2),
    client.notarize_hash(hash3),
]
results = await asyncio.gather(*tasks)

# ❌ BAD: Sequential processing
result1 = await client.notarize_hash(hash1)
result2 = await client.notarize_hash(hash2)  # Waits for result1
result3 = await client.notarize_hash(hash3)  # Waits for result2
```

---

## Configuration

### Environment Variables

```bash
# Blockchain network
BLOCKCHAIN_RPC_URL=http://localhost:8545
BLOCKCHAIN_CHAIN_ID=1337

# Smart contracts
BLOCKCHAIN_CONTRACT_ADDRESS=0x...  # HashRegistry contract
BLOCKCHAIN_NFT_CONTRACT_ADDRESS=0x...  # NFT contract

# Server wallet (pays all gas fees)
BLOCKCHAIN_PRIVATE_KEY=0x...  # Keep secure!

# Gas settings
BLOCKCHAIN_GAS_LIMIT=300000
BLOCKCHAIN_GAS_PRICE_GWEI=20.0

# Arweave
ARWEAVE_GATEWAY=https://arweave.net
```

### Loading Configuration

```python
from abs_blockchain import BlockchainClient
from abs_blockchain.config import BlockchainConfig, get_blockchain_config

# Default config (from environment)
client = BlockchainClient()

# Custom config
config = BlockchainConfig(
    rpc_url="http://localhost:8545",
    chain_id=1337,
    contract_address="0x...",
    nft_contract_address="0x...",
    private_key="0x...",
    gas_limit=300000,
    gas_price_gwei=20.0,
)
client = BlockchainClient(config)
```

---

## Quick Reference Cheat Sheet

```python
from abs_blockchain import BlockchainClient, NotarizationType

client = BlockchainClient()

# 1. HASH REGISTRY (simple, cheap)
result = await client.notarize_hash(file_hash)

# 2. NFT - RECOMMENDED (one-call)
result = await client.mint_nft_from_file(file_path, file_hash, metadata)

# 3. NFT - ADVANCED (manual control)
arweave = await client.upload_to_arweave(file_path, file_hash)
result = await client.mint_nft(file_hash, arweave.arweave_url, metadata)

# 4. QUERY METHODS
status = await client.get_transaction_status(tx_hash)
metadata = await client.get_nft_metadata(token_id)
gas = await client.estimate_gas(NotarizationType.HASH)
address = client.get_wallet_address()
balance = await client.get_wallet_balance()
```

---

## Examples

See working examples in `examples/`:
- `01_basic_notarization.py` - Hash registry examples
- `02_nft_minting.py` - Both NFT approaches
- `03_complete_workflow.py` - Full integration with abs_orm

Run examples:
```bash
poetry run python examples/01_basic_notarization.py
poetry run python examples/02_nft_minting.py
poetry run python examples/03_complete_workflow.py
```

---

## Questions for LLMs to Ask Users

When integrating abs_blockchain, ask:

1. **Notarization Type**:
   - "Do you want a simple proof (free tier) or an NFT certificate (premium tier)?"

2. **NFT Method Choice**:
   - "Do you have the file path (use `mint_nft_from_file()`) or already have an Arweave URL (use `mint_nft()`)?"

3. **Metadata**:
   - "What information should be included in the certificate metadata?"
   - "What preview image should be used for the NFT?"

4. **Gas Budget**:
   - "What's your gas budget? (Hash: 50k, NFT: 150k)"

5. **Batch Processing**:
   - "Are you processing one document or multiple documents?"

---

## Mock vs Real Implementation

**Current Status**: 100% MOCKED

All methods return fake data for development. No actual blockchain interaction.

**TODO for Real Implementation**:
1. Add Web3.py integration
2. Deploy HashRegistry smart contract
3. Deploy NFT smart contract
4. Implement Arweave uploads
5. Add transaction confirmation waiting
6. Add comprehensive error handling
7. Add event listening
8. Add retry logic with exponential backoff

**Testing**:
```bash
# Run tests
poetry run pytest -v

# All tests pass with mock implementation
# 24 tests total (11 client + 13 contract manager)
```

---

## Support

For questions or issues:
- Check `CLAUDE.md` for 5-minute quick start
- Review examples in `examples/`
- Run tests with `poetry run pytest -v`
- See integration examples in `examples/03_complete_workflow.py`
