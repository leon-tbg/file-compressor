import struct
from pathlib import Path

from file_compressor import huffman

def parse_header(blob: bytes) -> tuple[dict[int, int], int, int]:
    (n, ) = struct.unpack_from(">H", blob, 0)
    offset = 2
    freq_table = {}
    for _ in range(n):
        symbol, freq = struct.unpack_from(">BI", blob, offset)
        freq_table[symbol] = freq
        offset += 5
    (original_length, ) = struct.unpack_from(">I", blob, offset)
    offset += 4
    return freq_table, original_length, offset

def decode_bytes(blob: bytes) -> bytes:
    freq_table, original_length, offset = parse_header(blob)

    if original_length == 0:
        return b""
    if len(freq_table) == 1:
        (symbol, ) = freq_table
        return bytes([symbol]) * original_length

    root = huffman.build_freq_tree(freq_table)
    codes = huffman.build_codes(root)
    reverse_table = {code: symbol for symbol, code in codes.items()}

    out = bytearray()
    current = ""
    for byte in blob[offset:]:
        for bit in f"{byte:08b}":
            current += bit
            if current in reverse_table:
                out.append(reverse_table[current])
                current = ""
                if len(out) == original_length:
                    return bytes(out)
    return bytes(out)

def decode_file(path: str):
    return decode_bytes(Path(path).read_bytes())