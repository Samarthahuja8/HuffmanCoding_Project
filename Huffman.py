import heapq, os

class BinaryTreeNode:

    def __init__(self,value,freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self,other):
        return self.freq < other.freq
    
    def __eq__(self, o):
        return self.freq == o.freq

class HuffmanCoding:

    def __init__(self,path):
        self.path = path
        self.__heap = []
        self.__codes = {}
        self.__reverseCodes = {}
    
    def __make_frequency_dic(self,text):
        freq_dic = {}
        for i in text:
            if i not in freq_dic:
                freq_dic[i] = 0
            freq_dic[i]+=1
        
        return freq_dic

    def __build_heap(self,freq_dic):
        for key in freq_dic:
            frequency = freq_dic[key]
            binary_tree = BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binary_tree)

    def __buildTree(self):
        while(len(self.__heap)>1):
            node_1 = heapq.heappop(self.__heap)
            node_2 = heapq.heappop(self.__heap)
            freq_sum = node_1.freq + node_2.freq
            new_node = BinaryTreeNode(None,freq_sum)
            new_node.left = node_1
            new_node.right = node_2
            heapq.heappush(self.__heap,new_node)
        return
    
    def __buildCodesHelper(self,root,curr_bits):
        if root is None:
            return
        
        if root.value is not None:
            self.__codes[root.value] = curr_bits
            self.__reverseCodes[curr_bits] = root.value
            return
        
        self.__buildCodesHelper(root.left,curr_bits+"0")
        self.__buildCodesHelper(root.right,curr_bits+"1")

    def __buildCodes(self):
        root = heapq.heappop(self.__heap)
        self.__buildCodesHelper(root,"")

    def __getEncodedText(self,text):
        encoded_text = ""
        for char in text:
            encoded_text += self.__codes[char]
        
        return encoded_text

    def __getPaddedText(self,encoded_text):
        padded_amount = 8 - (len(encoded_text)%8)
        for i in range(padded_amount):
            encoded_text+='0'

        padded_info = "{0:08b}".format(padded_amount)

        padded_encoded_text = padded_info + encoded_text

        return padded_encoded_text

    def __getBytesArray(self,padded_encoded_text):

        array = []
        for i in range(0,len(padded_encoded_text),8):
            byte = padded_encoded_text[i:i+8]
            array.append(int(byte,2))

        return array

    def compress(self):
        #get file from path
        #read text from file
        file_name,file_extension = os.path.splitext(self.path)
        output_path = file_name+".bin"

        with open(self.path,'r+') as file, open(output_path,'wb') as output:

        #make frequency dictionary using the text
            text = file.read()
            text = text.rstrip()
            freq_dic = self.__make_frequency_dic(text)

            #construct the heap from frequency_dict
            self.__build_heap(freq_dic)

            #construct the binary tree from heap
            self.__buildTree()

            #construct the codes from binary tree
            self.__buildCodes()

            #creating the encoded text using the codes
            encoded_text = self.__getEncodedText(text)

            #pad encoded text
            paded_encoded_text = self.__getPaddedText(encoded_text)

            bytes_array = self.__getBytesArray(paded_encoded_text)
            final_bytes = bytes(bytes_array)

            output.write(final_bytes)

            #put this paded encoded text into the binary file
            #return this binary file as output
        print('compressed')
        return output_path
    
    def __removePadding(self,text):
        padded_info = text[:8]
        extra_padding = int(padded_info,2)

        text = text[8:]
        text_after_padding_removed = text[:-1*extra_padding]
        return text_after_padding_removed

    def __decodeText(self,text):
        decoded_text = ""
        current_bit = ""
        for bit in text:
            current_bit +=bit
            if current_bit in self.__reverseCodes:
                character = self.__reverseCodes[current_bit]
                decoded_text+=character
                current_bit = ""
        
        return decoded_text


    def decompress(self,input_path):
        filename,file_extension = os.path.splitext(self.path)
        output_path = filename+"_decompress"+".txt"
        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bit_string +=bits
                byte = file.read(1)
            actual_text = self.__removePadding(bit_string)
            decompress_text = self.__decodeText(actual_text)
            output.write(decompress_text)


path = 'C:/Users/samar/OneDrive/Desktop/sample.txt'
h = HuffmanCoding(path)

output_path = h.compress()
h.decompress(output_path)