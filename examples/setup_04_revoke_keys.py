#!/usr/bin/env python3
"""
SETUP EXAMPLE 4: Revoke/Repudiate Keys from Smart Contracts

This example demonstrates key revocation and repudiation:
1. Revoke NOTARY_ROLE from compromised wallet
2. Revoke MINTER_ROLE from compromised wallet
3. Deactivate user custodial wallets
4. Emergency stop functionality
5. Audit trail for revocations

IMPORTANT: Revocation is critical for security.
Owner can revoke authorization at any time using browser wallet.
All operations are MOCKED for development.
"""

import asyncio


async def main():
    print("=" * 80)
    print("SETUP 4: REVOKE/REPUDIATE KEYS")
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
    print("  1. Compromised private key")
    print("  2. Employee termination")
    print("  3. Security breach")
    print("  4. User account closure")
    print("  5. Suspicious activity")
    print("  6. Platform shutdown")
    print()

    # Scenario 1: Revoke server wallet
    print("1️⃣ REVOKE SERVER WALLET (Emergency)")
    print("-" * 50)
    print("Scenario: Server wallet private key compromised")
    print()

    compromised_server = "0x1111111111111111111111111111111111111111"
    print(f"⚠️  Compromised wallet: {compromised_server}")
    print()

    print("Step 1: Revoke NOTARY_ROLE from HashRegistry")
    print(f"  HashRegistry.revokeRole(NOTARY_ROLE, {compromised_server})")
    print("  Waiting for browser wallet signature...")
    print()

    # MOCK revocation
    revoke_notary_tx = "0x" + "a" * 64
    print(f"✅ NOTARY_ROLE revoked!")
    print(f"   TX Hash: {revoke_notary_tx}")
    print()

    print("Step 2: Revoke MINTER_ROLE from NFT Contract")
    print(f"  NFTContract.revokeRole(MINTER_ROLE, {compromised_server})")
    print("  Waiting for browser wallet signature...")
    print()

    # MOCK revocation
    revoke_minter_tx = "0x" + "b" * 64
    print(f"✅ MINTER_ROLE revoked!")
    print(f"   TX Hash: {revoke_minter_tx}")
    print()

    print("Step 3: Generate new server wallet")
    new_server = "0x2222222222222222222222222222222222222222"
    print(f"New server wallet: {new_server}")
    print()

    print("Step 4: Re-authorize new server wallet")
    print("  Run setup_02_authorize_server.py with new wallet")
    print()

    # Scenario 2: Revoke user wallet
    print("2️⃣ REVOKE USER WALLET")
    print("-" * 50)
    print("Scenario: User closes account or suspicious activity")
    print()

    user_wallet = "0x2222222222222222222222222222222222222221"
    user_id = 42
    print(f"User ID: {user_id}")
    print(f"User wallet: {user_wallet}")
    print()

    print("Step 1: Deactivate wallet in database (abs_orm)")
    print()
    print("```python")
    print("async with get_session() as session:")
    print("    wallet_repo = UserWalletRepository(session)")
    print(f"    await wallet_repo.deactivate_wallet(user_id={user_id})")
    print("    await session.commit()")
    print("```")
    print()

    print("✅ User wallet deactivated!")
    print()

    print("Step 2: User's existing notarizations remain valid")
    print("  - Historical records are immutable")
    print("  - NFTs remain in blockchain")
    print("  - Only future notarizations are blocked")
    print()

    # Scenario 3: Blacklist addresses
    print("3️⃣ BLACKLIST ADDRESSES (Smart Contract)")
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

    # MOCK pause
    pause_hash_tx = "0x" + "d" * 64
    print(f"✅ HashRegistry paused!")
    print(f"   TX Hash: {pause_hash_tx}")
    print()

    print("Pause NFT Contract:")
    print("  NFTContract.pause()")
    print("  Waiting for browser wallet signature...")
    print()

    # MOCK pause
    pause_nft_tx = "0x" + "e" * 64
    print(f"✅ NFT Contract paused!")
    print(f"   TX Hash: {pause_nft_tx}")
    print()

    print("⚠️  All notarizations are now blocked")
    print("    Unpause when issue is resolved: contract.unpause()")
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
