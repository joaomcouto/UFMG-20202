#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>
#include <unistd.h>

struct persona
{
    int id;
    char *name;
    int id_couple;
    int priority_couple;
};

int nAttempts;
int idNext = -1;
int idCurrent = 0;
#define personaCount 8

int ovenInterest[personaCount];

int interestCount = 0;
struct persona **personaArray;

pthread_mutex_t interestMutex;
pthread_mutex_t ovenMutex;
pthread_mutex_t initMutex;

//pthread_cond_t coupleGate ;
//pthread_cond_t

pthread_cond_t ovenGate[personaCount];
pthread_cond_t updateGate;

int randomInt(int a, int b)
{
    /*
    Retorna um inteiro aleatório no intervalo [a, b]
    */
    int rand = (int)1000 * drand48();
    return (rand % (b - a)) + a;
}

int init = 1;

void check_couple_presence(struct persona *p, int *ovenInterest){
if(!((p->name == "Kripke") || (p->name == "Stuart"))){
        if(ovenInterest[p->id_couple] == 1){
            p->priority_couple = 2;
            printf("status presença do namorado(a) de %s = 1\n", p->name);
        }
        else
        {
            p->priority_couple = 1;
            printf("status presença do namorado(a) de %s = 0\n", p->name);
        }     
        }// checa se já tem um membro do casal na fila e define quem chegou primeiro.   
}
       
void wait_oven(struct persona *p)
{
    sleep(randomInt(3, 6));
    pthread_mutex_lock(&initMutex);
    if (init == 1)
    {
        idNext = p->id;
        init++;

        pthread_mutex_lock(&interestMutex);
        ovenInterest[p->id] = 1;                     

        printf("%s quer usar o forno\n", p->name);

        //deee
        printf("[");
        for (int i = 0; i < personaCount; i++)
        {
            printf("%d", ovenInterest[i]);
        }
        printf("]\n");
        //buugggg

        pthread_mutex_unlock(&interestMutex);
    }
    else
    {
        pthread_mutex_lock(&interestMutex);
        ovenInterest[p->id] = 1;
        printf("%s quer usar o forno\n", p->name);
        check_couple_presence(p, ovenInterest); // checa se já tem um membro do casal na fila e define quem chegou primeiro.    
        //deee
        printf("[");
        for (int i = 0; i < personaCount; i++)
        {
            printf("%d", ovenInterest[i]);
        }
        printf("]\n");
        //buugggg

        pthread_mutex_unlock(&interestMutex);
    }
    pthread_mutex_unlock(&initMutex);

    pthread_mutex_lock(&ovenMutex);

    while (idNext != p->id)
    {
        pthread_cond_wait(&ovenGate[p->id], &ovenMutex);
    }
    //Nesse ponto o use_oven abaixo é chamado, ele tem que fazer o print de usando e quando sair pedir pra atualizar o nextId
}

int getIdNext()
{
    int amountWaiting = 0;
    for (int i = 0 ; i < personaCount ; i++){
        if (ovenInterest[i] == 1) amountWaiting = amountWaiting + 1 ;
    }
    if(amountWaiting!=0){
        int * waitingIndexes = (int *) malloc(sizeof(int) * amountWaiting) ;
        
        int j = 0 ;
        for (int i =0  ; i < personaCount ; i++){
            if (ovenInterest[i] == 1) {
                waitingIndexes[j] = i ;
                j = j + 1 ;
            }
        }

        int rando = randomInt(0, amountWaiting );
        //printf("Get index pegou o random %d dentre %d e ta mandando o index %d\n", rando,amountWaiting, waitingIndexes[rando]) ;
        int a = waitingIndexes[rando] ;
        free(waitingIndexes);
        return a ;
    } else {
        init = 1 ;
        return -1 ;
    }

    //int rando = randomInt(0, 8);
    //while (ovenInterest[rando] != 1)
      //  rando = randomInt(0, 8);
        //printf("%d", rando) ;

    //return rando;
}

void use_oven(struct persona *p)
{
    printf("%s começar a esquenta algo\n", p->name);
    sleep(1);

    pthread_mutex_lock(&interestMutex); //Impede entrada de novos durante o calculo do proximo em cima do vetor ovenInterest

    ovenInterest[p->id] = 0;
    idNext = getIdNext(); //Dentro dessa função tem que ter a porra toda de calcular quem é o proximo
    

    //ovenInterest[p->id] = 0;
    printf("%s vai comer\n", p->name);
    //deee
    
    printf("[");
    for (int i = 0; i < personaCount; i++)
    {
        printf("%d", ovenInterest[i]);
    }
    printf("]\n");
    
    //printf("O escolhido foi %d\n", idNext);
    //buugggg
    pthread_mutex_unlock(&ovenMutex);
    pthread_cond_signal(&ovenGate[idNext]); //Experimentar com a possibilidade de fazer com apenas um ovenGate e n um array
    pthread_mutex_unlock(&interestMutex);

   
    //thread_cond_signal(&updateGate) ;
}

