# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\mediapipe\torch_pose_util.py
import math
import pdb

# from utils.rotation_transformation import euler_angles_to_matrix
import numpy as np
import torch
import torch.nn.functional as F
from scipy.spatial.transform import Rotation as R


def create_perspective_matrix(aspect_ratio):
    kDegreesToRadians = np.pi / 180.0
    near = 1
    far = 10000
    perspective_matrix = np.zeros(16, dtype=np.float32)

    # Standard perspective projection matrix calculations.
    f = 1.0 / np.tan(kDegreesToRadians * 63 / 2.0)

    denom = 1.0 / (near - far)
    perspective_matrix[0] = f / aspect_ratio
    perspective_matrix[5] = f
    perspective_matrix[10] = (near + far) * denom
    perspective_matrix[11] = -1.0
    perspective_matrix[14] = 1.0 * far * near * denom

    # If the environment's origin point location is in the top left corner,
    # then skip additional flip along Y-axis is required to render correctly.

    perspective_matrix[5] *= -1.0
    return perspective_matrix


def project_points(points_3d, transformation_matrix, pose_vectors, image_shape):
    P = create_perspective_matrix(image_shape[1] / image_shape[0]).reshape(4, 4).T
    P = torch.tensor(P, dtype=points_3d.dtype, device=points_3d.device)
    L, N, _ = points_3d.shape

    projected_points = torch.zeros(
        (L, N, 2), dtype=points_3d.dtype, device=points_3d.device
    )
    for i in range(L):
        points_3d_frame = points_3d[i]
        ones = torch.ones(
            (points_3d_frame.shape[0], 1),
            dtype=points_3d.dtype,
            device=points_3d.device,
        )
        points_3d_homogeneous = torch.cat([points_3d_frame, ones], dim=1)
        transformation = torch.matmul(
            transformation_matrix,
            euler_and_translation_to_matrix(
                pose_vectors[i][:3], pose_vectors[i][3:]
            ).to(transformation_matrix.dtype),
        )
        transformed_points = torch.matmul(
            points_3d_homogeneous, transformation.T
        ).matmul(P.T)
        projected_points_frame = transformed_points[:, :2] / transformed_points[:, 3:4]
        projected_points_frame[:, 0] = (projected_points_frame[:, 0] + 1) * 0.5
        projected_points_frame[:, 1] = (projected_points_frame[:, 1] + 1) * 0.5
        projected_points[i] = projected_points_frame
    return projected_points


def invert_projection(
    projected_points, transformation_matrix, pose_vectors, image_shape
):
    P = create_perspective_matrix(image_shape[1] / image_shape[0])
    P_inv = torch.inverse(P)

    L, N, _ = projected_points.shape
    points_3d = torch.zeros(
        (L, N, 3), dtype=projected_points.dtype, device=projected_points.device
    )

    for i in range(L):
        projected_points_frame = projected_points[i]

        projected_points_frame[:, 0] = (projected_points_frame[:, 0] / 0.5) - 1
        projected_points_frame[:, 1] = (projected_points_frame[:, 1] / 0.5) - 1

        ones = torch.ones(
            (projected_points_frame.shape[0], 1), dtype=projected_points.dtype
        )
        projected_points_homogeneous = torch.cat(
            [projected_points_frame, torch.ones((N, 1), dtype=projected_points.dtype)],
            dim=1,
        )

        transformed_points = torch.matmul(projected_points_homogeneous, P_inv.T)

        transformation_inv = torch.inverse(
            torch.matmul(
                transformation_matrix,
                euler_and_translation_to_matrix(
                    pose_vectors[i][:3], pose_vectors[i][3:]
                ).to(torch.float32),
            )
        )
        points_3d_homogeneous = torch.matmul(transformed_points, transformation_inv.T)

        points_3d_frame = points_3d_homogeneous[:, :3] / points_3d_homogeneous[:, 3:4]
        points_3d[i] = points_3d_frame

    return points_3d


def project_points_with_trans(points_3d, transformation_matrix, image_shape):
    P = create_perspective_matrix(image_shape[1] / image_shape[0])
    L, N, _ = points_3d.shape
    projected_points = torch.zeros(
        (L, N, 2), dtype=points_3d.dtype, device=points_3d.device
    )
    for i in range(L):
        points_3d_frame = points_3d[i]
        ones = torch.ones((points_3d_frame.shape[0], 1), dtype=points_3d.dtype)
        points_3d_homogeneous = torch.cat([points_3d_frame, ones], dim=1)

        transformed_points = torch.matmul(
            points_3d_homogeneous, transformation_matrix.T
        ).matmul(P.T)

        projected_points_frame = transformed_points[:, :2] / transformed_points[:, 3:4]
        projected_points_frame[:, 0] = (projected_points_frame[:, 0] + 1) * 0.5
        projected_points_frame[:, 1] = (projected_points_frame[:, 1] + 1) * 0.5
        projected_points[i] = projected_points_frame

    return projected_points


