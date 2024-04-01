def Partition(A, start_index, end_index):
    compared_component, i = A[end_index], start_index-1
    for j in range(start_index, end_index):
        if A[j] <= compared_component:
            i +=1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[end_index] = A[end_index], A[i+1]
    return i+1
A = [1, 12,15, 78, 468, 1654, 1, 3 , 15 ,6, 48, 654,465 , 465, 631, 65,464 ,46,847 ,6354, 6,456, 14 ,64]
def QuickSort(A, start_index, end_index):
    if start_index > end_index: return None
    q = Partition(A, start_index, end_index)
    QuickSort(A, start_index, q-1)
    QuickSort(A, q+1, end_index)

print(A, QuickSort(A, 0, len(A)-1))