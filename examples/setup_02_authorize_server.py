#!/usr/bin/env python3
"""
SETUP EXAMPLE 2: Authorize Server Wallet as Notary

This example demonstrates authorizing the server wallet to notarize documents:
1. Generate/configure server wallet
2. Grant NOTARY_ROLE to server wallet on HashRegistry
3. Grant MINTER_ROLE to server wallet on NFT contract
4. Verify authorizations

IMPORTANT: This is done by the contract owner using their browser wallet.
All operations are MOCKED for development.
"""

import asyncio


async def main():
    print("=" * 80)
    print("SETUP 2: AUTHORIZE SERVER WALLET AS NOTARY")
    print("=" * 80)
    print()

    # Contract addresses (from previous step)
    hash_registry = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    nft_contract = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
    owner_wallet = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"

    print("📋 Contract Information:")
    print(f"   HashRegistry: {hash_registry}")
    print(f"   NFT Contract: {nft_contract}")
    print(f"   Owner: {owner_wallet}")
    print()

    # Step 1: Server wallet
    print("1️⃣ SERVER WALLET")
    print("-" * 50)
    print("The server wallet pays gas fees for all notarizations (gasless service)")
    print()

    server_wallet = "0x1111111111111111111111111111111111111111"
    print(f"Server wallet: {server_wallet}")
    print()
    print("⚠️  SECURITY: Store private key in environment variable:")
    print("   BLOCKCHAIN_PRIVATE_KEY=0x...")
    print()
    print("⚠️  FUNDING: This wallet needs ETH for gas fees:")
    print("   Recommended: 1-10 ETH depending on volume")
    print("   Monitor balance and alert when low")
    print()

    # Step 2: Authorize on HashRegistry
    print("2️⃣ GRANT NOTARY_ROLE (HashRegistry)")
    print("-" * 50)
    print("This allows server wallet to register hashes on behalf of users")
    print()
    print("Function call:")
    print(f"  HashRegistry.grantRole(NOTARY_ROLE, {server_wallet})")
    print()
    print("Waiting for browser wallet signature...")
    print()

    # MOCK authorization
    auth_hash_tx = "0x" + "c" * 64

    print(f"✅ NOTARY_ROLE granted!")
    print(f"   TX Hash: {auth_hash_tx}")
    print(f"   Authorized: {server_wallet}")
    print(f"   Contract: {hash_registry}")
    print()

    # Step 3: Authorize on NFT contract
    print("3️⃣ GRANT MINTER_ROLE (NFT Contract)")
    print("-" * 50)
    print("This allows server wallet to mint NFTs on behalf of users")
    print()
    print("Function call:")
    print(f"  NFTContract.grantRole(MINTER_ROLE, {server_wallet})")
    print()
    print("Waiting for browser wallet signature...")
    print()

    # MOCK authorization
    auth_nft_tx = "0x" + "d" * 64

    print(f"✅ MINTER_ROLE granted!")
    print(f"   TX Hash: {auth_nft_tx}")
    print(f"   Authorized: {server_wallet}")
    print(f"   Contract: {nft_contract}")
    print()

    # Step 4: Verify authorizations
    print("4️⃣ VERIFY AUTHORIZATIONS")
    print("-" * 50)
    print("Checking roles...")
    print()

    # MOCK verification
    has_notary_role = True
    has_minter_role = True

    print(f"HashRegistry NOTARY_ROLE: {'✅ Authorized' if has_notary_role else '❌ Not authorized'}")
    print(f"NFT Contract MINTER_ROLE: {'✅ Authorized' if has_minter_role else '❌ Not authorized'}")
    print()

    # Step 5: Test notarization
    print("5️⃣ TEST NOTARIZATION")
    print("-" * 50)
    print("Testing hash registration...")
    print()

    test_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
    print(f"Test hash: {test_hash}")
    print("Calling HashRegistry.registerHash() with server wallet...")
    print()

    # MOCK test
    test_tx = "0x" + "e" * 64

    print(f"✅ Test successful!")
    print(f"   TX Hash: {test_tx}")
    print(f"   Hash registered by: {server_wallet}")
    print()

    print("=" * 80)
    print("✅ Server wallet authorized successfully!")
    print()
    print("Summary:")
    print(f"  ✅ Server wallet: {server_wallet}")
    print(f"  ✅ NOTARY_ROLE on HashRegistry")
    print(f"  ✅ MINTER_ROLE on NFT Contract")
    print(f"  ✅ Test notarization successful")
    print()
    print("Next steps:")
    print("1. Run setup_03_create_user_wallets.py to create custodial wallets")
    print("2. Start the notarization service")
    print("3. Monitor server wallet balance")
    print()
    print("⚠️  IMPORTANT:")
    print("- Server wallet private key must be kept secure")
    print("- Use AWS KMS, HashiCorp Vault, or similar for production")
    print("- Set up alerts for low balance")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
