/* Isolated machine-code execution, NOT a DOS emulator or full-game test.
 * Loads user-owned bytes at laboratory addresses and executes narrow verified
 * regions in the CPU's 32-bit compatibility mode. Linux x86-64/GCC, -no-pie.
 * Three external display/UI helpers are replaced by RET. The network screen,
 * input loop, DOS/4GW, IPX, and extension initializer are NOT executed.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <errno.h>

#define CB 0x10000000u
#define DB 0x20000000u
#define XB 0x30000000u
#define MB 0x40000000u
#define FB 0x41000000u
#define SB 0x42000000u
#define GB 0x50000000u
#define FBP (FB+0x8000u)
#define SITE 0x76d78u
#define CONT 0x76d9eu
struct Regs { uint32_t eax, ecx, edx, ebx, ebp, esi, edi, flags; } input, output;
uint64_t saved_rsp;
uint32_t stacktop, target32, start_esp, end_esp;
extern void invoke32(void);
__asm__(
".text\n.global invoke32\ninvoke32:\n"
"push %rbp\npush %rbx\npush %r12\npush %r13\npush %r14\npush %r15\n"
"mov %rsp,saved_rsp(%rip)\nmov stacktop(%rip),%esp\n"
"pushq $0x23\nleaq compat32(%rip),%rax\npushq %rax\nlretq\n"
".code32\ncompat32:\nmov $0x2b,%cx\nmov %cx,%ds\nmov %cx,%es\n"
"mov input+0,%eax\nmov input+4,%ecx\nmov input+8,%edx\nmov input+12,%ebx\n"
"mov input+16,%ebp\nmov input+20,%esi\nmov input+24,%edi\n"
"pushl input+28\npopfl\nmov %esp,start_esp\ncall *target32\n"
"mov %eax,output+0\nmov %ecx,output+4\nmov %edx,output+8\nmov %ebx,output+12\n"
"mov %ebp,output+16\nmov %esi,output+20\nmov %edi,output+24\n"
"pushfl\npopl output+28\nmov %esp,end_esp\n"
"pushl $0x33\npushl $resume64\nlretl\n"
".code64\nresume64:\nmov saved_rsp(%rip),%rsp\n"
"pop %r15\npop %r14\npop %r13\npop %r12\npop %rbx\npop %rbp\nret\n");
struct Blob { unsigned char *p; size_t n; };
static struct Blob cp,dp,xp,ca,da,xa,gate;
static unsigned char *code, *data, *ext, *frame;
static uint32_t *mail;
static int checks=0, failures=0;
static void die(const char *m){perror(m);exit(2);}
static struct Blob load(const char *dir,const char *name){
 char path[4096];if(snprintf(path,sizeof path,"%s/%s",dir,name)>=(int)sizeof path){errno=ENAMETOOLONG;die("path");}
 FILE*f=fopen(path,"rb");if(!f)die(path);if(fseek(f,0,SEEK_END))die("seek");long n=ftell(f);if(n<0||n>16000000)die("size");rewind(f);
 struct Blob b={malloc((size_t)n),(size_t)n};if(!b.p)die("malloc");if(fread(b.p,1,b.n,f)!=b.n)die("read");fclose(f);return b;
}
static unsigned char *map_at(uint32_t a,size_t n){
 size_t size=(n+4095)&~(size_t)4095;
 void*p=mmap((void*)(uintptr_t)a,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0);
 if(p==MAP_FAILED)die("mmap");
 return p;
}
static void check(const char *name,int ok){++checks;if(!ok)++failures;printf("%s %s\n",ok?"PASS":"FAIL",name);}
static void put32(unsigned char*p,size_t o,uint32_t v){memcpy(p+o,&v,4);}
static uint16_t word(unsigned char*p,size_t o){uint16_t v;memcpy(&v,p+o,2);return v;}
static void jump_at(unsigned char*p,uint32_t from,uint32_t to){p[0]=0xe9;uint32_t v=to-from-5;memcpy(p+1,&v,4);}
static void regs(void){input=(struct Regs){0x11223344,0x66778899,0x12345678,0x22334455,FBP,0x44556677,0x55667788,0x246};}
static void run(uint32_t off){target32=CB+off;invoke32();}
static void reset(int patch,int mode){
 memcpy(code,ca.p,ca.n);memcpy(data,da.p,da.n);memcpy(ext,xa.p,xa.n);
 memset(frame,0,65536);memset(mail,0,4096);
 code[CONT]=0xc3; /* Stop before the rest of Main_Screen_ input processing. */
 code[0x920cd]=code[0x10c2f0]=code[0x79f8a]=0xc3; /* Declared external helper stubs. */
 data[0x21f3a]=(unsigned char)mode;data[0x21bdd]=1; /* Avoid uninitialized field/UI allocation. */
 memset(data+0x32f7e,0,8);data[0x24198]=0;data[0x21f2d]=0x7f;
 data[0x21a08]=0;data[0x21a09]=0;regs();
 if(patch)jump_at(code+SITE,CB+SITE,GB);
}
int main(int argc,char**argv){
 setbuf(stdout,NULL);if(argc!=2){fprintf(stderr,"usage: native_probe FIXTURE_DIRECTORY\n");return 2;}
 cp=load(argv[1],"code_pre.bin");dp=load(argv[1],"data_pre.bin");xp=load(argv[1],"extension_pre.bin");
 ca=load(argv[1],"code_post.bin");da=load(argv[1],"data_post.bin");xa=load(argv[1],"extension_post.bin");gate=load(argv[1],"gate.bin");
 code=map_at(CB,cp.n);data=map_at(DB,dp.n);ext=map_at(XB,xp.n);mail=(uint32_t*)map_at(MB,4096);frame=map_at(FB,65536);map_at(SB,65536);
 unsigned char*g=map_at(GB,4096);if(gate.n>4096){fprintf(stderr,"gate too large\n");return 2;}memcpy(g,gate.p,gate.n);stacktop=SB+65520;
 memcpy(code,cp.p,cp.n);memcpy(data,dp.p,dp.n);memcpy(ext,xp.p,xp.n);memset(frame,0,65536);
 uint32_t extstart=0x423b5;put32(frame,0x8000-0x9c,XB+extstart);put32(frame,0x8000-0x88,XB+extstart);put32(frame,0x8000-0x84,DB);put32(frame,0x8000-0x80,CB);
 unsigned char saved=code[0x1596f6];code[0x1596f6]=0xc3;regs();input.eax=XB+0x50;run(0x1596c4);code[0x1596f6]=saved;
 check("original-extension-relocation-loop-code",cp.n==ca.n&&!memcmp(code,ca.p,ca.n));
 check("original-extension-relocation-loop-data",dp.n==da.n&&!memcmp(data,da.p,da.n));
 check("original-extension-relocation-loop-extension",xp.n==xa.n&&!memcmp(ext,xa.p,xa.n));
 check("original-extension-relocation-loop-balanced-stack",start_esp==end_esp);
 reset(0,3);unsigned char*before=malloc(da.n),*after=malloc(da.n);if(!before||!after)die("malloc");
 int good=1;for(int i=0;i<8;i++)data[0x32f7e + i]=(unsigned char)(17+i*29);memcpy(before,data,da.n);
 for(int i=0;i<8;i++){regs();input.eax=(uint32_t)i;run(0xea5a3);struct Regs want=input;want.eax=data[0x32f7e + i];if(memcmp(&want,&output,sizeof want)||start_esp!=end_esp)good=0;}
 check("original-getter-eight-synthetic-player-flags-registers-flags-stack",good);
 check("original-getter-no-game-data-writes",!memcmp(before,data,da.n));
 data[0x32f7e + 0x105]=0x9a;regs();input.eax=0x105;run(0xea5a3);
 check("original-getter-upper-EAX-ABI-probe-not-real-player",output.eax==0x19a);
 for(int mode=2;mode<=3;mode++){
  reset(0,mode);run(SITE);memcpy(after,data,da.n);struct Regs baseline=output;uint16_t baseline_exit=word(frame,0x804a);
  check(mode==2?"baseline-mode2-selects-network-screen":"baseline-mode3-selects-network-screen",word(data,0x21a08)==37&&data[0x24198]==1&&baseline_exit==1);
  reset(1,mode);mail[0]=1;memcpy(before,data,da.n);struct Regs original=input;run(SITE);
  check(mode==2?"defer-mode2-preserves-game-data":"defer-mode3-preserves-game-data",!memcmp(before,data,da.n));
  check(mode==2?"defer-mode2-preserves-registers-flags-stack":"defer-mode3-preserves-registers-flags-stack",!memcmp(&original,&output,sizeof original)&&start_esp==end_esp);
  check(mode==2?"defer-mode2-only-request-no-native-flag":"defer-mode3-only-request-no-native-flag",mail[1]==1&&mail[2]==0&&mail[3]==0&&word(frame,0x804a)==0&&!memcmp(data+0x32f7e,"\0\0\0\0\0\0\0\0",8));
  mail[1]=0;check(mode==2?"unready-mode2-mailbox-only":"unready-mode3-mailbox-only",!memcmp(before,data,da.n)&&word(frame,0x804a)==0);
  mail[2]=1;regs();run(SITE);
  check(mode==2?"allow-mode2-equals-original-data-and-registers":"allow-mode3-equals-original-data-and-registers",!memcmp(after,data,da.n)&&!memcmp(&baseline,&output,sizeof baseline)&&word(frame,0x804a)==baseline_exit&&start_esp==end_esp);
  check(mode==2?"allow-mode2-consumes-one-permit":"allow-mode3-consumes-one-permit",mail[1]==0&&mail[2]==0&&mail[3]==1);
  memcpy(before,data,da.n);regs();run(SITE);
  check(mode==2?"second-request-mode2-defers":"second-request-mode3-defers",mail[1]==1&&mail[2]==0&&!memcmp(before,data,da.n));
  reset(1,mode);run(SITE);
  check(mode==2?"disabled-mode2-preserves-baseline":"disabled-mode3-preserves-baseline",!memcmp(after,data,da.n)&&!memcmp(&baseline,&output,sizeof baseline));
 }
 reset(0,0);run(SITE);memcpy(after,data,da.n);struct Regs single=output;
 reset(1,0);mail[0]=1;run(SITE);check("single-player-pass-through",!memcmp(after,data,da.n)&&!memcmp(&single,&output,sizeof single)&&mail[1]==0);
 /* Enter the real field-comparison prelude using synthetic UI field IDs. */
 reset(1,3);mail[0]=1;put32(frame,0x8076,7);data[0x24162]=7;data[0x24163]=0;data[0x21976]=data[0x21977]=0;
 memcpy(before,data,da.n);run(0x76d62);
 check("real-field-prelude-matching-next-button-defers",mail[1]==1&&!memcmp(before,data,da.n)&&word(frame,0x804a)==0);
 reset(1,3);mail[0]=1;put32(frame,0x8076,6);data[0x24162]=7;data[0x24163]=0;run(0x76d62);
 check("real-field-prelude-other-button-does-not-ready",mail[1]==0);
 reset(1,3);mail[0]=1;put32(frame,0x8076,7);data[0x24162]=7;data[0x24163]=0;data[0x21976]=1;data[0x21977]=0;run(0x76d62);
 check("real-field-prelude-skip-fields-does-not-ready",mail[1]==0);
 reset(1,3);mail[0]=1;run(SITE);mail[2]=1;regs();input.ebp=FBP+0x1000;run(SITE);
 check("release-uses-fresh-frame-not-saved-caller-pointer",word(frame,0x804a)==0&&word(frame,0x904a)==1);
 printf("SUMMARY checks=%d failures=%d scope=isolated-x86-32-not-full-game\n",checks,failures);
 return failures?1:0;
}
