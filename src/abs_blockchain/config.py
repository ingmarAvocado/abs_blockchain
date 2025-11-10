"""
Blockchain configuration
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BlockchainConfig(BaseSettings):
    """Blockchain configuration settings"""

    model_config = SettingsConfigDict(
        env_prefix="BLOCKCHAIN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Ethereum/Web3 settings
    rpc_url: str = "http://localhost:8545"  # Default to local node
    chain_id: int = 1337  # Local development chain
    contract_address: str = "0x0000000000000000000000000000000000000000"  # Placeholder
    nft_contract_address: str = "0x0000000000000000000000000000000000000000"  # Placeholder

    # Private key for server wallet (GASLESS - server pays)
    private_key: str = "0x0000000000000000000000000000000000000000000000000000000000000000"

    # Gas settings
    gas_limit: int = 300000
    gas_price_gwei: float = 20.0  # Gas price in Gwei

    # Arweave settings
    arweave_gateway: str = "https://arweave.net"
    arweave_wallet_path: str = "./arweave-wallet.json"

    # Retry settings
    max_retries: int = 3
    retry_delay_seconds: float = 2.0


def get_blockchain_config() -> BlockchainConfig:
    """Get blockchain configuration"""
    return BlockchainConfig()
