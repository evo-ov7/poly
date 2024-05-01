import math
class _void:
 def __init__(self):
  self.test = None
class _test2:
 def __init__(self):
  self.test2 = None
class really_long_name_my_obj:
 def __init__(self):
  self.bit = None
class main_nest2:
 def __init__(self):
  self.for4 = None
class main_nest:
 def __init__(self):
  self.content = None
  self.nested = main_nest2()
class main_my_obj:
 def __init__(self):
  self.value = None
  self.composite_array = memoryview(bytearray(8*4)).cast('I')
  self.leaf = None
  self.nested = main_nest()
  self.imported_object = None
def really_long_name_add(x,y):
 return 162,11.037
def main_nester(nested,nested3):
 return main_add
def main_add(x,y):
 sum=x+y
 return sum,1.0
def main_add2(x=1,y=2):
 sum=x+y
 return sum,0.0
def main_id(x):
 return x
def main_main():
 func=main_add
 byte=0
 short=0
 int=0
 p=1365
 z1=12297829382473034410
 z2=14757395258967641292
 z4=17361641481138401520
 z8=18374966859414961920
 z16=18446462603027742720
 z32=18446744069414584320
 p=p&~p+1
 if p==0:
  p=32
 else:
  p=(p&z1!=0)|(p&z2!=0)<<(1&0x1f)|(p&z4!=0)<<(2&0x1f)|(p&z8!=0)<<(3&0x1f)|(p&z16!=0)<<(4&0x1f)
 int=p
 p2=4
 p3=12
 p2=p2>>p3|p2<<(32-p3&0x1f)
 int=p2
 while True:
  cool=4
  if int>2:
   break
  elif func!=main_add:
   cool=cool+(2*6-3)
 long=0
 float=0.0
 signed=-1
 double=0.0
 half=0.0
 tiny=0.0
 array=memoryview(bytearray(20*4)).cast('I')
 array[main_id(1)+4]=1
 obj=main_my_obj()
 obj.value=7
 obj.leaf=main_my_obj()
 obj.nested.content=32609532
 object2=obj.leaf
 del (array)
 del (object2)
 del (obj)
 num1,num2=main_add(1,1)
 num1,num2=really_long_name_add(1.0,1)
 array[2],y=main_add2(int,2)
 x,_=main_add2(1,1)
 main_add(1,3)
