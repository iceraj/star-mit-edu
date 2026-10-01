#!/usr/bin/env python3
"""Make a CheerpJ-compatible copy of an archived Apache POI 3.x JAR.

POI 3.x reads record type IDs such as ``RecordFactory``'s ``sid`` fields
with ``Field.getShort``. Java reflection reads ``static final`` fields
through ``Unsafe.getShortVolatile``, which the CheerpJ browser JVM does
not implement, so loading any ``.xls`` workbook fails with
``UnsatisfiedLinkError``. Without ``final`` the same call uses
``Unsafe.getShort``, which CheerpJ supports.

This script copies the JAR, clears ``ACC_FINAL`` on every
``static final short`` field in ``org/apache/poi`` classes, and drops the
original code signature (it no longer matches the modified classes). No
other bytes change. The original JAR is left untouched for Java Web Start.

Usage: patch_poi_for_cheerpj.py SOURCE.jar DEST.jar
"""

import struct
import sys
import zipfile

ACC_STATIC = 0x0008
ACC_FINAL = 0x0010

# Constant pool entry sizes (excluding the tag byte) for fixed-size tags.
CP_SIZES = {3: 4, 4: 4, 5: 8, 6: 8, 7: 2, 8: 2, 9: 4, 10: 4, 11: 4,
            12: 4, 15: 3, 16: 2, 17: 4, 18: 4, 19: 2, 20: 2}


def patch_class(data):
    """Return (patched bytes, number of fields changed)."""
    data = bytearray(data)
    if data[:4] != b"\xca\xfe\xba\xbe":
        return bytes(data), 0
    count = struct.unpack_from(">H", data, 8)[0]
    utf8 = {}
    pos, index = 10, 1
    while index < count:
        tag = data[pos]
        if tag == 1:
            length = struct.unpack_from(">H", data, pos + 1)[0]
            utf8[index] = bytes(data[pos + 3:pos + 3 + length])
            pos += 3 + length
        else:
            pos += 1 + CP_SIZES[tag]
        index += 2 if tag in (5, 6) else 1
    pos += 6  # access_flags, this_class, super_class
    interfaces = struct.unpack_from(">H", data, pos)[0]
    pos += 2 + 2 * interfaces
    fields = struct.unpack_from(">H", data, pos)[0]
    pos += 2
    changed = 0
    for _ in range(fields):
        flags, _name, desc, attrs = struct.unpack_from(">HHHH", data, pos)
        if (utf8.get(desc) == b"S"
                and flags & (ACC_STATIC | ACC_FINAL) == ACC_STATIC | ACC_FINAL):
            struct.pack_into(">H", data, pos, flags & ~ACC_FINAL)
            changed += 1
        pos += 8
        for _ in range(attrs):
            length = struct.unpack_from(">I", data, pos + 2)[0]
            pos += 6 + length
    return bytes(data), changed


def main(source, dest):
    total_fields = total_classes = 0
    with zipfile.ZipFile(source) as src, \
            zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src.infolist():
            name = info.filename
            upper = name.upper()
            if upper.startswith("META-INF/") and upper.endswith(
                    (".SF", ".RSA", ".DSA", ".EC")):
                continue
            data = src.read(info)
            if upper == "META-INF/MANIFEST.MF":
                data = b"Manifest-Version: 1.0\r\n\r\n"
            elif name.startswith("org/apache/poi/") and name.endswith(".class"):
                data, changed = patch_class(data)
                if changed:
                    total_classes += 1
                    total_fields += changed
            out.writestr(info, data)
    print(f"{dest}: cleared final on {total_fields} static short fields "
          f"in {total_classes} classes; signature removed")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
