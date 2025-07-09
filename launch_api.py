# -*- coding: utf-8 -*-
"""
Module for calling pump.fun API to create tokens.
"""
import os
import requests
import json
from config import API_KEY
from solders.keypair import Keypair
import mimetypes

def upload_avatar_to_ipfs(form_data, image_path, pool='pump', extra_metadata={}):
    print("DEBUG: Uploading avatar to IPFS, form_data =", form_data, "image_path =", image_path, "pool =", pool)
    
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    if pool in ['bonk', 'moonshot']:
        # Bonk和Moonshot池使用相同的IPFS服务
        with open(image_path, 'rb') as f:
            file_content = f.read()
        
        files = {
            'image': (os.path.basename(image_path), file_content, mime_type)
        }
        
        # 上传图片到Bonk的IPFS
        img_response = requests.post("https://nft-storage.letsbonk22.workers.dev/upload/img", files=files)
        print(f"DEBUG: {pool.capitalize()} IPFS image response status =", img_response.status_code)
        print(f"DEBUG: {pool.capitalize()} IPFS image response content =", img_response.text)
        
        if img_response.status_code != 200:
            return None
            
        img_uri = img_response.text
        
        # 创建元数据
        metadata_data = {
            'description': form_data.get('description', 'Token created via Coiner'),
            'image': img_uri,
            'name': form_data.get('name', ''),
            'symbol': form_data.get('symbol', ''),
            'website': "https://pumpportal.fun"
        }
        
        # Bonk和Moonshot池都需要createdOn字段
        if pool == 'bonk':
            metadata_data['createdOn'] = "https://bonk.fun"
        elif pool == 'moonshot':
            metadata_data['createdOn'] = "https://bonk.fun"  # Moonshot池也使用bonk.fun作为createdOn
        
        metadata_data.update(extra_metadata)
        
        metadata_response = requests.post(
            "https://nft-storage.letsbonk22.workers.dev/upload/meta",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(metadata_data)
        )
        print(f"DEBUG: {pool.capitalize()} IPFS metadata response status =", metadata_response.status_code)
        print(f"DEBUG: {pool.capitalize()} IPFS metadata response content =", metadata_response.text)
        
        if metadata_response.status_code == 200:
            metadata_uri = metadata_response.text
            print(f"DEBUG: {pool.capitalize()} metadataUri =", metadata_uri)
            return metadata_uri
        else:
            return None
    else:
        # Pump池使用原来的IPFS服务
        form_data.update(extra_metadata)
        files = {'file': (os.path.basename(image_path), open(image_path, 'rb'), mime_type)}
        response = requests.post("https://pump.fun/api/ipfs", data=form_data, files=files)
        print("DEBUG: Pump IPFS response status code =", response.status_code)
        print("DEBUG: Pump IPFS response content =", response.text)
        if response.status_code == 200:
            metadata_uri = response.json().get('metadataUri')
            print("DEBUG: Pump metadataUri =", metadata_uri)
            return metadata_uri
        else:
            return None

def create_token_with_avatar(name, ticker, image_path, amount=0.0, pool='pump', website='', twitter='', telegram='', description=''):
    print(f"DEBUG: Calling create_token_with_avatar, name={name}, ticker={ticker}, image_path={image_path}, amount={amount}, pool={pool}")
    # Build metadata
    form_data = {
        'name': name,
        'symbol': ticker,
        'description': description if description else f'{name} created via Coiner',
        'showName': 'true'
    }
    # 传递给IPFS的元数据字段
    extra_metadata = {}
    if website:
        extra_metadata['website'] = website
    if twitter:
        extra_metadata['twitter'] = twitter
    if telegram:
        extra_metadata['telegram'] = telegram
    metadata_uri = upload_avatar_to_ipfs(form_data, image_path, pool, extra_metadata)
    if not metadata_uri:
        print('DEBUG: Avatar upload failed, cannot create token.')
        return 'Avatar upload failed, cannot create token.'
    
    # Generate mint keypair
    mint_keypair = Keypair()
    mint = str(mint_keypair)  # Pass base58 private key string
    print(f"DEBUG: Generated mint = {mint}")
    
    token_metadata = {
        'name': name,
        'symbol': ticker,
        'uri': metadata_uri
    }
    
    # 根据池选择不同的参数
    if pool in ['bonk', 'moonshot']:
        priority_fee = 0.00005  # Bonk和Moonshot使用更低的优先级费用
    else:
        priority_fee = 0.0005   # Pump使用原来的优先级费用
    
    payload = {
        'action': 'create',
        'tokenMetadata': token_metadata,
        'mint': mint,  # Pass private key
        'denominatedInSol': 'true',  # 对于Moonshot池会被忽略，总是使用USDC
        'amount': amount,  # Amount to buy (0 = only create, no buy)
        'slippage': 10,
        'priorityFee': priority_fee,
        'pool': pool  # Use specified pool
    }
    
    print(f"DEBUG: Request payload = {payload}")
    url = f"https://pumpportal.fun/api/trade?api-key={API_KEY}"
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
    print("DEBUG: pump.fun response status code =", response.status_code)
    print("DEBUG: pump.fun response content =", response.text)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('errors'):
            return f"Token creation failed: {data.get('errors')}"
        signature = data.get('signature')
        if signature:
            return f"Token created successfully! Transaction link: https://solscan.io/tx/{signature}"
        else:
            return "Token created but no signature returned"
    else:
        return f"Token creation failed: {response.reason}" 