'''
reference:
Buchanan, C., Ip, T., Mabbitt, A., May, B., & Mound, D. (2015). 
Python web penetration testing cookbook: Over 60 indispensable Python recipes 
to ensure you always have the right code on hand for web application testing. 
Birmingham: Packt Publishing.

functions by phil: LSB,getLSB, hide, seek, part of the main
'''
from PIL import Image
import cv2

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np


'''
This is the future portion to remove non utf-8 characters from the user's message.
from unidecode import unidecode

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))
'''


#Least significant bit converter.
def LSB( pixVal, bit ):
    if bit == '1':
        pixVal = pixVal | 1 #00000001
    else:
        pixVal = pixVal & 254 #11111110
    return pixVal

#Returns the LSB to be appended to the binary string.
def getLSB( pixVal ):
    if pixVal & 1 == 0:
        return '0' 
    else:
        return '1'
    
#Yup, hide n seek time.
def hide(inFile, secretMess):
    secretMess = secretMess + chr(0) #Optional maker for the end of message. A random character could be used in the future.
    hiddenPixList = []#Store the new data.          
    img = Image.open( inFile )
    img = img.convert('RGBA') #Four values per pixel
    pixList = list( img.getdata() )#inFile image is converted to a list.Sweet.
        
    for i in range( len( secretMess ) ):
        asciiChar = ord( secretMess[i] )#Message char element converted to ascii.
        binaryChar = bin( asciiChar ) [2:] .zfill( 8 )#
           
        #Two separate lists keep the bits from alternating if they were stored in one list.
        hidePixEven = [] #contains bits 0-3
        hidePixOdd = []  #contains bits 4-7
            
        pixEven = pixList[ i*2 ]    #Two pixels per binary number
        pixOdd = pixList[ (i*2) +1 ]  
            
        for k in range( 0, 4 ):
            #Changes the LSB of pixEven/pixOdd to the corresponding bit.
            hidePixEven.append( LSB( pixEven[k], binaryChar[k] ) )
            hidePixOdd.append( LSB( pixOdd[k], binaryChar[ k+4 ] ) )    
        #Convert list to Tuple of 3
        hpeTuple = tuple( hidePixEven )
        hpoTuple = tuple( hidePixOdd )
        #Adds the tuple value to the list
        hiddenPixList.append( hpeTuple )
        hiddenPixList.append( hpoTuple )
    unusedImgPart = pixList[ len(secretMess) *2: ]  #Splice n Dice the original image list.
    hiddenPixList.extend( unusedImgPart )#Adds the rest of the unused image list to the hidden test list.
    newImg = Image.new( img.mode,img.size )
    newImg.putdata( hiddenPixList )
    newImg.save('hiddenImage.png')
    print("Success.")       

#Extract text message from image.
def seek(hideFile):
    pixList=[]
    hiddenImg = Image.open(hideFile)
    #
    hiddenImg = hiddenImg.convert('RGBA')
    pixList = list( hiddenImg.getdata() )
    #LSB are adding to the binary string
    messBinary ='0b'   
    decodeMess = ""
    bitCount = 0
    i=0
    
    while (messBinary != '0b00000000'):
        if bitCount == 8:
            #2 to 8 element in the binary string is converted to ascii int.
            #Ascii value is converted to char and added to the text String.
            decodeMess += chr(int(messBinary,2))
            #Reset the binary message variable .
            messBinary = '0b'
            #Reset the bit counter for the next binary string
            bitCount = 0
        #3-tuple value: RGB  
        tupleVal = pixList[i]
        #Retrieving the LSB from the RGB value
        for item in tupleVal:
            messBinary += getLSB(item)
            bitCount += 1    
        i+= 1#Onto the next element
      
    print("Your secret message: ")
    print( decodeMess )
'''
#Work in progress...
def hideImage( file1, file2):
    turkey = cv2.imread(file1)
    stuffing = cv2.imread(file2)
    wide, tall, channel = turkey.shape
    w2, t2, ch2 = stuffing.shape
    
    stuffing = cv2.resize(stuffing, (tall, wide) )
    stuffing = cv2.cvtColor(stuffing, cv2.COLOR_BGR2GRAY)
    cv2.imshow('altered file2',stuffing)
    cv2.imshow('file1', turkey)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    for x in range( 0, wide ):
        for y in range( 0, tall):
            bwVal = stuffing.item(x,y)
            redVal = turkey.item(x,y,2) #opencv BGR
            
            if bwVal == 0:
                newRed = redVal & 254
            else:
                newRed = redVal | 1
            turkey.itemset((x, y,2), newRed)  
    cv2.imshow('merged images', turkey )
    cv2.imshow('original', cv2.imread(file1))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('savedMerged.png', turkey )
       
#Work in progress...            
def separateImage(inFile, originalWide, originalHeight, ch ):
    turkey = cv2.imread(inFile)
    wide, tall, channel = turkey.shape 
    #http://stackoverflow.com/questions/9710520/opencv-createimage-function-isnt-working
    #Thanks David for the advice about the immutable numpy array.
    image = np.zeros(( tall, wide, ch ), np.uint8)
    #not sure if this is needed. Does cv2 store the image as a numpy array?
    cv2.imwrite('blank.png', image)
    blankIm = cv2.imread('blank.png')
         
    for x in range( 0, wide ):
        for y in range( 0, tall):
            bluValT, greValT, redValT = turkey.item(x,y)
                
'''    
#This is a check to see if the correct image is being processed.
def seeBoth( inFile, hideFile ):
    imBefore = cv2.imread(inFile)
    imAfter = cv2.imread(hideFile)
    cv2.imshow('Before', imBefore)
    cv2.imshow('After', imAfter)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  
#main
root = Tk()
#These are to be used in the hiding/removing image from an image.
#global w2, t2, ch2

while( True ):
    print("Steganography")
    print("1. Encrypt Text")
    print("2. Decrypt Text")
    print("3. Compare before & after")
    print("4. Exit")
    choice = input("Enter your poison: ")
    if choice == '1':
        #http://stackoverflow.com/questions/11664443/raw-input-across-multiple-lines-in-python
        print("Enter your secret mess")
        #Adds a sentinel value to the end of the user's message:'team48' 
        secretMess=''+ '\n'.join(iter(input, 'team48' ))
        #Use Tk to select image to hide the text message into.
        print("Select your image: ")
        inFile = askopenfilename()
        print (inFile)
        root.withdraw()
        #Merginig message
        hide( inFile, secretMess )
    elif choice == '2':
        #Use Tk to select image to remove the text message from.
        print("Select your image: ")
        hideFile = askopenfilename()
        #Removing message
        seek( hideFile )
    elif choice == '3':
        #Before and after comparison.
        seeBoth( inFile, hideFile )
    elif choice == '4':
        #End program
        print("Sbohem -goodbye in czech")
        break
    elif choice =='5':
        #Work in progress. Hiding image in an image is completed. Pil usage
        file1 = 'Star-Wars-Darth-Vader-Wallpaper.png'
        file2 = 'star-wars-yoda-spinoff-film.png'
        #hideImage( file1, file2 )
    elif choice =='6':
        #Work in progress. Removing image from image. opencv2 usage
        print("Select your image: ")
        inFile = askopenfilename()
        print (inFile)
        root.withdraw()
        #separateImage( inFile, w2, t2, ch2 )
    


    
    

