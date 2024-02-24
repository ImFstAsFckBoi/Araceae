"""
A simple wrapper  class providing a common interface for
reading image frames from different video sources.
- `vcfile`: Video file (`cv2.VideoCapture`)
- `vccamera`: Raspberry pi camera (`Picamera2`)
"""

import cv2
from nptyping import NDArray


class LastFrameException(Exception):
    ...


class vccommon:
    """Base class for the VC api."""
    def __init__(self):
        """Initialize the video resource."""
        raise NotImplementedError()

    def read(self) -> NDArray:
        """Read one frame from the video source.
        When frames are exhausted, a LatFrameException will be raised."""
        raise NotImplementedError()

    def __del__(self):
        """Release the video resource"""
        ...


class vcfile(vccommon):
    def __init__(self, file: str):
        self.__vc = cv2.VideoCapture(file)

    def read(self) -> NDArray:
        ret, im = self.__vc.read()
        if not ret:
            raise LastFrameException('Could not read')
        return im

    def __del__(self):
        self.__vc.release()


try:
    from picamera2 import Picamera2  # type: ignore

    class vccamera(vccommon):  # type: ignore
        def __init__(self):
            self.__cam = Picamera2()
            self.__cam.start()

        def read(self) -> NDArray:
            im = self.__cam.capture_array()
            return cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

        def __del__(self):
            self.__cam.close()
            print('Closing capture')

except ImportError:
    class vccamera(vccommon):  # type: ignore
        def __init__(self):
            raise NotImplementedError(
                'Pi camera not available. '
                + 'Check your platform or systems packages.')
