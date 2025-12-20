import math

def cal(a):
    li = a.split(" ")
    res =0
    index1 =0
    index2 =0
    op =''
    if '^' in li:
        index1= li.index('^')
        op= li.pop(index1)
    elif '(' in li and ')' in li:
        index1= li.index('(')
        index2= li.index(')')
        sub_li = li[index1+1:index2]
        sub_eq = " ".join(sub_li)
        sub_res = cal(sub_eq)

        li= li[:index1] + [sub_res] + li[index2+1:]
        
        return cal(" ".join(li))
    elif '/' in li:
        index1= li.index('/')
        op= li.pop(index1)
    elif '*' in li:
        index1= li.index('*')
        op= li.pop(index1)
    elif '+' in li:
        index1= li.index('+')
        op= li.pop(index1)
    elif '-' in li:
        index1= li.index('-')
        op= li.pop(index1)
    # print(li, op)
    num1 = float(li.pop(index1-1))
    num2 = float(li[index1-1])
    
    match op:
        case '*':
            res = num1 * num2
        case '/':
            res = num1 / num2
        case '+':
            res = num1 + num2
        case '-':
            res = num1 - num2
        case '^':
            res = pow(num1 , num2)
    

    if len(li)>1:
        li[index1-1] = str(res)
        return cal(" ".join(li))
    else:
        
        li[0] = str(res)
        return li[0]
    

# print(cal("2 + 3 - ( 4 - 2 / 2 ) + 8"))


