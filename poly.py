import sys,copy,pprint,inspect,traceback,os
import types as ttttttt
pynamespace = ttttttt.SimpleNamespace
debug = False
sample_programm = """
//blash
namespace
object void
 test b4
 
object test2
 test2 void
namespace end

namespace really_long_name
object my_obj
 bit b1
function add(x f2,y s8)->(b4,f1)
 return 0xa2,11.037
namespace really_long_name end

namespace main
import really_long_name as imp



object nest2
 for my_obj

object nest
 content s8
 nested nest2*0

object my_obj
 value b4
 composite_array b4*8
 leaf my_obj
 nested nest*0
 imported_object imp.my_obj
 
function nester(nested fun(nested2 fun*(b4*)->(fun(b4)->()),void fun),nested3 fun(my_obj)->(fun))->(func fun(b1,b2)->())
 return add(fun(b1,b2)->())
 
function add(x b4,y b4)->(b4,f1)
 sum = x+y
 return sum,1.0
 
function add2(x=1 b4,y=2 b4)->(sum b4,sammy f1)
 sum = x + y
 return sum,0.
 
function id(x b2)->(x b2)
 return x
 
function main
 func = add
 byte = 0b
 short = 0s
 int = 0i
 int = 0b010101010101+..0
 int = 4 >>> 12
 loop
  cool = 4s
  if int>2
 break
  elif func!=add
   cool} + 2*6-3
 long = 0l
 float = 0f
 signed = 1i-
 double = 0d
 half = 0h
 tiny = 0q
 array = b4*(20)
 array[id(1)+4] = 1
 //array2 = array+4
 obj = my_obj()
 obj.value = 7
 obj.leaf = my_obj()
 obj.nested.content = 32609532
 object2 = obj.leaf
 delete(array)
 delete(object2)
 delete(obj)
 num1,num2 = add(1,1)
 num1,num2 = imp.add(1,1)
 array[2]=sum,y=sammy = add2(x= int,y= 2)
 x=sum,_ = add2(y= 1)
 add(1,3)
namespace main end
"""


operator_symbols = {"+","-","*","/","~","^","!","=",">","<","|","&","%","#"}
unary_float_operators = {"~>","~.","~^","~v"}
unary_integer_operators = {"+#1","+0..","+..0","~"}
unary_numeric_operators = {"+1","-1"}|unary_float_operators | unary_integer_operators
unary_access_operators = {".","[","(","c"}
unary_operators = unary_numeric_operators | unary_access_operators
binary_asymetric_operators = {">>","<<",">>>","<<<"}
binary_integer_operators = {"^","&","|"}|binary_asymetric_operators
binary_numeric_operators = {"+","-","*","/","%",">","<",">=","<="}|binary_integer_operators
binary_operators = {"=","!="}|binary_numeric_operators
operators = unary_operators|binary_operators
optional_operators = {"+#1","+0..","+..0",">>>","<<<"}
mandatory_operators = operators - optional_operators

literal_unary_float_operators = {"~.","~^","~v"}
literal_unary_integer_operators = {"+#1","+0..","+..0"}
literal_unary_numeric_operators = {"+","-","~"}|unary_integer_operators|unary_float_operators
literal_unary_access_operators = {".","[","("}
literal_unary_operators = unary_float_operators | unary_integer_operators| literal_unary_numeric_operators | literal_unary_access_operators
literal_binary_asymetric_operators = {">>","<<",">>>","<<<"}
literal_binary_integer_operators = {"^","&","|"}|literal_binary_asymetric_operators
literal_binary_numeric_operators = {"+","-","*","/","%",">","<",">=","<="}|literal_binary_integer_operators
literal_binary_operators = {"=","!="}|literal_binary_numeric_operators
literal_operators = literal_unary_operators|literal_binary_operators

control_flow_identifiers = {"if","else","elif","loop","break","continue"}
reserved_identifiers = {"v","return","delete"}|control_flow_identifiers
builtin_functions = {"delete"}

unsigned_integer_types = {"b1","b2","b4","b8"}
signed_integer_types = {"s1","s2","s4","s8"}
integer_types = unsigned_integer_types|signed_integer_types
floating_point_types = {"f1","f2","f4","f8"}
signed_types = signed_integer_types|floating_point_types
unsigned_types = unsigned_integer_types|floating_point_types
numeric_types = integer_types|floating_point_types
default_types = numeric_types|{"fun","*"}
unsigned_compatible_types = {"integer","unsigned","b","f"}|unsigned_types
signed_compatible_types = {"integer","signed","s","f"}|signed_types
float_compatible_types = {"signed","unsigned","f"}|floating_point_types
integer_compatible_types = {"integer","signed","unsigned","s","b"}|integer_types
numeric_compatible_types = float_compatible_types|integer_compatible_types|{"numeric"}
unspecific_types = numeric_compatible_types - default_types
type_specificity = {"*":-1,"numeric":0,"integer":1,"signed":1,"unsigned":1,"s":2,"b":2,"f":2}
compatible_types = {"numeric":numeric_compatible_types,"signed":signed_compatible_types,"unsigned":unsigned_compatible_types,"integer":integer_compatible_types,"s":signed_integer_types|{"s"},"b":unsigned_integer_types|{"b"},"f":floating_point_types|{"f"}}
for type in numeric_types:
 type_specificity[type]=3

b_max = [None,2**8-1,2**16-1,None,2**32-1,None,None,None,2**64-1]
s_max = [None,2**7-1,2**15-1,None,2**31-1,None,None,None,2**63-1]
s_min = [None,-2**7,-2**15,None,-2**31,None,None,None,-2**63]
size_suffix = [None,"b","s",None,"i",None,None,None,"l"]
bit_size = [None,8,16,None,32,None,None,None,64]
type_mask = [None,0xff,0xffff,None,0xffffffff,None,None,None,0xffffffffffffffff]
sign_mask = [None,0x80,0x8000,None,0x80000000,None,None,None,0x8000000000000000]
bitshift_mask = [None,0x7,0xf,None,0x1f,None,None,None,0x3f]



#unused symbols ` ' " ; @ $ \ : { } ?
#negative numbers are two's complement, overflow is always mod 2^N where N is the total number of bits in the type
#unary operators
# + absolute value            only for signed/floats
# - negate                    only for signed/floats
# ~ invert                    
#                             rounding to zero may result in either 0 or -0
# ~ round to nearest          in case of multiple nearest values, the result may be any of them
# ~. round to zero            
# ~^ round to infinity        
# ~v round to negative infinity
# +#1 popcount
# +0.. count leading zeros
# +..0 count trailing zeros
# (type) typeconversion       
#only some conversions are allowed, they are:
#conversions between different sizes of the same number type. if the destination type is smaller, the most significant bytes of integers are truncated and floating point numbers are rounded to the nearest representable value. if the destination type is larger, signed integers are sign-extended, unsigned integers are zero-extended and floating point numbers are rounded to the nearest representable value.
#conversions between signed and unsigned integers truncate if the destination type is smaller and ALWAYS zero-extend if the destination type is larger. there is also NO conversion of negative numbers, the two's complement is left as-is.
#conversions between integers and floats always result in the nearest representable value of the target type(clamping).
#conversions between integer pointer types, only to a type of the same or smaller size as the source, the data itself is not converted
#conversions from any pointer type,object type or function type to void and back. the resulting reference is only allowed to be used if the type before and after conversion to/from void is the same.
#conversions between any function type, uncluding void function. the resulting function may only be called if the function signature of the casted-to type matches the signature of the function pointed to.
# 
# . component access
# [ array access
# (arg,arg2) function call
#
#binary operators
# + add
# - subtract
# * multiply                     result is the lower half of the true result
# / division                     result is the quotient rounded towards zero, if the divisor is 0 the result is 0
# % mod/remainder                result is the remainder with same sign as quotient, if the divisor is 0 the result is the dividend
# ^ xor
# & and
# | or
# >> << bitshift                 signed right shift is sign-extending
# >>> <<< rotate
# > < >= <= = != comparison      
#
#function operators?
# min max
# sqrt sin cos etc
# floating point extraction functions?
# 
#return
#reserved identifiers
#constructors for the remaining types
#variable creation in compound assignment
#delete
#post top-level parsing sanity checks including in type parsing
#compound operator
#basic control flow
#type propagation
#c signed /%, cast to int
#c code block namespaces
#avoid reserved identifiers
#translate optional operators
#reserved name avoidance
#support empty namespace
#c add missing sign-extension when casting
#mark nested types as constant and prevent casting them
#done ^ todo v
#constant optimization
#inlining
#method syntax
#print types correctly in error messages
#figure out how to handle array length
#warning for ambiguous keyword parameters
#preserve constant base
#preserve comments
#generics
#reflection
#more operators ?
#vectors
#atomics
#c optimize spillage
#pointer arithmetic? / c void*
 
def create_programm():
 programm = pynamespace()
 programm.functions = {}
 programm.name = ""
 programm.namespaces = {}
 programm.objects = {}
 programm.parsed = False
 programm.done =False
 programm.global_prefix = ""
 programm.namespace_seperator="_"
 programm.indentation = "  "
 programm.next_identifier =0
 return programm
 
def create_namespace():
 namespace = pynamespace()
 namespace.name = ""
 namespace.imports = {}
 namespace.import_positions={}
 return namespace
 
def create_function():
 function = pynamespace()
 function.kind = "function"
 function.name = ""
 function.namespace = ""
 function.parameters = []
 function.variables = {}
 function.returns = []
 function.parameter_names = {}
 function.return_names = {}
 function.body = []
 function.type = None
 function.inputs = []
 function.value = None
 function.inline = False
 function.metadata = {}
 return function
 
def create_object():
 object = pynamespace()
 object.name = ""
 object.namespace = ""
 object.kind = "object"
 object.variables = {}
 object.methods = []
 object.body = []
 object.type = None
 object.inputs=[]
 object.value = None
 object.metadata ={}
 return object
 
def create_variable():
 variable = pynamespace()
 variable.kind = "variable"
 variable.name = ""
 variable.type = None
 variable.value = None
 variable.default = None
 variable.inputs = []
 variable.metadata = {}
 return variable
 
def create_constant():
 constant = pynamespace()
 constant.kind = "constant"
 constant.type = None
 constant.value = None
 constant.inputs = []
 constant.metadata = {}
 return constant
 
def create_assignment():
 assignment = pynamespace()
 assignment.kind = "assignment"
 assignment.destination = None
 assignment.expression = None
 assignment.special = False
 return assignment
 
def create_linear_expression():
 expression = pynamespace()
 expression.kind = "subexpression"
 expression.components = []
 expression.positions = []
 return expression
 
def create_operation():
 operation = pynamespace()
 operation.kind = ""
 operation.inputs = []
 operation.type = None
 operation.value =None
 operation.metadata = {}
 return operation
 
def create_type():
 type = pynamespace()
 type.kind = ""
 type.pointer = None
 type.length = None
 type.nested = None
 type.size = None
 type.string = ""
 type.parameters = []
 type.returns =[]
 return type
 
def create_control_flow():
 flow = pynamespace()
 flow.kind = ""
 flow.condition = None
 flow.body = []
 flow.next =None
 return flow
 
def warning(message,position,lineno):
 if debug:
  traceback.print_stack()
 if len(position) == 1:
  position = (position[0],0,len(source_lines[position[0]]))
 line,start,end = position
 #if line>0:
  #print(str(line-1)+": "+source_lines[line-1])
 print(str(line)+": "+source_lines[line])
 length = end-start
 indent = len(str(line))+2
 print((indent+start)*" "+length*"^")
 print("poly@"+str(lineno)+": "+message)
 #if line+1<len(source_lines):
  #print()
  #print(str(line+1)+": "+source_lines[line+1])

def error(message,position,lineno):
 warning(message,position,lineno)
 sys.exit(1)
 
def p(*args):
 for arg in args:
  pprint.pprint(arg,width=180)
 
def is_identifier_character(character):
 #ord(character)>=0x41 and ord(character)<=0x5a 
 if ord(character)>=0x61 and ord(character)<=0x7a or character == "_" or ord(character)>=0x30 and ord(character)<=0x39:
  return True
 return False
 
def is_character(character):
 if ord(character)>=0x61 and ord(character)<=0x7a or character == "_":
  return True
 return False
 
def is_number(character):
 if ord(character)>=0x30 and ord(character)<=0x39:
  return True
 return False
 
def skip_space(line,position):
 while position<len(line) and line[position] == " ":
  position+=1
 return position
 
def type_to_string(type):
 string=type.kind
 if type.pointer:
  string+="*"
 if type.kind=="fun" and not type.void:
  string+="("
  for parameter in type.parameters:
   if parameter.name:
    string+=parameter.name+" "
   string+=type_to_string(parameter.type)
   string+=","
  if string[-1]==",":
   string = string[:-1]
  string+=")->("
  for parameter in type.returns:
   if parameter.name:
    string+=parameter.name+" "
   string+=type_to_string(parameter.type)
   string+=","
  if string[-1]==",":
   string = string[:-1]
  string+=")"
 return string
 
def generate_identifier(name_prefix=""):
 number=programm.next_identifier
 if not name_prefix:
  basename="p"
 else:
  basename=name_prefix
 while number!=0:
  if number%36<10:
   basename+=chr(number%36+0x30)
  else:
   basename+=chr(number%36+0x61-10)
  number//=36
 programm.next_identifier+=1
 return basename
 
def check_variable_name(name,function):
 qualified_name = function.namespace.name+programm.namespace_seperator+name
 if name not in function.variables and name not in default_types|reserved_identifiers and name not in function.namespace.imports and qualified_name not in programm.functions and qualified_name not in programm.objects:
  return True
 return False
 
def generate_variable_name(function,invalid_names=set(),name_prefix=""):
 if name_prefix and name_prefix not in invalid_names and check_variable_name(name_prefix,function):
  return name_prefix
 while True:
  variable_name = generate_identifier(name_prefix)
  if variable_name not in invalid_names and check_variable_name(variable_name,function):
   break
 return variable_name
 
def check_global_name(name):
 for function in programm.functions.values():
  if name in function.variables:
   return False
 for namespace in programm.namespaces.values():
  if name == namespace.name or name in namespace.imports:
   return False
 if name in default_types|reserved_identifiers or name in programm.functions or name in programm.objects:
  return False
 return True
 
def generate_global_name(name_prefix="",invalid_names=set(),namespace=""):
 global_prefix =""
 if programm.done:
  global_prefix=programm.global_prefix
 if namespace:
  namespace+=programm.namespace_seperator
 name = global_prefix+namespace+name_prefix
 if name:
  if name not in invalid_names and check_global_name(name):
   return name
 while True:
  global_name = generate_identifier(name)
  if global_name not in invalid_names and check_global_name(global_name):
   break
 return global_name
 
def generate_variable(type,function,invalid_names=None,name_prefix=""):
 variable=create_variable()
 variable.name = generate_variable_name(function,invalid_names,name_prefix)
 variable.type = copy.deepcopy(type)
 function.variables[variable.name]=variable
 return variable
 
def skip_nested(open,close,terminator,context,direction="right"):
 line = context.line
 offset = context.offset
 nesting_level=0
 step = 1
 if direction == "reverse":
  step = -1
 while offset<len(line) and offset>=0:
  character = line[offset]
  if character == open:
   nesting_level+=step
  if character == close:
   nesting_level-=step
  if character == terminator and nesting_level==0:
   break
  offset+=step
 if offset==len(line) or offset<0 or nesting_level!=0:
  return False
 return offset
 
def is_unary_operator(string):
 length = min(4,len(string))
 while length>0:
  if string[:length] in literal_unary_operators:
   return string[:length]
  length-=1
 return ""
 
def is_binary_operator(string):
 length = min(3,len(string))
 while length>0:
  if string[:length] in literal_binary_operators:
   return string[:length]
  length-=1
 return ""

def split_on_space(context):
 line = context.line
 tokens = []
 positions = []
 character = context.offset
 space = False
 if line[character]==" ":
  space = True
 while character<len(line):
  start=character
  while character < len(line) and (line[character] == " " and space or line[character] != " " and not space):
   character+=1
  tokens.append(line[start:character])
  positions.append((context.line_position,start,character))
  space = not space
 return tokens,positions
  
def extract_expression(expression,position):
 positions = [position]
 i=0
 while i<len(positions):
  for input in expression.components[positions[i]].inputs:
   if isinstance(input,int):
    positions.append(input)
  i+=1
 positions.sort()
 assert positions[-1]==position
 for i in range(len(positions)):
  if i>0:
   assert positions[i-1]+1==positions[i]
 extraction_start=positions[0]
 extracted=create_linear_expression()
 extracted.components = copy.deepcopy(expression.components[extraction_start:position+1])
 extracted.positions = copy.deepcopy(expression.positions[extraction_start:position+1])
 for component in extracted.components:
  for i in range(len(component.inputs)):
   if isinstance(component.inputs[i],int):
    component.inputs[i]-=extraction_start
 expression.components[position]=None
 expression.positions[position]=None
 for component in expression.components[position+1:]:
  for i in range(len(component.inputs)):
   if isinstance(component.inputs[i],int):
    if component.inputs[i]>=position:
     component.inputs[i]-=len(positions)-1
 expression.components = expression.components[:extraction_start]+expression.components[position:]
 expression.positions = expression.positions[:extraction_start]+expression.positions[position:]
 return extracted,extraction_start,expression
 
