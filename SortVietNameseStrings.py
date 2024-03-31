import math, pickle, pathlib, sys, os
def CreateInformation_About_RadixValues(information_about_radix_values, radix):
    """
    Tạo array, mỗi element chứa thông tin về 1 value. Value là một phần tử của radix
    """
    for i in range(0, len(radix)):
        unicode_binary_representation = radix[i].encode('utf8')
        value_information=dict(base_10_representation=i, unicode_binary_value=int.from_bytes(unicode_binary_representation,byteorder='big'), unicode_binary_length=len(unicode_binary_representation))
        information_about_radix_values.append(value_information)
def ToRadixValue(unicode_binary_value, unicode_binary_length):
    return unicode_binary_value.to_bytes(length=unicode_binary_length, byteorder='big').decode('utf-8')
def Parent(i):
    return int((i+1)/2) -1
def Left(i):
    return 2*i + 1
def Right(i):
    return 2*i + 2
def MaxHeapify(dictionary_array, i, key_word):
    """
    Lấy thông tin key_word để so sánh
    """
    l,r = Left(i), Right(i)
    if (l <= len(dictionary_array)-1) and (dictionary_array[l][key_word] > dictionary_array[i][key_word]): largest = l
    else: largest = i
    if (r <= len(dictionary_array)-1) and (dictionary_array[r][key_word] > dictionary_array[largest][key_word]): largest = r
    if largest != i:
        dictionary_array[i], dictionary_array[largest] = dictionary_array[largest], dictionary_array[i]
        MaxHeapify(dictionary_array, largest, key_word)
def BuilMaxHeap(dictionary_array, key_word):
    """"
    Xắp xếp a dictionary array dựa vào độ lớn key_word
    """
    for i in range(int(  (len(dictionary_array)-1)/2  ),-1,-1): 
        MaxHeapify(dictionary_array, i, key_word)
def HeapSort(dictionary_array, key_word):
    """
    Sắp xếp the array on key_word values of the array elements
    """
    BuilMaxHeap(dictionary_array, key_word)
    # Reference ảnh hưởng cực lớn
    template = dictionary_array[:]
    for i in range(len(template)-1, -1,-1):
        dictionary_array[i] = template[0]
        template[0] = template[i]
        template.pop()
        MaxHeapify(template, 0, key_word)
def CheckExistKey(dictionary_array, start_index, end_index, key_word, key_word_value):
    #conditions: A tăng dần
    #Trả về index của element whose key_word value is key_word_value
    if end_index == start_index + 1: return -1
    median =  math.ceil((end_index+start_index)/2)
    if key_word_value == dictionary_array[median][key_word]: return median
    elif key_word_value < dictionary_array[median][key_word]: return CheckExistKey(dictionary_array, start_index, median, key_word, key_word_value)
    else: return CheckExistKey(dictionary_array, median, end_index, key_word, key_word_value)
def Base10Value(char, information_about_radix_values):
    unicode_binary_representation = char.encode('utf8')
    unicode_binary_value=int.from_bytes(unicode_binary_representation,byteorder='big')
    index = CheckExistKey(information_about_radix_values, -1, len(information_about_radix_values), 'unicode_binary_value', unicode_binary_value)
    if index == -1: print("ERROR: invalid character '%s'"%char, file=sys.stderr)
    else: return information_about_radix_values[index]['base_10_representation']

#Ghi dictionary array vao file text lan sau khong can chay lai
#========== Initilize ============
def CoungtingSort_OnDigit(strings, order, information_about_radix_values):
    old_strings = strings[:]
    position_of_order = len(strings[0]) - order
    base = len(information_about_radix_values)
    count = [0]*base
    for string in old_strings:
        char = string[position_of_order]
        base_10_value_of_char = Base10Value(char, information_about_radix_values)
        if base_10_value_of_char == None:
            print("Hint: invalid character near '%s'"%string)
        count[base_10_value_of_char] +=1
    for i in range(1, base): count[i] += count[i-1]
    for i in range(len(strings)-1, -1, -1):
        char = old_strings[i][position_of_order]
        base_10_value_of_char = Base10Value(char, information_about_radix_values)
        strings[count[base_10_value_of_char]-1] = old_strings[i]
        count[base_10_value_of_char] -= 1
    pass
def SortSringsAlphabetically(strings, collation, number_of_digit):
    #Match number_of_digit condition
    for i in range(0, len(strings)):
        length = len(strings[i])
        if length < number_of_digit:
            strings[i] += ' '*(number_of_digit-length)
        if length > number_of_digit:
            strings[i] = strings[i][0:number_of_digit]
    #load file, tiet kiệm O(1500)
    pickle_file_name = '%(name)s.pickle'%collation
    if pathlib.Path(pickle_file_name).is_file():
        with open(pickle_file_name, 'rb') as file:
            information_about_radix_values=pickle.load(file)
            print('AAAA')
    else:
        radix, information_about_radix_values = collation['collation'], []
        CreateInformation_About_RadixValues(information_about_radix_values, radix)
        HeapSort(information_about_radix_values, 'unicode_binary_value')
        with open(pickle_file_name, 'wb') as file:
            pickle.dump(information_about_radix_values, file)
            print('BBB')
    #Sort
    for order in range(1, number_of_digit+1):
        CoungtingSort_OnDigit(strings, order, information_about_radix_values)

collation  = dict(collation="AaÁáÀàẢảÃãẠạĂăẮắẰằẲẳẴẵẶặÂâẤấẦầẨẩẪẫẬậBbCcDdĐđEeÉéÈèẺẻẼẽẸẹÊêẾếỀềỂểỄễỆệGgHhIiÍíÌìỈỉĨĩỊịKkLlMmNnOoÓóÒòỎỏÕõỌọÔôỐốỒồỔổỖỗỘộƠơỚớỜờỞởỠỡỢợPpQqRrSsTtUuÚúÙùỦủŨũỤụƯưỨứỪừỬửỮữỰựVvXxYyÝýỲỳỶỷỸỹỴỵ ", #179 charactercollation_name = 'VietNamese Collation'
                  name='VietNamese Colation')
print(os.getcwd())
with open('%s/names.txt'%os.getcwd(), 'r') as file:
    strings = file.read()
strings = strings.split('\n')
print(len(strings))
SortSringsAlphabetically(strings, collation, 30)
for string in strings:print(string)

