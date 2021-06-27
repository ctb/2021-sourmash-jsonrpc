import sourmash
from remote_index import RemoteIndex

ss = sourmash.load_one_signature('podar-ref/1.sig.gz', ksize=31)

remote = RemoteIndex('http://localhost:5000')
remote = remote.select(ksize=31)

print(remote.search(ss, threshold=0.0))
