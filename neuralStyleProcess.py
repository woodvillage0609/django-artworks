# USAGE
# python neural_style_transfer.py --image images/baden_baden.jpg --model models/instance_norm/starry_night.t7

# import the necessary packages
# import argparse
import imutils
import time
import cv2
#own
import os
import numpy as np
# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--model", required=True,
# 	help="neural style transfer model")
# ap.add_argument("-i", "--image", required=True,
# 	help="input image to apply neural style transfer to")
# args = vars(ap.parse_args())

# load the neural style transfer model from disk
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def neuralStyleTransfer(image, action):
	
	# print("[INFO] loading style transfer model...")
	target = os.path.join(APP_ROOT, 'models/')

	if action == 'UDNIE':
		output = net = cv2.dnn.readNetFromTorch(target + 'udnie.t7')
	elif action == 'CANDY':
		net = cv2.dnn.readNetFromTorch(target + 'candy.t7')
	elif action == 'MOSAIC':
		net = cv2.dnn.readNetFromTorch(target + 'mosaic.t7')
	elif action == 'PINK':
		net = cv2.dnn.readNetFromTorch(target + 'pink_style_1800.t7')
	elif action == 'SCREAM':
		net = cv2.dnn.readNetFromTorch(target + 'the_scream.t7')
	elif action == 'LA_MUSE':
		net = cv2.dnn.readNetFromTorch(target + 'la_muse.t7')
	elif action == 'FIRE':
		net = cv2.dnn.readNetFromTorch(target + 'Fire_Style_22000_Iterations.t7')
	elif action == 'FLAME':
		net = cv2.dnn.readNetFromTorch(target + 'flame_style_4500.t7')
	elif action == 'RAIN':
		net = cv2.dnn.readNetFromTorch(target + 'rain_style_iter_4000.t7')
	elif action == 'LANDSCAPE':
		net = cv2.dnn.readNetFromTorch(target + 'landscape_style_11600.t7')
	elif action == 'GOLD_BLACK':
		net = cv2.dnn.readNetFromTorch(target + 'gold_black_2700.t7')
	elif action == 'TRIANGLE':
		net = cv2.dnn.readNetFromTorch(target + 'triangle_style_1000.t7')
	elif action == 'STARRY_NIGHT':
		net = cv2.dnn.readNetFromTorch(target + 'starry_night.t7')
	elif action == 'STARRY_NIGHT_2500':
		net = cv2.dnn.readNetFromTorch(target + 'starry_night_2500.t7')
	elif action == 'WAVE':
		net = cv2.dnn.readNetFromTorch(target + 'the_wave.t7')
	elif action == 'FEATHERS':
		net = cv2.dnn.readNetFromTorch(target + 'feathers.t7')
	elif action == 'COMPOSITION':
		net = cv2.dnn.readNetFromTorch(target + 'composition_vii.t7')

	# load the input image, resize it to have a width of 600 pixels, and
	# then grab the image dimensions
	
	# img = cv2.imread(image)
	# img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	img = cv2.cvtColor(image, cv2.IMREAD_COLOR)

	img = imutils.resize(img, width=1600)
	(h, w) = img.shape[:2]

	# construct a blob from the image, set the input, and then perform a
	# forward pass of the network
	blob = cv2.dnn.blobFromImage(img, 1.0, (w, h),
		(103.939, 116.779, 123.680), swapRB=False, crop=False)
	net.setInput(blob)
	# start = time.time()
	output = net.forward()
	# end = time.time()

	# reshape the output tensor, add back in the mean subtraction, and
	# then swap the channel ordering
	output = output.reshape((3, output.shape[2], output.shape[3]))
	output[0] += 103.939
	output[1] += 116.779
	output[2] += 123.680
	output /= 255.0
	output = output.transpose(1, 2, 0)

	# show information on how long inference took
	# print("[INFO] neural style transfer took {:.4f} seconds".format(
	# 	end - start))

	# # show the images
	# cv2.imshow("Output", output)
	# cv2.waitKey(0)

	output = cv2.normalize(output, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

	output = (output * 255).astype(np.uint8)

	output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

	# filename, file_extension = os.path.splitext(filename)
	# print(filename)
	# newFileName = 'processedImg'+ '_' + filename + file_extension
	# cv2.imwrite(output)
	# print(newFileName)
	# print(directoryName)
	return output
	# return newFileName