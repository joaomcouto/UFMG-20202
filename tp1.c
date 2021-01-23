#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>
#include <unistd.h>

struct persona
{
    int id;
    char *name;
};

int nAttempts;
int idNext ;
#define personaCount 8

int ovenInterest[personaCount] ;

int interestCount = 0 ;

pthread_mutex_t interestMutex ;
pthread_mutex_t ovenMutex ;

//pthread_cond_t coupleGate ;
//pthread_cond_t 

pthread_cond_t ovenGate[personaCount] ;
pthread_cond_t updateGate ;


/*
int fetch_next(){
    int coupleBool[3] ;
    int couple = 0 ;
    int i;
    for (i = 0 ; i < 6 ; i = i + 2){
        if(ovenInterest[i]+ovenInterest[i+1] > 1) {
        coupleBool[i/2] = 1 ;
        couple = 1 ;
        }
    }
    if(couple){
        


    } else{

    }





} 
*/

/////////////
//GLOBAL VAR: int init = 1 ;
wait_oven(struct persona * p){
    pthread_mutex_lock(&initMutex);
    if(init == 1) {
        idNext = p->id ; 
        init++ ;
    }
    else{
        pthread_mutex_lock(&interestMutex);
        ovenInterest[p->id] = 1 ;
        printf("%s quer usar o forno\n", p->name);
        pthread_mutex_unlock(&interestMutex);
    } 
    pthread_mutex_unlock(&initMutex);

    pthread_mutex_lock(&ovenMutex);

    while(idNext != p->id){
        thread_cond_wait(&ovenGate[p->id], &ovenMutex);
    }
    //Nesse ponto o use_oven abaixo é chamado, ele tem que fazer o print de usando e quando sair pedir pra atualizar o nextId
}

use_oven(struct persona * p){
    printf("%s começar a esquenta algo\n", p->name);
    sleep(1) ;

    pthread_mutex_lock(&interestMutex); //Impede entrada de novos durante o calculo do proximo em cima do vetor ovenInterest

    idNext = getIdNext() ; //Dentro dessa função tem que ter a porra toda de calcular quem é o proximo
    pthread_mutex_unlock(&ovenMutex);

    pthread_cond_signal(&ovenGate[idNext]); //Experimentar com a possibilidade de fazer com apenas um ovenGate e n um array

    pthread_mutex_unlock(&interestMutex); 
    

    //thread_cond_signal(&updateGate) ;
}




//void * oven(void * data){
  //  pthread_mutex_lock(&interestMutex);

   // thread_cond_wait(&ovenGate[i], &ovenMutex);
//}

/////////

/*
wait_oven(struct persona * p){
    //while(1):
    pthread_mutex_lock(&interestMutex);
    ovenInterest[p->id] = 1 ;
    printf("%s quer usar o forno\n", p->name);
    pthread_mutex_unlock(&interestMutex);
    //pthread_cond_signal(&updateGate)

    thread_cond_wait(&ovenGate[i], &ovenMutex);

    printf("Usando o oven ..") ;


    signal(proxRecebeu)




    //
    //printf("%s quer usar o forno\n", p->name);
    //ovenInterest[p->id] = 1 ;
    //idNext = fetch_next() ;
    //


    //while(p->id != idNext){

    //}
} 

void * oven(void * data){
    while(1){
        // lock(interestMutex)
        //idProx = calculo do proximo, -1 se não for definido
        //if (idProx != -1){
            //Manda signal(ovenGate[idProx])
            //thread_cond_wait(proxRecebeu, mutexProxRecebeu)
            //Registrar proximo antedido (não quer)
            //unlock(mutexProxRecebeu)
            //unlock(interestMutex)
            

        //}

        else
            //pthread_cond_wait(&updateGate,&interestMutex) ;
    } 

    

} 



use_oven(struct persona * p){

}
*/

eat(struct persona * p){

} 

work(struct persona * p){

} 

void * oven_user(void * data)
{
    struct persona * p = (struct persona *) data ;
    int i;
    for(i = 0 ; i < nAttempts ; i++){
        wait_oven(p) ;
        use_oven(p) ;
        eat(p) ;
        work(p) ;
    } 
    pthread_exit(EXIT_SUCCESS) ;
}

int main(int agrc, char **argv)
{

    pthread_mutex_init(&interestMutex, NULL);


    nAttempts = atoi(argv[1]);
    char *names[personaCount] = {
        "Sheldon",
        "Amy",
        "Howard",
        "Bernardette",
        "Leonard",
        "Penny",
        "Kripke",
        "Stuart"
        };

    struct persona **personaArray = (struct persona **)malloc(personaCount * sizeof(struct persona));

    int i;
    for (i = 0; i < personaCount; i++)
    {
        personaArray[i] = (struct persona *)malloc(sizeof(struct persona));
        personaArray[i]->id = i;
        personaArray[i]->name = names[i];
        ovenInterest[i] = 0 ;
    }

    pthread_t ovenTid ;
    pthread_create(&ovenTid, NULL, oven , personaArray[i]) ;

    pthread_t personaTids[personaCount];
    for (i = 0; i < personaCount; i++)
    {
        pthread_create(&personaTids[i], NULL, oven_user, personaArray[i])
    }

    pthread_t rajTid;
    pthread_create(&rajTid, NULL, oven_checker, NULL);

    for (i = 0; i < personaCount; i++){
        pthread_join(personaTids[i], NULL) ;
    }    


    pthread_cancel(rajTid) ;

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
