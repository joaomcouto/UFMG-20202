#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

int fifo_next = 0;
int next_2a = 0 ;
int filled_pages = 0;
int readCount = 0; // Conta o número de operações de tipo R (read)
int writeCount = 0; // Conta o número de operações de tipo W (write)
//readCount +_ writeCount = número de linhas no arquivo

struct physical_page
{
    unsigned addr; // guarda o endereço lógico do programa que a página armazena em dado instante de tempo
    int init_bit; // inidica se a página já está em uso no momento em que é escolhida para alguma substituição
    int dirty_bit; // indica que o página contida nessa posição de memória foi modificada desde seu "swap-in". Auxiliar na contagem de dirty pages
    int chance_bit;// indica se essa página foi referenciada recentemente, essa informação é utilizada durante o 2a
    double time;  // time: armazena o tempo da última referência à página. Utilizamos este campo para avaliar qual é a pagina "least recently used"
    char last_op;  // indica qual foi a ultima operação leitura ou escrita pra printar
};

struct logical_page
{
    unsigned ref_addr;  // guarda o endereçco fısico para a o qual esta pagina PODE estar mapeada(dependendo do bit de validação)
    int validation_bit; // indica se o endereço físico apontado pelo outro campo dessa struct ainda contém essa página ou já foi substituido por outra
};

int randomInt(int a, int b)
{
    /*
    Retorna um inteiro aleatório no intervalo [a, b]
    */
    int rand = (int)1000 * drand48();
    return (rand % (b - a)) + a;
}

void print_physical_memory(struct physical_page **physical_mem, int num_pages) //Função utilizada para printar o estado final da memória física
{

    printf("Endereço Lógico  |  Frame  |  Dirty bit  |  Útlima Operação\n");

    for (int i = 0; i < num_pages; i++)
    {
        printf("%15x  |  %5d  |  %9d  |  %15c\n", physical_mem[i]->addr, i, physical_mem[i]->dirty_bit, physical_mem[i]->last_op);
    }
}

void free_physical_memory(struct physical_page **physical_mem, int num_pages) // Utilizada para liberar a memória física simulada ao final da simulação
{

    for (int i = 0; i < num_pages; i++)
    {
        free(physical_mem[i]);
    }
}

void free_page_table(struct logical_page **page_table, int page_table_nrows) //Utilizada para liberar a tabela de páginas ao final da simulação
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

void init_physical_mem(struct physical_page **physical_mem, int num_pages) //Inicialização da memória física
{

    for (int i = 0; i < num_pages; i++)
    {
        physical_mem[i] = (struct physical_page *)malloc(sizeof(struct physical_page));
        physical_mem[i]->addr = 0x00000000;
        physical_mem[i]->dirty_bit = 0;
        physical_mem[i]->init_bit = 0;
        physical_mem[i]->chance_bit = 0;
        physical_mem[i]->time = -1;
    }
}

void init_page_table(struct logical_page **page_table, int page_table_nrows) //Inicialização da tabela de páginas
{

    for (int i = 0; i < page_table_nrows; i++)
    {
        page_table[i] = (struct logical_page *)malloc(sizeof(struct logical_page));
        page_table[i]->ref_addr = 0x00000000;
        page_table[i]->validation_bit = 0;
    }
}

