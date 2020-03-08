# import the necessary packages
from Hashing import convert_hash
from Hashing import hamming
from Hashing import dhash
from imutils import paths
import pickle
import vptree
import cv2


imagePaths = list(paths.list_images('images'))
hashes = {}

for (i, imagePath) in enumerate(imagePaths):

    print("[INFO] processing image {}/{}".format(i + 1,
                                                 len(imagePaths)))
    image = cv2.imread(imagePath)

    h = dhash(image)
    h = convert_hash(h)

    l = hashes.get(h, [])
    l.append(imagePath)
    hashes[h] = l

print("[INFO] building VP-Tree...")
points = list(hashes.keys())
tree = vptree.VPTree(points, hamming)


print("[INFO] serializing VP-Tree...")
f = open('hashes/tree.pickle', "wb")
f.write(pickle.dumps(tree))
f.close()

print("[INFO] serializing hashes...")
f = open('hashes/hashes.pickle', "wb")
f.write(pickle.dumps(hashes))
f.close()
