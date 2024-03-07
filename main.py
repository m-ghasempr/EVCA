print("Importing libraries...")
import os
import sys
import time
import glob
import argparse
from pathlib import Path

print("Libraries imported successfully.\n\n")


def check_existence(input_args):
    files_list = []
    if input_args.dir:
        files_list = [file for file in glob.glob('{}/*.yuv'.format(input_args.dir))]
    elif input_args.input:
        if Path(input_args.input).is_file():
            files_list = [input_args.input]
    else:
        return files_list, False

    return files_list, True


def print_custom_help():
    print("EVCA:    Enhanced Video Complexity Analyzer v1.0")
    print("Usage:   python3 main.py [options]")
    print("\nOptions:")
    print("-h /--help                Show this help text and exit.")
    print("-m /--method              Feature extraction method. Default is EVCA. [VCA, EVCA, SITI] ")
    print("-fi/--filter              Edge detection filter. Default is Sobel filter. [sobel, canny] ")
    print("-i /--input               Raw YUV input file name.")
    print("-d /--dir                 The directory of batch files.")
    print("-r /--resolution          Set the resolution [w]x[h]. Default is 1920x1080.")
    print("-b /--block_size          Set the block size. Default is 32. [8, 16, 32]")
    print("-f /--frames              Maximum number of frames for features extraction.")
    print("-p /--pix_fmt             yuv format. Default is yuv420. [yuv420, yuv444] ")
    print("-s /--sample_rate         Frame subsampling. Default is 1 ")
    print("-c /--csv                 Name of csv to write features. Default is ./csv/test.csv")
    print("-bi/--block_info          Write block level features into a csv. Default is disabled")
    print("-pi/--plot_info           Plot per frame features. Default is disabled")
    print("-dp/--dpi                 Image quality of the saved output. Default is 100.")
    
def get_parser_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(add_help=False,)
        parser.add_argument('-i',  '--input', type=str)
        parser.add_argument('-d',  '--dir', type=str)
        parser.add_argument('-m',  '--method', type=str, default='EVCA')
        parser.add_argument('-r',  '--resolution', type=str, default='1920x1080')
        parser.add_argument('-b',  '--block_size', type=int, default='32')
        parser.add_argument('-f',  '--frames', type=int, default='30')
        parser.add_argument('-c',  '--csv', type=str, default='./csv/test.csv')
        parser.add_argument('-p',  '--pix_fmt', type=str, default='yuv420')
        parser.add_argument('-s',  '--sample_rate', type=int, default='1') 
        parser.add_argument('-bi', '--block_info', type=int, default='0')
        parser.add_argument('-pi', '--plot_info', type=int, default='0')
        parser.add_argument('-dp', '--dpi', type=int, default='100')
        parser.add_argument('-fi', '--filter', type=str, default='sobel')
        
        return parser.parse_args()
    
def main():
    # Check if the help option is explicitly provided
    if '-h' in sys.argv or '--help' in sys.argv:
        print_custom_help()
    else:
        
        args = get_parser_arguments()

        import torch
        from libs.EVCA import EVCA
        from libs.SITI import SITI
        # Your main script logic goes here
        print("EVCA: Enhanced Video Complexity Analyzer v1.0.")

        # Check input file(s) existence.
        input_list, success = check_existence(args)
        if success:
            print("Start to extract features...")
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            t1 = time.time()
            if args.method == 'EVCA':
                EVCA(args,input_list,device)
            elif args.method == 'VCA':
                EVCA(args,input_list,device)
            elif args.method == 'SITI':
                SITI(args,input_list,device)
            else:
                print('Unsupported method.')
            t2 = time.time()
            print(f'Feature extraction completed in {t2-t1:.2f} seconds.')
        else:
            print('Input file or directory is not specified.')
        
if __name__ == "__main__":
    main()
