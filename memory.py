PAGE_SIZE = 1024

PAGE_TABLE = {
    0: 5,
    1: 2,
    2: 9,
    3: 1
}

SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}


def translate_page(address):
    page = address // PAGE_SIZE
    offset = address % PAGE_SIZE

    if page not in PAGE_TABLE:
        return None

    frame = PAGE_TABLE[page]
    physical_address = frame * PAGE_SIZE + offset

    return physical_address


def translate_segment(segment, offset):
    if segment not in SEGMENT_TABLE:
        return None

    base, limit = SEGMENT_TABLE[segment]

    if offset >= limit:
        return None

    return base + offset


print("=" * 60)
print("PAGING ADDRESS TRANSLATION")
print("=" * 60)

addresses = [260, 1500, 3000, 5000]

for address in addresses:
    result = translate_page(address)

    if result is None:
        print("Logical address", address, "-> PAGE FAULT")
    else:
        page = address // PAGE_SIZE
        offset = address % PAGE_SIZE
        print(
            "Logical address", address,
            "-> Page", page,
            "Offset", offset,
            "-> Physical address", result
        )


print()
print("=" * 60)
print("SEGMENTATION ADDRESS TRANSLATION")
print("=" * 60)

segment_addresses = [
    (0, 150),
    (1, 350),
    (2, 100)
]

for segment, offset in segment_addresses:
    result = translate_segment(segment, offset)

    if result is None:
        print(
            "Segment", segment,
            "Offset", offset,
            "-> SEGMENTATION FAULT"
        )
    else:
        print(
            "Segment", segment,
            "Offset", offset,
            "-> Physical address", result
        )