def euler_angles_to_matrix(euler_angles, convention):
    """
    Convert Euler angles to a rotation matrix.

    Parameters:
    euler_angles (torch.Tensor): a tensor of shape (3,) representing the Euler angles.
    convention (str): a string representing the convention of the Euler angles (e.g., 'XYZ', 'ZYX').

    Returns:
    torch.Tensor: a tensor of shape (3, 3) representing the rotation matrix.
    """
    assert euler_angles.shape == (3,), "Euler angles should be a tensor of shape (3,)"
    assert len(convention) == 3, "Convention should have 3 characters"

    # Get individual angles and ensure same type and device
    device = euler_angles.device
    dtype = euler_angles.dtype
    euler_angles = euler_angles / 180 * math.pi
    x, y, z = euler_angles

    # Calculate rotation matrices for each axis
    cos_x, sin_x = torch.cos(x), torch.sin(x)
    cos_y, sin_y = torch.cos(y), torch.sin(y)
    cos_z, sin_z = torch.cos(z), torch.sin(z)

    R_x = torch.tensor(
        [[1, 0, 0], [0, cos_x, -sin_x], [0, sin_x, cos_x]], dtype=dtype, device=device
    )

    R_y = torch.tensor(
        [[cos_y, 0, sin_y], [0, 1, 0], [-sin_y, 0, cos_y]], dtype=dtype, device=device
    )

    R_z = torch.tensor(
        [[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]], dtype=dtype, device=device
    )

    # Map convention to corresponding rotation matrices
    rotations = {"X": R_x, "Y": R_y, "Z": R_z}

    # Apply rotations according to the convention
    R = rotations[convention[0]]
    for axis in convention[1:]:
        R = torch.mm(rotations[axis], R)

    return R


def euler_and_translation_to_matrix(euler_angles, translation_vector):
    # rotation = torch.tensor(R.from_euler('xyz', euler_angles, degrees=True).as_matrix(), dtype=torch.float32)
    rotation = euler_angles_to_matrix(euler_angles, "XYZ")
    # rotation = euler_to_rotation_matrix(euler_angles)
    matrix = torch.eye(4, dtype=euler_angles.dtype, device=euler_angles.device)
    matrix[:3, :3] = rotation
    matrix[:3, 3] = translation_vector
    return matrix


def matrix_to_euler_and_translation(matrix):
    rotation_matrix = matrix[:3, :3]
    translation_vector = matrix[:3, 3]

    sy = torch.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)

    singular = sy < 1e-6

    if not singular:
        x = torch.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        y = torch.atan2(-rotation_matrix[2, 0], sy)
        z = torch.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        x = torch.atan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        y = torch.atan2(-rotation_matrix[2, 0], sy)
        z = torch.zeros_like(x)

    euler_angles = torch.stack([x, y, z], dim=-1)  # 转换为度数
    return euler_angles, translation_vector


def smooth_pose_seq(pose_seq, window_size=5):
    smoothed_pose_seq = torch.zeros_like(pose_seq)

    for i in range(len(pose_seq)):
        start = max(0, i - window_size // 2)
        end = min(len(pose_seq), i + window_size // 2 + 1)
        smoothed_pose_seq[i] = torch.mean(pose_seq[start:end], dim=0)

    return smoothed_pose_seq


def smooth_pose_seq(pose_seq, window_size=5):
    # 增加一个维度用于卷积 (batch_size, channels, sequence_length)
    pose_seq = pose_seq.unsqueeze(0).permute(0, 2, 1)  # [1, 6, 100]

    # 创建平滑卷积核，每个通道都应用相同的卷积
    kernel = (
        torch.ones(6, 1, window_size, dtype=pose_seq.dtype, device=pose_seq.device)
        / window_size
    )

    # 使用组卷积进行平滑
    smoothed_pose_seq = F.conv1d(pose_seq, kernel, padding=window_size // 2, groups=6)

    # 移除不需要的维度并返回 (output should be [100, 6])
    smoothed_pose_seq = smoothed_pose_seq.squeeze(0).permute(1, 0)

    return smoothed_pose_seq


def lmk_tranform(lmk3d, pose_seq, template_mat):
    trans_mat_list = [
        euler_and_translation_to_matrix(pose_seq[i][:3], pose_seq[i][3:])
        for i in range(len(pose_seq))
    ]
    trans_mat_arr = torch.stack(trans_mat_list)
    trans_mat_inv_frame_0 = torch.linalg.inv(trans_mat_arr[0])
    pose_seq = []

    for i in range(len(trans_mat_arr)):
        pose_mat = trans_mat_inv_frame_0 @ trans_mat_arr[i]
        euler_angles, translation_vector = matrix_to_euler_and_translation(pose_mat)
        pose_seq.append(torch.cat((euler_angles, translation_vector), 0))
    pose_seq = torch.stack(pose_seq)
    pose_seq = smooth_pose_seq(pose_seq)

    projected_vertices = project_points(lmk3d, template_mat, pose_seq, [512, 512])

    return projected_vertices
