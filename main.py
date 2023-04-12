from gooey import Gooey, GooeyParser
from generator import generate
import sys
from multiprocessing import freeze_support
# import codecs

# if sys.stdout.encoding != 'UTF-8':
#     sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
# if sys.stderr.encoding != 'UTF-8':
#     sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# utf8_stdout = os.fdopen(sys.stdout.fileno(), mode='w', encoding='utf-8', closefd=False)
# sys.stdout = utf8_stdout

@Gooey(
    advanced=True,
    program_name="Word-wise Ebook Generator",
    default_size=(800, 800))
def main():
    desc = "Application to generate word-wise ebooks"
    parser = GooeyParser(description=desc)
    parser.add_argument("--input_file", metavar='Đường dẫn file input', required=True, widget='FileChooser')
    #
    config_g = parser.add_argument_group('Cấu Hình')   
    config_g.add_argument("--hint_level", metavar='Hint Level', type=int, default=1, help=
"""
1 - Mức độ thấp (chỉ hiển thị một số từ khó)
2 - Mức độ khá thấp
3 - Mức độ trung bình
4 - Mức độ cao
5 - Mức độ rất cao (hiển thị tất cả)
""", choices=[1, 2, 3, 4, 5])
    config_g.add_argument("--lang", metavar='Ngôn ngữ', default="vi", choices=["vi", "en"],
        help="Ngôn ngữ cho word-wise (en: Tiếng Anh, vi: Tiếng Việt ...)")
    #
    out_fmt = parser.add_argument_group('Định dạng Output')   
    out_fmt.add_argument("--out_epub", metavar='EPUB', default=False, action="store_true")
    out_fmt.add_argument("--out_azw3", metavar='AZW3', default=False, action="store_true")
    out_fmt.add_argument("--out_pdf", metavar='PDF', default=False, action="store_true")
    #
    misc_g = parser.add_argument_group('Miscellaneous') 
    misc_g.add_argument("--debug", metavar='Debug', default=False, help="tắt/bật debug", action="store_true")
    misc_g.add_argument("--num_threads", metavar='Số luồng chạy song song', type=int, default=8)
    args = parser.parse_args()
    #
    generate(args)

if __name__ == '__main__':
    freeze_support()
    main()
