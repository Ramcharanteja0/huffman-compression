import heapq
import pickle
import os


class Node:


    def __init__(self,char,freq):

        self.char=char
        self.freq=freq
        self.left=None
        self.right=None



    def __lt__(self,node):

        return self.freq < node.freq




def build_tree(text):


    frequency={}


    for char in text:

        frequency[char]=frequency.get(char,0)+1



    heap=[]


    for char,freq in frequency.items():

        heapq.heappush(
            heap,
            Node(char,freq)
        )

    if len(heap) == 1:
        single = heapq.heappop(heap)
        root = Node(None, single.freq)
        root.left = single
        heapq.heappush(heap, root)


    while len(heap)>1:


        left=heapq.heappop(heap)

        right=heapq.heappop(heap)


        merged=Node(
            None,
            left.freq+right.freq
        )


        merged.left=left
        merged.right=right


        heapq.heappush(
            heap,
            merged
        )



    return heap[0]





codes={}



def generate_codes(node,current=""):


    if node is None:
        return


    if node.char is not None:

        codes[node.char]=current


    generate_codes(
        node.left,
        current+"0"
    )


    generate_codes(
        node.right,
        current+"1"
    )





def compress_file(input_file,output_file):
    global codes
    codes.clear()


    with open(input_file,"rb") as f:

        text=f.read()

    if not text:
        with open(output_file,"wb") as f:
            pickle.dump({"tree": None, "encoded": ""}, f)
        return 0.0



    root=build_tree(text)



    generate_codes(root)



    encoded = "".join(codes[char] for char in text)



    data={

        "tree":root,

        "encoded":encoded

    }



    with open(output_file,"wb") as f:

        pickle.dump(data,f)



    original=os.path.getsize(input_file)

    compressed=os.path.getsize(output_file)

    if original == 0:
        ratio = 0.0
    else:
        ratio=100-(compressed/original*100)


    return round(ratio,2)






def decompress_file(input_file,output_file):


    with open(input_file,"rb") as f:

        data=pickle.load(f)

    if data.get("tree") is None:
        with open(output_file, "wb") as f:
            pass
        return



    root=data["tree"]

    encoded=data["encoded"]



    result=bytearray()

    node=root



    for bit in encoded:


        if bit=="0":

            node=node.left

        else:

            node=node.right



        if node.char is not None:


            result.append(node.char)

            node=root



    with open(output_file,"wb") as f:

        f.write(result)