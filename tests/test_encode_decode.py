from pathlib import Path

from file_compressor.encode import encode_file
from file_compressor.decode import decode_file

samples_path = Path(__file__).parent.parent / "samples"

def test_encode_decode():
    encoded = encode_file(str(samples_path / "sample-file.txt"))
    Path(samples_path / "sample-file-compressed.comp").write_bytes(encoded)
    decoded = decode_file(str(samples_path / "sample-file-compressed.comp"))
    Path(samples_path / "sample-file-decoded.txt").write_bytes(decoded)
    assert Path(samples_path / "sample-file.txt").read_bytes() == Path(samples_path / "sample-file-decoded.txt").read_bytes()