//void * oven(void * data){
//  pthread_mutex_lock(&interestMutex);

// thread_cond_wait(&ovenGate[i], &ovenMutex);
//}

/*
wait_oven(struct persona * p){
    while(1):
    pthread_mutex_lock(&interestMutex);
    ovenInterest[p->id] = 1 ;
    printf("%s quer usar o forno\n", p->name);
    pthread_mutex_unlock(&interestMutex);
    pthread_cond_signal(&updateGate)

    thread_cond_wait(&ovenGate[i], &ovenMutex);

    printf("Usando o oven ..") ;


    signal(proxRecebeu)
 
    printf("%s quer usar o forno\n", p->name);
    ovenInterest[p->id] = 1 ;
    idNext = fetch_next() ;
    


    while(p->id != idNext){

    }
} 

void * oven(void * data){
    while(1){
        lock(interestMutex)
        idProx = calculo do proximo, -1 se não for definido
        if (idProx != -1){
            Manda signal(ovenGate[idProx])
            thread_cond_wait(proxRecebeu, mutexProxRecebeu)
            Registrar proximo antedido (não quer)
            unlock(mutexProxRecebeu)
            unlock(interestMutex)
            

        }

        else
            pthread_cond_wait(&updateGate,&interestMutex) ;
    } 

    

} 



use_oven(struct persona * p){

}
*/

void eat(struct persona *p)
{
    sleep(randomInt(3, 6));
}

void work(struct persona *p)
{
    printf("%s voltou para o trabalho\n", p->name);
    sleep(randomInt(3, 6));
}

void *oven_user(void *data)
{
    struct persona *p = (struct persona *)data;
    int i;
    for (i = 0; i < nAttempts; i++)
    {
        wait_oven(p);
        use_oven(p);
        eat(p);
        work(p);
    }
    pthread_exit(EXIT_SUCCESS);
}

int main(int agrc, char **argv)
{
    //printf("Cheguei aqui\n");
    pthread_mutex_init(&interestMutex, NULL);
    pthread_mutex_init(&ovenMutex, NULL);
    pthread_mutex_init(&initMutex, NULL);

    for (int i = 0; i < personaCount; i++) pthread_cond_init(&ovenGate[i], NULL) ;

    nAttempts = atoi(argv[1]);
    char *names[personaCount] = {
        "Sheldon",
        "Amy",
        "Howard",
        "Bernardette",
        "Leonard",
        "Penny",
        "Kripke",
        "Stuart"};

    int idCouples[personaCount] = {1, 0, 3, 2, 5, 4 , 6, 7};

    personaArray = (struct persona **)malloc(personaCount * sizeof(struct persona)); //declarado globalmente para poder acessar os dados de casais ao checar prioridade

    int i;
    for (i = 0; i < personaCount; i++)
    {
        personaArray[i] = (struct persona *)malloc(sizeof(struct persona));
        personaArray[i]->id = i;
        personaArray[i]->name = names[i];
        personaArray[i]->id_couple = idCouples[i];
        ovenInterest[i] = 0;
    }

    // pthread_t ovenTid ;
    //pthread_create(&ovenTid, NULL, oven , personaArray[i]) ;

    pthread_t personaTids[personaCount];
    for (i = 0; i < personaCount; i++)
    {
        pthread_create(&personaTids[i], NULL, oven_user, personaArray[i]);
    }

    // pthread_t rajTid;
    //pthread_create(&rajTid, NULL, oven_checker, NULL);

    for (i = 0; i < personaCount; i++)
    {
        pthread_join(personaTids[i], NULL);
    }

    //pthread_cancel(rajTid) ;

    return 0;
}

/*Parte da solução requer o uso de uma mutex para o forno, que servirá como a trava do monitor
para as operações que os personagens podem fazer sobre ele.
*/

/*
Além da mutex, você precisará de
um conjunto de variáveis de condição para controlar a sincronização do acesso dos casais ao
forno: uma variável para enfileirar o segundo membro de um casal se o outro já estiver
esperando, e outra variável de condição para controlar as regras de precedência no acesso direto
ao forno.
*/
