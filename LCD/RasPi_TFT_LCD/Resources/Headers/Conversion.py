##-------------------------------------------------------------------------------
>>> format(14, '#010b')
'0b00001110'

## The format() function simply formats the input following the Format Specification 
## mini language. The # makes the format include the 0b prefix, and the 010 size formats the output to fit in 10 characters width, with 0 padding; 2 characters for the 0b prefix, the other 8 for the binary digits.

## This is the most compact and direct option.

## If you are putting the result in a larger string, use str.format() and put the second argument for the format() function after the colon of the placeholder {:..}:

>>> 'The produced output, in binary, is: {:#010b}'.format(14)
'The produced output, in binary, is: 0b00001110'

## If you did not want the 0b prefix, simply drop the # and adjust the length of the field:

>>> format(14, '08b')
'00001110'

##-------------------------------------------------------------------------------

def binary(num, pre='0b', length=8, spacer=0):
    return '{0}{{:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])
    
print binary(1)

## Output: '0b00000001'

##-------------------------------------------------------------------------------

bin(1)[2:].zfill(8)

## Output: '00000001'

##-------------------------------------------------------------------------------

print str(1).zfill(2) 
print str(10).zfill(2) 
print str(100).zfill(2)

## 01
## 10
## 100

##-------------------------------------------------------------------------------
