import struct
from pathlib import Path

from file_compressor import huffman

def build_header(freq_table: dict[int, int], original_length: int) -> bytes:
    header = struct.pack(">H", len(freq_table))
    for symbol, freq in sorted(freq_table.items()):
        header += struct.pack(">BI", symbol, freq)
    header += struct.pack(">I", original_length)
    return header

def encode_bytes(blob: bytes) -> bytes:
    freq_table = huffman.build_freq_table(blob)
    root = huffman.build_freq_tree(freq_table)
    codes = huffman.build_codes(root)

    bits = "".join(codes[b] for b in blob)
    bits += "0" * (-len(bits) % 8)

    payload = bytes(int(bits[i: i + 8], 2) for i in range(0, len(bits), 8))
    return build_header(freq_table, len(blob)) + payload

def encode_file(path:str) -> bytes:
    return encode_bytes(Path(path).read_bytes())