#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

int fifo_next = 0;
int filled_pages = 0;
int lidas = 0;
int escritas = 0; // #TODO mudar pra ingles

struct physical_page
{
    unsigned addr;   // endereço logico (linha do arquivo.log) que vai ser vinculado  à pagina
    int control_bit; // bit indica se a página já está em uso no momento da substituição
    int dirty_bit;   // vira 1 quando existe escrita na pagina
    int chance_bit;  //Utilizado no 2a
    double time;     // era pra usar no lru mas nao precisou
    char last_op;    // indica qual foi a ultima operação leitura ou escrita pra printar
};

struct logical_page
{
    unsigned ref_addr;  // indica a posição no vetor physical_page
    int validation_bit; // indica se o endereço mapeado ali ainda é valido
};

int randomInt(int a, int b)
{
    /*
    Retorna um inteiro aleatório no intervalo [a, b]
    */
    int rand = (int)1000 * drand48();
    return (rand % (b - a)) + a;
}

void print_physical_memory(struct physical_page **physical_mem, int num_pages)
{

    printf("Endereço Lógico  |  Frame  |  Dirty bit  |  Útlima Operação\n");

    for (int i = 0; i < num_pages; i++)
    {
        printf("%15x  |  %5d  |  %9d  |  %15c\n", physical_mem[i]->addr, i, physical_mem[i]->dirty_bit, physical_mem[i]->last_op);
    }
}

void free_physical_memory(struct physical_page **physical_mem, int num_pages)
{

    for (int i = 0; i < num_pages; i++)
    {
        free(physical_mem[i]);
    }
}

void free_page_table(struct logical_page **page_table, int page_table_nrows)
{

    for (int i = 0; i < page_table_nrows; i++)
    {
        free(page_table[i]);
    }
}

int get_s(unsigned page_size)
{ //Determinação do número s de bits menos significativos associado com o endereçamento de páginas

    unsigned temp;
    temp = page_size;
    unsigned s = 0;

    while (temp > 1)
    {
        temp = temp >> 1;
        s++;
    }

    return s;
}

void init_physical_mem(struct physical_page **physical_mem, int num_pages)
{

    for (int i = 0; i < num_pages; i++)
    {
        physical_mem[i] = (struct physical_page *)malloc(sizeof(struct physical_page));
        physical_mem[i]->addr = 0x00000000;
        physical_mem[i]->dirty_bit = 0;
        physical_mem[i]->control_bit = 0;
        physical_mem[i]->chance_bit = 0;
        physical_mem[i]->time = -1;
    }
}

void init_page_table(struct logical_page **page_table, int page_table_nrows)
{

    for (int i = 0; i < page_table_nrows; i++)
    {
        page_table[i] = (struct logical_page *)malloc(sizeof(struct logical_page));
        page_table[i]->ref_addr = 0x00000000;
        page_table[i]->validation_bit = 0;
    }
}

