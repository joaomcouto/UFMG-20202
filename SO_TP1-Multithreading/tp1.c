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

#define personaCount 8
int nAttempts;
int idNext = -1;
int idCurrent = 0;
int init = 1;

int deadlock = 0;
int ovenInterest[personaCount];
int interestCount = 0;
struct persona **personaArray;

pthread_mutex_t interestMutex;
pthread_mutex_t ovenMutex;
pthread_mutex_t initMutex;
pthread_mutex_t rajMutex;

pthread_cond_t ovenGate[personaCount];
pthread_cond_t updateGate;

void print_oven(){
                //deee
        printf("[");
        for (int i = 0; i < personaCount; i++)
        {
            printf("%d", ovenInterest[i]);
        }
        printf("] \n");
        //buugggg

        // printf("next = %d", idNext);
}

int check_empty_line(){

    int sum = 0;

    for (int i = 0; i < personaCount; i++)
    {
       sum += ovenInterest[i];
    }

    if (sum > 0)
    {
        return 0;
    }else return 1;

}

int existsCouple(){

    int sheldon = ovenInterest[0];
    int amy = ovenInterest[1];
    int howard = ovenInterest[2];
    int bernardette = ovenInterest[3];
    int leonard = ovenInterest[4];
    int penny = ovenInterest[5];
    int couple;

    if((sheldon && amy) || (howard && bernardette) || (leonard && penny)){
        return 1;
    }else
    {
        return 0;
    }
    

};

int check_couple(int *ovenInterest){

    int sheldon = ovenInterest[0];
    int amy = ovenInterest[1];
    int howard = ovenInterest[2];
    int bernardette = ovenInterest[3];
    int leonard = ovenInterest[4];
    int penny = ovenInterest[5];
    int couple;

    if((sheldon && amy) || (howard && bernardette) || (leonard && penny)){

        if (sheldon && amy)
        {
            if(!(leonard && penny)){ 
                if(personaArray[0]->priority_couple > personaArray[1]->priority_couple){ //checa se sheldon chegou primeiro e define ele como o próximo, caso contrário a amy vai primeiro.
                    return personaArray[0]->id;
                } 
                else{
                    personaArray[1]->priority_couple = -1;
                    return personaArray[1]->id; 
                } 

            }
            else
            {
                if(personaArray[4]->priority_couple > personaArray[5]->priority_couple){ //checa se leonard chegou primeiro e define ele como o próximo, caso contrário a penny vai primeiro.
                    return personaArray[4]->id;
                } 
                else {
                    personaArray[5]->priority_couple = -1;
                    return personaArray[5]->id; 
                }
            }
        
        } 
        else
        {
           if(howard && bernardette){ 
                if(personaArray[2]->priority_couple > personaArray[3]->priority_couple){ //checa se sheldon chegou primeiro e define ele como o próximo, caso contrário a amy vai primeiro.
                    return  personaArray[2]->id;
                } 
                else return  personaArray[3]->id; 

            }
            else
            {
                if(personaArray[4]->priority_couple > personaArray[5]->priority_couple){ //checa se leonard chegou primeiro e define ele como o próximo, caso contrário a penny vai primeiro.
                    return  personaArray[4]->id;
                } 
                else return  personaArray[5]->id; 
            }
        }

    }    
   
}

void check_deadlock(int *ovenInterest){

    int sheldon = ovenInterest[0];
    int amy = ovenInterest[1];
    int howard = ovenInterest[2];
    int bernardette = ovenInterest[3];
    int leonard = ovenInterest[4];
    int penny = ovenInterest[5];
    int kripke = ovenInterest[6];
    int stuart = ovenInterest[7];

  
    if((sheldon && howard && leonard) && !(amy || bernardette || penny)){
        deadlock = 1;
    }
    else if((amy && bernardette && penny) && !(sheldon || howard || leonard)){
        deadlock = 1;

    } else if((sheldon && howard && leonard) && (amy && bernardette && penny)){ 
        deadlock = 1;
            
    }else{
        if((sheldon && amy) || (howard && bernardette) || (leonard && penny)){
            if(ovenInterest[personaArray[idCurrent]->id_couple]==1){

            }
            idNext = personaArray[idCurrent]->id_couple;
            deadlock = 0;
        }else{

            if((sheldon || amy) && (leonard || penny) && (howard || bernardette)){
                deadlock = 1;
            }else
            {
                deadlock =  0; 
            }               
        }
        
    }

    return;
 
}

int check_single(int *ovenInterest){

    int sheldon = ovenInterest[0];
    int amy = ovenInterest[1];
    int howard = ovenInterest[2];
    int bernardette = ovenInterest[3];
    int leonard = ovenInterest[4];
    int penny = ovenInterest[5];
    int kripke = ovenInterest[6];
    int stuart = ovenInterest[7];

   
    if (sheldon || amy || howard || bernardette || leonard || penny){    
        if (sheldon || amy)
        {
            if(!(leonard || penny)){ 
                if(sheldon) return  personaArray[0]->id;
                if(amy) return  personaArray[1]->id; 
            }
            else
            {
                if(leonard) return  personaArray[4]->id;
                if(penny) return  personaArray[5]->id; 
            }
        
        } 
        else
        {
            if(howard || bernardette){ 
                if(howard) return  personaArray[2]->id;
                if(bernardette) return  personaArray[3]->id; 
            }
            else
            {
                if(leonard) return  personaArray[4]->id;
                if(penny) return  personaArray[5]->id; 
            }
        }
    }
    else
    {
        if(kripke){
            return  personaArray[6]->id;
        }else if(stuart) return  personaArray[7]->id; 
    }        


}

