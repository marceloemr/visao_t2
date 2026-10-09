import numpy as np
import cv2 as cv
import glob

## codigo de https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#flags = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE

ver_corners = 6
hor_corners = 9

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((ver_corners*hor_corners,3), np.float32)
objp[:,:2] = np.mgrid[0:ver_corners,0:hor_corners].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('imagens/2026*.jpg')

for fname in images:
    print(f"lendo imagem {fname}")
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (ver_corners,hor_corners), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        #cv.drawChessboardCorners(img, (ver_corners,hor_corners), corners2, ret)
        #cv.imshow('img', img)
        #cv.waitKey()

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv.imread('imagens/sem_tabuleiro.jpg') # preciso escolher uma imagem
#h,  w = img.shape[:2]
#newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
#
#dst = cv.undistort(img, mtx, dist, None, newcameramtx)
#
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
#cv.imshow('img calibrada', dst)
#cv.waitKey()

rvec_ref = rvecs[0]
tvec_ref = tvecs[0]

while True:
    try:
        user_input = input("Coordenada 3D: ").strip()

        if not user_input:
            break

        coords = [float(x) for x in user_input.split()]

        if len(coords) != 3:
            print("Erro: Digite exatamente três valores (X, Y e Z). Tente novamente.")
            continue

        X, Y, Z = coords

        point_3d = np.array([[[X, Y, Z]]], dtype=np.float32)
        projected_pts, _ = cv.projectPoints(point_3d, rvec_ref, tvec_ref, mtx, dist)
        pt_2d = (int(projected_pts[0][0][0]), int(projected_pts[0][0][1]))
        img_display = img.copy()

        cv.circle(img_display, pt_2d, 8, (0, 0, 255), -1)
        cv.putText(
            img_display,
            f"P({X}, {Y}, {Z})",
            (pt_2d[0] + 15, pt_2d[1] - 15),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        print(f"{X} {Y} {Z} -> {pt_2d[0]} {pt_2d[1]}")
        cv.imshow('Projecao 3D para 2D', img_display)
        cv.waitKey()

    except Exception as e:
        print(e)

cv.destroyAllWindows()
