# abs_blockchain Examples

Comprehensive examples demonstrating blockchain integration for abs_notary.

**⚠️ IMPORTANT: All blockchain operations are MOCKED for development.**

These examples show the API interface that will be used by the real implementation.

## 🚀 Quick Start

There are two types of examples:

**Setup Examples** (One-time, by platform owner):
- Deploy smart contracts with browser wallet
- Authorize server wallet as notary
- Create custodial wallets for users
- Revoke/repudiate compromised keys

**Usage Examples** (Ongoing operations):
- Notarize documents with hash registry
- Mint NFTs with Arweave storage
- Complete workflows integrating with abs_orm

## 📋 Setup Examples (One-Time)

Run these in order when setting up the platform:

### Setup 1: Deploy Smart Contracts (`setup_01_deploy_contracts.py`)
**What it shows:**
- Deploy HashRegistry contract (for simple notarizations)
- Deploy NFT contract (ERC-721 for premium certificates)
- Store contract addresses in configuration
- Verify contracts on block explorer

**Run it:**
```bash
poetry run python examples/setup_01_deploy_contracts.py
```

**Who runs this:** Platform owner with browser wallet (MetaMask, etc.)

**When:** Once, during initial platform setup

---

### Setup 2: Authorize Server Wallet (`setup_02_authorize_server.py`)
**What it shows:**
- Configure server wallet (pays gas fees)
- Grant NOTARY_ROLE on HashRegistry
- Grant MINTER_ROLE on NFT contract
- Verify authorizations
- Test notarization

**Run it:**
```bash
poetry run python examples/setup_02_authorize_server.py
```

**Who runs this:** Platform owner with browser wallet

**When:** Once, after contract deployment

---

### Setup 3: Create User Wallets (`setup_03_create_user_wallets.py`)
**What it shows:**
- Custodial wallet architecture
- Generate wallet for each user (linked to account/API key)
- Store encrypted private keys in vault
- Sign transactions on behalf of users
- Security best practices

**Run it:**
```bash
poetry run python examples/setup_03_create_user_wallets.py
```

**Who runs this:** Automated during user registration

**When:** Every time a new user registers

---

### Setup 4: Revoke/Repudiate Keys (`setup_04_revoke_keys.py`)
**What it shows:**
- Revoke NOTARY_ROLE from compromised server wallet
- Revoke MINTER_ROLE from compromised wallet
- Deactivate user custodial wallets
- Blacklist addresses from smart contracts
- Emergency pause functionality
- Audit trail for revocations

**Run it:**
```bash
poetry run python examples/setup_04_revoke_keys.py
```

**Who runs this:** Platform owner with browser wallet

**When:** Emergency situations, security incidents, or user account closures

---

## 📋 Usage Examples (Ongoing Operations)

### 1. Basic Hash Notarization (`01_basic_notarization.py`)
**What it shows:**
- Simple hash registry notarization (lightweight, cheap)
- Wallet balance and address checking
- Gas estimation for transactions
- Transaction status verification
- Batch notarization (concurrent processing)

**Run it:**
```bash
poetry run python examples/01_basic_notarization.py
```

**Use case:**
- Free tier / basic notarization
- Simple proof-of-existence
- High-volume document notarization
- Cost-effective solution (50k gas vs 150k for NFT)

---

### 2. NFT Minting (`02_nft_minting.py`)
**What it shows:**
- Uploading files to Arweave permanent storage
- Minting NFTs with rich metadata
- Complete NFT workflow (upload + mint)
- Querying NFT metadata on-chain

**Run it:**
```bash
poetry run python examples/02_nft_minting.py
```

**Use case:**
- Premium tier notarization
- Transferable certificate of ownership
- Permanent file storage on Arweave
- Rich metadata (name, description, attributes)

---

### 3. Complete Workflow (`03_complete_workflow.py`)
**What it shows:**
- Complete integration with abs_orm
- Hash registry workflow (PENDING → PROCESSING → ON_CHAIN)
- NFT workflow with Arweave upload
- Database update patterns
- Certificate generation integration

**Run it:**
```bash
poetry run python examples/03_complete_workflow.py
```

**Use case:**
- Shows how abs_worker will use abs_blockchain
- Complete end-to-end notarization flow
- Integration points with other abs_* modules

---

## 🚀 Quick Start

All examples are self-contained with MOCK data:

