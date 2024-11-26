import ffmpeg
import os

from ffmpeg import overwrite_output

from hexEditorForGif import hexEditorForGif


def ffmDivideVideo(directory=None, divnum=-1, fpsnum=-1, piecesnum=5):
    fileName, _ = os.path.splitext(directory)
    fileName = os.path.basename(fileName)
    if not os.path.exists('.\\output'):
        os.mkdir('.\\output')
    if divnum == -1 and fpsnum == -1:
        ffmpeg.input(directory).output(f'.\\output\\{fileName}_output.gif').run(overwrite_output=True)
    elif fpsnum == -1:
        ffmpeg.input(directory).filter('scale', f'iw/{divnum}', f'ih/{divnum}').output(f'.\\output\\{fileName}_output.gif').run(overwrite_output=True)
    elif divnum == -1:
        ffmpeg.input(directory).output(f'{fileName}_output.gif').run()
    else:
        ffmpeg.input(directory).filter('scale',f'iw/{divnum}',f'ih/{divnum}').output(f'.\\output\\{fileName}_output.gif', r=f'{fpsnum}').run(overwrite_output=True)
    afterFile=f".\\output\\{fileName}_output.gif"
    streams = ffmpeg.probe(afterFile, select_streams='v')
    stream = next((stream for stream in streams.get('streams', []) if stream['codec_type'] == 'video'), None)
    iw = stream['width']
    ih = stream['height']
    if piecesnum == 5:
        x=0
        for i in range(5):
            output_filename = f".\\output\\{fileName}_{i}_output.gif"
            ffmpeg.input(afterFile).filter('crop','iw*0.2','ih',f'{x}',f'0').output(f'.\\output\\{fileName}_{i}_output.gif').run(overwrite_output=True)
            hexEditorForGif(output_filename)
            x=x+(iw*0.2)
    elif piecesnum == 10:
        x=0
        y=0
        index=0
        for i in range(2):
            for j in range(5):
                output_filename = f'.\\output\\{fileName}_{i}_output.gif'
                ffmpeg.input(afterFile).filter('crop', 'iw*0.2', 'ih*0.5', f'{x}', f'{y}').output(
                    f'.\\output\\{fileName}_{index}_output.gif').run(overwrite_output=True)
                hexEditorForGif(output_filename)
                x = x + (iw * 0.2)
                index = index + 1
            y = y + (ih * 0.5)
            x=0
    elif piecesnum == 15:
        x=0
        y=0
        index=0
        for i in range(3):
            for j in range(5):
                output_filename = f'.\\output\\{fileName}_{i}_output.gif'
                ffmpeg.input(afterFile).filter('crop', 'iw*0.2', 'ih*0.33', f'{x}', f'{y}').output(
                    f'.\\output\\{fileName}_{index}_output.gif').run(overwrite_output=True)
                hexEditorForGif(output_filename)
                x = x + (iw * 0.2)
                index = index + 1
            y=y + (ih * 0.33)
            x=0

