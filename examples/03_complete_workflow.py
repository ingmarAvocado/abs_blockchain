#!/usr/bin/env python3
"""
Example 3: Complete Notarization Workflow

This example demonstrates a complete workflow integrating with abs_orm:
- User chooses notarization type (HASH or NFT)
- System handles the complete blockchain flow
- Results are stored in database
- Certificate generation

IMPORTANT: All blockchain operations are MOCKED for development.
"""

import asyncio
from abs_blockchain import BlockchainClient, NotarizationType


async def notarize_document(
    file_path: str,
    file_hash: str,
    notarization_type: NotarizationType,
    client: BlockchainClient,
) -> dict:
    """
    Complete notarization workflow

    Returns:
        Dictionary with all notarization details for database storage
    """
    print(f"\n📄 Processing: {file_path}")
    print(f"   Hash: {file_hash[:20]}...")
    print(f"   Type: {notarization_type.value}")
    print()

    if notarization_type == NotarizationType.NFT:
        # NFT workflow: Upload to Arweave + Mint NFT
        print("  1. Uploading to Arweave...")
        arweave_result = await client.upload_to_arweave(file_path, file_hash)
        print(f"     ✅ Uploaded: {arweave_result.arweave_url}")

        print("  2. Minting NFT...")
        nft_result = await client.mint_nft(
            file_hash=file_hash,
            arweave_url=arweave_result.arweave_url,
            metadata={
                "name": f"Notarized Document - {file_path.split('/')[-1]}",
                "description": "Official notarization certificate",
                "image": arweave_result.arweave_url,
            },
        )
        print(f"     ✅ Minted: Token #{nft_result.token_id}")

        return {
            "transaction_hash": nft_result.transaction_hash,
            "block_number": nft_result.block_number,
            "gas_used": nft_result.gas_used,
            "notarization_type": "nft",
            "nft_token_id": nft_result.token_id,
            "arweave_url": arweave_result.arweave_url,
            "arweave_id": arweave_result.arweave_id,
            "status": "on_chain",
        }

    else:
        # Hash registry workflow: Simple hash submission
        print("  1. Submitting hash to registry...")
        hash_result = await client.notarize_hash(file_hash)
        print(f"     ✅ Registered: {hash_result.transaction_hash[:20]}...")

        return {
            "transaction_hash": hash_result.transaction_hash,
            "block_number": hash_result.block_number,
            "gas_used": hash_result.gas_used,
            "notarization_type": "hash",
            "nft_token_id": None,
            "arweave_url": None,
            "arweave_id": None,
            "status": "on_chain",
        }


async def main():
    print("=" * 80)
    print("EXAMPLE 3: COMPLETE NOTARIZATION WORKFLOW")
    print("=" * 80)
    print()

    client = BlockchainClient()

    # Scenario 1: Hash Registry (Free tier / basic notarization)
    print("📋 SCENARIO 1: HASH REGISTRY (Basic Notarization)")
    print("=" * 80)

    documents = [
        {
            "path": "/storage/files/receipt_001.pdf",
            "hash": "0x1111111111111111111111111111111111111111111111111111111111111111",
            "type": NotarizationType.HASH,
        },
        {
            "path": "/storage/files/receipt_002.pdf",
            "hash": "0x2222222222222222222222222222222222222222222222222222222222222222",
            "type": NotarizationType.HASH,
        },
    ]

    hash_results = []
    for doc in documents:
        result = await notarize_document(
            doc["path"], doc["hash"], doc["type"], client
        )
        hash_results.append(result)

    print("\n✅ Hash Registry Summary:")
    total_gas = sum(r["gas_used"] for r in hash_results)
    print(f"   Documents notarized: {len(hash_results)}")
    print(f"   Total gas used: {total_gas:,} units")
    print(f"   Average gas per doc: {total_gas // len(hash_results):,} units")
    print()

    # Scenario 2: NFT Minting (Premium tier / with certificate)
    print("\n📋 SCENARIO 2: NFT MINTING (Premium Notarization)")
    print("=" * 80)

    premium_documents = [
        {
            "path": "/storage/files/contract_001.pdf",
            "hash": "0x3333333333333333333333333333333333333333333333333333333333333333",
            "type": NotarizationType.NFT,
        },
        {
            "path": "/storage/files/legal_deed.pdf",
            "hash": "0x4444444444444444444444444444444444444444444444444444444444444444",
            "type": NotarizationType.NFT,
        },
    ]

    nft_results = []
    for doc in premium_documents:
        result = await notarize_document(
            doc["path"], doc["hash"], doc["type"], client
        )
        nft_results.append(result)

    print("\n✅ NFT Minting Summary:")
    total_gas = sum(r["gas_used"] for r in nft_results)
    print(f"   NFTs minted: {len(nft_results)}")
    print(f"   Total gas used: {total_gas:,} units")
    print(f"   Average gas per NFT: {total_gas // len(nft_results):,} units")
    print(f"   Token IDs: {', '.join(str(r['nft_token_id']) for r in nft_results)}")
    print()

    # Integration with abs_orm
    print("\n🔗 INTEGRATION WITH ABS_ORM")
    print("=" * 80)
    print("After blockchain confirmation, update database:")
    print()
    print("```python")
    print("async with get_session() as session:")
    print("    doc_repo = DocumentRepository(session)")
    print("    ")
    print("    await doc_repo.mark_as_on_chain(")
    print("        document_id=doc_id,")
    print("        transaction_hash=result['transaction_hash'],")
    print("        nft_token_id=result.get('nft_token_id'),")
    print("        arweave_file_url=result.get('arweave_url'),")
    print("        signed_json_path='/certs/cert.json',")
    print("        signed_pdf_path='/certs/cert.pdf',")
    print("    )")
    print("    ")
    print("    await session.commit()")
    print("```")
    print()

    print("=" * 80)
    print("✅ Example complete!")
    print("\nWorkflow Summary:")
    print("1. User uploads document → abs_orm creates PENDING record")
    print("2. Worker picks it up → Status: PROCESSING")
    print("3. Hash file → abs_utils.crypto.hash_file_async()")
    print("4. Blockchain notarization → abs_blockchain (this module)")
    print("5. Update database → abs_orm.mark_as_on_chain()")
    print("6. Generate certificates → abs_worker creates JSON/PDF")
    print("7. User downloads certificate → Status: ON_CHAIN")
    print("\n⚠️  NOTE: All blockchain operations are MOCKED for development")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
