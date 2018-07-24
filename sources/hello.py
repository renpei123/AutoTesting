#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('中文显示正常')
s1=72
s2=85
s3=(s2-s1)/s1*100
print(s3)
print('小明成绩提高了 {0:.1f}%'.format(s3))
age=3
if age>=18:
    print('Your age is %d' % age)
    print('Adult')
elif age>6:
    print('Your age is %d' % age)
    print('Teenager')
else:
    print('Your age is %d' % age)
    print('Kid')

S1=input('high(cm):')
S2=input('weight(kg):')
high=int(S1)
weight=int(S2)
BMI= weight/(high/100)**2
print(BMI)
if BMI>32:
    print('严重肥胖')
elif BMI<32 and BMI>28:
    print('肥胖')
elif BMI<28 and BMI>25:
    print('过重')
elif BMI<25 and BMI>18.5:
    print('正常')
elif BMI<18.5:
    print('过轻')

 
    
    
