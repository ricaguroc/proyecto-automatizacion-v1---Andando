import ipfshttpclient
from fastapi import HTTPException
import uuid

IPFS_URL = '/ip4/192.168.0.90/tcp/5001'

def upload_to_ipfs(content: str, ext: str) -> str:
    try:
        client = ipfshttpclient.connect(IPFS_URL)
        file = client.add_str(content)
        return file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS error: {e}")

def download_from_ipfs(cid: str) -> str:
    try:
        client = ipfshttpclient.connect(IPFS_URL)
        return client.cat(cid).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS read error: {e}")

def remove_from_ipfs(cid: str):
    try:
        client = ipfshttpclient.connect(IPFS_URL)
        client.pin.rm(cid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS delete error: {e}")
