#include <stdlib.h>
#include <stdint.h>
#include <math.h>
struct really_long_name_add_t { uint_least32_t r0; float r1;};
struct really_long_name_add_t really_long_name_add(float x,uint_least64_t y);
struct really_long_name_add_t main_add(uint_least32_t x,uint_least32_t y);
struct really_long_name_add_t main_add2(uint_least32_t x,uint_least32_t y);
void main_main(void);
struct main_nest {
 uint_least64_t content;
};
struct really_long_name_my_obj {
 uint_least8_t bit;
};
struct main_my_obj {
 struct main_nest nested[1];
 struct main_my_obj *leaf;
 struct really_long_name_my_obj *imported_object;
 uint_least32_t value;
 uint_least32_t composite_array[8];
};
struct really_long_name_add_t really_long_name_add(float x,uint_least64_t y) {
 struct really_long_name_add_t p;
 p.r0=162u;
 p.r1=11.037f;
 return p;
}
struct really_long_name_add_t main_add(uint_least32_t x,uint_least32_t y) {
 uint_least32_t sum;
 sum=x+y;
 struct really_long_name_add_t p1;
 p1.r0=sum;
 p1.r1=1.0f;
 return p1;
}
struct really_long_name_add_t main_add2(uint_least32_t x,uint_least32_t y) {
 uint_least32_t sum;
 sum=x+y;
 struct really_long_name_add_t p2;
 p2.r0=sum;
 p2.r1=0.0f;
 return p2;
}
void main_main(void) {
 struct really_long_name_add_t (*func)(uint_least32_t x,uint_least32_t y);
 uint_least8_t byte;
 uint_least16_t cool;
 float half;
 float tiny;
 uint_least32_t *array;
 struct main_my_obj *obj;
 struct main_my_obj *object2;
 uint_least32_t num1;
 float num2;
 float y;
 uint_least32_t x;
 uint_least16_t short3;
 uint_least32_t int4;
 uint_least64_t long5;
 float float6;
 uint_least32_t signed7;
 double double8;
 func=main_add;
 byte=(uint_least8_t)0u;
 short3=(uint_least16_t)0u;
 int4=0u;
 while(1){
  cool=(uint_least16_t)4u;
  if((int4&0xffffffff)>2u){
   break;
  }else if(func!=main_add){
   cool=cool+(uint_least16_t)2u;
  }
 }
 long5=(uint_least64_t)0u;
 float6=0.0f;
 signed7=~1u+1u;
 double8=0.0;
 half=0.0f;
 tiny=0.0f;
 array=malloc(sizeof(uint_least32_t)*20u);
 int4=array[4u];
 obj=malloc(sizeof(struct main_my_obj ));
 obj->value=7u;
 obj->leaf=malloc(sizeof(struct main_my_obj ));
 obj->nested->content=(uint_least64_t)32609532u;
 object2=obj->leaf;
 free(array);
 free(object2);
 free(obj);
 struct really_long_name_add_t p9=main_add(1u,1u);
 num1=p9.r0;
 num2=p9.r1;
 struct really_long_name_add_t pa=really_long_name_add(1.0f,(uint_least64_t)1u);
 num1=pa.r0;
 num2=pa.r1;
 struct really_long_name_add_t pb=main_add2(int4,2u);
 array[2u]=pb.r0;
 y=pb.r1;
 struct really_long_name_add_t pc=main_add2(1u,1u);
 x=pc.r0;
 main_add(1u,3u);
}
