

ts = "北京大学生活动中心"
ss = "北京,北京大学,大学生,学生,生活,活动,中心"
ts = "广州本田雅阁汽车"
ss = "广州本田,雅阁,本田雅阁,广州,本田,汽车"

seq = {}

for s in ss.split(","):
    ct = seq
    for i in range(len(s)):
        ct = ct.setdefault(s[i], {})
    ct["_is-word"] = True


print(seq)

words = []
cs = seq
start = 0
end = 0
for i in range(len(ts)):
    cs = cs.get(ts[i])
    end = i + 1
    if not cs or (len(cs) == 1 and "_is-word" in cs):
        words.append(ts[start:end])
        start = i + 1
        cs = seq
print(words)


reverseSeq = {}

for s in ss.split(","):
    ct = reverseSeq
    for i in range(len(s)-1, -1, -1):
        ct = ct.setdefault(s[i],{})

words = []
cs = reverseSeq
end = len(ts)
for i in range(len(ts)-1, -1, -1):
    cs = cs.get(ts[i])
    start = i
    if not cs:
        words.append(ts[start:end])
        end = i
        cs = reverseSeq
words.reverse()
print(words)


print("---------- DAG ")

words = {}
for i in range(len(ts)):
    cw = [i]
    cs = seq
    for ic in range(i, len(ts)):
        cs = cs.get(ts[ic])
        if not cs:
            break
        if "_is-word" in cs:
            cw.append(ic)
    words[i] = cw

print(words)