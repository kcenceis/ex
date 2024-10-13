import base64
import hashlib

import bencodepy


def convert(content):
    metadata = bencodepy.decode(content)
    metadata1 = {}
    for key in metadata.keys():
        key1 = key.decode("utf-8")
        metadata1[key1] = metadata[key]

    hashcontents = bencodepy.encode(metadata1['info'])

    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode("utf-8")
    # 打印
    return 'magnet:?xt=urn:btih:%s' % b32hash
