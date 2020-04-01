import cv2
import numpy as np 
from copy import deepcopy

class DrawingScreen():
    def __init__(self, img=None):
        self.drawing = False
        self.pt1_x = None
        self.pt1_y = None
        self.brush_size = 30
        self.set_image(img)
        self.mask_color = 0

    def set_image(self, img):
        if img is not None:
            self.image = img
        else:
            self.image = np.zeros((300, 300, 3), np.uint8)
        self.masked_image = deepcopy(self.image)
        self.mask = 255 * np.ones(self.image.shape[:2], np.uint8)

    def line_drawing(self,event,x,y,flags,param):
        # start drawing on mouse press
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
            self.drawing = True
            self.pt1_x = x
            self.pt1_y = y
            self.mask_color = 0 if event == cv2.EVENT_LBUTTONDOWN else 255

        # keep drawing unless mouse is released
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing==True:
                cv2.line(self.mask, (self.pt1_x, self.pt1_y), (x,y),
                    color=self.mask_color, thickness = self.brush_size)
                self.masked_image = cv2.bitwise_or(self.image, self.image, mask=self.mask)
                self.pt1_x = x
                self.pt1_y = y

        # finish drawing on mouse release
        elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
            self.drawing = False
            cv2.line(self.mask, (self.pt1_x, self.pt1_y), (x,y),
                color=self.mask_color, thickness = self.brush_size)
            self.masked_image = cv2.bitwise_or(self.image, self.image, mask=self.mask)


    def increase_brush(self):
        new_size = self.brush_size + 5
        if new_size < 150:
            self.brush_size = new_size
            print("[INFO] brush size increased to {}".format(new_size))

    def decrease_brush(self):
        new_size = self.brush_size - 5
        if new_size > 5:
            self.brush_size = new_size
            print("[INFO] brush size decreased to {}".format(new_size))

    def save_mask(self, filename=None):
        if filename is None:
            filename = "mask.png"

        transp_mask = cv2.merge([self.mask, self.mask, self.mask, 255 - self.mask])
        cv2.imwrite(filename, transp_mask)

        print("[INFO] saving file to {}".format(filename))

    def clear(self):
        self.mask = 255 * np.ones(self.image.shape[:2], np.uint8)
        self.masked_image = deepcopy(self.image)
        print("[INFO] mask cleared")
        
    def show_image(self, target_window):
        cv2.imshow(target_window, self.masked_image)

if __name__ == "__main__":
    import os
    import argparse

    def get_help():
        print("[INFO] help tips for {}".format(os.path.basename(__file__)))
        print("  Paint negative mask on top of an image with right click, erase with right click")
        print()
        print("  hotkeys:")
        print("  <h> - get this help tip")
        print("  <q> - quit window")
        print("  <s> - save mask to chosen path")
        print("  <c> - clear mask")
        print("  <+> - increase brush size")
        print("  <-> - decrease brush size")
        print()
    
    # parse arguments
    ag = argparse.ArgumentParser()
    ag.add_argument("-f", "--file", required=True,
        help="path to input video or image file")
    ag.add_argument("-m", "--mask", default=None,
        help="path to output mask image")
    ag.add_argument("-o", "--offset", default=0,
        help="offset frame to do draw the mask on whe the video is input")
    args = vars(ag.parse_args())

    # mask name
    maskfile = args["mask"]
    if maskfile is None:
        maskfile = args["file"].rsplit(".", 1)[0] + "_mask.png"

    # try read the file as an image
    bg_image = cv2.imread(args["file"])
    if bg_image is None:
        # try extract frame from video
        vidcap = cv2.VideoCapture(args["file"])
        for i in range(args["offset"] + 1):
            _, bg_image = vidcap.read()

    # create window
    WINDOW_NAME = "draw mask"
    cv2.namedWindow(WINDOW_NAME)
    cv2.startWindowThread()
    
    # display input options
    get_help()

    # start drawing part
    ds = DrawingScreen(img=bg_image)
    cv2.setMouseCallback(WINDOW_NAME, ds.line_drawing)

    # start drawing loop
    while(True):
        ds.show_image(WINDOW_NAME)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        if k == ord("s"):
            ds.save_mask(filename=maskfile)
        if k == ord("c"):
            ds.clear()
            ds.show_image(WINDOW_NAME)
        if k == ord("+"):
            ds.increase_brush()
        if k == ord("-"):
            ds.decrease_brush()
        if k == ord("h"):
            get_help()
        if cv2.getWindowProperty(WINDOW_NAME, 1) < 0:
            break

    print("[INFO] Done")
    cv2.destroyAllWindows()
