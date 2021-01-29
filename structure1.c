whille(True){
    if trylock(outro){
        if trylock (OutroParceiro){
            if trylock Forno {
                break; 
            }
            Unlock outroparceiro, outro
            Lock Forno
            Unlock forno
        } elif (trylock meuparceiro){
            Unlock Meuparceiro, outro
            "Niceness" //para não ficar tentando igual louco
        } elif (trylock Forno){
            break ;
        } 
        unlock outro ;
        
    }else if (trylock(OutroParceiro)){
        if (Trylock meuparceiro){
            Unlock meuParceiro, OutroParceiro
        } else if (Trylock(forno)){
            break ;
        } else {
            Unlock OutroParceiro; 
            if (trylock MeuParceiroUsando){
                Lock forno ; unlock forno .... outro positivos
            } else {
                Lock Forno ;
                Break;
            }       
        }
    }
}