```bash
cd /home/ingmar/code/abs_documents/abs_blockchain

# Run all examples
poetry run python examples/01_basic_notarization.py
poetry run python examples/02_nft_minting.py
poetry run python examples/03_complete_workflow.py
```

---

## 📚 API Reference

### BlockchainClient

```python
from abs_blockchain import BlockchainClient, NotarizationType

client = BlockchainClient()

# Hash registry notarization
result = await client.notarize_hash(
    file_hash="0x...",
    metadata={"filename": "doc.pdf"}
)

# NFT minting
arweave_result = await client.upload_to_arweave(
    file_path="/path/to/file.pdf",
    file_hash="0x..."
)

nft_result = await client.mint_nft(
    file_hash="0x...",
    arweave_url=arweave_result.arweave_url,
    metadata={"name": "My Document", ...}
)

# Utility methods
gas = await client.estimate_gas(NotarizationType.HASH)
status = await client.get_transaction_status(tx_hash)
balance = await client.get_wallet_balance()
address = client.get_wallet_address()
```

---

## 🔄 Integration Patterns

### With abs_orm (Document Repository)

```python
from abs_blockchain import BlockchainClient
from abs_orm import get_session, DocumentRepository

async def process_document(doc_id: int):
    client = BlockchainClient()

    async with get_session() as session:
        repo = DocumentRepository(session)
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

### With abs_utils (Logging & Crypto)

```python
from abs_blockchain import BlockchainClient
from abs_utils.logger import get_logger
from abs_utils.crypto import hash_file_async

logger = get_logger(__name__)

async def notarize_file(file_path: str):
    client = BlockchainClient()

    # Hash file
    file_hash = await hash_file_async(file_path)
    logger.info("File hashed", extra={"hash": file_hash})

    # Notarize
    result = await client.notarize_hash(file_hash)
    logger.info("Notarized", extra={
        "tx_hash": result.transaction_hash,
        "block": result.block_number
    })

    return result
```

---

## 🎯 Design Decisions

### Gasless Service
- **Server pays all gas fees** (user experience priority)
- Server wallet configured in `BlockchainConfig`
- Users never need crypto wallets or ETH
- Web2 UX with Web3 proofs

### Two Notarization Types

**Hash Registry (HASH):**
- ✅ Lightweight (50k gas)
- ✅ Cost-effective
- ✅ Fast
- ❌ No transferable certificate
- ❌ No permanent file storage

**NFT Minting (NFT):**
- ✅ Full ownership token
- ✅ Transferable certificate
- ✅ Permanent Arweave storage
- ✅ Rich metadata
- ❌ Higher cost (150k gas + Arweave fees)
- ❌ Slower (upload + mint)

### Mock Implementation
All methods return realistic mock data for development:
- Transaction hashes (0x-prefixed, 66 chars)
- Block numbers, gas estimates
- Arweave IDs and URLs
- NFT token IDs

This allows developers to build the full application while blockchain integration is being finalized.

---

## 🔧 Configuration

```python
# Environment variables (optional)
BLOCKCHAIN_RPC_URL=http://localhost:8545
BLOCKCHAIN_CHAIN_ID=1337
BLOCKCHAIN_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_NFT_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_PRIVATE_KEY=0x...
BLOCKCHAIN_GAS_LIMIT=300000
BLOCKCHAIN_GAS_PRICE_GWEI=20.0
BLOCKCHAIN_ARWEAVE_GATEWAY=https://arweave.net
```

---

## 💡 Tips for Developers

1. **Use mock client for development:**
   - All examples work without any blockchain setup
   - Focus on application logic first
   - Replace with real implementation later

2. **Gas estimation:**
   - Always estimate gas before transactions
   - Monitor gas usage for cost optimization
   - Consider batch processing for efficiency

3. **Error handling:**
   - Blockchain operations can fail
   - Implement retry logic with exponential backoff
   - Store failed transactions for manual review

4. **Status checking:**
   - Transactions may be pending for seconds/minutes
   - Implement polling or webhooks for status updates
   - Update database only after confirmation

---

## 🔗 Next Steps

After reviewing these examples:
1. Developers implement real Web3 integration
2. Add smart contract ABIs and deployment
3. Implement Arweave wallet and upload logic
4. Add comprehensive error handling and retries
5. Create integration tests with testnet
6. Deploy contracts to mainnet
7. Replace mock client with real implementation

---

## ❓ Questions?

Check the main README and CLAUDE.md for detailed architecture documentation!
