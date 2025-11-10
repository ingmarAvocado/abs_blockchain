"""
Smart Contract Management - For browser wallet operations

This module provides functions for ONE-TIME setup operations:
- Deploy smart contracts (HashRegistry, NFT)
- Authorize/revoke server wallet roles
- Emergency pause functionality
- Blacklist management

These operations are performed by the OWNER using a BROWSER WALLET
(MetaMask, WalletConnect, etc.), not by the server.
"""

from typing import Dict, Optional


class ContractManager:
    """
    Manager for smart contract deployment and administration.

    These methods are designed to be called from a frontend with browser wallet,
    NOT from the server. The server uses BlockchainClient for operational tasks.
    """

    def __init__(self, owner_address: str):
        """
        Initialize contract manager.

        Args:
            owner_address: Browser wallet address (will be contract owner)
        """
        self.owner_address = owner_address

    async def deploy_hash_registry(self) -> Dict[str, str]:
        """
        Deploy HashRegistry smart contract.

        This should be called from frontend with user's browser wallet.
        Returns contract address and transaction hash.

        Returns:
            {
                "contract_address": "0x...",
                "transaction_hash": "0x...",
                "deployer": "0x...",
                "contract_type": "HashRegistry"
            }
        """
        raise NotImplementedError(
            "deploy_hash_registry() must be implemented by developers. "
            "This requires Web3.py contract deployment with browser wallet signing."
        )

    async def deploy_nft_contract(
        self,
        name: str = "NotarizedDocument",
        symbol: str = "NOTARY"
    ) -> Dict[str, str]:
        """
        Deploy NFT smart contract (ERC-721).

        This should be called from frontend with user's browser wallet.

        Args:
            name: NFT collection name
            symbol: NFT collection symbol

        Returns:
            {
                "contract_address": "0x...",
                "transaction_hash": "0x...",
                "deployer": "0x...",
                "contract_type": "NFT",
                "name": "...",
                "symbol": "..."
            }
        """
        raise NotImplementedError(
            "deploy_nft_contract() must be implemented by developers. "
            "This requires Web3.py ERC-721 contract deployment with browser wallet signing."
        )

    async def grant_notary_role(
        self,
        contract_address: str,
        notary_address: str
    ) -> Dict[str, str]:
        """
        Grant NOTARY_ROLE to server wallet on HashRegistry.

        This authorizes the server wallet to register hashes.
        Called from frontend with owner's browser wallet.

        Args:
            contract_address: HashRegistry contract address
            notary_address: Server wallet address to authorize

        Returns:
            {
                "transaction_hash": "0x...",
                "contract_address": "0x...",
                "notary_address": "0x...",
                "role": "NOTARY_ROLE"
            }
        """
        raise NotImplementedError(
            "grant_notary_role() must be implemented. "
            "Call contract.grantRole(NOTARY_ROLE, notary_address) with browser wallet."
        )

    async def grant_minter_role(
        self,
        contract_address: str,
        minter_address: str
    ) -> Dict[str, str]:
        """
        Grant MINTER_ROLE to server wallet on NFT contract.

        This authorizes the server wallet to mint NFTs.
        Called from frontend with owner's browser wallet.

        Args:
            contract_address: NFT contract address
            minter_address: Server wallet address to authorize

        Returns:
            {
                "transaction_hash": "0x...",
                "contract_address": "0x...",
                "minter_address": "0x...",
                "role": "MINTER_ROLE"
            }
        """
        raise NotImplementedError(
            "grant_minter_role() must be implemented. "
            "Call contract.grantRole(MINTER_ROLE, minter_address) with browser wallet."
        )

    async def revoke_notary_role(
        self,
        contract_address: str,
        notary_address: str
    ) -> Dict[str, str]:
        """
        Revoke NOTARY_ROLE from address (emergency).

        Args:
            contract_address: HashRegistry contract address
            notary_address: Address to revoke

        Returns:
            {
                "transaction_hash": "0x...",
                "revoked_address": "0x...",
                "role": "NOTARY_ROLE"
            }
        """
        raise NotImplementedError(
            "revoke_notary_role() must be implemented. "
            "Call contract.revokeRole(NOTARY_ROLE, notary_address) with browser wallet."
        )

    async def revoke_minter_role(
        self,
        contract_address: str,
        minter_address: str
    ) -> Dict[str, str]:
        """
        Revoke MINTER_ROLE from address (emergency).

        Args:
            contract_address: NFT contract address
            minter_address: Address to revoke

        Returns:
            {
                "transaction_hash": "0x...",
                "revoked_address": "0x...",
                "role": "MINTER_ROLE"
            }
        """
        raise NotImplementedError(
            "revoke_minter_role() must be implemented. "
            "Call contract.revokeRole(MINTER_ROLE, minter_address) with browser wallet."
        )

    async def pause_contract(self, contract_address: str) -> Dict[str, str]:
        """
        Emergency pause contract (stops all operations).

        Args:
            contract_address: Contract to pause

        Returns:
            {
                "transaction_hash": "0x...",
                "contract_address": "0x...",
                "status": "paused"
            }
        """
        raise NotImplementedError(
            "pause_contract() must be implemented. "
            "Call contract.pause() with browser wallet (requires OpenZeppelin Pausable)."
        )

    async def unpause_contract(self, contract_address: str) -> Dict[str, str]:
        """
        Unpause contract (resume operations).

        Args:
            contract_address: Contract to unpause

        Returns:
            {
                "transaction_hash": "0x...",
                "contract_address": "0x...",
                "status": "active"
            }
        """
        raise NotImplementedError(
            "unpause_contract() must be implemented. "
            "Call contract.unpause() with browser wallet."
        )

    async def has_role(
        self,
        contract_address: str,
        role_name: str,
        address: str
    ) -> bool:
        """
        Check if address has specific role.

        Args:
            contract_address: Contract address
            role_name: Role to check ("NOTARY_ROLE" or "MINTER_ROLE")
            address: Address to check

        Returns:
            True if address has role, False otherwise
        """
        raise NotImplementedError(
            "has_role() must be implemented. "
            "Call contract.hasRole(role, address) view function."
        )
