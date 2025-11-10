#!/usr/bin/env python3
"""
SETUP EXAMPLE 1: Deploy Smart Contracts (One-Time Setup)

This example demonstrates the initial setup performed by the platform owner:
1. Connect browser wallet (MetaMask, WalletConnect, etc.)
2. Deploy HashRegistry contract
3. Deploy NFT contract (ERC-721)
4. Store contract addresses in environment

IMPORTANT: This is done ONCE by the platform owner using their browser wallet.
All operations are MOCKED for development.
"""

import asyncio


async def main():
    print("=" * 80)
    print("SETUP 1: DEPLOY SMART CONTRACTS")
    print("=" * 80)
    print()

    print("⚠️  PREREQUISITE: Browser wallet connected (MetaMask, WalletConnect, etc.)")
    print()

    # Browser wallet info
    browser_wallet = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
    print(f"🔗 Connected wallet: {browser_wallet}")
    print()

    # Step 1: Deploy HashRegistry contract
    print("1️⃣ DEPLOY HASH REGISTRY CONTRACT")
    print("-" * 50)
    print("Purpose: Store file hashes on-chain (lightweight notarization)")
    print()
    print("Contract features:")
    print("  - registerHash(bytes32 fileHash, string metadata)")
    print("  - getHash(bytes32 fileHash) → timestamp, notary")
    print("  - Role-based access control (NOTARY_ROLE)")
    print()
    print("Deploying HashRegistry.sol...")
    print("  Gas estimate: ~500,000 units")
    print("  Waiting for user to sign in browser...")
    print()

    # MOCK deployment result
    hash_registry_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    hash_registry_tx = "0x" + "a" * 64

    print(f"✅ HashRegistry deployed!")
    print(f"   Contract: {hash_registry_address}")
    print(f"   TX Hash: {hash_registry_tx}")
    print(f"   Owner: {browser_wallet}")
    print()

    # Step 2: Deploy NFT contract
    print("2️⃣ DEPLOY NFT CONTRACT (ERC-721)")
    print("-" * 50)
    print("Purpose: Mint NFTs as notarization certificates")
    print()
    print("Contract features:")
    print("  - mint(address to, uint256 tokenId, string metadata)")
    print("  - tokenURI(uint256 tokenId) → IPFS/Arweave metadata")
    print("  - Transferable ownership (ERC-721 standard)")
    print("  - Role-based access control (MINTER_ROLE)")
    print()
    print("Deploying NotarizedDocument.sol...")
    print("  Name: NotarizedDocument")
    print("  Symbol: NOTARY")
    print("  Gas estimate: ~2,000,000 units")
    print("  Waiting for user to sign in browser...")
    print()

    # MOCK deployment result
    nft_contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
    nft_tx = "0x" + "b" * 64

    print(f"✅ NFT Contract deployed!")
    print(f"   Contract: {nft_contract_address}")
    print(f"   TX Hash: {nft_tx}")
    print(f"   Owner: {browser_wallet}")
    print(f"   Name: NotarizedDocument")
    print(f"   Symbol: NOTARY")
    print()

    # Step 3: Configuration
    print("3️⃣ UPDATE CONFIGURATION")
    print("-" * 50)
    print("Add these addresses to your .env file:")
    print()
    print(f"BLOCKCHAIN_HASH_REGISTRY_ADDRESS={hash_registry_address}")
    print(f"BLOCKCHAIN_NFT_CONTRACT_ADDRESS={nft_contract_address}")
    print(f"BLOCKCHAIN_OWNER_ADDRESS={browser_wallet}")
    print()

    # Step 4: Verify deployment
    print("4️⃣ VERIFY CONTRACTS")
    print("-" * 50)
    print("Verify on block explorer (Etherscan, etc.):")
    print(f"  HashRegistry: https://etherscan.io/address/{hash_registry_address}")
    print(f"  NFT Contract: https://etherscan.io/address/{nft_contract_address}")
    print()

    print("=" * 80)
    print("✅ Smart contracts deployed successfully!")
    print()
    print("Next steps:")
    print("1. Run setup_02_authorize_server.py to authorize server wallet")
    print("2. Fund server wallet with ETH for gas fees")
    print("3. Start accepting notarization requests")
    print()
    print("⚠️  SECURITY NOTES:")
    print("- Keep your browser wallet private key secure")
    print("- You are the contract owner - only you can authorize notaries")
    print("- Consider using a multisig wallet for production")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