def replace_expression(expression,position,replacement_expression):
 assert expression.components[position]==None
 for component in replacement_expression.components:
  for i in range(len(component.inputs)):
   if isinstance(complement.inputs[i],int):
    component.inputs[i]+=position
 for component in expression.components[position+1:]:
  for i in range(len(component.inputs)):
   if isinstance(component.inputs[i],int):
    if component.inputs[i]>=position:
     component.inputs[i]+=len(replacement_expression.components)-1
 expression.components = expression.components[:position]+replacement_expression.components+expression.components[position+1:]
 expression.positions = expression.positions[:position]+replacement_expression.positions+expression.positions[position+1:]
 return expression
  
def cache_in_variable(expression,position,function,invalid_names=set(),name_prefix=""):
 assignment = create_assignment()
 variable = generate_variable(expression.components[position].type,function,invalid_names,name_prefix)
 variable_expression = create_linear_expression()
 variable_expression.components.append(variable)
 variable_expression.positions.append(expression.positions[position])
 variable.value = expression.components[position].value
 assignment.destination=variable_expression
 assignment.expression,position,old_expression = extract_expression(expression,position)
 return variable,assignment,position,old_expression
 
def expression_can_cause_side_effects(expression):
 for operation in expression.components:
  if operation.kind == "(":
   return True#more sophisticated analysis possible, but only if we don't add global variables
 return False

def rename_variable(old_name,new_name,function):
 assert check_variable_name(new_name,function)
 variable = function.variables[old_name]
 variable.name = new_name
 function.variables[new_name] = variable
 del function.variables[old_name]

def rename_function(old_name,new_name):
 assert check_global_name(new_name)
 function = programm.functions[old_name]
 function.name = new_name
 programm.functions[function.name] = function
 del programm.functions[old_name]
 
def rename_objects(objects):
 type_translations = {}
 for old_name,new_name in objects:
  assert check_global_name(new_name)
  object = programm.objects[old_name]
  type_translations[old_name]=new_name
  object.name = new_name
  object.type.kind = new_name
  programm.objects[object.name] = object
  del programm.objects[old_name]
 rename_types(type_translations)
 
def rename_fields(fields):
 type_translations={}
 for old_name,new_name,object in fields:
  type_translations[object.name+old_name]=new_name
  variable = object.variables[old_name]
  variable.name = new_name
  object.variables[variable.name] = variable
  del object.variables[old_name]
 rename_fields2(type_translations)

def replace_reserved_identifiers(reserved_identifiers):
 for function in list(programm.functions.values()):
  if function.name in reserved_identifiers:
   old_name = function.name
   function.name = generate_global_name(function.name,reserved_identifiers)
   programm.functions[function.name] = function
   del programm.functions[old_name]
  for variable in list(function.variables):
   if variable in reserved_identifiers:
    new_name = generate_variable_name(function,invalid_names=reserved_identifiers,name_prefix=variable)
    rename_variable(variable,new_name,function)
 type_translations = {}
 for object in list(programm.objects.values()):
  if object.name in reserved_identifiers:
   type_translations[object.name]=generate_global_name(object.name,reserved_identifiers)
   old_name = object.name
   object.name = type_translations[object.name]
   object.type.kind = object.name
   programm.objects[object.name] = object
   del programm.objects[old_name]
 rename_types(type_translations)
 type_translations.clear()
 for object in list(programm.objects.values()):
  for variable in list(object.variables.values()):
   if variable.name in reserved_identifiers:
    type_translations[object.name+variable.name]=generate_variable_name(object,reserved_identifiers,variable.name)
    old_name = variable.name
    variable.name = type_translations[object.name+variable.name]
    object.variables[variable.name] = variable
    del object.variables[old_name]
 rename_fields2(type_translations)
 
def transform_inline_function(destination,expression2,context):
 preamble=[]
 for i in range(2):
  expression = destination
  if i==1:
   expression = expression2
  if expression:
   for i,operation in enumerate(expression.components):
    if operation.kind=="(":
     input = expression.components[operation.inputs[0]]
     if input.kind == "function":
      function = input
     elif input.value:
      function = input.value
     else:
      continue
     if function.inline:
      function2 = copy.deepcopy(function)
      invalid_names = list(context.function.variables)
      for variable in function2.variables.values():
       if variable.name in context.function.variables:
        rename_variable(variable.name,generate_variable_name(function2,invalid_names,variable.name),function2)
      function_call,hole_position,expression = extract_expression(expression,i)
      parameter_expressions = []
      parameter_count = len(function_call.components[-1].inputs)-1
      for i in range(parameter_count):
       parameter_location = function_call.components[-1].inputs[i+1]
       parameter_expression,_,function_call = extract_expression(function_call,parameter_location)
       parameter_expressions.append(parameter_expression)
      assert parameter_count == len(function2.parameters)
      for i,variable in enumerate(function2.parameters.values()):
       variable_expression = create_linear_expression()
       variable_expression.components.append(variable)
       variable_expression.positions.append([0])
       assignment = create_assignment()
       assignment.destination = variable_expression
       assignment.expression = parameter_expressions[i]
       preamble.append(assignment)  
      if len(function2.returns)==1 and len(expression.components)>1:
       return_variable = generate_variable(function2.returns[0].type,function2,invalid_names)
       variable_expression = create_linear_expression()
       variable_expression.components.append(return_variable)
       variable_expression.positions.append([0])
       replace_expression(expression,hole_position,variable_expression)
       context.return_expressions = [variable_expression]
      else:
       expression=None
      preamble.extend(transform_inline_function_body(function2.body,context))
 return destination,expression2,preamble
 
def transform_inline_instruction(instruction,transformer,context):
 declarations=[]
 if instruction.kind=="assignment" and (not instruction.special or not instruction.destination):
  instruction.destination,instruction.expression,declaration = transformer(instruction.destination,instruction.expression,context)
  declarations.extend(declaration)
 elif instruction.kind=="assignment" and instruction.special:
  if instruction.destination=="return":
   for i,_ in enumerate(instruction.expression):
    _,instruction.expression[i],declaration = transformer(None,instruction.expression[i],context)
    declarations.extend(declaration)
  else:
   context.return_expressions = []
   if instruction.destination:
    for i,_ in enumerate(instruction.destination):
     instruction.destination[i],_,declaration = transformer(instruction.destination[i],None,context)
     declarations.extend(declaration)
     context.return_expressions.append(instruction.destination[i])
   _,instruction.expression,declaration = transformer(None,instruction.expression,context)
   declarations.extend(declaration)
   del context.return_expressions
   instruction = None
 else:
  assert instruction.kind in control_flow_identifiers
 return instruction,declarations
 
def transform_instruction(instruction,transformer,context):
 declarations=[]
 if instruction.kind=="assignment" and (not instruction.special or not instruction.destination):
  instruction.destination,instruction.expression,declaration = transformer(instruction.destination,instruction.expression,context)
  declarations.extend(declaration)
 elif instruction.kind=="assignment" and instruction.special:
  if instruction.destination=="return":
   for i,_ in enumerate(instruction.expression):
    _,instruction.expression[i],declaration = transformer(None,instruction.expression[i],context)
    declarations.extend(declaration)
  else:
   _,instruction.expression,declaration = transformer(None,instruction.expression,context)
   declarations.extend(declaration)
   for i,_ in enumerate(instruction.destination):
    instruction.destination[i],_,declaration = transformer(instruction.destination[i],None,context)
    declarations.extend(declaration)
 else:
  assert instruction.kind in control_flow_identifiers
 return instruction,declarations
 
def transform_code(code,expression_transformer,context,instruction_transformer=transform_instruction):
 i=0
 while i < len(code):
  instruction = code[i]
  code[i],declaration =instruction_transformer(instruction,expression_transformer,context)
  if declaration:
   if not code[i]:
    del code[i]
   code = code[:i]+declaration+code[i:]
  else:
   i+=1
  if instruction.kind in control_flow_identifiers and instruction.body:
   instruction.body = transform_code(instruction.body,expression_transformer,context,instruction_transformer)
   
 return code

def cache_binary_operator(expression,operator_index,context,invalid_names=set()):
 preamble=[]
 binary_expression,hole_position,expression = extract_expression(expression,operator_index)
 operand1_variable,operand1_instruction,hole_position,binary_expression = cache_in_variable(binary_expression,binary_expression.components[-1].inputs[0],context.function,invalid_names=invalid_names)
 preamble.append(operand1_instruction)
 variable_expression = create_linear_expression()
 variable_expression.components.append(operand1_variable)
 variable_expression.positions.append((0,0,0))
 expression = replace_expression(expression,hole_position,variable_expression)
 operand2_variable,operand2_instruction,hole_position,binary_expression = cache_in_variable(binary_expression,binary_expression.components[-1].inputs[1],context.function,invalid_names=invalid_names)
 preamble.append(operand2_instruction)
 return operand1_variable,operand2_variable,preamble,expression

def transform_rename_fields(destination,expression2,context):
 preamble=[]
 type_translations = context.type_translations
 for expression in [destination,expression2]:
  if expression:
   for i,operation in enumerate(expression.components):
    if i>0 and operation.kind=="." and expression.components[i-1].type.kind+operation.inputs[1] in type_translations:
     operation.inputs[1]=type_translations[expression.components[i-1].type.kind+operation.inputs[1]]
 return destination,expression2,preamble

def rename_fields2(type_translations):
 context = pynamespace()
 context.type_translations = type_translations
 for function in programm.functions.values():
  context.function = function
  function.body = transform_code(function.body,transform_rename_fields,context)

def transform_rename_types(destination,expression2,context):
 preamble=[]
 type_translations = context.type_translations
 for expression in [destination,expression2]:
  if expression:
   for operation in expression.components:
    if operation.type and operation.type.kind in type_translations:
     operation.type.kind = type_translations[operation.type.kind]
 return destination,expression2,preamble

def rename_types(type_translations):
 for object in programm.objects.values():
  for variable in object.variables.values():
   if variable.type.kind in type_translations:
    variable.type.kind = type_translations[variable.type.kind]
 context = pynamespace()
 context.type_translations = type_translations
 for function in programm.functions.values():
  context.function = function
  function.body = transform_code(function.body,transform_rename_types,context)
  for variable in function.parameters:
   if variable.type.kind in type_translations:
    variable.type.kind = type_translations[variable.type.kind]
  for variable in function.returns:
   if variable.type.kind in type_translations:
    variable.type.kind = type_translations[variable.type.kind]
    
def transform_optional_operators(destination,expression2,context):
 preamble=[]
 for expression in [destination,expression2]:
  i=0
  while expression and i<len(expression.components):
   operation = expression.components[i]
   if operation.kind in optional_operators and operation.kind not in context.supported_operators:
    if operation.kind in {">>>","<<<"}:
     operand1,operand2,declarations,expression = cache_binary_operator(expression,i,context)
     preamble.extend(declarations)
     code=[]
     shift = operation.kind[:-1]
     if shift[0]==">":
      shift2 = "<<"
     else:
      shift2 = ">>"
     code.append(" "+operand1.name+"="+operand1.name+shift+operand2.name+"  |  "+operand1.name+" "+shift2+" "+str(bit_size[operation.type.size])+"-"+operand2.name)
     code2=parse_code_body(code,context.function)
     preamble.extend(code2)
     i=0
    elif operation.kind=="+#1":
     variable,variable_assignment,hole_position,expression = cache_in_variable(expression,i,context.function)
     variable_assignment.expression.components = variable_assignment.expression.components[:-1]
     variable_assignment.expression.positions = variable_assignment.expression.positions[:-1]
     preamble.append(variable_assignment)
     variable_expression=create_linear_expression()
     variable_expression.components.append(variable)
     variable_expression.positions.append((0,0,0))
     expression = replace_expression(expression,hole_position,variable_expression)
     code=[]
     if "popcount" not in context.function.metadata:
      m1 = generate_variable_name(context.function,name_prefix="m1")
      m2 = generate_variable_name(context.function,name_prefix="m2")
      m4 = generate_variable_name(context.function,name_prefix="m4")
      context.function.metadata["popcount"]=(m1,m2,m4)
      code.append(" "+m1+"=0x5555555555555555"+"l")
      code.append(" "+m2+"=0x3333333333333333"+"l")
      code.append(" "+m4+"=0x0f0f0f0f0f0f0f0f"+"l")
     m1,m2,m4 = context.function.metadata["popcount"]
     code.append(" "+variable.name+"="+variable.name+" - "+variable.name+">>1&"+m1+"(b"+str(operation.type.size)+")")
     code.append(" "+variable.name+"="+variable.name+"&"+m2+"(b"+str(operation.type.size)+")"+" + "+variable.name+">>2&"+m2+"(b"+str(operation.type.size)+")")
     code.append(" "+variable.name+"="+variable.name+">>4+"+variable.name+"&"+m4+"(b"+str(operation.type.size)+")")
     size = operation.type.size
     size2 = 8
     while size>1:
      code.append(" "+variable.name+"="+variable.name+">>"+str(size2)+"+"+variable.name)
      size = size//2
      size2 = size2*2
     code.append(" "+variable.name+"}&0x"+format(bitshift_mask[operation.type.size],"x"))
     code2=parse_code_body(code,context.function)
     preamble.extend(code2)
     i=0
    elif operation.kind in {"+0..","+..0"}:
     variable,variable_assignment,hole_position,expression = cache_in_variable(expression,i,context.function)
     variable_assignment.expression.components = variable_assignment.expression.components[:-1]
     variable_assignment.expression.positions = variable_assignment.expression.positions[:-1]
     preamble.append(variable_assignment)
     variable_expression=create_linear_expression()
     variable_expression.components.append(variable)
     variable_expression.positions.append((0,0,0))
     expression = replace_expression(expression,hole_position,variable_expression)
     code=[]
     if operation.kind =="+..0" and "count_trailing_zeros" not in context.function.metadata:
      z1 = generate_variable_name(context.function,name_prefix="z1")
      z2 = generate_variable_name(context.function,name_prefix="z2")
      z4 = generate_variable_name(context.function,name_prefix="z4")
      z8 = generate_variable_name(context.function,name_prefix="z8")
      z16 = generate_variable_name(context.function,name_prefix="z16")
      z32 = generate_variable_name(context.function,name_prefix="z32")
      context.function.metadata["count_trailing_zeros"]=(z1,z2,z4,z8,z16,z32)
      code.append(" "+z1+"=0xaaaaaaaaaaaaaaaa"+"l")
      code.append(" "+z2+"=0xcccccccccccccccc"+"l")
      code.append(" "+z4+"=0xf0f0f0f0f0f0f0f0"+"l")
      code.append(" "+z8+"=0xff00ff00ff00ff00"+"l")
      code.append(" "+z16+"=0xffff0000ffff0000"+"l")
      code.append(" "+z32+"=0xffffffff00000000"+"l")
     elif operation.kind =="+0.." and "count_leading_zeros" not in context.function.metadata:
      z1 = generate_variable_name(context.function,name_prefix="z1")
      z2 = generate_variable_name(context.function,name_prefix="z2")
      z4 = generate_variable_name(context.function,name_prefix="z4")
      z8 = generate_variable_name(context.function,name_prefix="z8")
      z16 = generate_variable_name(context.function,name_prefix="z16")
      z32 = generate_variable_name(context.function,name_prefix="z32")
      context.function.metadata["count_leading_zeros"]=(z1,z2,z4,z8,z16,z32)
      code.append(" "+z1+"=0x5555555555555555"+"l")
      code.append(" "+z2+"=0x3333333333333333"+"l")
      code.append(" "+z4+"=0x0f0f0f0f0f0f0f0f"+"l")
      code.append(" "+z8+"=0x00ff00ff00ff00ff"+"l")
      code.append(" "+z16+"=0x0000ffff0000ffff"+"l")
      code.append(" "+z32+"=0x00000000ffffffff"+"l")
     if operation.kind == "+0..":
      z1,z2,z4,z8,z16,z32 = context.function.metadata["count_leading_zeros"]
     else:
      z1,z2,z4,z8,z16,z32 = context.function.metadata["count_trailing_zeros"]
     var2 = generate_variable_name(context.function)
     z_cast = ""
     if operation.type.size<8 or operation.type.kind[0]=="s":
      z_cast="("+operation.type.kind+")"
     code.append(" "+variable.name+"="+variable.name+" & "+variable.name+"~+1")
     code.append(" if "+variable.name+"=0")
     code.append("  "+variable.name+"="+str(bit_size[operation.type.size]))
     code.append(" else")
     tmp_code ="  "+variable.name+"="+variable.name+"&"+z1+z_cast+"!=0"
     tmp_code+=" | "+variable.name+"&"+z2+z_cast+"!=0<<1"
     tmp_code+=" | "+variable.name+"&"+z4+z_cast+"!=0<<2"
     if operation.type.size>1:
      tmp_code+=" | "+variable.name+"&"+z8+z_cast+"!=0<<3"
     if operation.type.size>2:
      tmp_code+=" | "+variable.name+"&"+z16+z_cast+"!=0<<4"
     if operation.type.size>4:
      tmp_code+=" | "+variable.name+"&"+z32+z_cast+"!=0<<5"
     code.append(tmp_code)
     code2=parse_code_body(code,context.function)
     preamble.extend(code2)
     i=0
   else:
    i+=1
 return destination,expression2,preamble

def convert_unsupported_operators(supported_operators):
 context = pynamespace()
 context.supported_operators = supported_operators
 for function in programm.functions.values():
  context.function = function
  function.body = transform_code(function.body,transform_optional_operators,context)
  function.metadata.clear()

