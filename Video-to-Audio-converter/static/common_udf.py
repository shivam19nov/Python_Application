from moviepy.editor import *
import re
import os
import pandas as pd


ls_vid_frmt = tuple(map(lambda s: s.lower(),[i.strip() for i in re.split('\n|,',""".WEBM
                                                    .MPG, .MP2, .MPEG, .MPE, .MPV
                                                    .OGG
                                                    .MP4, .M4P, .M4V
                                                    .AVI, .WMV
                                                    .MOV, .QT
                                                    .FLV, .SWF"""
                                            )
                ]))

def get_opt_path(input_path):
    output_path = os.path.join(os.path.dirname(input_path), "Vid_Aud_Convert")
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    return output_path

def aud_vid_convert(src_file, tgt_file_in, hq= None):
    try:
        tgt_file = tgt_file_in + '.wav' if hq else tgt_file_in + '.mp3'
        quality = 'High' if hq else 'Low'
        videoclip = VideoFileClip(src_file)
        audioclip = videoclip.audio
        audioclip.write_audiofile(tgt_file)
        return (src_file, tgt_file, quality, True)
    except Exception as error:
        print(error)
        return (src_file, tgt_file, quality, False)
    finally:
        audioclip.close()
        videoclip.close()

def file_convert(input_file, output_path, quality_tmp):
    file_status_ls = []
    quality = True if quality_tmp == 'hq_mp3' else False
    if input_file.strip().endswith(ls_vid_frmt):
        vid_file_pth = input_file
        aud_file_pth = os.path.join(output_path,os.path.splitext(os.path.basename(input_file))[0])
        if os.path.isfile(vid_file_pth):
            temp_dict = {}
            temp_dict['src_file'], temp_dict['tgt_file'], temp_dict['tgt_file_qlt'], temp_dict['status'] = aud_vid_convert(vid_file_pth, aud_file_pth, quality)
            file_status_ls.append(temp_dict)
    return file_status_ls

def dir_walk(input_path, output_path, quality_tmp):
    file_status_ls = []
    quality = True if quality_tmp == 'hq_mp3' else False
    for walk_path, dir_fnd, files_fnd in os.walk(input_path):
        for file in files_fnd:
            if file.strip().endswith(ls_vid_frmt):
                vid_file_pth = os.path.join(walk_path,file)
                aud_file_pth = os.path.join(output_path,os.path.splitext(file)[0])
                if os.path.isfile(vid_file_pth) and not(os.path.isfile(aud_file_pth)):#.exists()
                    temp_dict = {}
                    temp_dict['src_file'], temp_dict['tgt_file'], temp_dict['tgt_file_qlt'], temp_dict['status'] = aud_vid_convert(vid_file_pth, aud_file_pth, quality)
                    file_status_ls.append(temp_dict)
    return file_status_ls

def create_df(file_status_ls):
    df_temp = pd.DataFrame(file_status_ls)
    df = df_temp.reset_index()
    df['index'] = df.index + 1
    return df