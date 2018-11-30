import PIL
from PIL import Image as img
import urllib.request as url

import io
import math
import os

class binary_file:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'rb')
        self.size = os.path.getsize(filename)
        self.current_pos = 0
    def __del__(self):
        self.file.close()
    def __iter__(self):
        return self
    def __next__(self):
        nb = self.next_byte()
        if(nb):
            return nb
        raise StopIteration()
    def next_byte(self):
        try:
            byte = bin(ord(self.file.read(1)))[2:]
        except TypeError:
            return False
        return '0'*(8-len(byte))+byte




class data_img:

    def __init__(self,img_path, bits_per_char=8):
        self.pil_image = data_img.load_image(img_path)
        self.max_data_size = data_img
        self.bits_per_char = bits_per_char      

    def load_image(img_path):
        def get_pil_image(uri):
            image = img.open(io.BytesIO(url.urlopen(uri).read()))
            return image
        if(str(type(img_path)).startswith("<class 'PIL")): # a clunky check to see if img_path is a PIL image
            pil_image = img_path
        if(os.path.exists(img_path)):
            pil_image = img.open(img_path)
        else:
            try:
                pil_image = get_pil_image(img_path)
            except ValueError:
                raise FileNotFoundError("the file is not found")
        return pil_image

    def encode_text(text, bits_per_char=8):
        text+="\0"
        def convert_to_padded_binary(char):
            bin_value = bin(ord(char))[2:]
            return '0'*(bits_per_char-len(bin_value))+bin_value
        return map(convert_to_padded_binary, text)
        
    def decode_text(byte_array):
        def bin_to_char(byte_string):
            return chr(int(byte_string, 2))
            
        return ''.join(map(bin_to_char, byte_array))

    def decode_text_from_image(self):
        image = self.pil_image
        pixels = image.load()
        width = image.size[0]
        height = image.size[1]
        output = ""
        last_char = ""
        sequence = ''
        kill = False
        for y in range(height):
            if(kill):
                break
            for x in range(width):
                
                if(kill):
                    break
                for i in range(3):
                    last_bit = bin(pixels[x,y][i])[2:][-1]
                    
                    sequence += last_bit
                    if(len(sequence) == self.bits_per_char):
                        last_char = chr(int(sequence, 2))
                        sequence = ''
                        if(last_char == '\0'):
                            kill = True
                            break
                        
                        output+=last_char
        return output
                        

    def resize_image_to_data(self, data_size_bits, resize_method=img.ANTIALIAS):
        needed_pixels = math.ceil(data_size_bits+15/3) #fifteen bits from overhead
        width, height = self.pil_image.size
        scale = math.ceil(math.sqrt(needed_pixels/(width*height)))
        self.pil_image = self.pil_image.resize((width*scale, height*scale), resize_method)
        return self

    def calculate_storage_size(self):
        return math.floor((self.pil_image.size[0]*self.pil_image.size[1]*3)/8)

    def save(self, filename):
        if(filename.endswith('.png')):
            pass
        else:
            filename+=".png"
        self.pil_image.save(filename, "PNG")
      
    def hide_text_in_image(self, text):
        def sub_last_bit_in_int(num, bit):
            num = list(bin(num)[2:])
            num[-1] = str(bit)
            return int(''.join(num), 2)    
        image = self.pil_image
        pixels = self.pil_image.load()
        bits = ''.join(data_img.encode_text(text))
        bit_length = len(bits)
        width, height = image.size
        bit_index = 0
        kill = False
        for y in range(height):
            if(kill):
                break
            for x in range(width):
                colors = list(pixels[x,y])
                for i in range(3):
                    colors[i] = sub_last_bit_in_int(colors[i], bits[bit_index])
                    bit_index+=1
                    if(bit_index>bit_length-1):
                        kill = True
                        break
                pixels[x,y] = tuple(colors)
                if(kill):
                    break
                    
        return self





if(__name__ == '__main__'):
    f = data_img("new_thing.png").decode_text_from_image()
    print(f)





    
