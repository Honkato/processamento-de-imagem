import cv2

if __name__ == '__main__':
    img = cv2.imread("geraldo_ruido.png")

    media = cv2.blur(img, (5,5))

    cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    cv2.namedWindow("media", cv2.WINDOW_NORMAL)

    cv2.imshow("original", img)
    cv2.imshow("media", media)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()