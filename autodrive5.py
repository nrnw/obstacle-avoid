#auto drive method using vertical edge detection + auto stop at dark added

import cv2
import numpy as np
import urllib.request
import keyboard



root_url = "http://192.168.8.25"  #ESP url
def sendRequest(url):
	n = urllib.request.urlopen(url) # send request to ESP

def get_data(url):#using this function we can request url(send data) and receive data in single line
	global data
	n = urllib.request.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
	n = n.decode("utf-8") # convert raw html bytes format to string :3
	data = n

#function to rescale image
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def v_edge(im_resized):
	im_strip=im_resized[180:240,0:360]#get the lower strip
	im_gray = cv2.cvtColor(im_strip,cv2.COLOR_BGR2GRAY)
	im_blur = cv2.GaussianBlur(im_gray,(5,5),cv2.BORDER_DEFAULT)#apply gausiaan filter to reduce noise
	sobelx64f = cv2.Sobel(im_blur,cv2.CV_64F,1,0,ksize=3)#take sobel in x-direction
	abs_sobel64f = np.absolute(sobelx64f)#to get both edges -ve values willnot cancel here
	sobel_8u = np.uint8(abs_sobel64f)
	sobel_8u_bgr = cv2.cvtColor(sobel_8u,cv2.COLOR_GRAY2BGR)#making 3 channel to v-stack
	flatten=sobel_8u.sum(axis=0)#sum all columns to one row
	# plt.plot(flatten) #plot the result
	# plt.show()

	#draw max line
	max_val=np.amax(flatten)#find max value
	max_index_col = np.argmax(flatten, axis=0)#find max indice
	#draw line and write max value on image
	im_resized=cv2.line(im_resized,(max_index_col,0),(max_index_col,240),(0,255,0),1)
	im_resized=cv2.putText(im_resized,str(max_val),(5,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

	result=np.vstack((im_resized,sobel_8u_bgr))
	# cv2.imwrite('test.jpg',result)

	return result,max_index_col,max_val


def dark_detector(im_resized):
	im_gray = cv2.cvtColor(im_resized,cv2.COLOR_BGR2GRAY)
	ret1,th1 = cv2.threshold(im_gray,20,255,cv2.THRESH_BINARY)

	total_px=240*360
	white_px=np.count_nonzero(th1 == 255)#255
	black_px=np.count_nonzero(th1 == 0)#0

	black_perc=(black_px/total_px)*100
	white_perc=(white_px/total_px)*100

	return black_perc,white_perc

def fourier(im_resized):

	im_gray = cv2.cvtColor(im_resized,cv2.COLOR_BGR2GRAY)

	f = np.fft.fft2(im_gray)
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = 20*np.log(np.abs(fshift))

	h,w=np.shape(magnitude_spectrum)
	b=2 #thickness of mask in pixels
	magnitude_spectrum[int(h/2)-b:int(h/2)+b,:]=0
	magnitude_spectrum[:,int(w/2)-b:int(w/2)+b]=0


	ret1,th1 = cv2.threshold(magnitude_spectrum,220,255,cv2.THRESH_BINARY)
	cv2.imshow('fourier',th1)

	white_count=np.count_nonzero(th1 == 255)#255

	return white_count

cap = cv2.VideoCapture("http://192.168.8.20:8082/videofeed")#open w8 camera feed

cv2.namedWindow('result', cv2.WINDOW_NORMAL)

get_data(root_url+"/0x0xFWD")
while True:
	ret,im = cap.read()
	im_resized=rescale_frame(im)
	result,max_index_col,max_val=v_edge(im_resized)#edge analysis
	black_perc,white_perc=dark_detector(im_resized)#dark detection to stop
	white_count=fourier(im_resized)

	cv2.imshow('result',result)

	IMU_data=data.split('x', -1)
	IMU_data=[float(i) for i in IMU_data]
	IMU_data=np.array(IMU_data)

	if (abs(IMU_data[5])<10):#flow valid only with no rotation
		pass
	else:
		# max_val=0
		pass
	control=1#To on off control for debugging
	keypress=keyboard.is_pressed('up') or keyboard.is_pressed('down') or keyboard.is_pressed('left') or keyboard.is_pressed('right') or keyboard.is_pressed('space')
	if(keypress==True):
		control=0

	if((black_perc>80 or white_count==0) and keypress==0 ):#at dark stop the robot
		sendRequest(root_url+"/0x0xSTOP")
		control=0




	if (control==True):
		if (max_index_col<180 and max_val>1000):#turn right
			get_data(root_url+"/1023x1023xRIGHT")
		elif (max_index_col>180 and max_val>1000):#turn left
			get_data(root_url+"/1023x1023xLEFT")
		else:
			get_data(root_url+"/900x900xFWD")

	if cv2.waitKey(1) == 27:
	    break


cv2.destroyAllWindows()
cap.release()
sendRequest(root_url+"/0x0xSTOP")
