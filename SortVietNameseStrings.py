import math, pickle, pathlib, sys, random

#=================Heap=================
def Parent(i):
    return int((i+1)/2) -1
def Left(i):
    return 2*i + 1
def Right(i):
    return 2*i + 2
def MaxHeapify(dictionary_array, index, key_word):
    #Lấy thông tin key_word để so sánh
    l,r = Left(index), Right(index)
    if (l <= len(dictionary_array)-1) and (dictionary_array[l][key_word] > dictionary_array[index][key_word]): largest = l
    else: largest = index
    if (r <= len(dictionary_array)-1) and (dictionary_array[r][key_word] > dictionary_array[largest][key_word]): largest = r
    if largest != index:
        dictionary_array[index], dictionary_array[largest] = dictionary_array[largest], dictionary_array[index]
        MaxHeapify(dictionary_array, largest, key_word)
def BuilMaxHeap(dictionary_array, key_word):
    #Xắp xếp a dictionary array dựa vào độ lớn key_word
    for i in range(int(  (len(dictionary_array)-1)/2  ),-1,-1): 
        MaxHeapify(dictionary_array, i, key_word)
def HeapSort(dictionary_array, key_word):
    #Sắp xếp the array on key_word values of the array elements
    BuilMaxHeap(dictionary_array, key_word)
    template = dictionary_array[:]
    for i in range(len(template)-1, -1,-1):
        dictionary_array[i] = template[0]
        template[0] = template[i]
        template.pop()
        MaxHeapify(template, 0, key_word)

##=================General functions=================
def CheckExistKey(dictionary_array, start_index, end_index, key_word, key_word_value):
    #conditions: A được xắp sếp tăng dần
    #Runningtime: O(lgn)
    #Trả về index của element whose key_word value is key_word_value
    global GLOBLE
    GLOBLE += 5
    if end_index == start_index + 1: return -1
    median =  math.ceil((end_index+start_index)/2)
    if key_word_value == dictionary_array[median][key_word]: return median
    elif key_word_value < dictionary_array[median][key_word]: return CheckExistKey(dictionary_array, start_index, median, key_word, key_word_value)
    else: return CheckExistKey(dictionary_array, median, end_index, key_word, key_word_value)

#=================Local functions=================
def CompareTwoStrings(stringA, stringB, information_about_radix_values):
    #So sánh dựa trên giá trị thực
    #conditions: V char in string E radix
    #Cases that are not covered: Thiếu xét 0 value at the highest order, AAAA > AB is wrong nếu so sánh bằng giá trị thực
    global GLOBLE, collation
    GLOBLE += 3
    if len(stringA) > len(stringB): return '>'
    elif len(stringA) < len(stringB): return '<'
    for digitA, digitB in zip(stringA, stringB):
        GLOBLE += 5
        #base_10_representationA, base_10_representationB = Base10Value(digitA, information_about_radix_values), Base10Value(digitB, information_about_radix_values) 
        base_10_representationA, base_10_representationB = collation['collation'].index(digitA), collation['collation'].index(digitB)
        if base_10_representationA > base_10_representationB: return '>'
        if base_10_representationA < base_10_representationB: return '<'
    return '='
def CreateInformation_About_RadixValues(information_about_radix_values, radix):
    #Tạo array, mỗi element chứa thông tin về 1 value. Value là một phần tử của radix
    for i in range(0, len(radix)):
        unicode_binary_representation = radix[i].encode('utf8')
        value_information=dict(base_10_representation=i, unicode_binary_value=int.from_bytes(unicode_binary_representation,byteorder='big'))
        information_about_radix_values.append(value_information)
def Base10Value(char, information_about_radix_values):
    """char E radix"""
    global GLOBLE
    GLOBLE += 5
    unicode_binary_representation = char.encode('utf8')
    unicode_binary_value=int.from_bytes(unicode_binary_representation,byteorder='big')
    index = CheckExistKey(information_about_radix_values, -1, len(information_about_radix_values), 'unicode_binary_value', unicode_binary_value)
    if index == -1: print("ERROR: invalid character '%s'"%char, file=sys.stderr)
    else: return information_about_radix_values[index]['base_10_representation']
def Initialize(strings, collation, number_of_digit):
    """Return information about radix values"""
    #Match string length condition
    for i in range(0, len(strings)):
        length = len(strings[i])
        if length < 25:
            strings[i] += ' '*(number_of_digit-length)
        if length > 25:
            strings[i] = strings[i][0:number_of_digit]
    #load file or create information about radix values
    pickle_file_name = '%(name)s.pickle'%collation
    if pathlib.Path(pickle_file_name).is_file():
        with open(pickle_file_name, 'rb') as file:
            information_about_radix_values = pickle.load(file)
        print("The file '%s' is loaded" % pickle_file_name)
    else:
        radix, information_about_radix_values = collation['collation'], []
        CreateInformation_About_RadixValues(information_about_radix_values, radix)
        HeapSort(information_about_radix_values, 'unicode_binary_value')
        with open(pickle_file_name, 'wb') as file:
            pickle.dump(information_about_radix_values, file)  
        print("We created a file named '%s' to stored your information" % pickle_file_name)
    return information_about_radix_values
