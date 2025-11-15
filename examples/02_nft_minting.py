#!/usr/bin/env python3
"""
Example 2: NFT Minting with Arweave Storage

This example demonstrates:
- Uploading files to Arweave permanent storage
- Minting NFTs with metadata
- Complete NFT notarization workflow
- Querying NFT metadata

IMPORTANT: All operations are MOCKED for development.
"""

import asyncio
from abs_blockchain import BlockchainClient, NotarizationType


async def main():
    print("=" * 80)
    print("EXAMPLE 2: NFT MINTING WITH ARWEAVE STORAGE")
    print("=" * 80)
    print()

    # Initialize blockchain client
    client = BlockchainClient()
    print("🔧 Initialized blockchain client (MOCK)\n")

    # APPROACH 1: Simple convenience method (RECOMMENDED)
    print("=" * 80)
    print("APPROACH 1: CONVENIENCE METHOD (RECOMMENDED)")
    print("=" * 80)
    print()

    file_path = "/storage/files/contract.pdf"
    file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"

    nft_metadata = {
        "name": "Notarized Document - Contract.pdf",
        "description": "Official notarization certificate for contract.pdf",
        "image": "https://abs-notary.com/assets/cert-preview.png",
        "external_url": f"https://abs-notary.com/verify/{file_hash}",
        "attributes": [
            {"trait_type": "Document Type", "value": "Contract"},
            {"trait_type": "File Hash", "value": file_hash},
            {"trait_type": "Notarization Date", "value": "2024-11-10"},
            {"trait_type": "Storage", "value": "Arweave"},
            {"trait_type": "Notary", "value": "abs_notary"},
        ],
    }

    print(f"File: {file_path}")
    print(f"Hash: {file_hash}")
    print("\nMinting NFT with automatic Arweave upload...")

    # One method call does everything!
    nft_result = await client.mint_nft_from_file(
        file_path=file_path,
        file_hash=file_hash,
        metadata=nft_metadata,
    )

    print(f"\n✅ NFT minted (with automatic Arweave upload)!")
    print(f"   TX Hash: {nft_result.transaction_hash}")
    print(f"   Token ID: {nft_result.token_id}")
    print(f"   Status: {nft_result.status.value}")
    print(f"   Block: {nft_result.block_number}")
    print(f"   Gas used: {nft_result.gas_used:,} units")
    print(f"   Arweave URL: {nft_result.arweave_url}")
    print()

    # APPROACH 2: Manual control (for advanced use cases)
    print("=" * 80)
    print("APPROACH 2: MANUAL CONTROL (ADVANCED)")
    print("=" * 80)
    print()

    print("Use this approach when you need:")
    print("- Separate error handling for upload vs minting")
    print("- To mint multiple NFTs from same Arweave upload")
    print("- To use existing Arweave URLs")
    print("- Custom retry logic")
    print()

    # Step 1: Upload to Arweave
    print("1️⃣ UPLOAD FILE TO ARWEAVE")
    print("-" * 50)
    file_path2 = "/storage/files/certificate.pdf"
    file_hash2 = "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    print(f"File: {file_path2}")
    print(f"Hash: {file_hash2}")
    print("Uploading to Arweave...")

    arweave_result = await client.upload_to_arweave(file_path2, file_hash2)

    print(f"\n✅ Upload complete!")
    print(f"   Arweave ID: {arweave_result.arweave_id}")
    print(f"   URL: {arweave_result.arweave_url}")
    print(f"   File size: {arweave_result.file_size:,} bytes")
    print(f"   Cost: {arweave_result.cost_ar} AR")
    print()

    # Step 2: Mint NFT
    print("2️⃣ MINT NFT WITH METADATA")
    print("-" * 50)

    nft_metadata2 = {
        "name": "Notarized Document - Certificate.pdf",
        "description": "Official notarization certificate",
        "document": arweave_result.arweave_url,  # Link to actual document
        "image": "https://abs-notary.com/assets/cert-preview.png",
        "external_url": f"https://abs-notary.com/verify/{file_hash2}",
        "attributes": [
            {"trait_type": "Document Type", "value": "Certificate"},
            {"trait_type": "File Hash", "value": file_hash2},
            {"trait_type": "Storage", "value": "Arweave"},
        ],
    }

    print("NFT Metadata:")
    print(f"  Name: {nft_metadata2['name']}")
    print(f"  Description: {nft_metadata2['description']}")
    print(f"  Attributes: {len(nft_metadata2['attributes'])} traits")
    print("\nMinting NFT...")

    # Estimate gas first
    gas_estimate = await client.estimate_gas(NotarizationType.NFT)
    print(f"Estimated gas: {gas_estimate:,} units")

    nft_result2 = await client.mint_nft(
        file_hash=file_hash2,
        arweave_url=arweave_result.arweave_url,
        metadata=nft_metadata2,
    )

    print(f"\n✅ NFT minted!")
    print(f"   TX Hash: {nft_result2.transaction_hash}")
    print(f"   Token ID: {nft_result2.token_id}")
    print(f"   Status: {nft_result2.status.value}")
    print(f"   Block: {nft_result2.block_number}")
    print(f"   Gas used: {nft_result2.gas_used:,} units")
    print(f"   Arweave URL: {nft_result2.arweave_url}")
    print()

    # Step 3: Query NFT metadata
    print("3️⃣ QUERY NFT METADATA")
    print("-" * 50)
    metadata = await client.get_nft_metadata(nft_result2.token_id)

    print(f"Token ID: {metadata['token_id']}")
    print(f"Name: {metadata['name']}")
    print(f"Description: {metadata['description']}")
    print("Attributes:")
    for attr in metadata["attributes"]:
        print(f"  - {attr['trait_type']}: {attr['value']}")
    print()

    print("=" * 80)
    print("✅ Example complete!")
    print("\nNFT vs Hash Registry:")
    print("- Hash Registry: Lightweight, cheap (50k gas)")
    print("- NFT: Full ownership token, metadata, Arweave storage (150k gas)")
    print("- NFT provides transferable certificate of notarization")
    print("- Hash registry is sufficient for simple proof-of-existence")
    print("\n⚠️  NOTE: All operations are MOCKED for development")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
