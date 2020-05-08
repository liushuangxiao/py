import sys

def lcs(w1,w2):
    l1 = len(w1)
    l2 = len(w2)
    result = [[[""] for i in range(l1+1) ] for i in range(l2+1)]
    for i1 in range(0,l1):
        c1 = w1[i1]
        for i2 in range(0,l2):
            c2 = w2[i2]
            if c1 == c2 :
                result[i2+1][i1+1] = [ i + c1 for i in result[i2][i1]]
            else:
                t1 = result[i2][i1+1][0]
                t2 = result[i2+1][i1][0]
                if len(t1) > len (t2):
                    result[i2+1][i1+1] = result[i2][i1+1]
                elif len(t1) == len (t2):
                    result[i2+1][i1+1] = list(set(result[i2][i1+1] + result[i2+1][i1]))
                else:
                    result[i2+1][i1+1] = result[i2+1][i1]
    return result

w1 = "ABCBDAB"
w2 = "BDCABA"
result = lcs(w1,w2)

print("%s\t%s\t%s" % (w1, w2, ",".join(result[len(w2)][len(w1)])))