#========== Specific Radix Sort ============
def CoungtingSort_OnDigit(strings, order, information_about_radix_values):
    """Conditions: V char in a string E radix"""
    global GLOBLE
    global collation
    GLOBLE += 5
    old_strings = strings[:]
    position_of_order = len(strings[0]) - order
    base = len(information_about_radix_values)
    count = [0]*base
    for string in old_strings:
        GLOBLE += 5
        char = string[position_of_order]
        base_10_value_of_char = collation['collation'].index(char)
        if base_10_value_of_char == None:
            print("Hint: invalid character near '%s'"%string)
        count[base_10_value_of_char] +=1
    for i in range(1, base): 
        count[i] += count[i-1]
        GLOBLE += 2
    for i in range(len(strings)-1, -1, -1):
        GLOBLE += 5
        char = old_strings[i][position_of_order]
        base_10_value_of_char = collation['collation'].index(char)
        strings[count[base_10_value_of_char]-1] = old_strings[i]
        count[base_10_value_of_char] -= 1
    pass
def StringRadixSort(strings, information_about_radix_values):
    """Conditions: V len(string) = a constant. V char in a string E radix"""
    global GLOBLE
    for order in range(1, len(strings[0])+1):
        GLOBLE += 2
        CoungtingSort_OnDigit(strings, order, information_about_radix_values)

#============ Specific Quick Sort ============
def Partition(strings, start_index, end_index, information_about_radix_values):
    global GLOBLE
    global collation
    GLOBLE += 7
    pivot = random.randint(start_index, end_index)
    strings[pivot], strings[end_index] = strings[end_index], strings[pivot]
    pivot = end_index
    i = start_index - 1
    for j in range(start_index, end_index):
        GLOBLE += 2
        if CompareTwoStrings(strings[j], strings[pivot], information_about_radix_values) in '<=':
            GLOBLE += 2
            i +=1
            strings[i], strings[j] = strings[j], strings[i]
    strings[i+1], strings[end_index] = strings[end_index], strings[i+1]
    return i+1
def StringQuickSort(strings, start_index, end_index, information_about_radix_values):
    global GLOBLE
    GLOBLE += 4
    if start_index > end_index: return None
    q = Partition(strings, start_index, end_index, information_about_radix_values)
    StringQuickSort(strings, start_index, q-1, information_about_radix_values)
    StringQuickSort(strings, q+1, end_index, information_about_radix_values)

#============ Run the program ============
#Input
collation  = dict(collation="AaÁáÀàẢảÃãẠạĂăẮắẰằẲẳẴẵẶặÂâẤấẦầẨẩẪẫẬậBbCcDdĐđEeÉéÈèẺẻẼẽẸẹÊêẾếỀềỂểỄễỆệGgHhIiÍíÌìỈỉĨĩỊịKkLlMmNnOoÓóÒòỎỏÕõỌọÔôỐốỒồỔổỖỗỘộƠơỚớỜờỞởỠỡỢợPpQqRrSsTtUuÚúÙùỦủŨũỤụƯưỨứỪừỬửỮữỰựVvXxYyÝýỲỳỶỷỸỹỴỵ ", #179 charactercollation_name = 'VietNamese Collation'
                  name='VietNamese Colation')
with open('names.txt', 'r') as file:
    strings = file.read()
strings = strings.split('\n')
number_of_digit = 25

import time
start_time = time.time()
GLOBLE, GLOBLE1 = 0, 0
#initialize
#information_about_radix_values = Initialize(strings, collation, number_of_digit)
#sort
#StringQuickSort(strings, 0, len(strings)-1, information_about_radix_values) #O(nlgn) in normal situations the hidden constant factor is 5 but in this case depending on circumstances it range from 80 to 8+digit*72! The running time of the algorithm is depedning heavy on the CompareTwoStrings() function, the less similar the strings are the faster the algorithm is
#StringRadixSort(strings, information_about_radix_values) #takes digit*(4 + 2n*360 + radix) on every case = θ(d(2n +k))
#nlgn*digit*30 
#digit*2n*360
#display
for string in strings:print(string)
print("len: %s" % len(strings))
print('Running time: %s' %GLOBLE)
print("Real time: %s seconds ---" % (time.time() - start_time))
print("Radix: %s"%GLOBLE1 )
#Using two algorithms to sort 17,900 names 
#Radix sort takes 11.74 seconds
#Quicksort takes 9.36 minutes
#3 213 223
#1 396 435

#len = 5362
#183 142 185          8+25*72×5362×log₂5392         ~109e6 worst case
# 12 497 990         25*(2+(5+2*k+2*n*5))
