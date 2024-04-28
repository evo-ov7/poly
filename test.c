#include <stdlib.h>
#include <stdint.h>
#include <math.h>
struct really_long_name_add_t { uint32_t r0; float r1;};
struct really_long_name_add_t really_long_name_add(float x,uint64_t y);
struct really_long_name_add_t main_add(uint32_t x,uint32_t y);
struct really_long_name_add_t main_add2(uint32_t x,uint32_t y);
uint16_t main_id(uint16_t x);
void main_main(void);
struct main_nest {
 uint64_t content;
};
struct really_long_name_my_obj {
 uint8_t bit;
};
struct main_my_obj {
 struct main_nest nested[1];
 struct main_my_obj *leaf;
 struct really_long_name_my_obj *imported_object;
 uint32_t value;
 uint32_t composite_array[8];
};
struct really_long_name_add_t really_long_name_add(float x,uint64_t y) {
 struct really_long_name_add_t p4;
 p4.r0=162u;
 p4.r1=11.037f;
 return p4;
}
struct really_long_name_add_t main_add(uint32_t x,uint32_t y) {
 uint32_t sum;
 sum=x+y;
 struct really_long_name_add_t p5;
 p5.r0=sum;
 p5.r1=1.0f;
 return p5;
}
struct really_long_name_add_t main_add2(uint32_t x,uint32_t y) {
 uint32_t sum;
 sum=x+y;
 struct really_long_name_add_t p6;
 p6.r0=sum;
 p6.r1=0.0f;
 return p6;
}
uint16_t main_id(uint16_t x) {
 return x;
}
void main_main(void) {
 struct really_long_name_add_t (*func)(uint32_t x,uint32_t y);
 uint8_t byte;
 uint16_t cool;
 float half;
 float tiny;
 uint32_t *array;
 struct main_my_obj *obj;
 struct main_my_obj *object2;
 uint32_t num1;
 float num2;
 float y;
 uint32_t x;
 uint32_t p;
 uint64_t z1;
 uint64_t z2;
 uint64_t z4;
 uint64_t z8;
 uint64_t z16;
 uint64_t z32;
 uint32_t p1;
 uint32_t p2;
 uint8_t p3;
 uint16_t short7;
 uint32_t int8;
 uint64_t long9;
 float floata;
 uint32_t signedb;
 double doublec;
 func=main_add;
 byte=(uint8_t)0u;
 short7=(uint16_t)0u;
 int8=0u;
 p=1365u;
 z1=(uint64_t)12297829382473034410u;
 z2=(uint64_t)14757395258967641292u;
 z4=(uint64_t)17361641481138401520u;
 z8=(uint64_t)18374966859414961920u;
 z16=(uint64_t)18446462603027742720u;
 z32=(uint64_t)18446744069414584320u;
 p=p&~p+1u;
 if(p==0u){
  p=32u;
 }else{
  p1=(p&(uint32_t)z1)!=0u|((p&(uint32_t)z2)!=0u)<<((uint8_t)1u&0x1f)|((p&(uint32_t)z4)!=0u)<<((uint8_t)2u&0x1f)|((p&(uint32_t)z8)!=0u)<<((uint8_t)3u&0x1f)|((p&(uint32_t)z16)!=0u)<<((uint8_t)4u&0x1f);
  p=(uint32_t)p1;
 }
 int8=p;
 p2=4u;
 p3=(uint8_t)12u;
 p2=p2>>(p3&0x1f)|p2<<((uint8_t)32u-p3&0x1f);
 int8=p2;
 while(1){
  cool=(uint16_t)4u;
  if(int8>2u){
   break;
  }else if(func!=main_add){
   cool=cool+((uint16_t)2u*(uint16_t)6u-(uint16_t)3u);
  }
 }
 long9=(uint64_t)0u;
 floata=0.0f;
 signedb=~1u+1u;
 doublec=0.0;
 half=0.0f;
 tiny=0.0f;
 array=malloc(sizeof(uint32_t)*20u);
 array[main_id((uint16_t)1u)+(uint16_t)4u]=1u;
 obj=malloc(sizeof(struct main_my_obj ));
 obj->value=7u;
 obj->leaf=malloc(sizeof(struct main_my_obj ));
 obj->nested->content=(uint64_t)32609532u;
 object2=obj->leaf;
 free(array);
 free(object2);
 free(obj);
 struct really_long_name_add_t pd=main_add(1u,1u);
 num1=pd.r0;
 num2=pd.r1;
 struct really_long_name_add_t pe=really_long_name_add(1.0f,(uint64_t)1u);
 num1=pe.r0;
 num2=pe.r1;
 struct really_long_name_add_t pf=main_add2(int8,2u);
 array[2u]=pf.r0;
 y=pf.r1;
 struct really_long_name_add_t pg=main_add2(1u,1u);
 x=pg.r0;
 main_add(1u,3u);
}
