#include <stdlib.h>
#include <stdint.h>
#include <math.h>
struct main_nest2;
struct main_nest;
struct really_long_name_my_obj;
struct main_my_obj;
struct really_long_name_add_t { uint_least32_t  r0; float  r1;};
struct really_long_name_add_t really_long_name_add(float  x,uint_least64_t  y);
struct nested3_t { void *r0;};
struct return_pb { void (*r0)(uint_least32_t);};
struct main_nester_t { void (*r0)(uint_least8_t,uint_least16_t);};
struct main_nester_t main_nester(void (*nested)(struct return_pb (*)(uint_least32_t  *),void *),struct nested3_t (*nested3)(struct main_my_obj *));
struct really_long_name_add_t main_add(uint_least32_t  x,uint_least32_t  y);
struct really_long_name_add_t main_add2(uint_least32_t  x,uint_least32_t  y);
uint_least16_t main_id(uint_least16_t  x);
void main_main(void);
struct main_nest2 {
 struct main_my_obj *fora;
};
struct main_nest {
 uint_least64_t  content;
 struct main_nest2 nested[1];
};
struct really_long_name_my_obj {
 uint_least8_t  bit;
};
struct main_my_obj {
 struct main_nest nested[1];
 struct main_my_obj *leaf;
 struct really_long_name_my_obj *imported_object;
 uint_least32_t  value;
 uint_least32_t  composite_array[8];
};
struct really_long_name_add_t really_long_name_add(float  x,uint_least64_t  y) {
 struct really_long_name_add_t pc;
 pc.r0=162u;
 pc.r1=11.037f;
 return pc;
}
struct main_nester_t main_nester(void (*nested)(struct return_pb (*)(uint_least32_t  *),void *),struct nested3_t (*nested3)(struct main_my_obj *)) {
 struct main_nester_t pd;
 pd.r0=(void (*)(uint_least8_t,uint_least16_t))main_add;
 return pd;
}
struct really_long_name_add_t main_add(uint_least32_t  x,uint_least32_t  y) {
 uint_least32_t  sum;
 sum=x+y;
 struct really_long_name_add_t pe;
 pe.r0=sum;
 pe.r1=1.0f;
 return pe;
}
struct really_long_name_add_t main_add2(uint_least32_t  x,uint_least32_t  y) {
 uint_least32_t  sum;
 sum=x+y;
 struct really_long_name_add_t pf;
 pf.r0=sum;
 pf.r1=0.0f;
 return pf;
}
uint_least16_t main_id(uint_least16_t  x) {
 return x;
}
void main_main(void) {
 struct really_long_name_add_t (*func)(uint_least32_t,uint_least32_t);
 uint_least8_t  byte;
 uint_least16_t  cool;
 float  half;
 float  tiny;
 uint_least32_t  *array;
 struct main_my_obj *obj;
 struct main_my_obj *object2;
 uint_least32_t  num1;
 float  num2;
 float  y;
 uint_least32_t  x;
 uint_least32_t  p;
 uint_least64_t  z1;
 uint_least64_t  z2;
 uint_least64_t  z4;
 uint_least64_t  z8;
 uint_least64_t  z16;
 uint_least64_t  z32;
 uint_least32_t  p1;
 uint_least32_t  p2;
 uint_least8_t  p3;
 uint_least16_t  short4;
 uint_least32_t  int5;
 uint_least64_t  long6;
 float  float7;
 uint_least32_t  signed8;
 double  double9;
 func=main_add;
 byte=(uint_least8_t)0u;
 short4=(uint_least16_t)0u;
 int5=0u;
 p=1365u;
 z1=(uint_least64_t)12297829382473034410u;
 z2=(uint_least64_t)14757395258967641292u;
 z4=(uint_least64_t)17361641481138401520u;
 z8=(uint_least64_t)18374966859414961920u;
 z16=(uint_least64_t)18446462603027742720u;
 z32=(uint_least64_t)18446744069414584320u;
 p=p&~p+1u;
 if((p&0xffffffff)==0u){
  p=32u;
 }else{
  p1=(p&(uint_least32_t)z1)!=0u|((p&(uint_least32_t)z2)!=0u)<<((uint_least8_t)1u&0x1f)|((p&(uint_least32_t)z4)!=0u)<<((uint_least8_t)2u&0x1f)|((p&(uint_least32_t)z8)!=0u)<<((uint_least8_t)3u&0x1f)|((p&(uint_least32_t)z16)!=0u)<<((uint_least8_t)4u&0x1f);
  p=(uint_least32_t)p1;
 }
 int5=p;
 p2=4u;
 p3=(uint_least8_t)12u;
 p2=(p2&0xffffffff)>>(p3&0x1f)|p2<<((uint_least8_t)32u-p3&0x1f);
 int5=p2;
 while(1){
  cool=(uint_least16_t)4u;
  if((int5&0xffffffff)>2u){
   break;
  }else if(func!=main_add){
   cool=cool+((uint_least16_t)2u*(uint_least16_t)6u-(uint_least16_t)3u);
  }
 }
 long6=(uint_least64_t)0u;
 float7=0.0f;
 signed8=~1u+1u;
 double9=0.0;
 half=0.0f;
 tiny=0.0f;
 array=malloc(sizeof(uint_least32_t)*20u);
 array[main_id((uint_least16_t)1u)+(uint_least16_t)4u]=1u;
 obj=malloc(sizeof(struct main_my_obj ));
 obj->value=7u;
 obj->leaf=malloc(sizeof(struct main_my_obj ));
 obj->nested->content=(uint_least64_t)32609532u;
 object2=obj->leaf;
 free(array);
 free(object2);
 free(obj);
 struct really_long_name_add_t pg=main_add(1u,1u);
 num1=pg.r0;
 num2=pg.r1;
 struct really_long_name_add_t ph=really_long_name_add(1.0f,(uint_least64_t)1u);
 num1=ph.r0;
 num2=ph.r1;
 struct really_long_name_add_t pi=main_add2(int5,2u);
 array[2u]=pi.r0;
 y=pi.r1;
 struct really_long_name_add_t pj=main_add2(1u,1u);
 x=pj.r0;
 main_add(1u,3u);
}
