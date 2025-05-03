podman run -d --name ipfs \
    -v $(pwd)/config:/data/ipfs:Z \
    -p 5001:5001 \
    ipfs/go-ipfs:latest \
    daemon --offline
