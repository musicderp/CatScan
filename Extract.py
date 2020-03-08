from Hashing import process_images
from Hashing import chunk
from Hashing import hamming
from multiprocessing import Pool
from multiprocessing import cpu_count
from imutils import paths
import numpy as np
import pickle
import os
import vptree

processThreads = 8
if __name__ == "__main__":

    procs = processThreads if processThreads > 0 else cpu_count()
    procIDs = list(range(0, procs))

    print("[INFO] grabbing image paths...")
    allImagePaths = sorted(list(paths.list_images('images/')))
    numImagesPerProc = len(allImagePaths) / float(procs)
    numImagesPerProc = int(np.ceil(numImagesPerProc))

    chunkedPaths = list(chunk(allImagePaths, numImagesPerProc))

    payloads = []

    for (i, imagePaths) in enumerate(chunkedPaths):
        outputPath = os.path.sep.join(["pickles/", "proc_{}.pickle".format(i)])

        data = {
            "id": i,
            "input_paths": imagePaths,
            "output_path": outputPath
        }
        payloads.append(data)

    print("[INFO] launching pool using {} processes...".format(procs))
    pool = Pool(processes=procs)
    pool.map(process_images, payloads)

    print("[INFO] waiting for processes to finish...")
    pool.close()
    pool.join()
    print("[INFO] multiprocessing complete")

    print("[INFO] combining hashes...")
    hashes = {}

    for p in paths.list_files('pickles/', validExts=(".pickle"), ):

        data = pickle.loads(open(p, "rb").read())

        for (tempH, tempPaths) in data.items():
            imagePaths = hashes.get(tempH, [])
            imagePaths.extend(tempPaths)
            hashes[tempH] = imagePaths

    print("[INFO] serializing hashes...")
    f = open('hashes/hashes.pickle', "wb")
    f.write(pickle.dumps(hashes))
    f.close()

    points = list(hashes.keys())
    tree = vptree.VPTree(points, hamming)

    print("[INFO] serializing VP-Tree...")
    f = open('hashes/tree.pickle', "wb")
    f.write(pickle.dumps(tree))
    f.close()
