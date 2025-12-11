from abc import ABC, abstractmethod #permet de définir une classe abstraite

class Vehicule(ABC):    #class mère/abstraite
    def __init__(self,marque:str,id:int,modele:str,categorie:str,etat:str,tarif:float,couleur:str):
        self.marque:str = marque
        self.id:int = id
        self.modele:str = modele
        self.categorie:str = categorie
        self.etat:str = etat
        self.tarif:float = tarif
        self.couleur:str = couleur


class Voiture(Vehicule):
    AGE_MINI = 18

    def __init__(self,marque:str,id:int,modele:str,categorie:str,etat:str,tarif:float,couleur:str,nbrPortes:int,motorisation:str):
        super().__init__(marque,id,modele,categorie,etat,tarif,couleur)

        self.nbrPortes:int = nbrPortes
        self.motorisation:str = motorisation
    
    def get_description(self):
        return self.nbrPortes, self.couleur
    
    def set_model(self,nouvModel):
        self.modele = nouvModel

    def ageIsOk(self,ageUtilisateur):
        return ageUtilisateur >= self.AGE_MINI



class Moto(Vehicule):
    AGE_MINI = 18

    def __init__(self,marque:str,id:int,modele:str,categorie:str,etat:str,tarif:float,couleur:str,motorisation:str,cylindre:int):
        super().__init__(marque,id,modele,categorie,etat,tarif,couleur)

        self.motorisation:str = motorisation
        self.cylindre:int = cylindre

    def ageIsOk(self,ageUtilisateur):
        return ageUtilisateur >= self.AGE_MINI

class Camion(Vehicule):
    AGE_MINI = 21

    def __init__(self,marque:str,id:int,modele:str,categorie:str,etat:str,tarif:float,couleur:str,nbrPortes:int,motorisation:str,remorque:bool):
        super().__init__(marque,id,modele,categorie,etat,tarif,couleur)

        self.nbrPortes:int = nbrPortes
        self.motorisation:str = motorisation
        self.remorque:bool = remorque

    def ageIsOk(self,ageUtilisateur):
        return ageUtilisateur >= self.AGE_MINI

if __name__ == '__main__':

    voiture1 = Voiture("dacia",52,"sandero","SUV","bon",25.5,"rouge",5,"électrique")
    print(voiture1.get_description())

    if (voiture1.ageIsOk(19)):
        print("age ok")
    else:
        print("trop jeune")