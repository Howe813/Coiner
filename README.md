# 🪙 Coiner

> 一个强大的GUI工具，用于在 pump.fun、bonk.fun、moonshot.so 等平台批量创建代币

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Howe813/Coiner?tab=MIT-1-ov-file)

## ✨ 功能特性

- 🚀 **多平台支持** - 支持 Pump、Bonk、Moonshot 一键批量发射代币
- 🎨 **自定义配置** - 支持自定义名称、代码、头像、购买金额、池选择
- 🔗 **社交链接** - 支持 Website、Twitter、Telegram 等社交链接元数据
- 📝 **描述定制** - 支持自定义 description 字段
- 🎯 **界面美观** - 现代化GUI界面，用户体验流畅

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

#### 获取API密钥
1. 访问 [LaunchPortal.fun Trading API Setup](https://launchportal.fun/trading-api/setup)
2. 按照页面指引生成API密钥
3. 复制生成的密钥

#### 配置环境变量
创建 `.env` 文件并添加以下配置：

```env
API_KEY=your-api-key-here
WALLET_PRIVATE_KEY=your-wallet-private-key
```

### 3. 运行程序

```bash
python main.py
```

## 📋 核心参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `name` | 代币名称 | ✅ |
| `ticker` | 代币代码 | ✅ |
| `image` | 头像文件路径 | ✅ |
| `amount` | 购买金额 | ✅ |
| `pools` | 选择要发射的平台 | ✅ |
| `website` | 网站链接 | ❌ |
| `twitter` | Twitter链接 | ❌ |
| `telegram` | Telegram链接 | ❌ |
| `description` | 自定义描述 | ❌ |

## ⚙️ API配置说明

### 环境变量

| 变量名 | 说明 | 来源 |
|--------|------|------|
| `API_KEY` | 用于代币创建和交易的API密钥 | [pumpportal.fun](https://launchportal.fun/trading-api/setup) |
| `WALLET_PRIVATE_KEY` | 钱包私钥，用于签名交易 | 您的钱包（可选） |

### 支持的平台

- **Pump.fun** - 允许amount=0，使用launch.fun IPFS，计价单位SOL
- **Bonk.fun** - 要求amount>0，使用bonk.fun IPFS，计价单位SOL
- **Moonshot.com** - 要求amount>0，使用bonk.fun IPFS，计价单位USDC

## 🔧 兼容性

- ✅ 所有社交字段均为小写（website、twitter、telegram），完全兼容主流平台元数据要求
- ✅ 仅填写的社交字段会写入元数据，无默认值
- ✅ 支持多种图片格式（JPG、PNG、GIF、BMP）

## 📝 使用示例

1. **单平台创建**：选择单个平台（Pump/Bonk/Moonshot）创建代币
2. **多平台批量**：同时选择多个平台批量创建代币
3. **自定义元数据**：添加社交链接和描述信息
4. **灵活购买**：支持0金额创建或指定购买金额

## 👨‍💻 开发者

**开发者**: [@ddngxgd](https://x.com/ddngxgd)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

**注意**：请妥善保管您的API密钥和私钥，不要泄露给他人。 
