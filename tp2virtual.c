#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

int fifo_next = 0;

int lidas = 0;
int escritas = 0; // temporárias só pra ajudar no debug, depois apagarei


struct physical_page
{
    unsigned addr;
    int control_bit;
    int dirty_bit;
    int alloc_order;
    char last_op;
};

struct logical_page
{
    unsigned ref_addr;
    int validation_bit;
};

void print_physical_memory(struct physical_page **physical_mem, int num_pages){

     printf("Endereço Lógico  |  Dirty biy  |  Útlima Operação\n");

    for (int i = 0; i < num_pages; i++)
    {
        printf("%15x  |  %9d  |  %15c\n", physical_mem[i]-> addr, physical_mem[i]->dirty_bit,physical_mem[i]->last_op);
    }
}


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
        physical_mem[i]->dirty_bit = 0;
        physical_mem[i]->control_bit = 0;
        physical_mem[i]->alloc_order = 0;
    }

    printf("MF init ok\n");

}

void init_page_table(struct logical_page **page_table, int page_table_nrows)
{

    for (int i = 0; i <page_table_nrows; i++)
    {
        page_table[i] = (struct logical_page*)malloc(sizeof(struct logical_page));
        page_table[i]->ref_addr = 0x00000000;
        page_table[i]->validation_bit = 0;
    }

    printf("tb init ok\n");
}

void allocate_memory(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr, 
    char *method, char op, int *page_faults, int *dirty_pages, int num_pages )
    {
  
    int ref_addr, old_addr;

    if (strcmp(method, "fifo") == 0)
    {
 
        if(page_table[addr]->validation_bit == 0){
        
            *page_faults+=1;

            
            if(physical_mem[fifo_next]->control_bit == 1)
            {
            old_addr = physical_mem[fifo_next]->addr;
            
            page_table[old_addr]->validation_bit = 0;

            if (physical_mem[fifo_next]->dirty_bit == 1) {
                *dirty_pages += 1;  
            }
            }

            page_table[addr]->ref_addr = fifo_next;
            page_table[addr]->validation_bit = 1;

            physical_mem[fifo_next]->addr = addr;
            physical_mem[fifo_next]->control_bit = 1;
            physical_mem[fifo_next]->dirty_bit = 0;
        
            if (op == 'W')
            {   
                escritas++;
                physical_mem[fifo_next]->dirty_bit = 1;
                physical_mem[fifo_next]->last_op = 'W';
                
            }else
            {
                lidas++;
                physical_mem[fifo_next]->last_op = 'R';
            }

            fifo_next = (fifo_next+1) % num_pages;
            
        }else if (op == 'W')
            {
                escritas++;
                ref_addr = page_table[addr]->ref_addr;
                physical_mem[ref_addr]->dirty_bit = 1;
                physical_mem[ref_addr]->last_op = 'W';
            }
        else{
            lidas++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->last_op = 'R';
        }
    }
}





int main(int agrc, char **argv){

clock_t start_t, end_t;


printf("Executando Simulador...\n");

double total_t;
int total_access, page_faults, dirty_pages;

unsigned addr;
char op;

total_access = 0;
page_faults = 0;
dirty_pages = 0;



char *method = argv[1]; 
char *file_name = argv[2]; 
unsigned page_size = 1024 * atoi(argv[3]);
unsigned mem_size = 1024 * atoi(argv[4]);

unsigned s = get_s(page_size);

long int page_table_nrows = pow(2,(32-s));
int num_pages = mem_size/page_size;

struct physical_page **physical_mem = (struct physical_page**)malloc(num_pages*sizeof(struct physical_page));
struct logical_page **page_table = (struct logical_page**)malloc(page_table_nrows*sizeof(struct logical_page));

init_physical_mem(physical_mem, num_pages);
init_page_table(page_table, page_table_nrows);

FILE *program = fopen(file_name, "r");


total_access = 0;

start_t = clock();
while (fscanf(program,"%x %c",&addr,&op) !=EOF)
{
    addr = addr >> s;

    allocate_memory(physical_mem, page_table, addr, method, op, &page_faults, &dirty_pages, num_pages);
    // print_physical_memory(physical_mem, num_pages);

    if (op == 'W' || op == 'R')
    {
        total_access++;
    }

}
fclose(program);
end_t = clock();
total_t = (double)(end_t-start_t)/CLOCKS_PER_SEC;

printf("Arquivo de Entrada: %s\nTamanho da memoria: %d KB\nTamanho da pagina: %d KB\nTécnica de Reposição: %s\nTotal de Acessos: %d\nPagefaults: %d\nDirty Pages: %d\nTempo de Execução: %f\n", file_name, mem_size/1024, page_size/1024, method, total_access, page_faults, dirty_pages, total_t);


print_physical_memory(physical_mem, num_pages);

printf("L %d, E %d\n", lidas, escritas);

// free() // reminder to free things



return 0;
}