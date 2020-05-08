
def max_sum(a):
    sum = [0] * len(a)
    sum[0] = a[0]
    for i in range(1,len(a)):
        n = a[i]
        if sum[i-1] > 0 :
            sum[i] = n + sum[i-1];
        else:
            sum[i] = n
    return max(sum)

a= [-4, 101,-101, 13,-7,-3,12]
print(max_sum(a))