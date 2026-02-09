# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\mediapipe\draw_util_refine.py
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2


class FaceMeshVisualizer:
    def __init__(self, forehead_edge=False):
        self.mp_drawing = mp.solutions.drawing_utils
        mp_face_mesh = mp.solutions.face_mesh
        self.mp_face_mesh = mp_face_mesh
        self.forehead_edge = forehead_edge

        DrawingSpec = mp.solutions.drawing_styles.DrawingSpec
        f_thick = 2
        f_rad = 1
        right_iris_draw = DrawingSpec(
            color=(0, 0, 255), thickness=f_thick, circle_radius=f_rad
        )
        right_eye_draw = DrawingSpec(
            color=(10, 200, 180), thickness=f_thick, circle_radius=f_rad
        )
        right_eyebrow_draw = DrawingSpec(
            color=(10, 220, 180), thickness=f_thick, circle_radius=f_rad
        )
        left_iris_draw = DrawingSpec(
            color=(0, 0, 255), thickness=f_thick, circle_radius=f_rad
        )
        left_eye_draw = DrawingSpec(
            color=(180, 200, 10), thickness=f_thick, circle_radius=f_rad
        )
        left_eyebrow_draw = DrawingSpec(
            color=(180, 220, 10), thickness=f_thick, circle_radius=f_rad
        )
        head_draw = DrawingSpec(
            color=(10, 200, 10), thickness=f_thick, circle_radius=f_rad
        )

        mouth_draw_obl = DrawingSpec(
            color=(10, 180, 20), thickness=f_thick, circle_radius=f_rad
        )
        mouth_draw_obr = DrawingSpec(
            color=(20, 10, 180), thickness=f_thick, circle_radius=f_rad
        )

        mouth_draw_ibl = DrawingSpec(
            color=(100, 100, 30), thickness=f_thick, circle_radius=f_rad
        )
        mouth_draw_ibr = DrawingSpec(
            color=(100, 150, 50), thickness=f_thick, circle_radius=f_rad
        )

        mouth_draw_otl = DrawingSpec(
            color=(20, 80, 100), thickness=f_thick, circle_radius=f_rad
        )
        mouth_draw_otr = DrawingSpec(
            color=(80, 100, 20), thickness=f_thick, circle_radius=f_rad
        )

        mouth_draw_itl = DrawingSpec(
            color=(120, 100, 200), thickness=f_thick, circle_radius=f_rad
        )
        mouth_draw_itr = DrawingSpec(
            color=(150, 120, 100), thickness=f_thick, circle_radius=f_rad
        )

        FACEMESH_LIPS_OUTER_BOTTOM_LEFT = [
            (61, 146),
            (146, 91),
            (91, 181),
            (181, 84),
            (84, 17),
        ]
        FACEMESH_LIPS_OUTER_BOTTOM_RIGHT = [
            (17, 314),
            (314, 405),
            (405, 321),
            (321, 375),
            (375, 291),
        ]

        FACEMESH_LIPS_INNER_BOTTOM_LEFT = [
            (78, 95),
            (95, 88),
            (88, 178),
            (178, 87),
            (87, 14),
        ]
        FACEMESH_LIPS_INNER_BOTTOM_RIGHT = [
            (14, 317),
            (317, 402),
            (402, 318),
            (318, 324),
            (324, 308),
        ]

        FACEMESH_LIPS_OUTER_TOP_LEFT = [
            (61, 185),
            (185, 40),
            (40, 39),
            (39, 37),
            (37, 0),
        ]
        FACEMESH_LIPS_OUTER_TOP_RIGHT = [
            (0, 267),
            (267, 269),
            (269, 270),
            (270, 409),
            (409, 291),
        ]

        FACEMESH_LIPS_INNER_TOP_LEFT = [
            (78, 191),
            (191, 80),
            (80, 81),
            (81, 82),
            (82, 13),
        ]
        FACEMESH_LIPS_INNER_TOP_RIGHT = [
            (13, 312),
            (312, 311),
            (311, 310),
            (310, 415),
            (415, 308),
        ]

        FACEMESH_CUSTOM_FACE_OVAL = [
            (176, 149),
            (150, 136),
            (356, 454),
            (58, 132),
            (152, 148),
            (361, 288),
            (251, 389),
            (132, 93),
            (389, 356),
            (400, 377),
            (136, 172),
            (377, 152),
            (323, 361),
            (172, 58),
            (454, 323),
            (365, 379),
            (379, 378),
            (148, 176),
            (93, 234),
            (397, 365),
            (149, 150),
            (288, 397),
            (234, 127),
            (378, 400),
            (127, 162),
            (162, 21),
        ]

        # mp_face_mesh.FACEMESH_CONTOURS has all the items we care about.
        face_connection_spec = {}

        # if self.forehead_edge:
        #     for edge in mp_face_mesh.FACEMESH_FACE_OVAL:
        #         face_connection_spec[edge] = head_draw
        # else:
        #     for edge in FACEMESH_CUSTOM_FACE_OVAL:
        #         face_connection_spec[edge] = head_draw

        for edge in mp_face_mesh.FACEMESH_LEFT_EYE:
            face_connection_spec[edge] = left_eye_draw

        for edge in mp_face_mesh.FACEMESH_LEFT_EYEBROW:
            face_connection_spec[edge] = left_eyebrow_draw

        # for edge in mp_face_mesh.FACEMESH_LEFT_IRIS:
        #    face_connection_spec[edge] = left_iris_draw

        for edge in mp_face_mesh.FACEMESH_RIGHT_EYE:
            face_connection_spec[edge] = right_eye_draw
        for edge in mp_face_mesh.FACEMESH_RIGHT_EYEBROW:
            face_connection_spec[edge] = right_eyebrow_draw
        # for edge in mp_face_mesh.FACEMESH_RIGHT_IRIS:
        #    face_connection_spec[edge] = right_iris_draw

        for edge in FACEMESH_LIPS_OUTER_BOTTOM_LEFT:
            face_connection_spec[edge] = mouth_draw_obl
        for edge in FACEMESH_LIPS_OUTER_BOTTOM_RIGHT:
            face_connection_spec[edge] = mouth_draw_obr
        for edge in FACEMESH_LIPS_INNER_BOTTOM_LEFT:
            face_connection_spec[edge] = mouth_draw_ibl
        for edge in FACEMESH_LIPS_INNER_BOTTOM_RIGHT:
            face_connection_spec[edge] = mouth_draw_ibr
        for edge in FACEMESH_LIPS_OUTER_TOP_LEFT:
            face_connection_spec[edge] = mouth_draw_otl
        for edge in FACEMESH_LIPS_OUTER_TOP_RIGHT:
            face_connection_spec[edge] = mouth_draw_otr
        for edge in FACEMESH_LIPS_INNER_TOP_LEFT:
            face_connection_spec[edge] = mouth_draw_itl
        for edge in FACEMESH_LIPS_INNER_TOP_RIGHT:
            face_connection_spec[edge] = mouth_draw_itr

        self.iris_landmark_spec = {468: right_iris_draw, 473: left_iris_draw}
        self.face_connection_spec = face_connection_spec

    def draw_landmarks(self, image_size, keypoints, L_E=None, R_E=None, normed=False):
        ini_size = [512, 512]
        image = np.zeros([ini_size[1], ini_size[0], 3], dtype=np.uint8)
        new_landmarks = landmark_pb2.NormalizedLandmarkList()
        for i in range(keypoints.shape[0]):
            landmark = new_landmarks.landmark.add()
            if normed:
                landmark.x = keypoints[i, 0]
                landmark.y = keypoints[i, 1]
            else:
                landmark.x = keypoints[i, 0] / image_size[0]
                landmark.y = keypoints[i, 1] / image_size[1]
            landmark.z = 1.0

        self.mp_drawing.draw_landmarks(
            image=image,
            landmark_list=new_landmarks,
            connections=self.face_connection_spec.keys(),
            landmark_drawing_spec=None,
            connection_drawing_spec=self.face_connection_spec,
        )
        image = cv2.resize(image, (image_size[0], image_size[1]))
        if L_E is not None:
            left_iris_x = int(L_E[0] * image_size[0])
            left_iris_y = int(L_E[1] * image_size[1])
            right_iris_x = int(R_E[0] * image_size[0])
            right_iris_y = int(R_E[1] * image_size[1])

            image = cv2.circle(
                img=image,
                center=(left_iris_x, left_iris_y),
                radius=3,
                color=(0, 0, 255),
                thickness=3,
            )
            image = cv2.circle(
                img=image,
                center=(right_iris_x, right_iris_y),
                radius=3,
                color=(0, 0, 255),
                thickness=3,
            )
        return image
