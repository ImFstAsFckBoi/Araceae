"""
A simple wrapper  class providing a common interface for
reading image frames from different video sources.
- `vcfile`: Video file (`cv2.VideoCapture`)
- `vccamera`: Raspberry pi camera (`Picamera2`)
"""

import cv2
from numpy import zeros, uint8
from nptyping import NDArray
from typing import Protocol, Iterable, Iterator, Any


class LastFrameException(Exception):
    ...


class vccommon(Iterable, Protocol):
    """Base class for the VC api."""
    def __init__(self):
        """Initialize the video resource."""
        ...

    def read(self) -> NDArray:
        """Read one frame from the video source.
        When frames are exhausted, a LatFrameException will be raised."""
        ...

    def vc_object(self) -> Any:
        """Get the underlying video capture object."""
        ...

    def __del__(self) -> None: ...
    def __iter__(self) -> Iterator[NDArray]: ...
    def __next__(self) -> NDArray: ...


class vcfile(vccommon):
    def __init__(self, file: str):
        self.__vc = cv2.VideoCapture(file)

    def read(self) -> NDArray:
        ret, im = self.__vc.read()
        if not ret:
            raise LastFrameException('Could not read')
        return im

    def vc_object(self) -> cv2.VideoCapture:
        return self.__vc

    def __del__(self) -> None:
        self.__vc.release()

    def __iter__(self) -> Iterator[NDArray]:
        return self

    def __next__(self) -> NDArray:
        ret, im = self.__vc.read()
        if not ret:
            raise StopIteration
        return im


class vcnull(vccommon):
    def __init__(self, height: int, width: int, length: int = -1):
        self.__frame = zeros((height, width), dtype=uint8)
        self.__len = length

    def read(self) -> NDArray:
        if self.__len == 0:
            raise LastFrameException
        self.__len -= 1
        return self.__frame

    def vc_object(self) -> NDArray:
        return self.__frame

    def __del__(self) -> None: ...

    def __iter__(self) -> Iterator[NDArray]:
        return self

    def __next__(self) -> NDArray:
        if self.__len == 0:
            raise StopIteration
        self.__len -= 1
        return self.__frame


try:
    from picamera2 import Picamera2  # type: ignore

    class vccamera():  # type: ignore
        def __init__(self):
            self.__cam = Picamera2()
            self.__cam.start()

        def read(self) -> NDArray:
            im = self.__cam.capture_array()
            return cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

        def __del__(self) -> None:
            self.__cam.close()

        def vc_object(self) -> Picamera2:
            return self.__cam

        def __iter__(self) -> Iterator[NDArray]:
            return self

        def __next__(self) -> NDArray:
            return self.read()

except ImportError:
    class vccamera():  # type: ignore
        def __init__(self):
            raise NotImplementedError(
                'Pi camera not available. '
                + 'Check your platform or systems packages.')