void execute_fifo(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                  char op, int *page_faults, int *dirty_pages, int num_pages)
{

    int ref_addr, old_addr;

    if (page_table[addr]->validation_bit == 0)
    { //Se a pagina não estiver valida na memoria fisica...

        *page_faults += 1; // Temos um page fault

        if (physical_mem[fifo_next]->control_bit == 1)
        {
            old_addr = physical_mem[fifo_next]->addr;

            page_table[old_addr]->validation_bit = 0; // lembrar de fazer isso para todos os algortimos sempre que substirtuir uma pagina

            if (physical_mem[fifo_next]->dirty_bit == 1)
            {
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
        }
        else
        {
            lidas++;
            physical_mem[fifo_next]->last_op = 'R';
        }

        fifo_next = (fifo_next + 1) % num_pages;
    }
    else if (op == 'W')
    {
        escritas++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->dirty_bit = 1;
        physical_mem[ref_addr]->last_op = 'W';
    }
    else
    {
        lidas++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->last_op = 'R';
    }
}

void execute_2a(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                char op, int *page_faults, int *dirty_pages, int num_pages)
{

    int ref_addr, old_addr;

    if (page_table[addr]->validation_bit == 0)
    { //Se a pagina não estiver valida na memoria fisica...

        while (physical_mem[fifo_next]->chance_bit == 1)
        {
            physical_mem[fifo_next]->chance_bit = 0;
            fifo_next = (fifo_next + 1) % num_pages;
        }
        //physical_mem[fifo_next]->chance_bit = 1;

        *page_faults += 1; // Temos um page fault

        if (physical_mem[fifo_next]->control_bit == 1) //A memoria a ser substituida ja foi setada antes
        {
            old_addr = physical_mem[fifo_next]->addr; //Pegamos o indice virtual da pagina a ser substituida

            page_table[old_addr]->validation_bit = 0; // Invalidamos seu bit pois ela esta sendo substituida na memoria fisica

            if (physical_mem[fifo_next]->dirty_bit == 1)
            {
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
        }
        else
        {
            lidas++;
            physical_mem[fifo_next]->last_op = 'R';
        }

        fifo_next = (fifo_next + 1) % num_pages;
    }
    //No caso da pagina ja estar presente na memoria virtual
    else if (op == 'W')
    {
        escritas++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->dirty_bit = 1;
        physical_mem[ref_addr]->last_op = 'W';
        physical_mem[ref_addr]->chance_bit = 1;
    }
    else
    {
        lidas++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->last_op = 'R';
        physical_mem[ref_addr]->chance_bit = 1;
    }
}

void execute_lru(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                 char op, int *page_faults, int *dirty_pages, int num_pages)
{

    int ref_addr, least;

    if (page_table[addr]->validation_bit == 0)
    {

        *page_faults += 1;

        double menor;
        if (*page_faults > num_pages)
        {
            menor = physical_mem[0]->time;
            least = 0;
        }
        else
        {
            menor = 0;
        }

        for (int i = 0; i < num_pages; i++)
        {

            if (physical_mem[i]->time < menor)
            {
                menor = physical_mem[i]->time;
                least = i;
            }
        }

        if (physical_mem[least]->control_bit == 1)
        {
            ref_addr = physical_mem[least]->addr;
            page_table[ref_addr]->validation_bit = 0;
            if (physical_mem[least]->dirty_bit == 1)
                *dirty_pages += 1;
            physical_mem[least]->dirty_bit = 0;
        }

        physical_mem[least]->addr = addr;
        physical_mem[least]->control_bit = 1;
        physical_mem[least]->dirty_bit = 0;
        physical_mem[least]->time = (double)clock() / CLOCKS_PER_SEC;

        page_table[addr]->ref_addr = least;
        page_table[addr]->validation_bit = 1;

        if (op == 'W')
        {
            escritas++;
            physical_mem[least]->dirty_bit = 1;
            physical_mem[least]->last_op = 'W';
        }
        else
        {
            lidas++;
            physical_mem[least]->last_op = 'R';
        }
    }
    else
    {

        if (op == 'W')
        {
            escritas++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->dirty_bit = 1;
            physical_mem[ref_addr]->last_op = 'W';
        }
        else if (op == 'R')
        {
            lidas++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->last_op = 'R';
        }

        physical_mem[ref_addr]->time = (double)clock() / CLOCKS_PER_SEC;
    }
}

void execute_new(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                 char op, int *page_faults, int *dirty_pages, int num_pages)
{

    int ref_addr, index;

    if (page_table[addr]->validation_bit == 0)
    {

        *page_faults += 1;

        if (*page_faults > num_pages)
        {
            index = randomInt((num_pages - 1) / 2, num_pages - 1);
        }
        else
        {
            index = num_pages - 1;
        }

        if (physical_mem[index]->control_bit == 1)
        {
            ref_addr = physical_mem[index]->addr;
            page_table[ref_addr]->validation_bit = 0;
            if (physical_mem[index]->dirty_bit == 1)
                *dirty_pages += 1;
        }

        for (int i = index; i > 0; i--)
        {

            *physical_mem[i] = *physical_mem[i - 1];
            ref_addr = physical_mem[i]->addr;
            page_table[ref_addr]->ref_addr = i;
        }

        physical_mem[0]->addr = addr;
        physical_mem[0]->control_bit = 1;
        physical_mem[0]->dirty_bit = 0;

        page_table[addr]->ref_addr = 0;
        page_table[addr]->validation_bit = 1;

        if (op == 'W')
        {
            escritas++;
            physical_mem[0]->dirty_bit = 1;
            physical_mem[0]->last_op = 'W';
        }
        else
        {
            lidas++;
            physical_mem[0]->last_op = 'R';
        }
    }
    else
    {

        if (op == 'W')
        {
            escritas++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->dirty_bit = 1;
            physical_mem[ref_addr]->last_op = 'W';
        }
        else
        {
            lidas++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->last_op = 'R';
        }

        int temp_index = page_table[addr]->ref_addr;
        struct physical_page *temp = (struct physical_page *)malloc(sizeof(struct physical_page));
        *temp = *physical_mem[temp_index];
        for (int i = temp_index; i > 0; i--)
        {
            *physical_mem[i] = *physical_mem[i - 1];
            ref_addr = physical_mem[i]->addr;
            page_table[ref_addr]->ref_addr = i;
        }
        *physical_mem[0] = *temp;

        free(temp);
    }
}

void allocate_memory(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                     char *method, char op, int *page_faults, int *dirty_pages, int num_pages)
{

    if (strcmp(method, "fifo") == 0)
    {
        execute_fifo(physical_mem, page_table, addr, op, page_faults, dirty_pages, num_pages);
    }

    if (strcmp(method, "lru") == 0)
    {
        execute_lru(physical_mem, page_table, addr, op, page_faults, dirty_pages, num_pages);
    }

    if (strcmp(method, "2a") == 0)
    {
        execute_2a(physical_mem, page_table, addr, op, page_faults, dirty_pages, num_pages);
    }

    if (strcmp(method, "new") == 0)
    {
        execute_new(physical_mem, page_table, addr, op, page_faults, dirty_pages, num_pages);
    }
}

int main(int agrc, char **argv)
{

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
    unsigned page_size = 1024 * atoi(argv[3]); //dados da memória em Kb
    unsigned mem_size = 1024 * atoi(argv[4]);

    unsigned s = get_s(page_size);

    long int page_table_nrows = pow(2, (32 - s));
    int num_pages = mem_size / page_size; // numero de frames na memória fisica

    struct physical_page **physical_mem = (struct physical_page **)malloc(num_pages * sizeof(struct physical_page));
    struct logical_page **page_table = (struct logical_page **)malloc(page_table_nrows * sizeof(struct logical_page));

    init_physical_mem(physical_mem, num_pages);    // inicializa vetor de structs que representa memória fisica
    init_page_table(page_table, page_table_nrows); // inicializa tabela de paginas (mapeamento)

    FILE *program = fopen(file_name, "r");

    total_access = 0;

    start_t = clock();
    while (fscanf(program, "%x %c", &addr, &op) != EOF)
    {
        addr = addr >> s;

        allocate_memory(physical_mem, page_table, addr, method, op, &page_faults, &dirty_pages, num_pages);
        // print_physical_memory(physical_mem, num_pages); //descomentar para ver a memoria fisica em cada alteração

        if (op == 'W' || op == 'R') // se n for W ou R é pra desconsiderar o acesso.
        {
            total_access++;
        }
    }

    fclose(program);
    end_t = clock();
    total_t = (double)(end_t - start_t) / CLOCKS_PER_SEC;

    printf("Arquivo de Entrada: %s\nTamanho da memoria: %d KB\nTamanho da pagina: %d KB\nTécnica de Reposição: %s\nTotal de Acessos: %d\nPagefaults: %d\nDirty Pages: %d\nTempo de Execução: %f\n", file_name, mem_size / 1024, page_size / 1024, method, total_access, page_faults, dirty_pages, total_t);

    print_physical_memory(physical_mem, num_pages);

    printf("\nLeitura: %d, Escrita: %d\n", lidas, escritas);

    free_page_table(page_table, page_table_nrows);
    free_physical_memory(physical_mem, num_pages);

    free(page_table);
    free(physical_mem);

    return 0;
}