void execute_fifo(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                  char op, int *page_faults, int *dirty_pages, int num_pages) //Rotina responsável pela alocação de uma página em memória física utilizando fifo
{

    int ref_addr, old_addr;

    if (page_table[addr]->validation_bit == 0)
    { //Se o validation bit for zero a pagina apontada por page_table[addr] não é valida na memoria fisica...Temos um miss

        *page_faults += 1; // Temos portanto um page fault

        if (physical_mem[fifo_next]->init_bit == 1) //Avaliamos se o quadro a ser substituido já foi utilizado para outra página antes
        {
            old_addr = physical_mem[fifo_next]->addr; //Pegando o o endereço lógica da pagina já presente lá

            page_table[old_addr]->validation_bit = 0; //Em sendo o caso, precisamos de informar a essa página que ela não é mais valida, pois será substituida

            if (physical_mem[fifo_next]->dirty_bit == 1) // Incrementamos a contagem de dirty pages se a página sendo substituida tiver passado por writes
            // Em um sistema real, isso acarretaria na escrita da página no disco... O equivalente em nossa simulação é contar mais um dirty page
            {
                *dirty_pages += 1;
            }
        }

        page_table[addr]->ref_addr = fifo_next; //A entrada a tabela de páginas referente ao endereço lógico sendo "swapped in"  é atualizada com o endereço fisico da página escolhida pelo fifo para substituição
        page_table[addr]->validation_bit = 1; //Natualmente, o endereço apontado é valido

        //Atualizamos agora a memoria física
        physical_mem[fifo_next]->addr = addr; //Atualizamos o endereço logico apontado pela página física
        physical_mem[fifo_next]->init_bit = 1; //Asseguramos que proximas iterações do algoritmo consigam identificar essa página como ocupada
        physical_mem[fifo_next]->dirty_bit = 0; //Como em teoria estamos fazendo swap in do disco agora, a página não esta "suja" (fora de sincronia com o disco)

        if (op == 'W')
        {
            writeCount++;
            physical_mem[fifo_next]->dirty_bit = 1;
            physical_mem[fifo_next]->last_op = 'W';
        }
        else //No caso de ser apenas uma leitura..
        {
            readCount++;
            physical_mem[fifo_next]->last_op = 'R';
        }

        fifo_next = (fifo_next + 1) % num_pages;//Passamos o ponteiro do vivo para a próxima posição de memória
    }
    else if (op == 'W') //Chegar nesse else significa que estamos lidando com um hit..
    //..Então no caso do fifo basta incrementar o número de escritar/leituras, o last_op para o print do estado final..
    {
        
        writeCount++; 
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->dirty_bit = 1; //E no caso de ser uma escrita, indica que essa página agora esta fora de sincroniza com o disco AKA dirty
        physical_mem[ref_addr]->last_op = 'W';
    }
    else
    {
        readCount++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->last_op = 'R';
    }
}

// O CÓDIGO DOS OUTROS MÉTODOS SÃO EM SUA MAIOR PARTE MUITO PARECIDOS COM O FIFO
// DESTE PONTO EM DIANTE OPTAMOS POR COMENTAR APENAS AS LINHAS QUE SÃO NOTAVELMENTE PARTICULARES DE CADA ALGORITMO

void execute_2a(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                char op, int *page_faults, int *dirty_pages, int num_pages)
{

    int ref_addr, old_addr;

    if (page_table[addr]->validation_bit == 0)
    { //Se a pagina não estiver valida na memoria fisica... 

        //Procuramos a primeira página em mem física que tenha o bit de chance igual a zero
        while (physical_mem[next_2a]->chance_bit == 1) 
        //Ao encontrar uma pagina com o bit de chance igual a 1, podemos dizer que a chance "foi gasta" portanto setamos pra zero e olhamos a próxima página
        {
            physical_mem[next_2a]->chance_bit = 0;
            next_2a = (next_2a+ 1) % num_pages;
        }

        //Como descrito na documentação, obtemos por setar a chance pra 1 apenas quando a memória é referenciada DEPOIS de ser swapped in
        //Para mudar esse comportamento basta descomentar a linha a baixo.. Dai o chance-bit passa a ser zero tambem depois de um swap in
        //physical_mem[next_2a]->chance_bit = 1; 

        *page_faults += 1; 

        //Daqui pra baixo é quase identico ao fifo, já comentado acima

        if (physical_mem[next_2a]->init_bit == 1) 
        {
            old_addr = physical_mem[next_2a]->addr; 

            page_table[old_addr]->validation_bit = 0; 

            if (physical_mem[next_2a]->dirty_bit == 1)
            {
                *dirty_pages += 1;
            }
        }

        page_table[addr]->ref_addr = next_2a;
        page_table[addr]->validation_bit = 1;

        physical_mem[next_2a]->addr = addr;
        physical_mem[next_2a]->init_bit = 1;
        physical_mem[next_2a]->dirty_bit = 0;

        if (op == 'W')
        {
            writeCount++;
            physical_mem[next_2a]->dirty_bit = 1;
            physical_mem[next_2a]->last_op = 'W';
        }
        else
        {
            readCount++;
            physical_mem[next_2a]->last_op = 'R';
        }

        next_2a = (next_2a + 1) % num_pages;
    }

    else if (op == 'W')
    {
        writeCount++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->dirty_bit = 1;
        physical_mem[ref_addr]->last_op = 'W';
        physical_mem[ref_addr]->chance_bit = 1; //Aqui, uma diferença em relação ao código do fifo acima: setamos o bit de chance para 1 quando uma página é referenciada
    }
    else
    {
        readCount++;
        ref_addr = page_table[addr]->ref_addr;
        physical_mem[ref_addr]->last_op = 'R';
        physical_mem[ref_addr]->chance_bit = 1;//Aqui, uma diferença em relação ao código do fifo acima: setamos o bit de chance para 1 quando uma página é referenciada
    }
}