def parse_identifier_string(line):
 i=0
 if i<len(line) and is_character(line[i]):
  i+=1
  while i<len(line) and is_identifier_character(line[i]):
   i+=1
 return line[:i]
 
def verify_identifier_string(string,context):
 offset = context.offset
 name = parse_identifier_string(string)
 if name != string:
  error("invalid identifier character "+string[len(name)],(context.line_position,offset+len(name),offset+len(name)+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  
def append_expressions(expression1,expression2):
 for i in range(len(expression2.components)):
  for e in range(len(expression2.components[i].inputs)):
   expression2.components[i].inputs[e] += len(expression1.components)
 for i in range(len(expression2.components)):
  expression1.components.append(expression2.components[i])
  expression1.positions.append(expression2.positions[i])
  
def type_intersection(type1,type2):
 if type1.kind == "*":
  if type2.kind in numeric_types and not type2.pointer:
   return None
  return copy.deepcopy(type2)
 if type2.kind == "*":
  if type1.kind in numeric_types and not type1.pointer:
   return None
  return copy.deepcopy(type1)
 if type1.kind!=type2.kind and (type1.kind not in numeric_compatible_types or type2.kind not in numeric_compatible_types) or type1.pointer!=type2.pointer  or (type1.size and type2.size and type1.size != type2.size):
  return None
 if type1.kind == type2.kind:
  return copy.deepcopy(type1)
 type = create_type()
 if type1.size or type2.size:
  if type1.size:
   type.size = type1.size
  else:
   type.size = type.size
 specificity1 = type_specificity[type1.kind]
 specificity2 = type_specificity[type2.kind]
 if specificity1>specificity2:
  tmp = type1
  type1=type2
  type2=tmp
  tmp = specificity1
  specificity1 = specificity2
  specificity2 = tmp
 if type1.kind not in compatible_types or type2.kind not in compatible_types[type1.kind]:
  return None
 if specificity1!=specificity2 or specificity1!=1:
  type.kind = type2.kind
  if specificity2==2 and type.size:
   type.kind+=str(type.size)
 else:
  types = {type1.kind,type2.kind}
  size = ""
  if type.size:
   size = str(type.size)
  if types == {"integer","unsigned"}:
   type.kind = "b"+size
  elif types == {"integer","signed"}:
   type.kind = "s"+size
  elif types == {"unsigned","signed"}:
   type.kind = "f"+size
 if type1.string:
  type.string = type1.string
 if type2.string:
  type.string = type2.string
 return type
 
def new_variable(variable_name,variable_start,variable_type,context):
 if not check_variable_name(variable_name,context.function):
  if variable_name in default_types:
   error("cannot use type "+variable_name+" as variable",(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  if variable_name in reserved_identifiers:
   error("cannot use reserved identifier "+variable_name+" as variable",(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  if variable_name in context.function.namespace.imports:
   error("cannot use imported namespace "+variable_name+" as variable",(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  if variable_name in context.function.variables:
   error("variable "+variable_name+" already exists in "+context.function.name,(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  qualified_name = context.function.namespace.name+programm.namespace_seperator+variable_name
  if qualified_name in programm.objects:
   error("cannot use object "+variable_name+" as variable",(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  if qualified_name in programm.functions:
   error("cannot use function "+variable_name+" as variable",(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  if variable_type.kind in unspecific_types:
   error("ambiguous type "+variable_type.kind,(context.line_position,variable_start,variable_start+len(variable_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  assert False
 variable = create_variable()
 variable.name = variable_name
 variable.type = copy.deepcopy(variable_type)
 expression = create_linear_expression()
 expression.components.append(variable)
 expression.positions.append((context.line_position,variable_start,variable_start+len(variable_name)))
 return variable,expression
  
def propagate_types(expression,context):
 change=True
 while change:
  change=False
  for operator in expression.components:
   if operator.type and operator.type.kind not in unspecific_types:
    if operator.value != None and operator.type.kind in integer_types:
     operator.value = int(operator.value)
    for index,input in enumerate(operator.inputs):
     if isinstance(input,int) and expression.components[input].type:
      if expression.components[input].type.kind in unspecific_types:
       change=True
       if operator.kind not in binary_asymetric_operators or index==0:
        expression.components[input].type = copy.deepcopy(operator.type)
        if operator.kind=="constant":
         if operator.type in integer_types:
          operator.value = int(operator.value)
       else:
        new_type = create_type()
        if expression.components[input].type.kind in {"s","signed"}:
         new_type.kind="s1"
        else:
         new_type.kind="b1"
        new_type.size=1
        new_type.string=new_type.kind
        expression.components[input].type = new_type
   
    
   
 for index,operator in enumerate(expression.components):
  if operator.type and operator.type.kind in unspecific_types:
   error("couldn't statically type "+operator.type.kind,expression.positions[index],inspect.getframeinfo(inspect.currentframe()).lineno)

def parse_constant(context):
 line = context.line
 offset = context.offset
 start = offset
 mode = "decimal"
 binary = {"0","1"}
 hex = {"a","b","c","d","e","f"}
 if not is_number(line[offset]) and line[offset]!=".":
  error("expected number",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if line[offset]=="0":
  if offset+1<len(line):
   if line[offset+1] in {"x","b"}:
    if offset+2<len(line):
     if line[offset+1] == "x" and (is_number(line[offset+2]) or line[offset+2] in hex):
      mode="hexadecimal"
      offset+=2
     elif line[offset+1] == "x":
      error("expected hexnumber",(context.line_position,offset+2,offset+3),inspect.getframeinfo(inspect.currentframe()).lineno)
     elif line[offset+1] == "b" and line[offset+2] in binary:
      mode="binary"
      offset+=2
    elif line[offset+1] == "x":
     error("expected hexnumber",(context.line_position,offset+2,offset+3),inspect.getframeinfo(inspect.currentframe()).lineno)
 constant = create_constant()
 number = ""
 while offset<len(line):
  digit = line[offset]
  if mode == "fraction":
   if is_number(digit):
    number+=digit
   else:
    break
  elif mode == "decimal":
   if digit==".":
    mode = "fraction"
    number+=digit
   elif is_number(digit):
    number+=digit
   else:
    break
  elif mode == "binary":
   if digit in binary:
    number+=digit
   else:
    break
  elif mode == "hexadecimal":
   if (digit in hex or is_number(digit)) and (digit!="b" or len(number)!=2):
    if offset+1>=len(line) or (line[offset+1] not in hex and not is_number(line[offset+1])):
     error("expected hexnumber",(context.line_position,offset+1,offset+2),inspect.getframeinfo(inspect.currentframe()).lineno)
    number+=digit+line[offset+1]
    offset+=1
   else:
    break
  offset+=1
 type = create_type()
 value = None
 if mode == "decimal":
  value = float(number)
 elif mode == "fraction":
  value = float(number)
 elif mode == "binary":
  value = int(number,2)
 elif mode == "hexadecimal":
  value = int(number,16)
 suffixes = {"b":1,"s":2,"i":4,"l":8,"d":8,"f":4,"h":2,"q":1}
 size_suffix = ""
 if offset<len(line) and line[offset] in suffixes:
  number+=line[offset]
  size_suffix = line[offset]
  offset+=1
 if size_suffix in {"b","s","i","l"}:
  if mode =="fraction":
   error("invalid floating point suffix "+size_suffix,(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  value = int(value)
  size = suffixes[size_suffix]
  type.size = size
  if value > b_max[size]:
   error("value "+str(value)+" too big for "+size_suffix,(context.line_position,start,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  type.kind="integer"
 elif size_suffix in {"d","f","h","q"}:
  if mode in {"binary","hexadecimal"}:
   error("invalid integer suffix "+size_suffix,(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  size = suffixes[size_suffix]
  type.size = size
  type.kind = "f"+str(size)
 elif mode == "fraction":
  type.kind = "f"
 elif mode in {"binary","hexadecimal"}:
  value=int(value)
  type.kind = "integer"
 else:
  type.kind = "numeric"
 constant.type = type
 constant.value = value
 return constant,line[start:offset]
  
def parse_function_signature_components(context):
 line = context.line
 offset = context.offset
 parameters = [""]
 positions = [offset+1]
 nesting_level = 1
 offset+=1
 while offset<len(line):
  if line[offset] == "," and nesting_level==1:
   parameters.append("")
   positions.append(offset+1)
  else:
   if line[offset] == ")":
    nesting_level-=1
    if nesting_level==0:
     break
   parameters[-1]+=line[offset]
   if line[offset]=="(":
    nesting_level+=1
  offset+=1
 if nesting_level!=0:
  error("incomplete function signature",(context.line_position,positions[0],offset),inspect.getframeinfo(inspect.currentframe()).lineno)
 if not parameters[-1]:
  del parameters[-1]
  del positions[-1]
 return parameters,positions
 
def parse_function_signature_parameters(parameters,positions,context):
 line = context.line
 parameter_names={}
 returns=[]
 for i in range(len(parameters)):
  parameter = parameters[i]
  offset = positions[i]
  constant = None
  parameter_variable=create_variable()
  offset2=0
  if " " in parameter and not(len(parameter)>=4 and parameter[:4] in{"fun(","fun*"}):
   parameter_name = parse_identifier_string(parameter)
   if not parameter_name:
    error("invalid character in return name",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   if parameter_name in parameter_names:
    error("duplicate return "+parameter_name,(context.line_position,offset,offset+len(parameter_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
   parameter_names[parameter_name]=parameter_variable
   parameter_variable.name = parameter_name
   offset2+=len(parameter_name)
   if parameter[offset2]=="=":
    offset2+=1
    context.offset = offset+offset2
    constant,constant_string = parse_constant(context)
    offset2+=len(constant_string)
    if offset2>=len(parameter):
     error("missing parameter type",(context.line_position,offset+offset2,offset+offset2+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   if parameter[offset2]!=" ":
    error("invalid character in return name",(context.line_position,offset+offset2,offset+offset2+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   offset2+=1
  context.offset=offset+offset2
  parameter_type = parse_type(context)
  parameter_variable.type = parameter_type
  if offset2+len(parameter_type.string)!=len(parameter):
   error("trailing characters in return declaration",(context.line_position,offset+offset2+len(parameter_type.string),offset+len(parameter)),inspect.getframeinfo(inspect.currentframe()).lineno)
  if constant:
   intersection = type_intersection(constant.type,parameter_type)
   if not intersection:
    error("constant type "+constant.type.kind+" incompatible with parameter type "+parameter_type.kind,(context.line_position,offset,offset+len(parameter)),inspect.getframeinfo(inspect.currentframe()).lineno)
   parameter_variable.default = constant.value
   if intersection.kind in integer_types:
    parameter_variable.default = int(parameter_variable.default) 
  returns.append(parameter_variable)
 return returns
 
def parse_function_signature(context,names_required=True):
 line = context.line
 offset = context.offset
 start = offset
 input_names = {}
 return_names = {}
 inputs = []
 returns =[]
 parameters,positions = parse_function_signature_components(context)
 inputs = parse_function_signature_parameters(parameters,positions,context)
 for i,input in enumerate(inputs):
  if not input.name and names_required:
   error("missing parameter",(context.line_position,positions[i],positions[i]+len(parameters[i])),inspect.getframeinfo(inspect.currentframe()).lineno)
  if input.name:
   input_names[input.name]=input
 if positions:
  offset = positions[-1]+len(parameters[-1])
 else:
  offset+=1
 if line[offset]!=")":
  error("expected )",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 offset+=1
 if offset+1<len(line) and line[offset:offset+2]=="->":
  offset+=2
  if len(line)<offset or line[offset]!="(":
   error("expected returns",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  context.offset=offset
  parameters,positions = parse_function_signature_components(context)
  returns = parse_function_signature_parameters(parameters,positions,context)
  for i,input in enumerate(returns):
   if input.default:
    error("default return value not allowed",(context.line_position,positions[i],positions[i]+len(parameters[i])),inspect.getframeinfo(inspect.currentframe()).lineno)
   if input.name:
    return_names[input.name]=input
  if positions:
   offset=positions[-1]+len(parameters[-1])+1
  else:
   offset+=2
 return inputs,returns,line[start:offset],input_names,return_names

def parse_type(context):
 line = context.line
 offset = context.offset
 type_start = offset
 basename = parse_identifier_string(line[offset:])
 if not basename:
  if  line[offset]=="*":
   basename="*"
  else:
   error("expected type",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 type = create_type()
 if basename in context.namespace.imports:
  offset2= offset+len(basename)
  basename = context.namespace.imports[basename]+programm.namespace_seperator
  if offset2>=len(line) or line[offset2]!=".":
   error("expected namespaced type name",(context.line_position,offset2,offset2+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  offset2+=1
  name = parse_identifier_string(line[offset2:])
  if not name:
   error("expected type name",(context.line_position,offset2,offset2+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  basename+=name
  if programm.parsed and basename not in programm.objects:
   error("unknown type "+basename,(context.line_position,offset,offset+offset2+1+len(name)),inspect.getframeinfo(inspect.currentframe()).lineno)
  offset+=len(basename)
  type.string = basename
 elif basename not in default_types:
  offset2=len(basename)
  type.string = basename
  basename = context.namespace.name+programm.namespace_seperator+basename
  if programm.parsed and basename not in programm.objects:
   error("unknown type "+basename,(context.line_position,offset,offset+offset2),inspect.getframeinfo(inspect.currentframe()).lineno)
  offset+=offset2
 else:
  offset+=len(basename)
  type.string = basename
 type.kind =basename
 if basename in numeric_types:
  type.size = int(basename[-1])
 if offset<len(line):
  if line[offset]=="*":
   type.pointer = True
   type.string += "*"
   offset+=1
   start = offset
   while offset<len(line) and is_number(line[offset]):
    offset+=1
   if offset>start:
    type.length = int(line[start:offset])
    type.nested = True
    if type.length==0:
     if type.kind in numeric_compatible_types:
      error("single numbers are already nested",(context.line_position,type_start,offset),inspect.getframeinfo(inspect.currentframe()).lineno)
     type.pointer=False
    type.string += line[start:offset]
  if basename == "fun":
   if line[offset]=="(":
    type.void=False
    context.offset=offset
    type.parameters,type.returns,signature_string,type.parameter_names,type.return_names = parse_function_signature(context,names_required=False)
    type.string += signature_string
   else:
    type.void=True
 return type
 
def parse_unary_operator(operator,context):
 input = context.expression.components[-1]
 line = context.line
 offset = context.offset
 operation = create_operation()
 operation.kind = operator
 operation.inputs = [len(context.expression.components)-1]
 if operator in literal_unary_numeric_operators:
  if input.type.kind not in numeric_compatible_types:
   error("expected number for "+operator+" but got "+input.type.kind,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
  operator_type = create_type()
  if operator in {"+","-"}:
   operation.kind = operator+"1"
   operator_type.kind="s"
  elif operator in literal_unary_float_operators:
   operator_type.kind="f"
  elif operator in literal_unary_integer_operators:
   operator_type.kind="integer"
  else:
   operator_type.kind="numeric"
  result_type = type_intersection(input.type,operator_type)
  if not result_type:
   error("invalid input type "+input.type.kind+" for "+operator,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
  operation.type = result_type
  if input.value:
   pass#precompute
  return operation,context.offset+len(operator)
 elif operator in literal_unary_access_operators:
  if operator == ".":
   compartment_name = parse_identifier_string(line[offset+1:])
   if not compartment_name:
    error("missing name after .",(context.line_position,context.offset+1,context.offset+2),inspect.getframeinfo(inspect.currentframe()).lineno)
   if input.kind not in {"variable",".","["}:
    error("invalid input type "+input.type.kind+" for "+operator,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
   if input.type.kind not in programm.objects:
    error("invalid input type "+input.type.kind+" for "+operator,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
   if compartment_name not in programm.objects[input.type.kind].variables:
    error("object "+input.type.kind+" has no field "+compartment_name,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
   operation.inputs.append(compartment_name)
   operation.type = programm.objects[input.type.kind].variables[compartment_name].type
   return operation,offset+len(compartment_name)+1
  elif operator == "[":
   if not input.type.pointer:
    error("array access on non-pointer type "+input.type.kind,(context.line_position,offset,context.offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   context.offset = offset
   subexpression_end = skip_nested("[","]","]",context)
   offset+=1
   context.offset = offset
   context.line = line[:subexpression_end]
   old_expression = context.expression
   subexpression = parse_expression(context)
   context.expression = old_expression
   subexpression_type =subexpression.components[-1].type
   context.line = line
   new_type = create_type()
   new_type.kind="integer"
   new_type = type_intersection(subexpression_type,new_type)
   if not new_type:
    error("got type "+subexpression_type.string+" for array access",(context.line_position,offset,subexpression_end),inspect.getframeinfo(inspect.currentframe()).lineno)
   if subexpression_type.kind in unspecific_types:
    if new_type.kind in unspecific_types:
     if new_type.kind == "s":
      new_type.kind="s4"
     else:
      new_type.kind="b4"
     new_type.size=4
     new_type.string = new_type.kind
    subexpression.components[-1].type = new_type
   append_expressions(context.expression,subexpression)
   operation.inputs.append(len(context.expression.components)-1)
   operation.type = copy.deepcopy(input.type)
   operation.type.pointer = None
   return operation,subexpression_end+1
  elif operator == "(":
   if input.kind!="object" and (input.kind!="function" and input.type.kind!="fun" or  parse_identifier_string(line[offset+1:]) == "fun"):
    #typeconversion
    operation.kind="c"
    offset+=1
    if offset>=len(line):
     error("missing type",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
    context.offset=offset
    target_type = parse_type(context)
    if line[offset+len(target_type.string)]!=")":
     error("trailing characters after type",(context.line_position,offset+len(target_type.string),offset+len(target_type.string)+1),inspect.getframeinfo(inspect.currentframe()).lineno)
    if target_type.kind!="*" and input.type.kind!="*":
     if target_type.nested:
      error("cannot convert into nested type "+target_type.string,(context.line_position,offset,offset+len(target_type.string)),inspect.getframeinfo(inspect.currentframe()).lineno)
     if input.type.nested:
      error("cannot convert nested type "+input.type.string,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
     if (target_type.kind in numeric_compatible_types) != (input.type.kind in numeric_compatible_types):
      error("cannot convert type "+input.type.string+" into "+target_type.string,(context.line_position,offset,offset+len(target_type.string)),inspect.getframeinfo(inspect.currentframe()).lineno)
     if target_type.pointer != input.type.pointer:
      error("cannot convert type "+input.type.string+" into "+target_type.string,(context.line_position,offset,offset+len(target_type.string)),inspect.getframeinfo(inspect.currentframe()).lineno)
     if target_type.pointer and target_type.kind in numeric_types and input.type.size and target_type.size>input.type.size:
      error("cannot convert type "+input.type.string+" into "+target_type.string,(context.line_position,offset,offset+len(target_type.string)),inspect.getframeinfo(inspect.currentframe()).lineno)
    else:
     if target_type.kind in numeric_compatible_types and not target_type.pointer:
      error("cannot convert type "+input.type.string+" into "+target_type.string,(context.line_position,offset,offset+len(target_type.string)),inspect.getframeinfo(inspect.currentframe()).lineno)
     if input.type.kind in numeric_compatible_types and not input.type.pointer:
      error("cannot convert type "+input.type.string+" into "+target_type.string,(context.line_position,offset,offset+len(target_type.string)),inspect.getframeinfo(inspect.currentframe()).lineno)
    operation.inputs.append(target_type)
    operation.type = target_type
    return operation,offset+len(target_type.string)+1
   else:
    #function call
    if input.kind == "function":
     function = input
     function_name = input.name
    elif input.kind == "object":
     function = pynamespace()
     size = create_variable()
     size.type = create_type()
     size.type.kind = "integer"
     function.parameters =[size]
     function.parameter_names = {}
     function_name = input.name
     operation.kind = "allocation"
    else:
     function = input.type
     function_name = function.string
    context.offset = offset
    start = offset
    subexpressions,positions = parse_function_signature_components(context)
    if len(subexpressions)>len(function.parameters):
     error("too many parameters for function "+function_name,(context.line_position,offset,positions[-1]+len(subexpressions[-1])+2),inspect.getframeinfo(inspect.currentframe()).lineno)
    for i in range(len(function.parameters)):
     operation.inputs.append(None)
    positionals =True
    for i in range(len(subexpressions)):
     subexpression = subexpressions[i]
     position = positions[i]
     parameter_name = parse_identifier_string(subexpression)
     offset2 = len(parameter_name)
     if parameter_name and offset2+2<len(subexpression) and subexpression[offset2:offset2+2]=="= ":
      positionals=False
      if parameter_name not in function.parameter_names:
       error("parameter "+parameter_name+" not in function "+function.name,(context.line_position,position,position+len(parameter_name)),inspect.getframeinfo(inspect.currentframe()).lineno)
      parameter_location = function.parameters.index(function.parameter_names[parameter_name])
      offset2+=2
     else:
      if not positionals:
       error("positional parameter after named parameter",(context.line_position,position,position+len(subexpression)),inspect.getframeinfo(inspect.currentframe()).lineno)
      offset2=0
      parameter_location = i
     if operation.inputs[parameter_location+1]!=None:
      error("duplicate parameter "+str(parameter_location),(context.line_position,position,position+len(subexpression)),inspect.getframeinfo(inspect.currentframe()).lineno)
     parameter = function.parameters[parameter_location]
     context.offset = position+offset2
     context.line = line[:position+len(subexpression)]
     old_expression = context.expression
     result = parse_expression(context)
     context.line = line
     new_type = type_intersection(parameter.type,result.components[-1].type)
     if not new_type:
      error("got type "+result.components[-1].type.string+" for parameter of type "+parameter.type.string,(context.line_position,position,position+len(subexpression)),inspect.getframeinfo(inspect.currentframe()).lineno)
     result.components[-1].type = new_type
     append_expressions(old_expression,result)
     context.expression = old_expression
     operation.inputs[parameter_location+1]= len(context.expression.components)-1
    if input.kind != "object":
     for i in range(len(function.parameters)):
      if operation.inputs[i+1]==None:
       parameter = function.parameters[i]
       if not parameter.default:
        error("missing required parameter "+str(i),(context.line_position,start,positions[-1]+len(subexpressions[-1])+1),inspect.getframeinfo(inspect.currentframe()).lineno)
       constant = create_constant()
       constant.type = copy.deepcopy(parameter.type)
       constant.value = parameter.default
       context.expression.components.append(constant)
       context.expression.positions.append(context.expression.positions[operation.inputs[0]])
       operation.inputs[i+1]= len(context.expression.components)-1
     if len(function.returns)==1:
      operation.type = copy.deepcopy(function.returns[0].type)
     elif len(function.returns)>1:
      if function.kind == "function":
       operation.type = copy.deepcopy(function.type)
      else:
       operation.type = copy.deepcopy(function)
     operation.outputs = copy.deepcopy(function.returns)
     operation.output_names = function.return_names
    else:
     operation.type = copy.deepcopy(input.type)
     if not operation.inputs[1]:
      del operation.inputs[1]
     else:
      operation.type.pointer = True
      operation.type.length=context.expression.components[-1].value
    if not subexpressions:
     end=start+line[start:].find(")")+1
    else:
     end=positions[-1]+len(subexpressions[-1])+1
    return operation,end
 else:
  error("unknown unary operator "+operator,(context.line_position,context.offset,context.offset+len(operator)),inspect.getframeinfo(inspect.currentframe()).lineno)

def parse_unary_operator_stack(context):
 line = context.line
 offset = context.offset
 function = context.function
 identifier = parse_identifier_string(line[offset:])
 if identifier:
  offset += len(identifier)
  identifier_object = None
  if offset<len(line) and line[offset]=="." and identifier in function.namespace.imports:
   identifier2 = parse_identifier_string(line[offset+1:])
   if not identifier2:
    error("expected identifier after .",(context.line_position,offset+1,offset+2),inspect.getframeinfo(inspect.currentframe()).lineno)
   identifier = function.namespace.imports[identifier]+programm.namespace_seperator+identifier2
   offset += len(identifier2)+1
   if identifier in programm.functions:
    identifier_object = programm.functions[identifier]
   elif identifier in programm.objects:
    identifier_object = programm.objects[identifier]
   else:
    error("missing import "+identifier2,(context.line_position,offset-len(identifier),offset),inspect.getframeinfo(inspect.currentframe()).lineno)
  else:
   qualified_name = function.namespace.name+programm.namespace_seperator+identifier
   if identifier in function.variables:
    identifier_object = function.variables[identifier]
   elif qualified_name in programm.functions:
    identifier_object = programm.functions[qualified_name]
   elif qualified_name in programm.objects:
    identifier_object = programm.objects[qualified_name]
   elif identifier in default_types:
    type = create_object()
    type.name = identifier
    type.type = parse_type(context)
    offset-=len(identifier)
    identifier = line[offset:offset+len(type.type.string)]
    offset +=len(type.type.string)
    identifier_object = type
   elif identifier in builtin_functions:
    builtin = create_function()
    builtin.name = identifier
    parameter = create_variable()
    parameter.type = create_type()
    if identifier == "delete":
     parameter.type.kind = "*"
     builtin.parameters.append(parameter)
    identifier_object = builtin
   else:
    error("undefined variable "+identifier,(context.line_position,offset-len(identifier),offset),inspect.getframeinfo(inspect.currentframe()).lineno)
  context.expression.components.append(identifier_object)
  context.expression.positions.append((context.line_position,offset-len(identifier),offset))
 elif offset<len(line) and is_number(line[offset]):
  constant,number = parse_constant(context)
  context.expression.components.append(constant)
  context.expression.positions.append((context.line_position,offset,offset+len(number)))
  offset+=len(number)
 while offset<len(line):
  if line[offset] == " " or is_character(line[offset]):
   if is_character(line[offset]):
    error("expected binary operator",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   return offset
  operator = is_unary_operator(line[offset:])
  if operator:
   if operator[-1] in literal_binary_operators:
    if offset+len(operator)<len(line) and (line[offset+len(operator)]==" " or is_identifier_character(line[offset+len(operator)])):
     if not len(operator)>1:
      return offset
     operator2 = is_unary_operator(line[offset:offset+len(operator)-1])
     if not operator2:
      error("unknown operator "+operator[:-1],(context.line_position,offset,offset+len(operator)-1),inspect.getframeinfo(inspect.currentframe()).lineno)
     operator = operator2
   context.offset=offset
   operation,operation_end = parse_unary_operator(operator,context)
   context.expression.components.append(operation)
   context.expression.positions.append((context.line_position,offset,operation_end))
   offset = operation_end
  else:
   return offset
 return offset
   
def parse_binary_operator(operator,operand1_index,context):
 operation = create_operation()
 operation.kind = operator
 operation.inputs = [operand1_index,len(context.expression.components)-1]
 operand1 = context.expression.components[operand1_index]
 operand2 = context.expression.components[-1]
 if operator not in literal_binary_asymetric_operators and not type_intersection(operand1.type,operand2.type):
  error("invalid types "+operand1.type.kind+" , "+operand2.type.kind+" for operator "+operator,(context.line_position,context.offset,context.offset+len(operator)),inspect.getframeinfo(inspect.currentframe()).lineno)
 if operator in literal_binary_numeric_operators:
  if operand1.type.kind not in numeric_compatible_types:
   error("invalid type "+operand1.type.kind+" for operator "+operator,context.expression.positions[operand1_index],inspect.getframeinfo(inspect.currentframe()).lineno)
  if operand2.type.kind not in numeric_compatible_types:
   error("invalid type "+operand2.type.kind+" for operator "+operator,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
 if operator not in literal_binary_numeric_operators and operand1.type.kind not in numeric_compatible_types and operand1.type.kind != operand2.type.kind or ({operand1.type.kind,operand2.type.kind}&{"*"}):
  error("invalid types "+operand1.type.kind+" , "+operand2.type.kind+" for operator "+operator,(context.line_position,context.offset,context.offset+len(operator)),inspect.getframeinfo(inspect.currentframe()).lineno)
 if operator in literal_binary_integer_operators:
  if operand1.type.kind in compatible_types["f"]:
   error("invalid type "+operand1.type.kind+" for operator "+operator,context.expression.positions[operand1_index],inspect.getframeinfo(inspect.currentframe()).lineno)
  if operand2.type.kind in compatible_types["f"]:
   error("invalid type "+operand2.type.kind+" for operator "+operator,context.expression.positions[-1],inspect.getframeinfo(inspect.currentframe()).lineno)
   
 integer_type = create_type()
 integer_type.kind = "integer"
 if operator in literal_binary_numeric_operators:
  if operator in literal_binary_asymetric_operators:
   operation.type = type_intersection(operand1.type,integer_type)
   return operation
  else:
   result_type = type_intersection(operand1.type,operand2.type)
   if operator in literal_binary_integer_operators:
    result_type = type_intersection(result_type,integer_type)
   elif operator in {">","<",">=","<="}:
    operand1.type = copy.deepcopy(result_type)
    operand2.type = copy.deepcopy(result_type)
    result_type = create_type()
    result_type.kind = "b4"
    result_type.size = 4
   operation.type = result_type
   return operation
 else:
  if operator in {"=","!="}:
   result_type = type_intersection(operand1.type,operand2.type)
   operand1.type = copy.deepcopy(result_type)
   operand2.type = copy.deepcopy(result_type)
   result_type = create_type()
   result_type.kind = "b4"
   result_type.size = 4
   operation.type= result_type
  else:
   operation.type = copy.deepcopy(operand1.type)
  return operation
 
def apply_delayed_operator(delayed_operator,context):
 operator,operand1,operator_offset = delayed_operator
 context.offset=operator_offset
 operation = parse_binary_operator(operator,operand1,context)
 context.expression.components.append(operation)
 context.expression.positions.append((context.line_position,operator_offset,operator_offset+len(operator)))
 
def parse_expression(context):
 line = context.line
 offset = context.offset
 context.expression = create_linear_expression()
 function = context.function
 offset = skip_space(line,offset)
 context.offset = offset
 offset = parse_unary_operator_stack(context)
 if not context.expression.components:
  error("expected expression",(context.line_position,context.offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 delayed_operators = [None,None,None]
 while offset<len(line):
  operator = is_binary_operator(line[offset:])
  if operator:
   context.offset=offset+len(operator)
   operand1 = len(context.expression.components)-1
   offset2 = parse_unary_operator_stack(context)
   context.offset=offset
   operation = parse_binary_operator(operator,operand1,context)
   context.expression.components.append(operation)
   context.expression.positions.append((context.line_position,offset,offset+len(operator)))
   if offset2<len(line) and line[offset2]=="}":
    context.offset = offset2+1
    offset3 = parse_unary_operator_stack(context)
    if offset3==offset2+1:
     error("expected unary operator",(context.line_position,offset3,offset3+1),inspect.getframeinfo(inspect.currentframe()).lineno)
    offset2=offset3
   offset = offset2
  elif line[offset]==" ":
   if not line[offset:].strip(" "):
    break
   space_end = skip_space(line,offset)
   space_length = space_end-offset
   for i in range(space_length):
    if delayed_operators[i]:
     apply_delayed_operator(delayed_operators[i],context)
     delayed_operators[i]=None
   offset=space_end
   abacus=False
   if line[offset]=="}":
    context.offset = offset+1
    offset = parse_unary_operator_stack(context)
    if offset>=len(line):
     break
    abacus=True
   operator = is_binary_operator(line[offset:])
   if not operator:
    error("expected binary operator",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   offset+=len(operator)
   space_end2 = skip_space(line,offset)
   space_length2 = space_end2 - offset
   if space_length!=space_length2 and not abacus or abacus and space_length2 not in {space_length,0}:
    error("invalid spacing after operator",(context.line_position,offset,offset+space_length2+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   if space_length2>0:
    delayed_operators[space_length2-1]=(operator,len(context.expression.components)-1,offset-len(operator))
   else:
    delayed_operator=(operator,len(context.expression.components)-1,offset-len(operator))
   offset = space_end2
   context.offset = offset
   offset2 = parse_unary_operator_stack(context)
   if offset2==offset:
    error("expected unary operator",(context.line_position,offset2,offset2+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   if space_length2==0:
    apply_delayed_operator(delayed_operator,context)
   offset=offset2
  else:
   error("expected binary operator",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 for delayed_operator in delayed_operators:
  if delayed_operator:
   apply_delayed_operator(delayed_operator,context)
 return context.expression

def parse_function_body(function):
 body_lines = function.body
 context = pynamespace()
 context.function = function
 context.namespace = function.namespace
 dummy = pynamespace()
 dummy.body =[]
 control_flow_stack = [None,dummy]
 for body_index,(line,line_position) in enumerate(body_lines):
  if debug:
   print(line)
  context.line = line
  context.line_position = line_position
  indent = len(line)-len(line.lstrip(" "))
  offset = indent
  context.offset = indent
  identifier = parse_identifier_string(line[offset:])
  if not identifier:
   error("expected identifier",(line_position,indent,indent+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  nesting_level = len(control_flow_stack)-1
  last_control_flow=None
  if indent>nesting_level:
   error("unexpected indent",(line_position,nesting_level,indent),inspect.getframeinfo(inspect.currentframe()).lineno)
  if indent<nesting_level:
   if identifier in {"break","continue"}:
    loop_index=None
    for i in range(indent+1,len(control_flow_stack)-1):
     if control_flow_stack[i] and not loop_index and control_flow_stack[i].kind!="loop":
      error("can only "+identifier+" on loop",(line_position,indent,indent+len(identifier)),inspect.getframeinfo(inspect.currentframe()).lineno)
     if control_flow_stack[i] and not loop_index and control_flow_stack[i].kind=="loop":
      loop_index=i
     elif control_flow_stack[i] and loop_index and control_flow_stack[i].kind == "loop":
      error("cannot "+identifier+" multiple loops",(line_position,indent,i),inspect.getframeinfo(inspect.currentframe()).lineno)
   else:
    last_control_flow = control_flow_stack[-1]
    control_flow_stack = control_flow_stack[:indent+1]
    if not control_flow_stack[-1]:
     error("invalid indent",(line_position,1,indent),inspect.getframeinfo(inspect.currentframe()).lineno)
  variable_start = offset
  offset+=len(identifier)
  offset = skip_space(line,offset)
  if identifier in control_flow_identifiers:
   flow = create_control_flow()
   flow.kind = identifier
   if flow.kind in {"else","elif"}:
    if not last_control_flow:
     error("missing prior if",(line_position,indent,offset),inspect.getframeinfo(inspect.currentframe()).lineno)
    last_control_flow.next = flow
   if flow.kind in {"if","elif"}:
    context.offset=offset
    condition = parse_expression(context)
    new_type = create_type()
    new_type.kind = "integer"
    new_type = type_intersection(condition.components[-1].type,new_type)
    if not new_type:
     error("condition must be of integer type, got "+context.expression.components[-1].type.kind,(line_position,offset,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
    if condition.components[-1].type.kind in unspecific_types:
     if new_type.kind in unspecific_types:
      if new_type.kind in {"s","signed"}:
       new_type.kind="s4"
      else:
       new_type.kind="b4"
      new_type.size=4
      new_type.string=new_type.kind
     condition.components[-1].type.kind=new_type
    flow.condition = context.expression
   control_flow_stack[-1].body.append(flow)
   if flow.kind in {"if","elif"}:
    propagate_types(flow.condition,context)
   if flow.kind not in {"break","continue"}:
    next_indent = indent
    i=body_index+1
    if i>=len(body_lines):
     error("expected indented expression",(line_position,len(line)-1,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
    while i<len(body_lines):
     next_line = body_lines[i][0]
     next_indent = len(next_line)-len(next_line.lstrip(" "))
     tmp_identifier = parse_identifier_string(next_line[next_indent:])
     if tmp_identifier in {"break","continue"}:
      i+=1
      continue
     if next_indent<len(control_flow_stack) and i==body_index+1:
      error("invalid indent",(body_lines[body_index+1][1],next_indent,len(control_flow_stack)),inspect.getframeinfo(inspect.currentframe()).lineno)
     break
    while next_indent>len(control_flow_stack):
     control_flow_stack.append(None)
    control_flow_stack.append(flow)
   continue
  if offset>= len(line):
   error("incomplete expression",(line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  assignment = create_assignment()
  if identifier =="return":
   assignment.destination="return"
   assignment.expression =[]
   i=0
   while offset<len(line):
    context.offset=offset
    end=skip_nested("(",")",",",context)
    if not end:
     end = len(line)
    context.line = line[:end]
    expression = parse_expression(context)
    context.line = line
    if not type_intersection(expression.components[-1].type,function.returns[i].type):
     error("return value is of type "+expression.components[-1].type.kind+" but should be "+function.returns[i].type.kind,(line_position,offset,end),inspect.getframeinfo(inspect.currentframe()).lineno)
    expression.components[-1].type = copy.deepcopy(function.returns[i].type)
    propagate_types(expression,context)
    assignment.expression.append(expression)
    offset= skip_space(line,end+1)
    i+=1
   if len(assignment.expression)!=len(function.returns):
    error("missing return value(s)",(line_position,len(line),len(line)+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   assignment.special = True
   control_flow_stack[-1].body.append(assignment)
   continue
  comma = skip_nested("(",")",",",context)
  if not comma and line[offset]=="=" and identifier not in function.variables:
   #new variable creation
   context.offset = offset+1
   expression = parse_expression(context)
   assignment.expression = expression
   if expression.components[-1].type.kind =="integer" and expression.components[-1].type.size:
    expression.components[-1].type.kind="b"+str(expression.components[-1].type.size)
    expression.components[-1].type.string="b"+str(expression.components[-1].type.size)
   propagate_types(expression,context)
   variable,expression = new_variable(identifier,variable_start,expression.components[-1].type,context)
   variable.value = expression.components[-1].value
   function.variables[identifier] = variable
   assignment.destination = expression
   control_flow_stack[-1].body.append(assignment)
   propagate_types(expression,context)
   continue
  if comma and comma < len(line):
   #compound assignment
   assignment.special = True
   context.offset = len(line)-1
   expression_seperator = skip_nested("(",")","=",context,"reverse")
   if not expression_seperator or expression_seperator<comma:
    error("expected = for compound assignment",(line_position,len(line)-1,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
   expression_start = skip_space(line,expression_seperator+1)
   context.offset = expression_start
   context.expression = create_linear_expression()
   parse_unary_operator_stack(context)
   assignment.expression = context.expression
   compound_function = context.expression.components[-1]
   if len(compound_function.outputs)==0:
    error("expected function for compound assignment",(line_position,expression_start+1,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
   given_names = set()
   offset = indent
   positionals =True
   return_count=0
   assignment.destination = []
   for i in range(len(compound_function.outputs)):
    assignment.destination.append(None)
   while comma<expression_seperator:
    context.offset = offset
    comma = skip_nested("(",")",",",context)
    if not comma:
     comma=expression_seperator
    end = comma
    while line[end-1]==" ":
     end-=1
    equals = line[:end].rfind("=")
    subexpression_start = skip_space(line,offset)
    return_name = parse_identifier_string(line[equals+1:])
    if equals>offset and return_name == line[equals+1:end]:
     positionals=False
     if return_name in given_names:
      error("return value "+return_name+" already assigned",(line_position,equals,end),inspect.getframeinfo(inspect.currentframe()).lineno)
     given_names.add(return_name)
     if return_name not in compound_function.output_names:
      error("function returns no value "+return_name,(line_position,equals,end),inspect.getframeinfo(inspect.currentframe()).lineno)
     return_position = compound_function.outputs.index(compound_function.output_names[return_name])
     end = equals
    elif line[subexpression_start:subexpression_start+2]not in{"_ ","_,","_="}:
     if not positionals:
      error("positional return after named return",(line_position,offset,end),inspect.getframeinfo(inspect.currentframe()).lineno)
     if return_count>=len(compound_function.outputs):
      error("function is out of return values",(line_position,offset,end),inspect.getframeinfo(inspect.currentframe()).lineno)
     return_position = return_count
     return_name = compound_function.outputs[return_position].name
     given_names.add(return_name)
     return_count+=1
    if line[subexpression_start:subexpression_start+2] not in  {"_ ","_,","_="}:
     context.offset = subexpression_start
     first_identifier = parse_identifier_string(line[context.offset:])
     if first_identifier not in function.variables and context.offset+len(first_identifier) == end:
      variable,variable_expression = new_variable(line[context.offset:end],context.offset,compound_function.outputs[return_position].type,context)
      variable.value = compound_function.outputs[return_position].value
      function.variables[variable.name]=variable
      assignment.destination[return_position] = variable_expression
     else:
      context.expression = create_linear_expression()
      parse_unary_operator_stack(context)
      if context.expression.components[-1].type.kind != compound_function.outputs[return_position].type.kind:
       error("trying to assign "+compound_function.outputs[return_position].type.kind+" to "+context.expression.components[-1].type.kind,(line_position,offset,comma),inspect.getframeinfo(inspect.currentframe()).lineno)
      if context.expression.components[-1].type.nested:
       error("nested references are constant and cannot be assigned to",(line_position,offset,comma),inspect.getframeinfo(inspect.currentframe()).lineno)
      assignment.destination[return_position] = context.expression
      propagate_types(context.expression,context)
    offset = comma+1
   control_flow_stack[-1].body.append(assignment)
   propagate_types(assignment.expression,context)
   continue
  #binary operator maybe?
  context.expression = create_linear_expression()
  offset = parse_unary_operator_stack(context)
  destination_end = offset
  if not line[offset:].strip(" "):
   #naked function call
   if context.expression.components[-1].kind!="(":
    error("missing assignment",(line_position,indent,indent+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   assignment.expression = context.expression
   assignment.special = True
   control_flow_stack[-1].body.append(assignment)
   propagate_types(assignment.expression,context)
   continue
  else:
   #general case
   if context.expression.components[-1].type.nested:
    error("nested references are constant and cannot be assigned to",(line_position,indent,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   offset = skip_space(line,offset)
   propagate_types(context.expression,context)
   if line[offset]=="=":
    assignment.destination = context.expression
    context.offset = offset+1
    assignment.expression = parse_expression(context)
   elif line[offset]=="}":
    #once-only...
    destination = context.expression
    if destination.components[-1].kind=="[":
     array = destination.components[-1]
     array_position = destination.positions[-1]
     subexpression_start = array.inputs[0]
     subexpression_end = array.inputs[1]+1
     subexpression = create_linear_expression()
     subexpression.components = destination.components[subexpression_start:subexpression_end]
     subexpression.positions = destination.positions[subexpression_start:subexpression_end]
     if array.inputs[0]>0:
      array_variable_position = (context.line_position,indent,destination.positions[array.inputs[0]][2])
      array_variable,array_variable_assignment,hole_position,destination = cache_in_variable(destination,array.inputs[0],function)
      assert hole_position==0
      destination.components[hole_position]=array_variable
      destination.positions[hole_position]=array_variable_position
      control_flow_stack[-1].body.append(array_variable_assignment)
     else:
      array_variable = destination.components[0]
      array_variable_position = destination.positions[0]
     sub_variable,sub_variable_assignment,hole_position,destination = cache_in_variable(destination,destination.components[-1].inputs[1],function)
     assert hole_position==1
     destination.components[hole_position]=sub_variable
     destination.positions[hole_position]=(context.line_position,sub_variable_assignment.expression.positions[0][1],sub_variable_assignment.expression.positions[-1][2])
     control_flow_stack[-1].body.append(sub_variable_assignment)
     assignment.destination=destination
     substitute = array_variable.name+"["+sub_variable.name+"]"
    elif destination.components[-1].kind=="." and len(destination.components)>2:
     variable,variable_assignment,hole_position,destination = cache_in_variable(destination,len(destination.components)-2,function)
     assert hole_position == len(destination.components)-2
     control_flow_stack[-1].body.append(variable_assignment)
     destination.components[hole_position]=variable
     destination.positions[hole_position]=(context.line_position,indent,offset)
     assignment.destination=destination
     substitute = variable.name+"."+destination.components[-1].inputs[1]
    else:
     substitute = line[indent:destination_end]
     assignment.destination = context.expression
    context.line = line[:offset+1-len(substitute)]+substitute+line[offset+1:]
    context.offset = offset+1-len(substitute)
    assignment.expression = parse_expression(context)
    context.line = line
   else:
    error("expected expression",(line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
   destination_type = assignment.destination.components[-1].type
   source_type = assignment.expression.components[-1].type
   new_type = type_intersection(destination_type,source_type)
   if not new_type:
    error("cannot assign "+source_type.string+" to type "+destination_type.string,(line_position,offset+1,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
   assignment.expression.components[-1].type = new_type
   control_flow_stack[-1].body.append(assignment)
   propagate_types(assignment.expression,context)
   continue
 function.body = dummy.body
    
def parse_code_body(code,function):
 function_body = function.body
 function.body= []
 for i,line in enumerate(code):
  function.body.append((line,i))
 global source_lines
 stored_lines = source_lines
 source_lines = code
 parse_function_body(function)
 source_lines = stored_lines
 parsed = function.body
 function.body = function_body
 return parsed
    
def parse_object_body(object):
 body_lines = object.body
 context = pynamespace()
 context.namespace = object.namespace
 for line,line_position in body_lines:
  context.line = line
  context.line_position = line_position
  offset = skip_space(line,0)
  field_name = parse_identifier_string(line[offset:])
  if not field_name:
   error("expected field name",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  field_variable = create_variable()
  field_variable.name = field_name
  offset+=len(field_name)
  if offset>=len(line) or line[offset]!=" ":
   error("expected field type",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  offset+=1
  context.offset = offset
  field_type = parse_type(context)
  field_variable.type = field_type
  object.variables[field_name]=field_variable
  
def parse_namespace_delimiter(context):
 line = context.line
 offset = context.offset
 name_start = offset
 name = parse_identifier_string(line[offset:])
 #if not name:
  #error("expected name of namespace",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if name in default_types:
  error("cannot use type as namespace",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if name in reserved_identifiers:
  error("cannot use reserved name "+name+" as namespace",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if name!="end":
  offset += len(name)
 else:
  name=""
  offset-=1
 name_end = offset
 if line[offset:]:
  if line[offset]!=" ":
   error("unexpected symbol in namespace",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  offset = skip_space(line,offset)
  if line[offset:] !="end":
   error("trailing characters "+line[offset:]+" after namespace",(context.line_position,offset,offset+len(line[offset:])),inspect.getframeinfo(inspect.currentframe()).lineno)
  if context.namespace.name != name:
   error("encountered end of namespace "+name+" while in namespace "+context.namespace.name,(context.line_position,0,offset+len(line[offset:])),inspect.getframeinfo(inspect.currentframe()).lineno)
  context.namespace = None
 else:
  if context.namespace != None:
   error("attempt to declare namespace "+name+" while in namespace "+context.namespace.name,(context.line_position,0,offset+len(line[offset:])),inspect.getframeinfo(inspect.currentframe()).lineno)
  if name in programm.namespaces:
   error("duplicate declaration of namespace "+name,(context.line_position,0,offset+len(line[offset:])),inspect.getframeinfo(inspect.currentframe()).lineno)
  namespace = create_namespace()
  namespace.name = name
  programm.namespaces[name] = namespace
  context.namespace = namespace
 
def parse_import_declaration(context):
 line = context.line
 offset = context.offset
 tokens,positions = split_on_space(context)
 if len(tokens)==0:
  error("missing imported name",(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 name = tokens[0]
 verify_identifier_string(name,context)
 name2 = name
 if context.namespace == None:
  error("import outside namespace",(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 if name in context.namespace.imports.values():
  error("duplicate import of "+name,(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 if len(tokens)>1:
  if tokens[2] != "as":
   error("expected as",positions[2],inspect.getframeinfo(inspect.currentframe()).lineno)
  if len(tokens)<5:
   error("missing alias",(context.line_position,len(line),len(line)+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  if len(tokens)>5:
   error("unexpected "+tokens[6],positions[6],inspect.getframeinfo(inspect.currentframe()).lineno)
  name2 = tokens[4]
  context.offset = positions[4][1]
  verify_identifier_string(name2,context)
  if name2 in context.namespace.imports:
   error("duplicate import as "+name2,(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 if name2 in default_types:
  error("cannot use type as import",(context.line_position,context.offset,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 if name2 in reserved_identifiers:
  error("cannot use reserved name "+name2+" as import",(context.line_position,context.offset,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 programm.namespaces[context.namespace.name].imports[name2]=name
 programm.namespaces[context.namespace.name].import_positions[name2]=context.line_position
 
def parse_object_declaration(context):
 line = context.line
 offset = context.offset
 name = parse_identifier_string(line[offset:])
 if not name:
  error("invalid identifier character",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 offset += len(name)
 if line[offset:]:
  error("trailing characters "+line[offset:]+" after object",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if context.namespace == None:
  error("object outside namespace",(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 qualified_name = context.namespace.name+programm.namespace_seperator+name
 if qualified_name in programm.objects:
  error("duplicate declaration of object "+name,(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 object = create_object()
 object.name = qualified_name
 object.namespace = context.namespace
 object.type = create_type()
 object.type.kind = object.name
 programm.objects[qualified_name] = object
 return object
 
def parse_function_declaration(context):
 line = context.line
 offset = context.offset
 function = create_function()
 name = parse_identifier_string(line[offset:])
 if name == "inline" and line[offset+len(name)]==" ":
  function.inline=True
  offset = skip_space(line,offset+len(name))
  name = parse_identifier_string(line[offset:])
 if not name:
  error("missing function name",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if context.namespace == None:
  error("function outside namespace",(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 qualified_name = context.namespace.name+programm.namespace_seperator+name
 if qualified_name in programm.functions:
  error("duplicate declaration of function "+name,(context.line_position,0,len(line)),inspect.getframeinfo(inspect.currentframe()).lineno)
 function.name = qualified_name
 function.namespace = context.namespace
 function.type = create_type()
 function.type.kind="fun"
 function.type.string=line[offset:]
 function.type.void = False
 function.value = function.name
 offset+=len(name)
 if line[offset:]:
  if line[offset]!="(":
   error("expected (",(context.line_position,offset,offset+1),inspect.getframeinfo(inspect.currentframe()).lineno)
  context.offset = offset
  function.parameters,function.returns,_,function.parameter_names,function.return_names = parse_function_signature(context)
 function.type.parameters = copy.deepcopy(function.parameters)
 function.type.returns = copy.deepcopy(function.returns)
 programm.functions[qualified_name]= function
 for parameter in function.parameters:
  function.variables[parameter.name]=parameter
 return function
 
def parse_top_level(context):
 line = context.line
 declaration = line.split(" ",1)[0]
 context.offset = skip_space(line,len(declaration))
 body = None
 if declaration == "function":
  body = parse_function_declaration(context)
 elif declaration == "object":
  body = parse_object_declaration(context)
 elif declaration == "import":
  parse_import_declaration(context)
 elif declaration == "namespace":
  parse_namespace_delimiter(context)
 #else:  
  #body = parse_type_declaration(context)  
 #no custom types for now
 else:
  error("expected top-level statement, but got "+declaration,(context.line_position,0,1),inspect.getframeinfo(inspect.currentframe()).lineno)
 if body:
  body.position=context.line_position
 return body
  
def parse(lines):
 global programm
 top_level = None
 context = pynamespace()
 context.namespace = None
 for position,line in enumerate(lines):
  context.line = line
  context.line_position = position
  indent = len(line)-len(line.lstrip(" "))
  if not indent:
   top_level = None
  comment = line.find("//")
  if comment!=-1:
   line=line[:comment]
  line = line.rstrip(" ")
  context.line = line
  if line.strip(" "):
   if indent:
    if not top_level:
     error("unexpected indent",(position,0,indent),inspect.getframeinfo(inspect.currentframe()).lineno)
    top_level.body.append((line,position))
   else:
    top_level = parse_top_level(context)
 programm.parsed = True
 for space in programm.namespaces.values():
  for space2 in space.imports:
   if space.imports[space2] not in programm.namespaces:
    error("unknown namespace "+space.imports[space2],[space.import_positions[space2]],inspect.getframeinfo(inspect.currentframe()).lineno)
 for function in programm.functions.values():
  for parameter in function.parameters:
   if parameter.type.kind not in default_types:
    if parameter.type.kind not in programm.objects:
     error("unknown object "+parameter.type.kind,(function.position),inspect.getframeinfo(inspect.currentframe()).lineno)

 for object in programm.objects.values():
  parse_object_body(object)
 for function in programm.functions.values():
  parse_function_body(function)
 if programm.global_prefix:
  for function in list(programm.functions):
   rename_function(function,programm.global_prefix+function)
  renames=[]
  for object in programm.objects:
   renames.append((object,programm.global_prefix+object))
  rename_objects(renames)
 for function in programm.functions.values():
  if function.parameters:
   if function.parameters[0].type.kind not in default_types:
    programm.objects[function.parameters[0].type.kind].methods.append(function)
 programm.done=True
 return programm
  
def c_create_options():
 c_options = pynamespace()
 c_options.typedef = False
 c_options.precise_types = False
 c_options.preserve_field_order = False
 c_options.spill_into_variables = False
 return c_options
 
def c_create_context():
 c_context = pynamespace()
 c_context.options = None
 c_context.c_type = c_default_type
 c_context.returntypes = {}
 c_context.variables = set()
 c_context.object_alignments = {}
 return c_context
 
def c_create_expression():
 c_expression = pynamespace()
 c_expression.translation = ""
 c_expression.spill = False
 c_expression.precedence=0
 return c_expression
 
c_precise_type = {"b1":"uint8_t","b2":"uint16_t","b4":"uint32_t","b8":"uint64_t","s1":"uint8_t","s2":"uint16_t","s4":"uint32_t","s8":"uint64_t","f1":"float","f2":"float","f4":"float","f8":"double","*":"void"}
c_default_type = {"b1":"uint_least8_t","b2":"uint_least16_t","b4":"uint_least32_t","b8":"uint_least64_t","s1":"uint_least8_t","s2":"uint_least16_t","s4":"uint_least32_t","s8":"uint_least64_t","f1":"float","f2":"float","f4":"float","f8":"double","*":"void"}
c_operator_precedence={"(":1,"[":1,".":1,"~>":1,"~.":1,"~^":1,"~v":1,"+1":2,"-1":2,"~":2,"c":2,"%":3,"/":3,"*":3,"+":4,"-":4,"<<":5,">>":5,">":6,"<":6,">=":6,"<=":6,"=":7,"!=":7,"&":8,"^":9,"|":10}
c_translate_operator={"~>":"round","~.":"trunc","~^":"ceil","~v":"floor","+1":"+","-1":"-","~":"~","%":"%","/":"/","*":"*","+":"+","-":"-",">>":">>","<<":"<<",">":">","<":"<",">=":">=","<=":"<=","=":"==","!=":"!=","&":"&","^":"^","|":"|"}
c_translate_builtin={"delete":"free"}
c_translate_control_flow={"loop":"while(1){","if":"if(","elif":"}else if(","else":"}else{","break":"break;","continue":"continue;"}
c_spilling_operators={"+1","-1","*","+","-","<<"}
c_spillover_operators={"(","[","c","%","/",">>",">","<",">=","<=","=","!="}
c_reserved_identifiers={"alignas","alignof","auto","bool","break","case","char","const","constexpr","continue","default","do","double","else","enum","extern","false","float","for","goto","if","inline","int","long","nullptr","register","restrict","return","short","signed","sizeof","static","static_assert","struct","switch","thread_local","true","typedef","typeof","typeof_unqual","union","unsigned","void","volatile","while","_Alignas","_Alignof","_Atomic","_BitInt","_Bool","_Complex","_Decimal128","_Decimal32","_Decimal64","_Generic","_Imaginary","_Noreturn","_Static_assert","_Thread_local"}
  
def c_generate_returntype(type,name,context):
 if len(type.returns)==0:
  return "void",[]
 elif len(type.returns)==1 and type.returns[0].type.kind!="fun":
  return_type,declarations= c_translate_typename(type.returns[0].type,"",context)
  assert not declarations
  return return_type,[]
 else:
  string=""
  for parameter in type.returns:
   string+=type_to_string(parameter.type)
  if string not in context.returntypes:
   if name:
    identifier = generate_global_name(name+"_t",c_reserved_identifiers)
   else:
    identifier = generate_global_name("return",c_reserved_identifiers)
   declaration_stack = []
   return_type = identifier
   declaration = identifier+" {"
   for index,variable in enumerate(type.returns):
    declaration+=" "
    variable_name="r"+str(index)
    typename,declarations = c_translate_typename(variable.type,variable_name,context)
    if declarations:
     declarations.extend(declaration_stack)
     declaration_stack=declarations
    declaration+=typename+";"
   declaration+="};"
   declaration_stack.append("struct "+declaration)
   if context.options.typedef:
    declaration_stack.append("typedef struct "+return_type+" "+return_type+";")
   else:
    return_type = "struct "+return_type
   context.returntypes[string] = (return_type,declaration)
   return return_type,declaration_stack
  else:
   return_type,return_type_declaration = context.returntypes[string]
   return return_type,[]
 
def c_get_returntype(type,name,context):
 returntype,declarations = c_generate_returntype(type,name,context)
 assert not declarations
 return returntype
  
def c_translate_typename(type,name,context,not_pointer=False):
 output=""
 declarations=[]
 if type.kind !="fun":
  if type.kind in numeric_types and type.pointer and not type.nested:
   output+="void"
  elif type.kind in default_types:
   output+=context.c_type[type.kind]
  else:
   if not context.options.typedef:
    output+="struct "
   output+=type.kind
  if not type.pointer and type.kind in numeric_types or not_pointer:
   if name:
    output+=" "+name
  else:
   if not type.nested:
    output+=" *"+name
   else:
    output+=" "+name+"["+str(type.length)+"]"
 else:
  if not type.void:
   output,declarations = c_generate_returntype(type,name,context)
   output+=" "
   if not type.nested and not not_pointer:
    output+="(*"+name+")("
   else:
    output+=name+"("
   for variable in type.parameters:
    variable_name = ""
    if not_pointer:
     variable_name=variable.name
    variable_string,declarations2 = c_translate_typename(variable.type,variable_name,context)
    declarations2.extend(declarations)
    declarations=declarations2
    output+=variable_string+","
   if output[-1]==",":
    output=output[:-1]
   else:
    output+="void"
   output+=")"
   if type.nested:
    output+="["+str(type.length)+"]"
  else:
   output+="void *"+name
 if output[-1]==" ":
  output = output[:-1]
 return output,declarations
  
def c_get_typename(type,name,context,not_pointer=False):
 typename,declarations = c_translate_typename(type,name,context,not_pointer)
 assert not declarations
 return typename
  
def c_mark(destination,expression,context):
 if destination:
  for op in destination.components:
   if not context.operation or op.kind == context.operation:
    op.metadata["transformed"]=True
 if expression:
  for op in expression.components:
   if not context.operation or op.kind == context.operation:
    op.metadata["transformed"]=True
 return destination,expression,[]
  
def c_transform_expression(destination,expression,context):
 preamble=[]
 i=0
 while expression and i<len(expression.components):
  operation = expression.components[i]
  if operation.kind =="+1" and operation.type.kind in signed_integer_types:
   variable,variable_instruction,hole_position,expression = cache_in_variable(expression,i,context.function,invalid_names=c_reserved_identifiers)
   variable_instruction.expression.components = variable_instruction.expression.components[:-1]
   variable_instruction.expression.positions = variable_instruction.expression.positions[:-1]
   preamble.append(variable_instruction)
   variable_expression = create_linear_expression()
   variable_expression.components.append(variable)
   variable_expression.positions.append((0,0,0))
   expression = replace_expression(expression,hole_position,variable_expression)
   code = [" if "+variable.name+"&0x"+format(sign_mask[operation.type.size],"x")+"!=0","  "+variable.name+"="+variable.name+"~+1"]
   preamble.extend(parse_code_body(code,context.function))
   i=0
  elif operation.kind=="c" and not operation.type.pointer and (expression.components[operation.inputs[0]].type.kind in floating_point_types and operation.type.kind in integer_types or expression.components[operation.inputs[0]].type.kind in signed_integer_types and operation.type.kind in floating_point_types or expression.components[operation.inputs[0]].type.kind in signed_integer_types and operator.type.kind in signed_integer_types) and "transformed" not in operation.metadata:
   cast_expression,hole_position,expression = extract_expression(expression,i)
   cast_variable,cast_assignment,_,_ = cache_in_variable(cast_expression,len(cast_expression.components)-2,context.function,invalid_names=c_reserved_identifiers)
   preamble.append(cast_assignment)
   destination_variable = create_variable()
   destination_variable.type = copy.deepcopy(operation.type)
   destination_variable.name = generate_variable_name(context.function,invalid_names=c_reserved_identifiers)
   variable_expression = create_linear_expression()
   variable_expression.components.append(destination_variable)
   variable_expression.positions.append((0,0,0))
   expression = replace_expression(expression,hole_position,variable_expression)
   code = []
   if operation.type.kind in signed_integer_types and cast_variable.type.kind in signed_integer_types:
    code.append(" "+destination_variable.name+"="+cast_variable.name+"("+operation.type.kind+")")
    code.append(" if "+cast_variable.name+"&0x"+format(sign_mask[cast_variable.type.size],"x")+"!=0")
    code.append("  "+destination_variable+"}|0x"+format(type_mask[operation.type.size]^type_mask[cast_variable.type.size],"x"))
   elif operation.type.kind in integer_types:
    if operation.type.kind in signed_integer_types:
     code.append(" "+cast_variable.name+"="+cast_variable.name+"+"+str(s_max[operation.type.size]+1))
    code.append(" if "+cast_variable.name+"<=0")
    code.append("  "+cast_variable.name+"=0")
    code.append(" if "+cast_variable.name+">="+str(b_max[operation.type.size]))
    code.append("  "+destination_variable.name+"="+str(b_max[operation.type.size])+size_suffix[operation.type.size])
    code.append(" else")
    if operation.type.kind not in signed_integer_types:
     code.append("  "+destination_variable.name+"="+cast_variable.name+"("+operation.type.kind+")")
    if operation.type.kind in signed_integer_types:
     code.append("  "+destination_variable.name+"="+cast_variable.name+"("+operation.type.kind+")-"+str(s_max[operation.type.size]+1))
   elif operation.type.kind in floating_point_types:
    code.append(" "+cast_variable.name+"="+cast_variable.name+"+"+str(s_max[operation.type.size]+1))
    code.append(" "+destination_variable.name+"="+cast_variable.name+"("+operation.type.kind+")-"+str(s_max[operation.type.size]+1))
   code2=parse_code_body(code,context.function)
   context.operation = "c"
   code3 = transform_code(code2,c_mark,context)
   preamble.extend(code3)
   i=0
  elif operation.kind ==">>" and operation.type.kind in signed_integer_types and "transformed" not in operation.metadata:
   shift_expression,hole_position,expression = extract_expression(expression,i)
   operand1_variable,operand1_instruction,hole_position,shift_expression = cache_in_variable(shift_expression,shift_expression.components[-1].inputs[0],context.function,invalid_names=c_reserved_identifiers)
   preamble.append(operand1_instruction)
   variable_expression = create_linear_expression()
   variable_expression.components.append(operand1_variable)
   variable_expression.positions.append((0,0,0))
   expression = replace_expression(expression,hole_position,variable_expression)
   operand2_variable,operand2_instruction,hole_position,shift_expression = cache_in_variable(shift_expression,shift_expression.components[-1].inputs[1],context.function,invalid_names=c_reserved_identifiers)
   preamble.append(operand2_instruction)
   code = [" if "+operand1_variable.name+"&0x"+format(sign_mask[operation.type.size],"x")+"=0","  "+operand1_variable.name+"="+operand1_variable.name+">>"+operand2_variable.name," else","  "+operand1_variable.name+"="+operand1_variable.name+">>"+operand2_variable.name+"  |  0x"+format(type_mask[operation.type.size],"x")+" << "+str(bit_size[operation.type.size])+"-"+operand2_variable.name]
   code2=parse_code_body(code,context.function)
   context.operation = ">>"
   code3 = transform_code(code2,c_mark,context)
   preamble.extend(code3)
   i=0
  elif operation.kind in {"/","%"}  and "transformed" not in operation.metadata:
   divide_expression,hole_position,expression = extract_expression(expression,i)
   operand1_variable,operand1_instruction,_,divide_expression = cache_in_variable(divide_expression,divide_expression.components[-1].inputs[0],context.function,invalid_names=c_reserved_identifiers)
   preamble.append(operand1_instruction)
   operand2_variable,operand2_instruction,_,divide_expression = cache_in_variable(divide_expression,divide_expression.components[-1].inputs[1],context.function,invalid_names=c_reserved_identifiers)
   preamble.append(operand2_instruction)
   variable_expression = create_linear_expression()
   variable_expression.components.append(operand2_variable)
   variable_expression.positions.append((0,0,0))
   expression = replace_expression(expression,hole_position,variable_expression)
   code =[]
   if operation.type.kind in signed_integer_types:
    sign_variable_name = generate_variable_name(context.function,invalid_names=c_reserved_identifiers)
    #if operation.kind=="%":
     #code.append(" "+sign_variable_name+"="+operand1_variable.name+"&0x"+format(sign_mask[operation.type.size],"x"))
    #else:
    code.append(" "+sign_variable_name+"="+operand1_variable.name+"^"+operand2_variable.name+"&0x"+format(sign_mask[operation.type.size],"x"))
   code.append(" if "+operand2_variable.name+"!=0")
   if operation.type.kind in signed_integer_types:
    code.append("  "+operand1_variable.name+"="+operand1_variable.name+"+")
    code.append("  "+operand2_variable.name+"="+operand2_variable.name+"+")
    code.append("  "+operand2_variable.name+"="+operand1_variable.name+operation.kind+operand2_variable.name)
    code.append("  if "+sign_variable_name+"!=0")
    code.append("   "+operand2_variable.name+"}-")
   else:
    code.append("  "+operand2_variable.name+"="+operand1_variable.name+operation.kind+operand2_variable.name)
   if operation.kind == "%":
    code.append(" else")
    code.append("  "+operand2_variable.name+"="+operand1_variable.name)
   code2=parse_code_body(code,context.function)
   context.operation = operation.kind
   code3 = transform_code(code2,c_mark,context)
   preamble.extend(code3)
   i=0
  else:
   i+=1
 return destination,expression,preamble
  
def c_translate_expression(expression,context):
 variable_spill = context.options.spill_into_variables
 translated = []
 operators = expression.components
 for operator in operators:
  c_expression = c_create_expression()
  output=""
  if operator.kind =="variable":
   c_expression.translation= operator.name
   if operator.type.kind in integer_types and variable_spill:
    c_expression.spill=True
  elif operator.kind =="function":
   if operator.name not in builtin_functions:
    c_expression.translation=operator.name
   else:
    c_expression.translation= c_translate_builtin[operator.name]
  elif operator.kind=="constant":
   if operator.type.kind in floating_point_types:
    output=str(operator.value)
    if operator.type.size!=8:
     output+="f"
   else:
    if operator.value<0:
     twos_complement = (0xffffffffffffffff >> 64-bit_size[operator.type.size]) + (operator.value+1)
     output=str(twos_complement)
    else:
     output=str(operator.value)
    output+="u"
    if operator.type.size!=4:
     output = "("+context.c_type[operator.type.kind]+")"+output
     c_expression.precedence=2
   c_expression.translation=output
  elif operator.kind=="object":
   pass
  elif operator.kind in c_translate_operator and operator.type.kind in default_types:
   inputs = [translated[operator.inputs[0]]]
   if operator.kind in binary_operators:
    inputs.append(translated[operator.inputs[1]])
   input_translations =[]
   for i,input in enumerate(inputs):
    translation = input.translation
    if operator.kind in {">","<",">=","<="} and operator.type.kind in signed_integer_types:
     if input.precedence > c_operator_precedence["^"]:
      translation="("+translation+")"
     translation += "^0x"+format(sign_mask[operator.type.size],"x")
     input.precedence = c_operator_precedence["^"]
    if operator.kind in {">>","<<"} and i==1:
     if input.precedence > c_operator_precedence["&"]:
      translation="("+translation+")"
     translation += "&0x"+format(bitshift_mask[operator.type.size],"x")
     input.precedence = c_operator_precedence["&"]
    elif not context.options.precise_types and operator.kind in c_spillover_operators and operator.type.kind in integer_types:
     if input.spill:
      if input.precedence > c_operator_precedence["&"]:
       translation="("+translation+")"
      translation += "&0x"+format(type_mask[operator.type.size],"x")
      input.precedence = c_operator_precedence["&"]
    if input.precedence > c_operator_precedence[operator.kind] or (input.precedence == c_operator_precedence[operator.kind] and (input.precedence!=2 and i==1 or input.precedence==2 and i==0)):
     translation="("+translation+")"
    input_translations.append(translation)
   if operator.kind in unary_operators:
    if operator.kind in {"~>","~.","~^","~v"} and operator.type.size<8:
     c_expression.translation = c_translate_operator[operator.kind]+"f"+input_translations[0]
    elif operator.kind =="-1" and operator.type.kind in signed_integer_types:
     c_expression.translation="~"+translation+"+1u"
    else:
     c_expression.translation = c_translate_operator[operator.kind]+input_translations[0]
   elif operator.kind in binary_operators:
    if operator.kind=="%" and operator.type.kind in floating_point_types:
     if operator.type.size!=8:
      c_expression.translation = "fmodf("+input_translations[0]+","+input_translations[1]+")"
     else:
      c_expression.translation = "fmod("+input_translations[0]+","+input_translations[1]+")"
    else:
     c_expression.translation = input_translations[0]+c_translate_operator[operator.kind]+input_translations[1]
   if operator.kind in c_spilling_operators and operator.type.kind in integer_types:
    c_expression.spill=True
   if operator.kind=="-1" and operator.type.kind in signed_integer_types:
    c_expression.precedence = 4
   elif operator.kind=="%" and operator.type.kind in floating_point_types:
    c_expression.precedence=1
   else:
    c_expression.precedence = c_operator_precedence[operator.kind]
  elif operator.kind == "(":
   input_function = translated[operator.inputs[0]]
   translation = input_function.translation+"("
   for i in operator.inputs[1:]:
    parameter = translated[i]
    parameter_translation = parameter.translation
    if not context.options.precise_types and not variable_spill and parameter.spill and expression.components[i].kind!="function" and (not expression.components[i].type or expression.components[i].type.kind in numeric_types):
     if parameter.precedence > c_operator_precedence["&"]:
      parameter_translation="("+parameter_translation+")"
     parameter_translation += "&0x"+format(type_mask[expression.components[i].type.size],"x")
    translation+=parameter_translation+","
   if translation[-1]==",":
    translation=translation[:-1]
   translation+=")"
   c_expression.translation=translation
   c_expression.precedence=1
  elif operator.kind == "[":
   array = translated[operator.inputs[0]]
   index = translated[operator.inputs[1]]
   index_translation = index.translation
   if not context.options.precise_types and index.spill:
    if index.precedence > c_operator_precedence["&"]:
     index_translation="("+index_translation+")"
    index_translation += "&0x"+format(type_mask[expression.components[operator.inputs[1]].type.size],"x")
    index.precedence = c_operator_precedence["&"]
   input = expression.components[operator.inputs[0]]
   if input.type.kind in numeric_types and not input.type.nested:
    array_translation = array.translation
    if array.precedence > c_operator_precedence["c"]:
     array_translation = "("+array_translation+")"
    c_expression.translation="(("+context.c_type[input.type.kind]+" *)"+array_translation+")["+index_translation+"]"
   else:
    c_expression.translation = array.translation+"["+index_translation+"]"
   c_expression.precedence=1
  elif operator.kind == ".":
   object = translated[operator.inputs[0]]
   c_expression.translation = object.translation+"->"+operator.inputs[1]
   c_expression.precedence=1
  elif operator.kind == "c":
   input = expression.components[operator.inputs[0]]
   input_translation = translated[operator.inputs[0]]
   if not context.options.precise_types and input_translation.spill:
    translation = input_translation.translation
    if input_translation.precedence > c_operator_precedence["&"]:
     translation="("+translation+")"
    translation += "&0x"+format(type_mask[input.type.size],"x")
    input_translation.precedence = c_operator_precedence["&"]
   else:
    translation=input_translation.translation
   if input_translation.precedence > c_operator_precedence["c"]:
    translation = "("+translation+")"
   translation= "("+c_get_typename(operator.type,"",context)+")"+translation
   c_expression.translation = translation
   c_expression.precedence = c_operator_precedence["c"]
  elif operator.kind == "allocation":
   translation = "malloc(sizeof("
   type = copy.deepcopy(operator.type)
   if type.kind in numeric_types:
    type.pointer=False
   c_type = c_get_typename(type,"",context)
   if type.kind not in default_types:
    assert c_type[-1]=="*"
    c_type=c_type[:-1]
   translation+=c_type+")"
   if len(operator.inputs)>1:
    amount = translated[operator.inputs[1]]
    amount_translation = amount.translation
    if amount.precedence > c_operator_precedence["*"]:
     amount_translation="("+amount_translation+")"
    translation+="*"+amount_translation+")"
   else:
    translation+=")"
   c_expression.translation=translation
   c_expression.precedence=1
  elif operator.type.kind not in default_types:
   assert operator.kind in {"=","!="}
   objects = [translated[operator.inputs[0]],translated[operator.inputs[1]]]
   translations = []
   for i,object in enumerate(objects):
    translation = object.translation
    input = expression.components[operator.inputs[i]]
    if not input.type.pointer:
     translation = "&"+translation
    translations.append(translation)
   c_expression.translation = translations[0]+c_translate_operator[operator.kind]+translations[1]
   c_expression.precedence = 2
  else:
   assert False
  translated.append(c_expression)
 if not variable_spill and translated[-1].spill:
  translation = translated[-1].translation
  if translated[-1].precedence > c_operator_precedence["&"]:
   translation="("+translation+")"
  translation += "&0x"+format(type_mask[expression.components[-1].type.size],"x")
  translated[-1].precedence = c_operator_precedence["&"]
  translated[-1].translation = translation
 return translated[-1].translation
 
def c_translate_code(code,function,context):
 body = []
 for instruction in code:
  output=""
  if instruction.kind == "assignment" and not instruction.special and (instruction.expression.components[-1].type.kind!="fun" or  instruction.expression.components[-1].returns[0].type.kind!="fun"):
   output = c_translate_expression(instruction.destination,context)
   output+="="
   output+= c_translate_expression(instruction.expression,context)
   body.append(output+";")
  elif instruction.kind == "assignment":
   if not instruction.destination:
    output = c_translate_expression(instruction.expression,context)
    body.append(output+";")
   elif instruction.destination=="return" and len(instruction.expression)<2 and instruction.expression[0].components[-1].type.kind!="fun":
    output = "return"
    if instruction.expression:
     output+=" "+c_translate_expression(instruction.expression[0],context)
    body.append(output+";")
   else:
    if instruction.destination=="return":
     source_expression = instruction.expression
     function_type = function.type
    else:
     source_expression = instruction.destination
     function_type = instruction.expression.components[-1].type
    return_variable_name = generate_variable_name(function)
    function.variables[return_variable_name]=None
    output = c_get_returntype(function_type,"",context)
    output+=" "+return_variable_name
    if instruction.destination!="return":
     output+="="+c_translate_expression(instruction.expression,context)
    body.append(output+";")
    for i,destination in enumerate(source_expression):
     if destination:
      output = c_translate_expression(destination,context)
      if instruction.destination=="return":
       output = return_variable_name+".r"+str(i)+"="+output
      else:
       output+="="+return_variable_name+".r"+str(i)
      body.append(output+";")
    if instruction.destination=="return":
     body.append("return "+return_variable_name+";")
  elif instruction.kind in control_flow_identifiers:
   output = c_translate_control_flow[instruction.kind]
   if instruction.kind in {"if","elif"}:
    output+=c_translate_expression(instruction.condition,context)+"){"
   body.append(output)
   if instruction.body:
    body2 = c_translate_code(instruction.body,function,context)
    for i in range(len(body2)):
     body2[i]=" "+body2[i]
    body.extend(body2)
    if not instruction.next:
     body.append("}")
  else:
   assert False
  if debug:
   print(output)
 return body
 
def c_translate_function(function,context):
 body = []
 context.function=function
 body.append(c_get_typename(function.type,function.name,context,not_pointer=True)+" {")
 """for variable in list(function.variables):
  if variable in c_reserved_identifiers:
   new_name = generate_variable_name(function,invalid_names=c_reserved_identifiers,name_prefix=variable)
   rename_variable(variable,new_name,function)"""
 function.body = transform_code(function.body,c_transform_expression,context)
 body2 = []
 for variable in function.variables.values():
  if variable.name not in function.parameter_names:
   body2.append(c_get_typename(variable.type,variable.name,context)+";")
 body2.extend(c_translate_code(function.body,function,context))
 for i in range(len(body2)):
  body2[i]=" "+body2[i]
 body.extend(body2)
 body.append("}")
 return body
  
def c_translate_object(object,context):
 output = []
 sorted_fields = []
 if not context.options.preserve_field_order:
  current_size = 8
  while current_size>0:
   if current_size == 4:
    for variable in object.variables.values():
     if (not variable.type.nested or variable.type.kind in{"*","fun"}) and (variable.type.pointer or variable.type.kind not in numeric_types):
      sorted_fields.append(variable)
   for variable in object.variables.values():
    if variable.type.size == current_size and variable.type.kind in numeric_types and (not variable.type.pointer or variable.type.nested):
     sorted_fields.append(variable)
    elif variable.type.kind not in default_types and variable.type.nested and context.object_alignments[variable.type.kind]==current_size:
     sorted_fields.append(variable)
   current_size//=2
  assert len(sorted_fields)==len(object.variables)
 else:
  sorted_fields = object.variables
 object_typename,declarations = c_translate_typename(object.type,"",context,not_pointer=True)
 assert not declarations
 if context.options.typedef:
  output.append("struct "+object_typename+" {")
 else:
  output.append(object_typename+" {")
 declarations = []
 for field in sorted_fields:
  field_name,declarations2 = c_translate_typename(field.type,field.name,context)
  if declarations2:
   declarations2.extend(declarations)
   declarations=declarations2
  field_name2 = parse_identifier_string(field_name)
  if field_name2 == object_typename:
   output.append(" struct "+field_name+";")
  else:
   output.append(" "+field_name+";")
 output.append("};")
 declarations.extend(output)
 output = declarations
 if context.options.typedef:
  output.append("typedef struct "+object_typename+" "+object_typename+";")
 return output
  
def c_compute_object_alignment(object,context):
 alignment=1
 for variable in object.variables.values():
  if (variable.type.kind not in numeric_types or variable.type.pointer) and (not variable.type.nested or variable.type.kind in {"fun","*"}):
   alignment=max(alignment,4)
  elif variable.type.kind in numeric_types and (not variable.type.pointer or variable.type.nested):
   alignment=max(alignment,variable.type.size)
  elif variable.type.nested and variable.type.kind not in numeric_types:
   alignment=max(alignment,context.object_alignments[variable.type.kind])
 context.object_alignments[object.name]=alignment
  
def c_translate_programm(programm,c_options):
 convert_unsupported_operators({})
 replace_reserved_identifiers(c_reserved_identifiers)
 output = []
 output.append("#include <stdlib.h>")
 output.append("#include <stdint.h>")
 output.append("#include <math.h>") 
 context = c_create_context()
 context.options = c_options
 if context.options.precise_types:
  context.c_type=c_precise_type
 for function in programm.functions.values():
  for variable in function.variables.values():
   context.variables.add(variable.name)
 nested_objects=set()
 remaining_objects = len(programm.objects)
 sorted_objects = list(programm.objects.values())
 while remaining_objects:
  for object in sorted_objects[:remaining_objects]:
   for field in object.variables.values():
    if field.type.kind not in default_types and field.type.kind!="fun":
     if field.type.nested:
      nested_objects.add(field.type.kind)
  for i in range(remaining_objects):
   if sorted_objects[i].name in nested_objects:
    nested_object = sorted_objects[i]
    del sorted_objects[i]
    sorted_objects.insert(0,nested_object)
  remaining_objects = len(nested_objects)
  nested_objects.clear()
 for object in sorted_objects:
  c_compute_object_alignment(object,context)
  object_typename,declarations = c_translate_typename(object.type,"",context,not_pointer=True)
  assert not declarations
  output.append(object_typename+";")
 for function in programm.functions.values():
  context.function=function
  function_declaration,declarations = c_translate_typename(function.type,function.name,context,not_pointer=True)
  output.extend(declarations)
  output.append(function_declaration+";")
 for function in programm.functions.values():
  for variable in function.variables.values():
   if variable.type.kind == "fun":
    function_declaration,declarations = c_translate_typename(variable.type,"",context,not_pointer=True)
    output.extend(declarations)
 for object in sorted_objects:
  output.extend(c_translate_object(object,context))
 for function in programm.functions.values():
  output.extend(c_translate_function(function,context))
 return output
  
 
  
def python_create_options():
 options = pynamespace()
 options.indentation = " "
 options.spill_into_variables = False
 return options
 
def python_create_context():
 context = pynamespace()
 context.options = None
 return context
 
def python_create_expression():
 expression = pynamespace()
 expression.translation = ""
 expression.precedence=0
 expression.spill = False
 return expression
 
 
python_translate_type = {"b1":"B","b2":"H","b4":"I","b8":"L","s1":"b","s2":"h","s4":"i","s8":"l","f1":"e","f2":"e","f4":"f","f8":"d","*":""}
python_operator_precedence={"(":1,"[":1,".":1,"c":1,"~>":1,"~.":1,"~^":1,"~v":1,"+1":2,"-1":2,"~":2,"%":3,"/":3,"*":3,"+":4,"-":4,"<<":5,">>":5,"&":6,"^":7,"|":8,">":9,"<":9,">=":9,"<=":9,"=":9,"!=":9}
python_translate_operator={".":".","~>":"round(","~.":"math.trunc(","~^":"math.ceil(","~v":"math.floor(","+1":"+","-1":"-","~":"~","%":"%","/":"/","*":"*","+":"+","-":"-",">>":">>","<<":"<<",">":">","<":"<",">=":">=","<=":"<=","=":"==","!=":"!=","&":"&","^":"^","|":"|"}
python_spilling_operators={"*","+","-","<<","~"}
python_spillover_operators={"(","[","c","%","/",">>",">","<",">=","<=","=","!="}
python_translate_builtin={"delete":"del "}
python_translate_control_flow={"loop":"while True:","if":"if","elif":"elif","else":"else:","break":"break","continue":"continue"}
python_reserved_identifiers={"False","None","True","and","as","assert","async","await","break","class","continue","def","del","elif","else","except","finally","for","from","global","if","import","in","is","lambda","nonlocal","not","or","pass","raise","return","try","while","with","yield"}

def python_mark(destination,expression,context):
 if destination:
  for op in destination.components:
   if not context.operation or op.kind == context.operation:
    op.metadata["transformed"]=True
 if expression:
  for op in expression.components:
   if not context.operation or op.kind == context.operation:
    op.metadata["transformed"]=True
 return destination,expression,[]

def python_transform_expression(destination,expression,context):
 preamble=[]
 i=0
 while expression and i<len(expression.components):
  operation = expression.components[i]
  if operation.kind in {"/","%"}  and "transformed" not in operation.metadata:
   divide_expression,hole_position,expression = extract_expression(expression,i)
   operand1_variable,operand1_instruction,_,divide_expression = cache_in_variable(divide_expression,divide_expression.components[-1].inputs[0],context.function,invalid_names=python_reserved_identifiers)
   preamble.append(operand1_instruction)
   operand2_variable,operand2_instruction,_,divide_expression = cache_in_variable(divide_expression,divide_expression.components[-1].inputs[1],context.function,invalid_names=python_reserved_identifiers)
   preamble.append(operand2_instruction)
   variable_expression = create_linear_expression()
   variable_expression.components.append(operand2_variable)
   variable_expression.positions.append((0,0,0))
   expression = replace_expression(expression,hole_position,variable_expression)
   code =[]
   if operation.type.kind in signed_integer_types:
    sign_variable_name = generate_variable_name(context.function,invalid_names=python_reserved_identifiers)
    code.append(" "+sign_variable_name+"="+operand1_variable.name+"^"+operand2_variable.name+"&0x"+format(sign_mask[operation.type.size],"x"))
   code.append(" if "+operand2_variable.name+"!=0")
   if operation.type.kind in signed_integer_types:
    code.append("  "+operand1_variable.name+"="+operand1_variable.name+"+")
    code.append("  "+operand2_variable.name+"="+operand2_variable.name+"+")
    code.append("  "+operand2_variable.name+"="+operand1_variable.name+operation.kind+operand2_variable.name)
    code.append("  if "+sign_variable_name+"!=0")
    code.append("   "+operand2_variable.name+"}-")
   else:
    code.append("  "+operand2_variable.name+"="+operand1_variable.name+operation.kind+operand2_variable.name)
   if operation.kind == "%":
    code.append(" else")
    code.append("  "+operand2_variable.name+"="+operand1_variable.name)
   code2=parse_code_body(code,context.function)
   context.operation = operation.kind
   code3 = transform_code(code2,python_mark,context)
   preamble.extend(code3)
   i=0
  else:
   i+=1
 return destination,expression,preamble
  
def python_allocate(type,amount):
 if type.kind in numeric_types:
  translation = amount.translation
  if amount.precedence > python_operator_precedence["*"]:
   translation = "("+translation+")"
  return "memoryview(bytearray("+translation+"*"+str(type.size)+")).cast('"+python_translate_type[type.kind]+"')"
 elif type.kind in default_types:
  return "[None for i in range("+amount.translation+")]"
 else:
  if amount!=None:
   return "["+type.kind+"() for i in range("+amount.translation+")]"
  else:
   return type.kind+"()"
  
def python_translate_expression(expression,context):
 translated = []
 operators = expression.components
 for operator in operators:
  expression = python_create_expression()
  output=""
  if operator.kind =="variable":
   expression.translation= operator.name
   if context.options.spill_into_variables and operator.type.kind in integer_types:
    expression.spill=True
   expression.precedence=0
  elif operator.kind =="function":
   if operator.name not in builtin_functions:
    expression.translation=operator.name
   else:
    expression.translation= python_translate_builtin[operator.name]
   expression.precedence=0
  elif operator.kind=="constant":
   expression.translation = str(operator.value)
   expression.precedence=0
  elif operator.kind=="object":
   pass
  elif operator.kind in python_translate_operator:
   inputs = [translated[operator.inputs[0]]]
   if operator.kind in binary_operators:
    inputs.append(translated[operator.inputs[1]])
   input_translations =[]
   for i,input in enumerate(inputs):
    translation = input.translation
    if operator.kind =="<<" and i==1 or operator.kind==">>" and operator.type.kind in signed_integer_types and i==1:
     if input.precedence > c_operator_precedence["&"]:
      translation="("+translation+")"
     translation += "&0x"+format(bitshift_mask[operator.type.size],"x")
     input.precedence = c_operator_precedence["&"]
    elif operator.kind in python_spillover_operators and input.spill:
     if input.precedence > c_operator_precedence["&"]:
      translation="("+translation+")"
     translation += "&0x"+format(type_mask[operator.type.size],"x")
     input.precedence = c_operator_precedence["&"]
    if input.precedence > python_operator_precedence[operator.kind] or input.precedence==python_operator_precedence[operator.kind] and (i==1 or python_operator_precedence[operator.kind]==9):
     translation="("+translation+")"
    input_translations.append(translation)
   if operator.kind ==".":
    expression.translation = input_translations[0]+python_translate_operator[operator.kind]+operator.inputs[1]
   elif operator.kind in unary_operators:
    if operator.kind in {"~.","~^","~v"}:
     expression.translation = python_translate_operator[operator.kind]+input_translations[0]+")"
    elif operator.kind == "~>":
     expression.translation = python_translate_operator[operator.kind]+input_translations[0]+",0)"
    else:
     expression.translation = python_translate_operator[operator.kind]+input_translations[0]
   elif operator.kind in binary_operators:
    if operator.kind =="/" and operator.type.kind in integer_types:
     expression.translation = input_translations[0]+"//"+input_translations[1]
    else:
     expression.translation = input_translations[0]+python_translate_operator[operator.kind]+input_translations[1]
   expression.precedence = python_operator_precedence[operator.kind]
  elif operator.kind == "(":
   input_function = translated[operator.inputs[0]]
   translation = input_function.translation+"("
   for i in operator.inputs[1:]:
    parameter = translated[i]
    parameter_translation = parameter.translation
    translation+=parameter_translation+","
   if translation[-1]==",":
    translation=translation[:-1]
   translation+=")"
   expression.translation=translation
   expression.precedence=python_operator_precedence["("]
  elif operator.kind == "[":
   array = translated[operator.inputs[0]]
   index = translated[operator.inputs[1]]
   expression.translation = array.translation+"["+index.translation+"]"
   expression.precedence=python_operator_precedence["["]
  elif operator.kind == ".":
   object = translated[operator.inputs[0]]
   expression.translation = object.translation+"."+operator.inputs[1]
   expression.precedence=python_operator_precedence["."]
  elif operator.kind == "c":
   input = operators[operator.inputs[0]]
   input_translation = translated[operator.inputs[0]]
   input_types = {input.type.kind,operator.type.kind}
   if operator.type.kind in numeric_types and not operator.type.pointer:
    if input_types & signed_integer_types and input_types & unsigned_integer_types:
     translation = input_translation.translation
     if input_translation.precedence>python_operator_precedence["."]:
      translation = "("+translation+")"
     truncation = ""
     if operator.type.size<input.type.size:
      truncation="[:"+str(operator.type.size)+"]"
     expression.translation = "int.from_bytes("+translation+".to_bytes("+str(input.type.size)+",byteorder='little',signed="+str(input.type.kind in signed_integer_types)+")"+truncation+",byteorder='little',signed="+str(operator.type.kind not in unsigned_integer_types and operator.type.size<=input.type.size)+")"
     expression.precedence = 1
    elif input.type.kind in integer_types and operator.type.kind in floating_point_types:
     expression.translation = "float("+input_translation.translation+")"
     expression.precedence = 1
    elif input.type.kind in floating_point_types and operator.type.kind in integer_types:
     if operator.type.kind in unsigned_integer_types:
      mini = 0
      maxi = b_max[operator.type.size]
     else:
      mini = s_min[operator.type.size]
      maxi = s_max[operator.type.size]
     expression.translation = "int(max("+str(mini)+",min("+str(maxi)+","+input_translation.translation+")))"
    else:
     expression.translation = translated[operator.inputs[0]].translation
     expression.precedence = translated[operator.inputs[0]].precedence
   elif operator.type.kind in numeric_types and operator.type.pointer:
    input = translated[operator.inputs[0]]
    expression.translation = input.translation+".cast('"+python_translate_type[operator.type.kind]+"')"
    expression.precedence=1
   else:
    expression.translation = translated[operator.inputs[0]].translation
    expression.precedence = translated[operator.inputs[0]].precedence
  elif operator.kind == "allocation":
   if operator.type.pointer:
    expression.translation = python_allocate(operator.type,translated[operator.inputs[1]])
   else:
    expression.translation = python_allocate(operator.type,None)
   expression.precedence=1
  else:
   assert False
  translated.append(expression)
 if not context.options.spill_into_variables and translated[-1].spill:
  translation = translated[-1].translation
  if translated[-1].precedence > python_operator_precedence["&"]:
   translation="("+translation+")"
  translation += "&0x"+format(type_mask[expression.components[-1].type.size],"x")
  translated[-1].precedence = python_operator_precedence["&"]
  translated[-1].translation = translation
 return translated[-1].translation
 
def python_translate_code(code,function,context):
 indentation = context.options.indentation
 body = []
 for instruction in code:
  output=""
  if instruction.kind == "assignment" and not instruction.special:
   output = python_translate_expression(instruction.destination,context)
   output+="="
   output+= python_translate_expression(instruction.expression,context)
   body.append(output)
  elif instruction.kind == "assignment":
   if not instruction.destination:
    output = python_translate_expression(instruction.expression,context)
    body.append(output)
   else:
    if instruction.destination=="return":
     source_expression = instruction.expression
     function_type = function.type
    else:
     source_expression = instruction.destination
     function_type = instruction.expression.components[-1].type
    if instruction.destination!="return":
     output2=python_translate_expression(instruction.expression,context)
    for destination in source_expression:
     if destination:
      output += python_translate_expression(destination,context)+","
     else:
      output += "_," 
    if output[-1]==",":
     output = output[:-1]
    if instruction.destination=="return":
     body.append("return "+output)
    else:
     body.append(output+"="+output2)
  elif instruction.kind in control_flow_identifiers:
   output = python_translate_control_flow[instruction.kind]
   if instruction.kind in {"if","elif"}:
    output+=" "+python_translate_expression(instruction.condition,context)+":"
   body.append(output)
   if instruction.body:
    body2 = python_translate_code(instruction.body,function,context)
    for i in range(len(body2)):
     body2[i]=indentation+body2[i]
    body.extend(body2)
  else:
   assert False
  if debug:
   print(output)
 return body
 
def python_translate_function(function,context):
 indentation = context.options.indentation
 body = []
 context.function=function
 function.body = transform_code(function.body,python_transform_expression,context)
 output="def "+function.name+"("
 for parameter in function.parameters:
  output+=parameter.name
  if parameter.default:
   output+="="+str(parameter.default)
  output+=","
 if output[-1]==",":
  output=output[:-1]
 output+="):"
 body.append(output)
 #function.body = transform_code(function.body,transform_expression,context)
 body2 = python_translate_code(function.body,function,context)
 for i in range(len(body2)):
  body2[i]=indentation+body2[i]
 body.extend(body2)
 return body
  
def python_translate_object(object,context):
 indentation = context.options.indentation
 output = []
 output.append("class "+object.name+":")
 output.append(indentation+"def __init__(self):")
 for field in object.variables.values():
  if not field.type.nested:
   output.append(indentation+indentation+"self."+field.name+" = None")
  else:
   if field.type.length>0:
    expression = python_create_expression()
    expression.translation = str(field.type.length)
    expression.precedence=1
    output.append(indentation+indentation+"self."+field.name+" = "+python_allocate(field.type,expression))
   else:
    output.append(indentation+indentation+"self."+field.name+" = "+python_allocate(field.type,None))
 for method in object.methods:
  output2 = python_translate_function(method,context)
  for i in range(len(output2)):
   output2[i] = indentation+output2[i]
  output.extend(output2)
 return output
  
def python_translate_programm(programm,options):
 convert_unsupported_operators({})
 replace_reserved_identifiers(python_reserved_identifiers)
 output = []
 output.append("import math")
 context = python_create_context()
 context.options = options
 for object in programm.objects.values():
  output.extend(python_translate_object(object,context))
 for function in programm.functions.values():
  output.extend(python_translate_function(function,context))
 return output
  
  
"""
generic translation skeleton
  
def create_options():
 options = pynamespace()
 return options
 
def create_context():
 context = pynamespace()
 context.options = None
 return context
 
def create_expression():
 expression = pynamespace()
 expression.translation = ""
 expression.precedence=0
 return expression
 
translate_type = {"b1":"","b2":"","b4":"","b8":"","s1":"","s2":"","s4":"","s8":"","f1":"","f2":"","f4":"","f8":"","*":""}
operator_precedence={"(":1,"[":1,".":1,"c":1,"~>":1,"~.":1,"~^":1,"~v":1,"+1":2,"-1":2,"~":2,"c":2,"%":3,"/":3,"*":3,"+":4,"-":4,"<<":5,">>":5,">":6,"<":6,">=":6,"<=":6,"=":7,"!=":7,"&":8,"^":9,"|":10}
translate_operator={"~>":"","~.":"","~^":"","~v":"","+1":"+","-1":"-","~":"~","%":"%","/":"/","*":"*","+":"+","-":"-",">>":">>","<<":"<<",">":">","<":"<",">=":">=","<=":"<=","=":"==","!=":"!=","&":"&","^":"^","|":"|"}
translate_builtin={"delete":"free"}
translate_control_flow={"loop":"","if":"","elif":"","else":"","break":"","continue":""}
reserved_identifiers={}

def translate_typename(type,name,context):
 

def transform_expression(destination,expression,context):
 preamble=[]
 i=0
 while expression and i<len(expression.components):
  operation = expression.components[i]
  if operation.kind == "":
   i=0
  else:
   i+=1
 return destination,expression,preamble
  
def translate_expression(expression,context):
 translated = []
 operators = expression.components
 for operator in operators:
  expression = create_expression()
  output=""
  if operator.kind =="variable":
   expression.translation= operator.name
  elif operator.kind =="function":
   if operator.name not in builtin_functions:
    expression.translation=operator.name
   else:
    expression.translation= translate_builtin[operator.name]
  elif operator.kind=="constant":
   
  elif operator.kind=="object":
   pass
  elif operator.kind in translate_operator:
   inputs = [translated[operator.inputs[0]]]
   if operator.kind in binary_operators:
    inputs.append(translated[operator.inputs[1]])
   input_translations =[]
   for i,input in enumerate(inputs):
    translation = input.translation
    if input.precedence > operator_precedence[operator.kind]:
     translation="("+translation+")"
    input_translations.append(translation)
   if operator.kind in unary_operators:
    expression.translation = translate_operator[operator.kind]+input_translations[0]
   elif operator.kind in binary_operators:
    expression.translation = input_translations[0]+translate_operator[operator.kind]+input_translations[1]
   expression.precedence = operator_precedence[operator.kind]
  elif operator.kind == "(":
   input_function = translated[operator.inputs[0]]
   translation = input_function.translation+"("
   for i in operator.inputs[1:]:
    parameter = translated[i]
    parameter_translation = parameter.translation
    translation+=parameter_translation+","
   if translation[-1]==",":
    translation=translation[:-1]
   translation+=")"
   expression.translation=translation
   expression.precedence=operator_precedence["("]
  elif operator.kind == "[":
   array = translated[operator.inputs[0]]
   index = translated[operator.inputs[1]]
   expression.translation = array.translation+"["+index.translation+"]"
   expression.precedence=operator_precedence["["]
  elif operator.kind == ".":
   object = translated[operator.inputs[0]]
   expression.translation = object.translation+"."+operator.inputs[1]
   expression.precedence=operator_precedence["."]
  elif operator.kind == "c":
   input = expression.components[operator.inputs[0]]
   input_translation = translated[operator.inputs[0]]
   translation=input_translation.translation
   if input_translation.precedence > operator_precedence["c"]:
    translation = "("+translation+")"
   translation= "("+translate_typename(operator.type,"",context)+")"+translation
   expression.translation = translation
   expression.precedence = operator_precedence["c"]
  elif operator.kind == "allocation":
   
  else:
   assert False
  translated.append(expression)
 return translated[-1].translation
 
def translate_code(code,function,context):
 body = []
 for instruction in code:
  output=""
  if instruction.kind == "assignment" and not instruction.special:
   #if instruction.new_variable:
   output = translate_expression(instruction.destination,context)
   output+="="
   output+= translate_expression(instruction.expression,context)
   body.append(output)
  elif instruction.kind == "assignment":
   if not instruction.destination:
    output = translate_expression(instruction.expression,context)
    body.append(output)
   else:
    if instruction.destination=="return":
     source_expression = instruction.expression
     function_type = function.type
    else:
     source_expression = instruction.destination
     function_type = instruction.expression.components[-1].type
    if instruction.destination!="return":
     output2=translate_expression(instruction.expression,context)
    for i,destination in enumerate(source_expression):
     if destination:
      output += translate_expression(destination,context)+","
     else:
      output += "_," 
    if output[-1]==",":
     output = ouptput[:-1]
    if instruction.destination=="return":
     body.append("return "+output)
    else:
     body.append(output+"="+output2)
  elif instruction.kind in control_flow_identifiers:
   output = c_translate_control_flow[instruction.kind]
   if instruction.kind in {"if","elif"}:
    output+=translate_expression(instruction.condition,context)+"){"
   body.append(output)
   if instruction.body:
    body2 = translate_code(instruction.body,function,context)
    for i in range(len(body2)):
     body2[i]=context.indentation+body2[i]
    body.extend(body2)
    if not instruction.next:
     body.append("}")
  else:
   assert False
  print(output)
 return body
 
def translate_function(function,context):
 body = []
 context.function=function
 output+=""+function.name+"("
 for parameter in function.parameters:
  output+=parameter.name
  if parameter.default:
   output+="="+str(parameter.default)
  output+=translate_typename(parameter.type)
 output+="){"
 body.append(output)
 function.body = transform_code(function.body,transform_expression,context)
 body2 = []
 for variable in function.variables.values():
  if variable.name not in function.parameter_names:
   body2.append(variable.name+" "+translate_typename(variable.type))
 body2.extend(translate_code(function.body,function,context))
 for i in range(len(body2)):
  body2[i]=context.indentation+body2[i]
 body.extend(body2)
 body.append("}")
 return body
  
def translate_object(object,context):
 output = []
 output.append( object.name+"{")
 for field in object.variables.values():
  output.append(context.indentation+field.name+" "+translate_typename(field.type))
 output.append("}")
 return output
  
def translate_programm(programm,options):
 convert_unsupported_operators({})
 replace_reserved_identifiers(reserved_identifiers)
 output = []
 context = create_context()
 for object in programm.objects.values():
  output.extend(translate_object(object,context))
 for function in programm.functions.values():
  output.extend(translate_function(function,context))
 return output
"""  

  
command_line = sys.argv
programm = create_programm()
i=1
while i<len(command_line) and command_line[i][0]=="-":
 if command_line[i][:13]=="-indentation=":
  if len(command_line[i])<14:
   print("missing indentation amount")
   sys.exit(1)
  programm.indentation = " "*int(command_line[i][13:])
 elif command_line[i][:6]=="-debug":
  debug=True
 elif command_line[i][:21]=="-namespace_separator=":
  programm.namespace_seperator=command_line[i][21:]
 elif command_line[i][:8]=="-prefix=":
  programm.global_prefix = command_line[i][8:]
 else:
  print("unknown option "+command_line[i])
  sys.exit(1)
 i+=1

if len(command_line)<=i:
 print("no input file")
 sys.exit(1)
input_file = command_line[i]
with open(input_file,"r") as f:
 source = f.read()
if "." in input_file:
 input_file = input_file.rsplit(".",1)[0]
source_lines = source.split("\n")
programm = parse(source_lines)
i+=1
if len(command_line)<=i:
 print("no backend selected")
 sys.exit(1)
if command_line[i] in {"C","c"}:
 backend = "c"
 c_options = c_create_options()
 i+=1
 while i<len(command_line):
  if command_line[i][:8]=="-typedef":
   c_options.typedef=True
  elif command_line[i][:15]=="-exact_integers":
   c_options.precise_types=True
  elif command_line[i][:17]=="-same_field_order":
   c_options.preserve_field_order=True
  elif command_line[i][:23]=="-allow_visible_overflow":
   c_options.spill_into_variables=True
  else:
   print("unknown c option "+command_line[i])
   sys.exit(1)
 translation = c_translate_programm(programm,c_options)
 output_name = input_file+".c"
 if os.path.isfile(output_name):
  print(output_name+" already exists, not overwriting")
 with open(output_name,"w") as f:
  for line in translation:
   f.write(line+"\n")
elif command_line[i] in {"Python","python"}:
 backend = "python"
 python_options = python_create_options()
 i+=1
 while i<len(command_line):
  if command_line[i][:23]=="-allow_visible_overflow":
   python_options.spill_into_variables=True
  else:
   print("unknown python option "+command_line[i])
   sys.exit(1)
 translation = python_translate_programm(programm,python_options)
 output_name = input_file+".py"
 if os.path.isfile(output_name):
  print(output_name+" already exists, not overwriting")
 with open(output_name,"w") as f:
  for line in translation:
   f.write(line+"\n")
else:
 print("unknown backend "+command_line[i])
 sys.exit(1)