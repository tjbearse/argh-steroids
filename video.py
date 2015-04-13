import pygame
import cv2
import cv2.cv as cv
import numpy as np

class VidCapture():
    def __init__(self, surface, rate):
        self.surface = surface
        self.rate = rate
        self.count = 0

        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.writer = cv2.VideoWriter('video.avi', fourcc, 30, self.surface.get_size())

    def capture(self):
        if(self.count % self.rate == 0 and self.writer):
            img_str = pygame.image.tostring(self.surface, 'RGB')
            cv_image = cv.CreateImageHeader(self.surface.get_size(), cv.IPL_DEPTH_8U, 3)
            cv.SetData(cv_image, img_str)
            self.writer.write(np.asarray(cv_image[:,:]))
            if self.count > 300:
                self.publish()
        self.count += 1

    def publish(self):
        if(self.writer):
            self.writer.release()
            self.writer = None
        print "done"

    def __del__(self):
        self.publish()
