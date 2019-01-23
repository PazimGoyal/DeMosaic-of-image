import cv2
import numpy as np

#-------------image names 
# name of images you want to load
format1=".bmp"
format2=".jpg"
mosaic="pencils_mosaic"
org="pencils"



#------------PART1

#---image split and seprate R G B pattern Channels

image=cv2.imread(mosaic+format1)
image=np.float32(image)

b,g,r=cv2.split(image)



for i in range(b.shape[0]):
    for j in range(b.shape[1]):
        if i%2 ==0 and j%2 ==0:
           b[i][j]=b[i][j]
        else:
            b[i][j]=0
for i in range(r.shape[0]):
    for j in range(r.shape[1]):
        if i%2 ==0 and j%2 ==1:
           r[i][j]=r[i][j]
        elif i%2 ==1 and j%2 ==0:
           r[i][j]=r[i][j]
        else:
            r[i][j]=0
for i in range(g.shape[0]):
    for j in range(g.shape[1]):
        if i%2 ==1 and j%2 ==1:
           g[i][j]=g[i][j]
        else:
            g[i][j]=0


#---------------------creting Karnels and applying
## 3 X 3 Kernals for images
kb=np.array([[.25,.5,.25],[.5,1,.5],[.25,.5,.25]]) #kb kernal Blue
kg=np.array([[.25,.5,.25],[.5,1,.5],[.25,.5,.25]]) #kg Kernal Green
kr=np.array([[0,.25,0],[.25,1,.25],[0,.25,0]]) #kr Kernal Red



b1 = cv2.filter2D(b,-1, kb) #Blue After Filter 2D
g1 = cv2.filter2D(g,-1, kg) #Green After Filter 2D
r1 = cv2.filter2D(r,-1, kr) #Blue After Filter 2D

img = cv2.merge((b1,g1,r1)) #merge b g r
img=np.uint8(img) # convert float32 to uint8
cv2.imwrite(mosaic+"2"+format1,img) 
cv2.imshow("DUPLICATE IMAGE",img)


#------------------------- Reading Orignal Image , convert to float32 and split
#b2 is Blue Orignal g2 Green Orignal r2 is Red Orignal

imageorg=cv2.imread(org+format2)
imageorg=np.float32(imageorg)
b2,g2,r2=cv2.split(imageorg)



# bo orignal Blue in float32 between 0 and 1 
# bd new created Blue in float32 between 0 and 1
bo=b2/255
go=g2/255
ro=r2/255
bd=b1/255
gd=g1/255
rd=r1/255
bnew=((bo-bd)**2)**.5
gnew=((go-gd)**2)**.5
rnew=((ro-rd)**2)**.5



new=cv2.merge((bnew*255,gnew*255,rnew*255))
new=np.uint8(new)
cv2.imshow("MINUS",new)
cv2.imwrite(mosaic+"Minus"+format1,new)

#---------------------PART 2-------------------------------------
n1=gd-rd
n2=bd-rd  # subtract red channel
n1 = cv2.medianBlur(n1,3) #apply median blur
n2 = cv2.medianBlur(n2,3)
n1=(n1+rd) # add red channel
n2=(n2+rd)
n1=np.clip(n1,0,1) # clip values
n2=np.clip(n2,0,1)
n1=n1*255
n2=n2*255
n3=rd*255
img2 = cv2.merge((n2,n1,n3)) #merge channels
img2=np.uint8(img2) #convert to 0-255
cv2.imshow("METHOD",img2)
cv2.imwrite(mosaic+"3"+format1,img2)

image=np.uint8(image)
cv2.imshow("MOSIAC",image)

#----------------------creating diff image similar as above
b3=((bo-n2/255)**2)**.5
g3=((go-n1/255)**2)**.5
r3=((ro-rd)**2)**.5
new=cv2.merge((b3*255,g3*255,r3*255))
new=np.uint8(new)

cv2.imshow("MINUS2",new)
cv2.imwrite(mosaic+"Minus2"+format1,new)



cv2.moveWindow("MOSIAC", 0, 513)

cv2.imshow("ORIGNAL",np.uint8(imageorg))

cv2.moveWindow("ORIGNAL", 0, 0) 
cv2.moveWindow("DUPLICATE IMAGE", 610, 0)
cv2.moveWindow("MINUS", 610, 513)
cv2.moveWindow("METHOD", 1220, 0)
cv2.moveWindow("MINUS2", 1220, 513)
