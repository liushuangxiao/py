import re

mySent='This book is the best book on Python or M.L. I have ever laid eyes upon.'
print(mySent.split())

regEx = re.compile('\\W*')
listOfTokens = regEx.split(mySent)
print(listOfTokens)

print([tok.lower() for tok in listOfTokens if len(tok) > 0])