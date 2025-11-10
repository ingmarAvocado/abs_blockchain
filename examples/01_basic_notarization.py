#!/usr/bin/env python3
"""
Example 1: Basic Hash Notarization

This example demonstrates:
- Simple hash registry notarization (no NFT)
- Transaction status checking
- Gas estimation
- Wallet balance checking

IMPORTANT: All operations are MOCKED for development.
"""

import asyncio
from abs_blockchain import BlockchainClient, NotarizationType


async def main():
    print("=" * 80)
    print("EXAMPLE 1: BASIC HASH NOTARIZATION")
    print("=" * 80)
    print()

    # Initialize blockchain client
    client = BlockchainClient()
    print("🔧 Initialized blockchain client (MOCK)\n")

    # Check wallet
    print("1️⃣ WALLET INFORMATION")
    print("-" * 50)
    wallet_address = client.get_wallet_address()
    balance = await client.get_wallet_balance()
    print(f"Server wallet: {wallet_address}")
    print(f"Balance: {balance} ETH")
    print()

    # Estimate gas
    print("2️⃣ GAS ESTIMATION")
    print("-" * 50)
    gas_estimate = await client.estimate_gas(NotarizationType.HASH)
    print(f"Estimated gas for hash notarization: {gas_estimate:,} units")
    print()

    # Notarize a file hash
    print("3️⃣ NOTARIZE FILE HASH")
    print("-" * 50)
    file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
    print(f"File hash: {file_hash}")
    print("Submitting transaction...")

    result = await client.notarize_hash(
        file_hash=file_hash,
        metadata={
            "filename": "contract.pdf",
            "timestamp": 1699564800,
        },
    )

    print(f"\n✅ Transaction confirmed!")
    print(f"   TX Hash: {result.transaction_hash}")
    print(f"   Status: {result.status.value}")
    print(f"   Block: {result.block_number}")
    print(f"   Gas used: {result.gas_used:,} units")
    print(f"   Type: {result.notarization_type.value}")
    print()

    # Check transaction status
    print("4️⃣ CHECK TRANSACTION STATUS")
    print("-" * 50)
    status = await client.get_transaction_status(result.transaction_hash)
    print(f"Transaction status: {status.value}")
    print()

    # Multiple notarizations
    print("5️⃣ BATCH NOTARIZATION")
    print("-" * 50)
    hashes = [
        "0x1111111111111111111111111111111111111111111111111111111111111111",
        "0x2222222222222222222222222222222222222222222222222222222222222222",
        "0x3333333333333333333333333333333333333333333333333333333333333333",
    ]

    print(f"Notarizing {len(hashes)} files concurrently...")
    tasks = [client.notarize_hash(h) for h in hashes]
    results = await asyncio.gather(*tasks)

    for i, res in enumerate(results, 1):
        print(f"  {i}. TX: {res.transaction_hash[:20]}... | Block: {res.block_number}")

    print()

    print("=" * 80)
    print("✅ Example complete!")
    print("\nKey Takeaways:")
    print("- Hash notarization is lightweight (50k gas)")
    print("- Server wallet pays all gas fees (gasless for users)")
    print("- Transactions are confirmed on-chain")
    print("- Can batch multiple notarizations concurrently")
    print("\n⚠️  NOTE: All operations are MOCKED for development")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
