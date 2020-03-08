# import the necessary packages
from Hashing import convert_hash
from Hashing import dhash
import pickle
import time
import cv2


print("[INFO] loading VP-Tree and hashes...")
tree = pickle.loads(open('hashes/tree.pickle', "rb").read())
hashes = pickle.loads(open('hashes/hashes.pickle', "rb").read())

image = cv2.imread('images/raw/vh6ny97uocl41.jpg')
cv2.imshow("Query", image)

queryHash = dhash(image)
queryHash = convert_hash(queryHash)


print("[INFO] performing search...")
start = time.time()
results = tree.get_all_in_range(queryHash, 10)
results = sorted(results)
end = time.time()
print("[INFO] search took {} seconds".format(end - start))


for (d, h) in results:

    resultPaths = hashes.get(h, [])
    print("[INFO] {} total image(s) with d: {}, h: {}".format(
        len(resultPaths), d, h))

    for resultPath in resultPaths:

        result = cv2.imread(resultPath)
        cv2.imshow("Result", result)
        cv2.waitKey(0)