int randomInt(int a, int b)
{
    /*
    Retorna um inteiro aleatório no intervalo [a, b]
    */
    int rand = (int)1000 * drand48();
    return (rand % (b - a)) + a;
}

int setIdNext(int *ovenInterest)
{
   
    check_deadlock(ovenInterest);

    if(!deadlock){
        // printf("nextId from setnext %d\n", idNext);
        if(existsCouple()){
            idNext = check_couple(ovenInterest);
            // printf("nextId from setnext couple %d\n", idNext);
        }else{
        idNext = check_single(ovenInterest);
        // printf("nextId from setnext single %d\n", idNext);
    }
    } else 
    {
        while (deadlock);        
    }

        return idNext;

 }

void check_couple_presence(struct persona *p, int *ovenInterest){
if(!((p->name == "Kripke") || (p->name == "Stuart"))){
        if(ovenInterest[p->id_couple] == 1){
            p->priority_couple = 0; //namorado presente prioridade menor
            // printf("status presença do namorado(a) de %s = 1\n", p->name);
        }
        else
        {
            p->priority_couple = 1;// namorado ausente prioridade maior
            personaArray[p->id_couple]->priority_couple = 0;
            // printf("status presença do namorado(a) de %s = 0\n", p->name);
        }     
        }// checa se já tem um membro do casal na fila e define quem chegou primeiro.   
}
       
void wait_oven(struct persona *p)
{
    sleep(randomInt(2, 5));
    pthread_mutex_lock(&initMutex);
    if (check_empty_line())
    {
        // printf("name %s" ,p->name);
        idNext = p->id;
        // init++;

        pthread_mutex_lock(&interestMutex);
        ovenInterest[p->id] = 1;                     

        printf("%s quer usar o forno\n", p->name);
 
        pthread_mutex_unlock(&interestMutex);
        //sleep(1);
    }
    else
    {
        pthread_mutex_lock(&interestMutex);
        ovenInterest[p->id] = 1;
        printf("%s quer usar o forno\n", p->name);
        check_couple_presence(p, ovenInterest); // checa se já tem um membro do casal na fila e define quem chegou primeiro.    
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

void use_oven(struct persona *p)
{   
    printf("------->") ; 
    printf("%s começa a esquentar algo\n", p->name);
    idCurrent = p->id;
    ovenInterest[p->id] = 0;
    personaArray[p->id]->priority_couple = -1;
    sleep(1);
    
    pthread_mutex_lock(&interestMutex); //Impede entrada de novos durante o calculo do proximo em cima do vetor ovenInterest

    
    // printf("fila: ");
    print_oven();
    idNext = setIdNext(ovenInterest); //define a variável global nextId ou entra em looping até o raj resolver deadlocks. 
    // printf("  escolhido: %d\n", idNext);

    printf("%s vai comer\n", p->name);

    pthread_mutex_unlock(&ovenMutex);

    pthread_cond_signal(&ovenGate[idNext]); //Experimentar com a possibilidade de fazer com apenas um ovenGate e n um array
    pthread_mutex_unlock(&interestMutex);

   
    //thread_cond_signal(&updateGate) ;
}

void eat(struct persona *p)
{ 
    sleep(randomInt(2, 5));
}

void work(struct persona *p)
{
    printf("%s voltou para o trabalho\n", p->name);
    sleep(randomInt(2, 5));   
}

void raj_verify(){

    pthread_mutex_lock(&rajMutex); 
    check_deadlock(ovenInterest);
    // printf("Raj checked and deadlock = %d\n, nextid = %d  current id = %d\n", deadlock, idNext, idCurrent);
    // printf("nextid = %d  current id = %d\n", );
    // print_oven();

    if (deadlock == 1){
        int validId = 0;
        while(!validId){
            int id_aux = randomInt(0, 7);
            if((ovenInterest[id_aux] == 1) && (id_aux != idCurrent)) {
                idNext = id_aux;
                printf("Raj detectou um deadlock, liberando %s\n", personaArray[idNext]->name);
                deadlock = 0;
                validId = 1;
           }
        }
        
    }

    pthread_mutex_unlock(&rajMutex); 
}

void *oven_checker(void *data)
{
    
    while (1)
    {
        raj_verify();
        sleep(5);
    } 
    
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

    pthread_t personaTids[personaCount];
    for (i = 0; i < personaCount; i++)
    {
        pthread_create(&personaTids[i], NULL, oven_user, personaArray[i]);
    }

    pthread_t rajTid;
    pthread_create(&rajTid, NULL, oven_checker, NULL);

    for (i = 0; i < personaCount; i++)
    {
        pthread_join(personaTids[i], NULL);
    }

    pthread_cancel(rajTid);

    return 0;
}
