# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\motion_estimation_service.py
#! /usr/bin/env python3

import einops
import numpy as np
import torch

alpha = 1


class OFEstimator:
    def estimate(self, vid_arr):  # vidarr: t h w c (0-255)
        plan = 3
        if plan == 1:
            return self.op.predict_batch_based_on_first_frame(vid_arr)
        elif plan == 2:
            from service.optical_flow import optical_flow_client

            return optical_flow_client.predict(vid_arr)
        elif plan == 3:
            import cv2

            prev_frame = vid_arr[:-1]
            next_frame = vid_arr[1:]
            # func = lambda x: einops.rearrange(x, 't h w c -> (b t) h w c').type(torch.uint8).detach().cpu().numpy()
            func = lambda x: x.type(torch.uint8).detach().cpu().numpy()
            prev_frame = func(prev_frame)
            next_frame = func(next_frame)

            flows = []
            for p, n in zip(prev_frame, next_frame):
                prev_gray = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)
                next_gray = cv2.cvtColor(n, cv2.COLOR_BGR2GRAY)
                sparse = False

                if not sparse:
                    flow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                else:
                    # params for ShiTomasi corner detection
                    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

                    # Parameters for lucas kanade optical flow
                    lk_params = dict(
                        winSize=(15, 15),
                        maxLevel=3,
                        criteria=(
                            cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                            10,
                            0.03,
                        ),
                    )

                    p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

                    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, next_gray, p0, None, **lk_params)
                    return p1

                flow = einops.rearrange(flow, "h w two -> two h w")
                flows.append(flow)
            flows = np.stack(flows, axis=1)
            return flows
            # flows = torch.from_numpy(flows).unsqueeze(0).cuda()
            # out = flows
            # return out

    def flow2magnitude(self, flow):
        flow_x, flow_y = flow[0, ...], flow[1, ...]
        # flow_x = flow_x / flow.shape[-1]
        # flow_y = flow_y / flow.shape[-2]
        motion_mag = np.sqrt(np.square(flow_x) + np.square(flow_y))
        motion_mag *= 0.1  # 256 * 448 的情况
        motion_mag *= alpha
        # motion_mag /= 1.5
        # import ipdb
        # ipdb.set_trace()

        return motion_mag


def magnitude_to_bucket(magnitude):
    bucket = round(magnitude * 255)
    # assert bucket <= 128
    bucket = min(bucket, 255)
    bucket = max(bucket, 0)
    return bucket
    # if magnitude < 0.1:
    #     return 1
    # elif magnitude < 0.2:
    #     return 2
    # elif magnitude < 0.35:
    #     return 3
    # elif magnitude < 0.55:
    #     return 4
    # elif magnitude < 0.7:
    #     return 5
    # elif magnitude < 0.9:
    #     return 6
    # return 7
    # min_bucket = 1
    # max_bucket = 6
    # min_mag = 0
    # max_mag = 2
    # if magnitude > max_mag:
    #     return max_bucket + 1
    # else:
    #     every = (max_mag - min_mag) / (max_bucket - min_bucket + 1)
    #     return int((magnitude - min_mag) / every) + min_bucket


if __name__ == "__main__":
    test_mag = [i / 10.0 for i in range(30)]
    for t in test_mag:
        print(magnitude_to_bucket(t))


of = OFEstimator()


def get_motion_score(vid):
    flow = of.estimate(vid)
    magnitude = float(np.mean(of.flow2magnitude(flow), axis=(1, 2)).max())
    # magnitude1 = float(of.flow2magnitude(flow).mean())

    # print()
    # print()
    # print()
    # print('magnitude / magnitude1:', magnitude / magnitude1)
    # print()
    # print()
    # print()

    bucket = magnitude_to_bucket(magnitude)
    return bucket
