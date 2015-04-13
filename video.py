class DummyCap():
    def __init__(self):
        pass

    def capture(self):
        pass

    def publish(self):
        pass

class VidCapture():
    def __init__(self, surface, rate, filename):
        # evil trick to let people use game without cv
        global pygame
        import pygame
        global cv2
        import cv2
        global cv
        import cv2.cv as cv
        global np
        import numpy as np
        self.surface = surface
        self.rate = rate
        self.count = 0

        frame_rate = 60.0 / rate
        # normal game speed is 60fps

        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.writer = cv2.VideoWriter(filename, fourcc, frame_rate, self.surface.get_size())

    def capture(self):
        if(self.count == 0 and self.writer):
            img_str = pygame.image.tostring(self.surface, 'RGB')
            cv_image = cv.CreateImageHeader(self.surface.get_size(), cv.IPL_DEPTH_8U, 3)
            cv.SetData(cv_image, img_str)
            self.writer.write(np.asarray(cv_image[:,:]))
        self.count = (self.count + 1) % self.rate

    def publish(self):
        if(self.writer):
            self.writer.release()
            self.writer = None
        print "done"

    def __del__(self):
        self.publish()
