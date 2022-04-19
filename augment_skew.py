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

def checkColor(img):
	image = cv2.imread(img)
	if image.any() != None:
		if len(image.shape)==3:
			return True
		else:
			return False
	else:
		print("can't find " + img)

def convertGrayScale(img, dest):
	img = Image.open(img)
	imgGray = img.convert('L')
	imgGray.save(dest)

if selective == "partial":
	selected = ["automobile", "cat", "horse", "truck", "airplane"]
elif selective =="all":
	selected = labelList


for l in labelList:
	imglist = glob.glob(parent + "/" + l + "/*.jpg")
	#for img in imglist:
	#	if not checkColor(img):
	#		print(img)
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

