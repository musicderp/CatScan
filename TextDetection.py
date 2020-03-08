from imutils.object_detection import non_max_suppression
import numpy as np
import time
import cv2
import os
# for every file in directory, does text detection. if text is found, image deleted. if text is not,
# moved to /images/processed/
directory = 'images/raw'
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    print(path)
    if path[-3:] != "jpg":
        print("file is not a jpg smh")
    else:
        image = cv2.imread(path)
        orig = image.copy()
        (H, W) = image.shape[:2]

        (newW, newH) = (320, 320)
        rW = W / float(newW)
        rH = H / float(newH)

        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]

        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        print("[INFO] loading EAST text detector...")
        net = cv2.dnn.readNet("frozen_east_text_detection.pb")

        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        start = time.time()
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        end = time.time()

        print("[INFO] text detection took {:.6f} seconds".format(end - start))

        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []
        print(confidences)

        for y in range(0, numRows):

            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(0, numCols):

                if scoresData[x] < .5:
                    continue

                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        boxes = non_max_suppression(np.array(rects), probs=confidences)
        if boxes == []:
            os.rename(path, os.path.join("images/processed", filename))
        else:
            os.remove(path)
