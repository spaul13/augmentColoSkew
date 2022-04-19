import os, sys, glob, cv2, random
from PIL import Image

parent = "train"
labelList = os.listdir(parent + "/")
skew = int(sys.argv[1])
mode = sys.argv[2]
selective = sys.argv[3]

destDir = parent + "_" + sys.argv[1] + "/"
os.system("mkdir " + destDir)
skew =  skew/100


def convertGrayScale(image, dest):
	img = Image.open(image)
	imgGray = img.convert('L')
	imgGray.save(dest)

def convertGrayScaleCV(image, dest):
	img = cv2.imread(image)
	grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(dest, grayscale)

if selective == "partial":
	selected = ["automobile", "cat", "horse", "truck", "airplane"]
elif selective =="all":
	selected = labelList


for l in labelList:
	imglist = glob.glob(parent + "/" + l + "/*.jpg")
	if l in selected:
		selectNum = int(len(imglist)*skew)
	else:
		selectNum = int(len(imglist)*(1-skew))
		 
	if mode == "random":
		picgraylist = random.sample(imglist, selectNum)
	elif mode == "fixed":
		picgraylist = imglist[0:selectNum]
	
	piccolorlist = list(set(imglist) - set(picgraylist))

	os.system("mkdir " + destDir + l)

	for p in picgraylist:
		dest = destDir + l + "/" + p.split("/")[-1]
		convertGrayScale(p,dest)
	
	for p in piccolorlist:
		dest = destDir + l + "/" + p.split("/")[-1]
		os.system("scp " + p + " " + dest)
