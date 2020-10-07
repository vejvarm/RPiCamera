import io
import socket
import struct
import cv2 as cv
import pylab as pl

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.1.30', 8000))
server_socket.listen(0)


if __name__ == '__main__':
    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    img = None
    # pl.axis([-50, 50, 0, 10000])
    pl.ion()
    pl.show()

    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            file_bytes = pl.asarray(bytearray(image_stream.read()), dtype=pl.uint8)  # convert to numpy byte-like array
            image = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
            print(f'Image is {image.shape[0]}x{image.shape[1]}x{image.shape[2]}')
            if img is None:
                img = pl.imshow(image)
            else:
                img.set_data(image)
            pl.pause(0.0001)
            # image.verify()
            # print('Image is verified')
    finally:
        pl.show()
        connection.close()
        server_socket.close()