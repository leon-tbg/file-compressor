from collections import Counter
from dataclasses import dataclass, field
import heapq

@dataclass(order=True)
class Node:
    freq: int
    order: int
    symbol: int | None = field(default=None, compare=False)
    left: "Node | None" = field(default=None, compare=False)
    right: "Node | None" = field(default=None, compare=False)

def build_freq_table(data: bytes) -> dict[int, int]:
    return Counter(data)

def build_freq_tree(freq_table: dict[int, int]) -> Node:
    heap = []
    for counter, (symbol, freq) in enumerate(freq_table.items()):
        heap.append(Node(freq, counter, symbol))
    heapq.heapify(heap)

    counter = len(heap)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        parent = Node(a.freq + b.freq, counter, left=a, right=b)
        heapq.heappush(heap, parent)
        counter += 1

    return heap[0]

def build_codes(root: Node) -> dict[int, str]:
    codes: dict[int, str] = {}

    def traverse_tree(node: Node, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"

        traverse_tree(node.left, prefix + "0")
        traverse_tree(node.right, prefix + "1")

    traverse_tree(root, "")
    return codes
