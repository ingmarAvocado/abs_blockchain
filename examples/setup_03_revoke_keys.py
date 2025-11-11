#!/usr/bin/env python3
"""
SETUP EXAMPLE 3: Revoke/Repudiate Keys from Smart Contracts

This example demonstrates key revocation and repudiation:
1. Revoke NOTARY_ROLE from compromised server wallet
2. Revoke MINTER_ROLE from compromised server wallet
3. Blacklist addresses from smart contracts
4. Emergency pause functionality
5. Audit trail for revocations

IMPORTANT: Revocation is critical for security.
Owner can revoke authorization at any time using browser wallet.
All operations are MOCKED for development.
"""

import asyncio
from abs_blockchain import ContractManager


async def main():
    print("=" * 80)
    print("SETUP 3: REVOKE/REPUDIATE KEYS")
    print("=" * 80)
    print()

    # Contract info
    hash_registry = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    nft_contract = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
    owner_wallet = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"

    print("📋 REVOCATION SCENARIOS")
    print("-" * 50)
    print()
    print("When to revoke:")
    print("  1. Server wallet private key compromised")
    print("  2. Employee termination (had access to server wallet)")
    print("  3. Security breach detected")
    print("  4. Suspicious transaction activity")
    print("  5. Platform shutdown or migration")
    print()
    print("Note: With two-wallet architecture:")
    print("  - Browser wallet = Owner (you)")
    print("  - Server wallet = Signs everything")
    print("  - No per-user wallets to manage")
    print()

    # Scenario 1: Revoke server wallet
    print("1️⃣ REVOKE SERVER WALLET (Emergency)")
    print("-" * 50)
    print("Scenario: Server wallet private key compromised")
    print()

    compromised_server = "0x1111111111111111111111111111111111111111"
    print(f"⚠️  Compromised wallet: {compromised_server}")
    print()

    # Initialize ContractManager
    manager = ContractManager(owner_address=owner_wallet)

    # First grant the roles (simulating they were previously granted)
    print("Setting up initial state (granting roles)...")
    await manager.grant_notary_role(hash_registry, compromised_server)
    await manager.grant_minter_role(nft_contract, compromised_server)
    print()

    print("Step 1: Revoke NOTARY_ROLE from HashRegistry")
    print(f"  HashRegistry.revokeRole(NOTARY_ROLE, {compromised_server})")
    print("  Waiting for browser wallet signature...")
    print()

    # REAL revocation using ContractManager
    result = await manager.revoke_notary_role(hash_registry, compromised_server)
    print(f"✅ NOTARY_ROLE revoked!")
    print(f"   TX Hash: {result['transaction_hash']}")
    print()

    print("Step 2: Revoke MINTER_ROLE from NFT Contract")
    print(f"  NFTContract.revokeRole(MINTER_ROLE, {compromised_server})")
    print("  Waiting for browser wallet signature...")
    print()

    # REAL revocation using ContractManager
    result = await manager.revoke_minter_role(nft_contract, compromised_server)
    print(f"✅ MINTER_ROLE revoked!")
    print(f"   TX Hash: {result['transaction_hash']}")
    print()

    print("Step 3: Generate new server wallet")
    new_server = "0x2222222222222222222222222222222222222222"
    print(f"New server wallet: {new_server}")
    print()

    print("Step 4: Re-authorize new server wallet")
    print("  Run setup_02_authorize_server.py with new wallet")
    print("  Update BLOCKCHAIN_PRIVATE_KEY environment variable")
    print()

    # Scenario 2: Block user account
    print("2️⃣ BLOCK USER ACCOUNT (Application Level)")
    print("-" * 50)
    print("Scenario: Prevent specific user from creating new notarizations")
    print()
    print("Note: With two-wallet architecture, users don't have blockchain wallets.")
    print("User blocking happens at APPLICATION level (abs_orm), not blockchain level.")
    print()

    user_id = 42
    print(f"User ID: {user_id}")
    print()

    print("Block user in database (abs_orm):")
    print()
    print("```python")
    print("async with get_session() as session:")
    print("    user_repo = UserRepository(session)")
    print(f"    user = await user_repo.get({user_id})")
    print("    user.is_active = False  # Disable account")
    print("    await session.commit()")
    print("```")
    print()

    print("✅ User account blocked!")
    print()

    print("Effects:")
    print("  - User cannot create new notarizations (app prevents it)")
    print("  - Existing notarizations remain valid (immutable on blockchain)")
    print("  - NFTs still exist and are transferable")
    print("  - Server wallet continues working for other users")
    print()

    # Scenario 3: Blacklist addresses
    print("3️⃣ BLACKLIST ADDRESSES (Smart Contract Level)")
    print("-" * 50)
    print("Scenario: Prevent specific addresses from notarizing")
    print()

    blacklisted = "0x3333333333333333333333333333333333333333"
    print(f"Blacklisted address: {blacklisted}")
    print()

    print("Option A: Role-based (recommended)")
    print("  - Revoke NOTARY_ROLE (already shown above)")
    print("  - Clean and standard approach")
    print()

    print("Option B: Explicit blacklist mapping")
    print("  - Add to contract blacklist: blacklist[address] = true")
    print("  - Requires custom contract implementation")
    print()

    print("Function call:")
    print(f"  HashRegistry.addToBlacklist({blacklisted})")
    print("  Waiting for browser wallet signature...")
    print()

    # MOCK blacklist
    blacklist_tx = "0x" + "c" * 64
    print(f"✅ Address blacklisted!")
    print(f"   TX Hash: {blacklist_tx}")
    print()

    # Scenario 4: Emergency stop (Pause)
    print("4️⃣ EMERGENCY STOP (Pause Contract)")
    print("-" * 50)
    print("Scenario: Critical security issue - pause all notarizations")
    print()

    print("Pause HashRegistry:")
    print("  HashRegistry.pause()")
    print("  Waiting for browser wallet signature...")
    print()

    # REAL pause using ContractManager
    result = await manager.pause_contract(hash_registry)
    print(f"✅ HashRegistry paused!")
    print(f"   TX Hash: {result['transaction_hash']}")
    print()

    print("Pause NFT Contract:")
    print("  NFTContract.pause()")
    print("  Waiting for browser wallet signature...")
    print()

    # REAL pause using ContractManager
    result = await manager.pause_contract(nft_contract)
    print(f"✅ NFT Contract paused!")
    print(f"   TX Hash: {result['transaction_hash']}")
    print()

    print("⚠️  All notarizations are now blocked")
    print("    Unpause when issue is resolved: contract.unpause()")
    print()

    # Demonstrate unpause
    print("Step to unpause contracts:")
    print("  - After security issue resolved")
    print("  - Call unpause() on each contract")
    print()

    # REAL unpause using ContractManager
    await manager.unpause_contract(hash_registry)
    await manager.unpause_contract(nft_contract)
    print("✅ Contracts unpaused and operational again")
    print()

    # Scenario 5: Audit trail
    print("5️⃣ AUDIT TRAIL")
    print("-" * 50)
    print("All revocations are recorded on-chain:")
    print()

    print("Query role events:")
    print("  - RoleGranted(role, account, sender)")
    print("  - RoleRevoked(role, account, sender)")
    print()

    print("Example audit log:")
    print()
    print("| Date       | Action     | Role         | Address     | By        |")
    print("|------------|------------|--------------|-------------|-----------|")
    print("| 2024-01-01 | GRANTED    | NOTARY_ROLE  | 0x1111...   | Owner     |")
    print("| 2024-06-15 | REVOKED    | NOTARY_ROLE  | 0x1111...   | Owner     |")
    print("| 2024-06-15 | GRANTED    | NOTARY_ROLE  | 0x2222...   | Owner     |")
    print()

    # Best practices
    print("6️⃣ BEST PRACTICES")
    print("-" * 50)
    print()
    print("✅ Prevention:")
    print("  - Use hardware wallets for owner keys")
    print("  - Implement multi-sig for critical operations")
    print("  - Monitor all wallet activity")
    print("  - Rate limit transactions")
    print("  - Set up alerts for unusual activity")
    print()
    print("✅ Response:")
    print("  - Document incident response procedures")
    print("  - Keep backup of contract addresses and ABIs")
    print("  - Test revocation procedures regularly")
    print("  - Maintain communication channels with users")
    print()
    print("✅ Recovery:")
    print("  - Generate new server wallet")
    print("  - Re-authorize with contracts")
    print("  - Update environment variables")
    print("  - Notify affected users")
    print("  - Conduct post-mortem")
    print()

    print("=" * 80)
    print("✅ Revocation procedures documented!")
    print()
    print("Summary:")
    print("  ✅ Server wallet revocation")
    print("  ✅ User wallet deactivation")
    print("  ✅ Address blacklisting")
    print("  ✅ Emergency pause functionality")
    print("  ✅ Audit trail on-chain")
    print()
    print("⚠️  CRITICAL SECURITY:")
    print()
    print("Owner wallet must be secure:")
    print("  - Only owner can revoke/authorize")
    print("  - Consider using Gnosis Safe multisig")
    print("  - Never share owner private key")
    print("  - Use hardware wallet (Ledger, Trezor)")
    print()
    print("Key principle:")
    print("  'Revocation is easier than prevention'")
    print("  Design contracts with revocation in mind")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
