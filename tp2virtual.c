#include <stdio.h>
#include <stdlib.h>
#include <math.h>


struct physical_page
{
    unsigned addr;
    int control_bit;
    int line_position;
};

struct logical_page
{
    unsigned ref_addr;
    int validation_bit;
};

int get_s(unsigned page_size){

    unsigned temp; 
    temp = page_size;
    unsigned s = 0;

    while (temp>1)
    {
        temp = temp>>1;
        s++;
    }
    
return s; 

}

void init_physical_mem(struct physical_page **physical_mem, int num_pages)
{

    for (int i = 0; i < num_pages; i++)
    {
        physical_mem[i] = (struct physical_page*)malloc(sizeof(struct physical_page));
        physical_mem[i]->addr = 0x00000000;
        physical_mem[i]->control_bit = 0;
        physical_mem[i]->line_position = 0;

        printf("%x, %d, %d\n", physical_mem[i]->addr, physical_mem[i]->control_bit, physical_mem[i]->line_position);
    }

}


int main(int agrc, char **argv){


char *method = argv[1]; 
char *file = argv[2]; 
unsigned page_size = 1024 * atoi(argv[3]);
unsigned mem_size = 1024 * atoi(argv[4]);

unsigned s = get_s(page_size);

long int page_table_nrows = pow(2,(32-s));
int num_pages = mem_size/page_size;



struct physical_page **physical_mem = (struct physical_page**)malloc(num_pages*sizeof(struct physical_page));
struct logical_page **page_table = (struct logical_page**)malloc(page_table_nrows*sizeof(struct logical_page));

init_physical_mem(physical_mem, num_pages);


for (int i = 0; i < num_pages; i++)
{
    printf("%x, %d, %d\n", physical_mem[i]->addr, physical_mem[i]->control_bit, physical_mem[i]->line_position);
}



printf("%s, %s, %d, %d\n", method, file, page_size, mem_size);
printf("s = %d\n", s);

return 0;
}