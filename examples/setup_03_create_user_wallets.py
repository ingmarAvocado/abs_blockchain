#!/usr/bin/env python3
"""
SETUP EXAMPLE 3: Create Custodial Wallets for Users

This example demonstrates creating custodial wallets for users:
1. Generate wallet for user (linked to account/API key)
2. Store encrypted private key securely
3. Link wallet to user in database
4. Sign transactions on behalf of user

IMPORTANT: Custodial wallets are managed by the server.
Users never see or manage private keys - fully gasless Web2 UX.
All operations are MOCKED for development.
"""

import asyncio


async def main():
    print("=" * 80)
    print("SETUP 3: CREATE CUSTODIAL WALLETS FOR USERS")
    print("=" * 80)
    print()

    print("📋 CUSTODIAL WALLET ARCHITECTURE")
    print("-" * 50)
    print()
    print("Three types of wallets:")
    print("  1. Browser Wallet (Owner)")
    print("     - Deploys smart contracts")
    print("     - Authorizes server wallet")
    print("     - One-time setup only")
    print()
    print("  2. Server Wallet (Notary)")
    print("     - Pays gas fees for all transactions")
    print("     - Authorized to notarize")
    print("     - Never exposed to users")
    print()
    print("  3. User Wallets (Custodial)")
    print("     - One per user/API key")
    print("     - Signs notarization transactions")
    print("     - Managed by server")
    print("     - Users never see private keys")
    print()

    # Example users from abs_orm
    print("1️⃣ CREATE WALLETS FOR USERS")
    print("-" * 50)
    print()

    users = [
        {"id": 1, "email": "alice@example.com"},
        {"id": 2, "email": "bob@example.com"},
        {"id": 3, "email": "carol@example.com"},
    ]

    wallets = []
    for user in users:
        print(f"Creating wallet for user #{user['id']} ({user['email']})...")

        # MOCK: Generate wallet
        mock_address = f"0x{'2' * 39}{user['id']}"
        mock_private_key = f"0x{'f' * 64}"

        print(f"  ✅ Address: {mock_address}")
        print(f"  🔐 Private key: {mock_private_key[:10]}... (encrypted in vault)")
        print()

        wallets.append({
            "user_id": user["id"],
            "email": user["email"],
            "address": mock_address,
        })

    # Step 2: Store in database
    print("2️⃣ STORE IN DATABASE (abs_orm)")
    print("-" * 50)
    print()
    print("```python")
    print("# In abs_orm, add wallet table:")
    print("class UserWallet(Base):")
    print('    __tablename__ = "user_wallets"')
    print("    id = Column(Integer, primary_key=True)")
    print("    user_id = Column(Integer, ForeignKey('users.id'))")
    print("    address = Column(String(42), unique=True)")
    print("    encrypted_key = Column(Text)  # Encrypted with KMS")
    print("    created_at = Column(DateTime)")
    print("    is_active = Column(Boolean, default=True)")
    print("```")
    print()

    for wallet in wallets:
        print(f"Storing wallet for user #{wallet['user_id']}: {wallet['address']}")

    print()
    print("✅ All wallets stored in database")
    print()

    # Step 3: Sign transaction example
    print("3️⃣ SIGN TRANSACTION ON BEHALF OF USER")
    print("-" * 50)
    print()
    print("When user notarizes a document:")
    print()

    test_user = wallets[0]
    print(f"User: {test_user['email']} (ID: {test_user['user_id']})")
    print(f"Wallet: {test_user['address']}")
    print()

    print("Steps:")
    print("  1. User uploads document → abs_orm creates record")
    print("  2. Worker picks up document → Status: PROCESSING")
    print("  3. Retrieve user's wallet private key from vault")
    print("  4. Sign transaction with user's wallet")
    print("  5. Server wallet pays gas (gasless)")
    print("  6. Broadcast transaction")
    print("  7. Update abs_orm → Status: ON_CHAIN")
    print()

    # MOCK signing
    file_hash = "0xd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
    print(f"File hash: {file_hash}")
    print(f"Signing with user wallet: {test_user['address']}...")
    print()

    # MOCK signed transaction
    mock_signed_tx = "0x" + "a" * 200
    mock_tx_hash = "0x" + "b" * 64

    print(f"✅ Transaction signed!")
    print(f"   Signed by: {test_user['address']}")
    print(f"   TX Hash: {mock_tx_hash}")
    print(f"   Raw TX: {mock_signed_tx[:50]}...")
    print()

    # Step 4: Security best practices
    print("4️⃣ SECURITY BEST PRACTICES")
    print("-" * 50)
    print()
    print("✅ DO:")
    print("  - Store private keys encrypted in AWS KMS or HashiCorp Vault")
    print("  - Use separate encryption key per wallet")
    print("  - Rotate encryption keys regularly")
    print("  - Audit all wallet access")
    print("  - Monitor for suspicious activity")
    print("  - Implement rate limiting per wallet")
    print()
    print("❌ DON'T:")
    print("  - Store private keys in plain text")
    print("  - Log private keys")
    print("  - Expose private keys to users")
    print("  - Use same encryption key for all wallets")
    print("  - Store keys in application database")
    print()

    print("=" * 80)
    print("✅ Custodial wallet system configured!")
    print()
    print("Summary:")
    print(f"  ✅ Created {len(wallets)} custodial wallets")
    print("  ✅ Wallets linked to user accounts")
    print("  ✅ Private keys encrypted in vault")
    print("  ✅ Test transaction signed successfully")
    print()
    print("Next steps:")
    print("1. Run setup_04_revoke_keys.py to learn about key revocation")
    print("2. Implement wallet creation in user registration flow")
    print("3. Set up KMS/Vault for production")
    print()
    print("⚠️  USER EXPERIENCE:")
    print("- Users never see or manage private keys")
    print("- Fully gasless - no crypto wallet needed")
    print("- Web2 UX with Web3 proofs")
    print("- Users can export signed certificates")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
