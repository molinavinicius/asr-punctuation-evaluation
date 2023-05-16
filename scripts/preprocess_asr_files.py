import os
import re


def preprocess_dir(input_dir, 
                   output_dir, 
                   final_punctuation_marks=['.', '!', '?']) -> None:
    """
    Preprocesses text files in the input directory by removing line breaks, combining lines into paragraphs,
    segmenting the text based on final punctuation marks, and saving the preprocessed files to the output directory.

    Args:
        input_dir (str): Path to the input directory containing text files to preprocess.
        output_dir (str): Path to the output directory where preprocessed files will be saved.
        final_punctuation_marks (list, optional): List of final punctuation marks used for text segmentation.
            Use ".!?" to segment on sentences or ".!?,;:" to segment on any punctuation for punctuation analysis.
            Defaults to ['.', '!', '?'].

    Returns:
        None
    """
    for d in list(filter(lambda d: os.path.isdir(d), os.listdir())):
        os.makedirs(os.path.join(input_dir, d), exist_ok=True)
        files = list(filter(lambda f: f.endswith("txt"), os.listdir(d)))
        for f in files:
            with open(os.path.join(d, f)) as orig, open(os.path.join(output_dir, d, f), 'w') as pf:
                
                text = ''
                for line in orig:
                    text += ' ' + line.strip()
                text = text.replace("...", '=')
                segments = []
                
                segments += list(filter(lambda s: any(c.isalpha() or c.isdigit() for c in s), 
                                        re.findall(f".*?[{final_punctuation_marks}]", text)))
                for s in segments:
                    s = s.replace("etc", "etc.")
                    s = s.replace("=", '...')
                    s = s.strip()
                    if s: 
                        print(s)
                        print(s, file=pf)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Preprocess asr files")
    parser.add_argument('dir', type=str, help='Directory to preprocess')
    parser.add_argument('--output_dir', type=str, default='preprocessed_asr', help='Output directory')
    parser.add_argument('--final_punctuation_marks', type=str, default='.,!?;:', 
                        help='Final punctuation marks to create the segments. Use ".!?" to segment on sentences, '
                             'or ".!?,;:" to segment on any punctuation for punctuation analysis.')
    args = parser.parse_args()
    preprocess_dir(args.dir, args.output_dir, list(args.final_punctuation_marks))