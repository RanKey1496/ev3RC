import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, image_np = cap.read()
    frame = cv2.flip(image_np, 1)
    cv2.imshow('Camera Jimbo', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break