void execute_lru(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                 char op, int *page_faults, int *dirty_pages, int num_pages)
{

    int ref_addr, least; //Least armazena o indice da página na qual o menor tempo foi encontrado

    if (page_table[addr]->validation_bit == 0)
    {

        *page_faults += 1;

        double menor; //Armazena o tempo mais antigo encontrado até o momento
        if (*page_faults > num_pages) // Page_fault maior que num_pages significa que todas os quadros na memória física foram preenchidos pelo menos uma vez
        //Isso significa que teremos que fazer substituição de alguma página
        {
            menor = physical_mem[0]->time; //Iniciamos o menor tempo como o tempo da primeira posição na memória
            least = 0;
        }
        else
        {
            menor = 0;
        }

        for (int i = 0; i < num_pages; i++) //Navegamos por todas as paginas na memória física
        {

            if (physical_mem[i]->time < menor) //Se forem mais antigas que a atual mais antiga, substituimos menor e o indice da nova página mais antiga
            {
                menor = physical_mem[i]->time;
                least = i;
            }
        }
        //Fazemos as subtituições exatamente como visto nos algoritmos anteriores ..
        if (physical_mem[least]->init_bit == 1)
        {
            ref_addr = physical_mem[least]->addr;
            page_table[ref_addr]->validation_bit = 0;
            if (physical_mem[least]->dirty_bit == 1)
                *dirty_pages += 1;
            physical_mem[least]->dirty_bit = 0;
        }

        physical_mem[least]->addr = addr;
        physical_mem[least]->init_bit = 1;
        physical_mem[least]->dirty_bit = 0;
        physical_mem[least]->time = (double)clock() / CLOCKS_PER_SEC; //.. com a diferença que marcamos o tempo da inserção da página na mem física ..

        page_table[addr]->ref_addr = least;
        page_table[addr]->validation_bit = 1;

        if (op == 'W')
        {
            writeCount++;
            physical_mem[least]->dirty_bit = 1;
            physical_mem[least]->last_op = 'W';
        }
        else
        {
            readCount++;
            physical_mem[least]->last_op = 'R';
        }
    }
    else
    {

        if (op == 'W')
        {
            writeCount++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->dirty_bit = 1;
            physical_mem[ref_addr]->last_op = 'W';
        }
        else if (op == 'R')
        {
            readCount++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->last_op = 'R';
        }

        physical_mem[ref_addr]->time = (double)clock() / CLOCKS_PER_SEC; //.. E também quando a página é referenciada
    }
}

