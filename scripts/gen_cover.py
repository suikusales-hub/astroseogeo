import struct, zlib, os

path = r"E:\CodexChatGPTMigrated\SEOGEO\public\images\posts\cosine-similarity-seo-content-writing-guide\cover.png"
os.makedirs(os.path.dirname(path), exist_ok=True)

w, h = 1200, 630

def chunk(ctype, data):
    c = ctype + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
raw = b''
for y in range(h):
    row = b'\x00'
    for x in range(w):
        r = int(30 + 15 * (y / h))
        g = int(50 + 25 * (y / h))
        b_val = int(130 + 40 * (x / w))
        row += bytes([r, g, b_val])
    raw += row

idat = zlib.compress(raw)
png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

with open(path, 'wb') as f:
    f.write(png)
print('PNG created:', len(png), 'bytes')
