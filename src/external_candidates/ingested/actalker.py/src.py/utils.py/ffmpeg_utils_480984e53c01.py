# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\ffmpeg_utils.py
import cv2
import skvideo

# assert skvideo.__version__ >= "1.1.11"
# skvideo.setFFmpegPath('./ffmpeg')
# skvideo.utils.bpplut['yuva444p12le'] = [4, 48]
import skvideo.io

# install the following packages: #
# conda install -c conda-forge scikit-video ffmpeg  #


class VideoUtils(object):
    def __init__(
        self, video_path=None, output_video_path=None, bit_rate="origin", fps=25
    ):
        if video_path is not None:
            meta_data = skvideo.io.ffprobe(video_path)
            # avg_frame_rate = meta_data['video']['@r_frame_rate']
            # a, b = avg_frame_rate.split('/')
            # fps = float(a) / float(b)
            # fps = 25
            codec_name = "libx264"
            # codec_name = meta_data['video'].get('@codec_name')
            # if codec_name=='hevc':
            #     codec_name='h264'
            # profile = meta_data['video'].get('@profile')
            color_space = meta_data["video"].get("@color_space")
            color_transfer = meta_data["video"].get("@color_transfer")
            color_primaries = meta_data["video"].get("@color_primaries")
            color_range = meta_data["video"].get("@color_range")
            pix_fmt = meta_data["video"].get("@pix_fmt")
            if bit_rate == "origin":
                bit_rate = meta_data["video"].get("@bit_rate")
            else:
                bit_rate = None
            if pix_fmt is None:
                pix_fmt = "yuv420p"

            reader_output_dict = {"-r": str(fps)}
            writer_input_dict = {"-r": str(fps)}
            writer_output_dict = {
                "-pix_fmt": pix_fmt,
                "-r": str(fps),
                "-vcodec": str(codec_name),
            }
            # if bit_rate is not None:
            #     writer_output_dict['-b:v'] = bit_rate
            writer_output_dict["-crf"] = "17"

            # if video has alpha channel, convert to bgra, uint16 to process
            if pix_fmt.startswith("yuva"):
                writer_input_dict["-pix_fmt"] = "bgra64le"
                reader_output_dict["-pix_fmt"] = "bgra64le"
            elif pix_fmt.endswith("le"):
                writer_input_dict["-pix_fmt"] = "bgr48le"
                reader_output_dict["-pix_fmt"] = "bgr48le"
            else:
                writer_input_dict["-pix_fmt"] = "bgr24"
                reader_output_dict["-pix_fmt"] = "bgr24"

            if color_range is not None:
                writer_output_dict["-color_range"] = color_range
                writer_input_dict["-color_range"] = color_range
            if color_space is not None:
                writer_output_dict["-colorspace"] = color_space
                writer_input_dict["-colorspace"] = color_space
            if color_primaries is not None:
                writer_output_dict["-color_primaries"] = color_primaries
                writer_input_dict["-color_primaries"] = color_primaries
            if color_transfer is not None:
                writer_output_dict["-color_trc"] = color_transfer
                writer_input_dict["-color_trc"] = color_transfer

            writer_output_dict["-sws_flags"] = "full_chroma_int+bitexact+accurate_rnd"
            reader_output_dict["-sws_flags"] = "full_chroma_int+bitexact+accurate_rnd"
            # writer_input_dict['-pix_fmt'] = 'bgr48le'
            # reader_output_dict = {'-pix_fmt': 'bgr48le'}

            # -s 1920x1080
            # writer_input_dict['-s'] = '1920x1080'
            # writer_output_dict['-s'] = '1920x1080'
            # writer_input_dict['-s'] = '1080x1920'
            # writer_output_dict['-s'] = '1080x1920'

            print(writer_input_dict)
            print(writer_output_dict)

            self.reader = skvideo.io.FFmpegReader(
                video_path, outputdict=reader_output_dict
            )
        else:

            # fps = 25
            codec_name = "libopenh264"
            bit_rate = None
            pix_fmt = "yuv420p"

            reader_output_dict = {"-r": str(fps)}
            writer_input_dict = {"-r": str(fps)}
            writer_output_dict = {
                "-pix_fmt": pix_fmt,
                "-r": str(fps),
                "-vcodec": str(codec_name),
            }
            # if bit_rate is not None:
            #     writer_output_dict['-b:v'] = bit_rate
            writer_output_dict["-crf"] = "17"

            # if video has alpha channel, convert to bgra, uint16 to process
            if pix_fmt.startswith("yuva"):
                writer_input_dict["-pix_fmt"] = "bgra64le"
                reader_output_dict["-pix_fmt"] = "bgra64le"
            elif pix_fmt.endswith("le"):
                writer_input_dict["-pix_fmt"] = "bgr48le"
                reader_output_dict["-pix_fmt"] = "bgr48le"
            else:
                writer_input_dict["-pix_fmt"] = "bgr24"
                reader_output_dict["-pix_fmt"] = "bgr24"

            writer_output_dict["-sws_flags"] = "full_chroma_int+bitexact+accurate_rnd"
            print(writer_input_dict)
            print(writer_output_dict)

        if output_video_path is not None:
            self.writer = skvideo.io.FFmpegWriter(
                output_video_path,
                inputdict=writer_input_dict,
                outputdict=writer_output_dict,
                verbosity=1,
            )

    def getframes(self):
        return self.reader.nextFrame()

    def writeframe(self, frame):
        if frame is None:
            self.writer.close()
        else:
            self.writer.writeFrame(frame)


if __name__ == "__main__":
    test_video = "/Users/hmzjw/testdata/hybe/task_20220511/template_noaudio.mp4"
    output = "/Users/hmzjw/testdata/hybe/task_20220511/template_noaudio_idx.mp4"

    # init
    vid_util = VideoUtils(test_video, output)

    # read frame
    frame_idx = 0
    for frame in vid_util.getframes():
        if frame is None:
            break
        frame_idx += 1

        # pay attention if frame.shape[2]==4, it means frame has alpha channel, it should be seperated before procssing and merged with processed result
        # pay attention if frame.dtype is uint16, it should be normed by 65535
        # if frame.shape[2] == 4:
        #     bgr = frame[:,:, 0:3]
        #     alpha = frame[:,:,3:4]
        # else:
        #     bgr = frame

        cv2.putText(
            frame,
            "frame_index: " + str(frame_idx),
            (40, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

        # # norm [0-1]
        # if frame.dtype == 'uint16':
        #     bgr_normed = bgr / 65535
        # else:
        #     bgr_normed = bgr / 255
        #
        #
        # # show or process here #
        # # cv2.imshow('1', bgr_normed)
        # # cv2.waitKey(1)
        # # show or process here #
        #
        # # merge alpha and result
        # if frame.dtype == 'uint16':
        #     bgr_res = (bgr_normed * 65535).astype('uint16')
        # else:
        #     bgr_res = (bgr_normed * 255).astype('uint8')

        # if frame.shape[2] == 4:
        #     frame_res = np.concatenate([bgr_res, alpha], axis=2)
        # else:
        #     frame_res = bgr_res

        # write frame
        vid_util.writeframe(frame)
    print("Done. Total frames:{}".format(frame_idx))
