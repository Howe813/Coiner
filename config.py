# Coiner 配置文件
# 用于存储全局设置和常量
"""
Configuration file: Loads pump.fun API key and wallet private key from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API key for creating tokens
API_KEY = os.getenv('API_KEY', 'your-api-key-here')
# Wallet private key for signing transactions
WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY', '') 