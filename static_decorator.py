import cv2



class StaticDecorator:

    def __init__(self):
        pass

    def putText(img, text, org, fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=1.,color=[0,0,255],):
        img = cv2.putText(img, text, org, fontFace, fontScale, color, thickness=1, lineType=8, bottomLeftOrigin=False)
        return img