void execute_new(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr,
                 char op, int *page_faults, int *dirty_pages, int num_pages)
{
    //Nosso algoritmo de reposição novo é bastante similar ao LRU, a diferença é que ao invés de percorrer o vetor inteiro na busca da referencia mais distante
    //Simplesmente pegamos uma página aleátorio dentre as menos utilizadas.
    //Para tal bastou assegurar que toda nova inserção ocorra na primeira posição da memória
    //Assim asseguramos que as posições mais para o fim da memória são aquelas menos referenciadas
    int ref_addr, index;

    if (page_table[addr]->validation_bit == 0)
    {

        *page_faults += 1;

        if (*page_faults > num_pages) //No caso de ja termos preenchido todos os quadros da memória física ao menos uma vez..
        {
            index = randomInt((num_pages - 1) / 2, num_pages - 1); //Selecionamos uma página aleatoria dentre as menos referenciadas
        }
        else
        {
            index = num_pages - 1; // Do contrário, selecionamos a última posição da memória (que estara vazia, em vista que sempre inserimos no topo)
        }

        if (physical_mem[index]->init_bit == 1)
        {
            ref_addr = physical_mem[index]->addr;
            page_table[ref_addr]->validation_bit = 0;
            if (physical_mem[index]->dirty_bit == 1)
                *dirty_pages += 1;
        }

        for (int i = index; i > 0; i--) //Deslocamos todas a paginas acima do index selecionado uma pagina para baixo, assim podemos fazer o swap in da nova página no topo
        {

            *physical_mem[i] = *physical_mem[i - 1]; //Deslocamos cada págima
            ref_addr = physical_mem[i]->addr; 
            page_table[ref_addr]->ref_addr = i; //Atualizamos a referencia delas na tabela de páginas
        }

        //A reposição é igual já vimos antes nas outras rotinas, com a diferença de que o swap in é feito na primeira posição da memória (physical_mem[0])
        physical_mem[0]->addr = addr;
        physical_mem[0]->init_bit = 1;
        physical_mem[0]->dirty_bit = 0;

        page_table[addr]->ref_addr = 0;
        page_table[addr]->validation_bit = 1;

        if (op == 'W')
        {
            writeCount++;
            physical_mem[0]->dirty_bit = 1;
            physical_mem[0]->last_op = 'W';
        }
        else
        {
            readCount++;
            physical_mem[0]->last_op = 'R';
        }
    }
    else //Analogamente as referencias 'hit' são praticamente iguais, com a diferença de que repocisionamos a pagina referenciada no topo da mem física
    {

        if (op == 'W')
        {
            writeCount++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->dirty_bit = 1;
            physical_mem[ref_addr]->last_op = 'W';
        }
        else
        {
            readCount++;
            ref_addr = page_table[addr]->ref_addr;
            physical_mem[ref_addr]->last_op = 'R';
        }
        //Criamos uma cópia da página referenciada
        int temp_index = page_table[addr]->ref_addr;
        struct physical_page *temp = (struct physical_page *)malloc(sizeof(struct physical_page));
        *temp = *physical_mem[temp_index];
    
        for (int i = temp_index; i > 0; i--) //Deslocamos todas as páginas acima da referenciada uma posição para baixo
        {
            *physical_mem[i] = *physical_mem[i - 1];
            ref_addr = physical_mem[i]->addr;
            page_table[ref_addr]->ref_addr = i;
        }
        *physical_mem[0] = *temp; //Por mim copiamos a página referenciada no topo da memória física

        //Assim garantimos consistência na relação entre a idade das páginas e sua posição na mem física

        free(temp);
    }
}

void allocate_memory(struct physical_page **physical_mem, struct logical_page **page_table, unsigned addr, //Avalia o método escolhido e chamada a rotina correta para a alocação da página no endereço lógico addr
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

    double total_t; //Utilizado para calcular o tempo total de execução do programa
    int total_access, page_faults, dirty_pages; //Contadores de: número total de operações R ou W feitas na memória, faltas de pagina, dirty pages

    unsigned addr; //Armazena o endereço recebida da última linha lida do arquivo de entrada
    char op; //Idem para a operação (R ou W)

    total_access = 0; 
    page_faults = 0;
    dirty_pages = 0;

    char *method = argv[1];
    char *file_name = argv[2];
    unsigned page_size = 1024 * atoi(argv[3]);
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
    while (fscanf(program, "%x %c", &addr, &op) != EOF) //Le a proxima linha do arquivo
    {
        addr = addr >> s; //Desloca addr em s bits para capturar seu endereçamento a nivel de páginas

        allocate_memory(physical_mem, page_table, addr, method, op, &page_faults, &dirty_pages, num_pages);
        // print_physical_memory(physical_mem, num_pages); //descomentar para ver a memoria fisica em cada alteração

        if (op == 'W' || op == 'R') // se n for W ou R, desconsideramos o acesso.
        {
            total_access++;
        }
    }

    fclose(program);
    end_t = clock();
    total_t = (double)(end_t - start_t) / CLOCKS_PER_SEC;

    //Geração do relatorio
    printf("Arquivo de Entrada: %s\nTamanho da memoria: %d KB\nTamanho da pagina: %d KB\nTécnica de Reposição: %s\nTotal de Acessos: %d\nPagefaults: %d\nDirty Pages: %d\nTempo de Execução: %f\n", file_name, mem_size / 1024, page_size / 1024, method, total_access, page_faults, dirty_pages, total_t);

    //Impressão do estado final da memória física
    print_physical_memory(physical_mem, num_pages);

    //Impressão da contagem final de leituras e escritas
    printf("\nLeitura: %d, Escrita: %d\n", readCount, writeCount);


    //Desalocando a tabela de páginas e a simulação da memória física 
    free_page_table(page_table, page_table_nrows);
    free_physical_memory(physical_mem, num_pages);

    free(page_table);
    free(physical_mem);

    return 0;
}