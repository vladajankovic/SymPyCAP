import sympy
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider 

sympy.init_printing(use_latex=True)
def runcap(n,Phasor=False,LatexOutput=False):
    v="v"
    count = 1;
    exp1 = []
    eq1 = []
    #Pravljenje simbola za potencijale cvorova i Inicijalizacija jednacina na null
    for i in range(1,n[0]):
        exp1.append(sympy.Symbol(v+str(i)))
        eq1.append([])
    for elem in n[1:]:
        if elem[0] == "R":#Forma['R',4,1,"R1"]
            temp = sympy.Symbol(elem[3])
            #Jednacine po potncijalima cvorova za otpornike za prvi cvor
            if elem[1] != 0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=1/temp*exp1[elem[1]-1]#1/RvX
                else:
                    eq1[elem[1]-1]+=1/temp*exp1[elem[1]-1]
                if elem[2] !=0:
                    if not eq1[elem[2]-1]:
                        eq1[elem[2]-1]=(-1)/temp*exp1[elem[1]-1]
                    else:
                        eq1[elem[2]-1]-=1/temp*exp1[elem[1]-1]
            #Jednacine po potncijalima cvorova za otpornike za drugi cvor            
            if elem[2] !=0:
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=1/temp*exp1[elem[2]-1]
                else:
                    eq1[elem[2]-1]+=1/temp*exp1[elem[2]-1]
                if elem[1] != 0:
                    if not eq1[elem[1]-1]:
                        eq1[elem[1]-1]=-1/temp*exp1[elem[2]-1]
                    else:
                        eq1[elem[1]-1]-=1/temp*exp1[elem[2]-1]
        elif elem[0] == 'IG':#Forma['IG',ulazniCvor,izlazniCvor,"Znak"]
            #temp = sympy.Symbol("IG"+str(count))
            temp = sympy.Symbol(elem[3]);
            temp2 = sympy.Symbol("UG"+str(count))
            count = count + 1
            exp1.append(temp2)
            #Dovaanje relacije UGx = V1 - V2 u jenacine za resavanje
            
            if elem[1] !=0:
                if elem[2] !=0:
                    eq1.append(temp2-exp1[elem[1]-1]+exp1[elem[2]-1])
                else:
                    eq1.append(temp2-exp1[elem[1]-1])
            elif elem[2] !=0:
                eq1.append(temp2+exp1[elem[2]-1])
         
            #Jednacine po potencijalima cvoroa za IG
            #Iz prvog cvora izlazi pa posto se jednacine pisu sa leve strane tu ide sa plus
            #U drugi ulazi pa tu ide sa minus
            # EQ[1] + Ig; EQ[2] - Ig
            if elem[1] != 0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=temp
                else:
                    eq1[elem[1]-1]+=temp
            if elem[2] !=0:
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=-temp
                else:
                    eq1[elem[2]-1]-=temp
        elif elem[0] == 'UG':#Forma['UG',plusTerm,minusTerm,"vrednost"]
            #temp = sympy.Symbol("IG"+str(count))
            temp = sympy.Symbol("IG"+str(count));
            count = count + 1
            temp2 = sympy.Symbol(elem[3])
            exp1.append(temp)
            #Dodavanje jednacina UGx = V2 - V1 
            #I dodavanje struje IgX u jednacine cvorova
            # EQ[1] - IgX; EQ[2] + Ig
            if elem[1] !=0 and elem[2] != 0:
                eq1.append(temp2-exp1[elem[1]-1]+exp1[elem[2]-1])
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=-temp
                else:
                    eq1[elem[2]-1]-=temp
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=+temp
                else:
                    eq1[elem[1]-1]+=temp
            elif elem[1] !=0:
                eq1.append(temp2-exp1[elem[1]-1])
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=temp
                else:
                    eq1[elem[1]-1]+=temp
            elif elem[2] !=0:
                eq1.append(temp2+exp1[elem[2]-1])
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=-temp
                else:
                    eq1[elem[2]-1]-=temp
        elif elem[0] == 'L':#Proveri #Forma['L',PlusTerm,MinusTerm,pocetniUslov,"vrednost"] pocetni uslov -> "I0", "I1", ..., None
            temp = sympy.Symbol("s")*sympy.Symbol(elem[4]);
            if elem[3] != None:
                temp2 = sympy.Symbol(elem[3])/sympy.Symbol("s")
                #Dodavanje struje kalema u jednacine cvorova u Laplasovaom domenu
            if elem[1] !=0 and elem[2] != 0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=-(exp1[elem[2]-1]-exp1[elem[1]-1])/temp
                else:
                    eq1[elem[1]-1]-=(exp1[elem[2]-1]-exp1[elem[1]-1])/temp
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=(exp1[elem[2]-1]-exp1[elem[1]-1])/temp
                else:
                    eq1[elem[2]-1]+=(exp1[elem[2]-1]-exp1[elem[1]-1])/temp
                if elem[3] != None:
                    eq1[elem[1]-1]+=temp2
                    eq1[elem[2]-1]-=temp2
            elif elem[2] !=0:
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=(exp1[elem[2]-1])/temp
                else:
                    eq1[elem[2]-1]+=(exp1[elem[2]-1])/temp
                if elem[3] != None:
                    eq1[elem[2]-1]-=temp2
            elif elem[1] !=0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=-(-exp1[elem[1]-1])/temp
                else:
                    eq1[elem[1]-1]-=(-exp1[elem[1]-1])/temp
                if elem[3] != None:
                    eq1[elem[1]-1]+=temp2
        elif elem[0] == 'C':#Forma['C',plusTerm,minusTerm,pocetniUslov,"sympy.Symbol"] pocetni uslov -> None, "U0", "U1", ... 
            if elem[3] != None:
                temp2 = sympy.Symbol(elem[3])*sympy.Symbol(elem[4])
            temp = sympy.Symbol("s")*sympy.Symbol(elem[4])
            #Dodavanje struje kondezatora u jednacine cvorova u Laplasovom domenu
            if elem[1] !=0 and elem[2] != 0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=-(exp1[elem[2]-1]-exp1[elem[1]-1])*temp
                else:
                    eq1[elem[1]-1]-=(exp1[elem[2]-1]-exp1[elem[1]-1])*temp
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=(exp1[elem[2]-1]-exp1[elem[1]-1])*temp
                else:
                    eq1[elem[2]-1]+=(exp1[elem[2]-1]-exp1[elem[1]-1])*temp
                #Dodavanje pocetnih uslova 
                if elem[3] != None:
                    eq1[elem[1]-1]-=temp2
                    eq1[elem[2]-1]+=temp2
            elif elem[2] !=0:
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=(exp1[elem[2]-1])*temp
                else:
                    eq1[elem[2]-1]+=(exp1[elem[2]-1])*temp
                #Dodavanje pocetnih uslova
                if elem[3] != None:
                    eq1[elem[2]-1]+=temp2
            elif elem[1] !=0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=-(-exp1[elem[1]-1])*temp
                else:
                    eq1[elem[1]-1]-=(-exp1[elem[1]-1])*temp
                #Dodavanje pocetnih uslova
                if elem[3] != None:
                    eq1[elem[1]-1]-=temp2
                #eq1[elem[1]-1]+=temp
        elif elem[0]=="OpAmp": #Forma['OpAmp',[minusTerm,plusTerm],treci]
            #Dodavanje jednacina elemenata OpAmpa
            if elem[1][0]!=0 and elem[1][1]!=0:
                eq1.append(exp1[elem[1][1]-1]-exp1[elem[1][0]-1])
            elif elem[1][1]!=0:
                eq1.append(exp1[elem[1][1]-1])
            elif elem[1][0]!=0:
                eq1.append(-exp1[elem[1][0]-1])
            #Dodavanje struje OpAmpa u jednacinu cvora 3
            if elem[2]!=0:
                temp=sympy.Symbol("Iop"+str(count))
                count=count+1;
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=temp
                else:
                    eq1[elem[2]-1]+=temp
                exp1.append(temp);
        elif elem[0]=="VCVS":#Forma['VCVS',[plus,minus],[plus,minus],a,"sympy.Symbol_I2"] a-> string ili int
            #temp = sympy.Symbol("Ivcvs"+str(count))
            temp=sympy.Symbol(elem[4])
            count=count+1
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp
                else:
                    eq1[elem[2][0]-1]+=temp
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp
                else:
                    eq1[elem[2][1]-1]-=temp
            exp1.append(temp)#dodaj u promenjve 
            #prvi par DESNI PRISTUP
            if elem[2][0] != 0:
                if elem[2][1] != 0:
                    temp=exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp=exp1[elem[2][0]-1]
            elif elem[2][1] !=0:
                temp=-elem[2][1]
            #drugi par LEVI PRISTUP
            if elem[1][0]!= 0:
                if elem[1][1] != 0:
                    temp2=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp2=exp1[elem[1][0]-1]
            elif elem[1][1] !=0:
                temp2=-exp1[elem[1][1]-1]
            #u eq1
            eq1.append(temp-sympy.Symbol(elem[3])*temp2)
        elif elem[0] == "VCCS":#Forma['VCCS',[plus,minus],[plus,minus],g]
            #LEVI PRISTUP
            if elem[1][0]!= 0:
                if elem[1][1] != 0:
                    temp=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp=exp1[elem[1][0]-1]
            elif elem[1][1] !=0:
                temp=-exp1[elem[1][1]-1]
            temp=temp*sympy.Symbol(str(elem[3]))
            #DESNI PRISTUP
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp
                else:
                    eq1[elem[2][0]-1]+=temp
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp
                else:
                    eq1[elem[2][1]-1]-=temp
        elif elem[0] == "CCCS":#Forma['CCCS',[plus,minus],[plus,minus],a,"Symobol_I1"]
            #temp=sympy.Symbol("Icccs"+str(count))
            temp=sympy.Symbol(elem[4])
            #Prvi par LEVI PRISTUP
            if elem[1][0]!=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
            if elem[1][1]!=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
            exp1.append(temp)#Dodaj U promenjive 
            temp=temp*sympy.Symbol(elem[3])
            #Drugi par DESNI PRISTUP
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp
                else:
                    eq1[elem[2][0]-1]+=temp
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp
                else:
                    eq1[elem[2][1]-1]-=temp
            #PRVI PRISTUP JEDNACINA ZA NAPON
            if elem[1][0]!= 0:
                if elem[1][1] != 0:
                    temp2=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp2=exp1[elem[1][0]-1]
            elif elem[1][1] !=0:
                temp2=-exp1[elem[1][1]-1]
            #DODAJ KAO JEDNACINU
            eq1.append(temp2)
        elif elem[0]=="CCVS":#Proveri#Forma['CCVS',[plus,minus],[plus,minus],r,"Symbol_I1"]
            #temp=sympy.Symbol("Iccvs"+str(count))
            #count=count+1
            temp=sympy.Symbol(elem[4])
            exp1.append(temp)
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp
                else:
                    eq1[elem[2][0]-1]+=temp
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp
                else:
                    eq1[elem[2][1]-1]-=temp
            #prvi par DESNI PRISTUP
            if elem[2][0] != 0:
                if elem[2][1] != 0:
                    temp=exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp=exp1[elem[2][0]-1]
            elif elem[2][1] !=0:
                temp=-elem[2][1]
            #drugi par LEVI PRISTUP
            if elem[1][0]!= 0:
                if elem[1][1] != 0:
                    temp2=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp2=exp1[elem[1][0]-1]
            elif elem[1][1] !=0:
                temp2=-exp1[elem[1][1]-1]
            eq1.append(temp2);#DA LI OVDE TREBA EQ1 NE EXP1
            temp=temp/sympy.Symbol(str(elem[3]))#NAPON NA DESNOM PRISTUPU PODELI SA PARAMETROM
            ####Dodaj u jednacine
            if elem[1][0]!=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
            if elem[1][1]!=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
        elif elem[0]=="ABCD":#["ABCD",[plusTerm,minusTerm],[plusTerm,minusTerm],["A","B","C","D"],["I1","I2"]]
            temp=sympy.Symbol(elem[4][0])
            temp2=sympy.Symbol(elem[4][1])
            exp1.append(temp)
            exp1.append(temp2)
           
            if elem[1][0]!=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
           
            if elem[1][1]!=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
           
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=-temp2
                else:
                    eq1[elem[2][0]-1]-=temp2
           
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=temp2
                else:
                    eq1[elem[2][1]-1]+=temp2
           
            if elem[1][0]!=0:
                if elem[1][1]!=0:
                    temp3=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp3=exp1[elem[1][0]-1]
            elif elem[1][1]!=0:
                temp3=-exp1[elem[1][1]-1]
               
            if elem[2][0]!=0:
                if elem[2][1]!=0:
                    temp4=exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp4=exp1[elem[2][0]-1]
            elif elem[2][1]!=0:
                temp4=-exp1[elem[2][1]-1]
           
            temp5=sympy.Symbol(elem[3][0])*temp4+sympy.Symbol(elem[3][1])*temp2
            eq1.append(temp3-temp5)
            temp5=sympy.Symbol(elem[3][2])*temp4+sympy.Symbol(elem[3][3])*temp2
            eq1.append(temp-temp5)
            
        elif elem[0]=="IT":#Idealni transformator#Proveri#Forma["IT",[plus,minus],[plus,minus],m]
            temp = sympy.Symbol("Iit"+str(count))
            exp1.append(temp)
            count= count + 1
            #Levi Par; Levi Pristup
            if elem[1][0] !=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
            if elem[1][1] !=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
            #Desni Par; Desni Pristup
            temp=-temp*sympy.Symbol(elem[3])#pomnozi sa m
            if elem[2][0] !=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp
                else:
                    eq1[elem[2][0]-1]+=temp
            if elem[2][1] !=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp
                else:
                    eq1[elem[2][1]-1]-=temp
            #Dodavanje jednacine
            if elem[1][0]!=0:
                if elem[1][1]!=0:
                    temp = exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp = exp1[elem[1][0]-1]
            elif elem[1][1]!=0:
                temp = -exp1[elem[1][1]-1]
            #######################################
            if elem[2][0]!=0:
                if elem[2][1]!=0:
                    temp2 = exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp2 = exp1[elem[2][0]-1]
            elif elem[2][1]!=0:
                temp2 = -exp1[elem[2][1]-1]
            #########################################
            eq1.append(temp-sympy.Symbol(elem[3])*temp2)#problematicno
        elif elem[0]=="K":#Forma["K",[plus,minus],[plus,minus],[L1,L2,L12],[pocetan uslov1,pocetan uslov2],[sympy.Symbol_I1,sympy.Symbol_I2]]
            l1 = sympy.Symbol(elem[3][0])
            l2 = sympy.Symbol(elem[3][1])
            l12 = sympy.Symbol(elem[3][2])
            if elem[4][0] == None:
                pu1 = 0
            else:
                pu1 = sympy.Symbol(elem[4][0])
            if elem[4][1] == None:
                pu2 = 0
            else:
                pu2 = sympy.Symbol(elem[4][1])
            
            s=sympy.Symbol("s")
            #temp=sympy.Symbol("Ik"+count)
            temp=sympy.Symbol(elem[5][0])
            #count=count+1
            #temp2=Symobol("Ik"+count)
            temp2=sympy.Symbol(elem[5][1])
            #count=count+1
            exp1.append(temp)
            exp1.append(temp2)
            #Levi Par Pristupa
            if elem[1][0] !=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
            if elem[1][1] !=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
            #Desni Par Pristupa
            if elem[2][0] !=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp2
                else:
                    eq1[elem[2][0]-1]+=temp2
            if elem[2][1] !=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp2
                else:
                    eq1[elem[2][1]-1]-=temp2
            #dodavanje jednacina
            if elem[1][0]!=0:
                if elem[1][1]!=0:
                    temp3 = exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp3 = exp1[elem[1][0]-1]
            elif elem[1][1]!=0:
                temp3 = -exp1[elem[1][1]-1]
            temp4=l1*s*temp-l1*pu1+l12*s*temp2-l12*pu2
            eq1.append(temp3-temp4)#problematicno
            ###########################
            if elem[2][0]!=0:
                if elem[2][1]!=0:
                    temp3 = exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp3 = exp1[elem[2][0]-1]
            elif elem[2][1]!=0:
                temp3 = -exp1[elem[2][1]-1]
            temp4=l12*s*temp-l12*pu1+l2*s*temp2-l2*pu2
            eq1.append(temp3-temp4)#problematicno
        elif elem[0]=="Z":#NOVO#Forma["Z",plusTerm,minusTerm,"impedanca"]
            tempic = sympy.Symbol(elem[3])
            #Pravljenje jednacine za ubacivanje
            if elem[1]!=0:
                if elem[2]!=0:
                    temp = exp1[elem[1]-1] - exp1[elem[2]-1]
                else:
                    temp = exp1[elem[1]-1]
            elif elem[2]!=0:
                temp = -exp1[elem[2]-1]
            temp=temp/tempic
            #Ubacivanje u jenacine cvorova
            if elem[1]!=0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=temp
                else:
                    eq1[elem[1]-1]+=temp
            if elem[2]!=0:
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=-temp
                else:
                    eq1[elem[2]-1]-=temp
        elif elem[0]=="Y":#Forma ["Y",plusTerm,minusTerm,"admittanca"]
            tempic = sympy.Symbol(elem[3])
            #Pravljenje jednacine za ubacivanje
            if elem[1]!=0:
                if elem[2]!=0:
                    temp = exp1[elem[1]-1] - exp1[elem[2]-1]
                else:
                    temp = exp1[elem[1]-1]
            elif elem[2]!=0:
                temp = -exp1[elem[2]-1]
            temp=temp*tempic
            #Ubacivanje u jenacine cvorova
            if elem[1]!=0:
                if not eq1[elem[1]-1]:
                    eq1[elem[1]-1]=temp
                else:
                    eq1[elem[1]-1]+=temp
            if elem[2]!=0:
                if not eq1[elem[2]-1]:
                    eq1[elem[2]-1]=-temp
                else:
                    eq1[elem[2]-1]-=temp
        elif elem[0]=="T" and not Phasor:#Forma ["T",[plusSending,minusSending],[plusReceiving,minusReceiving],[sympy.SymbolI1,sympy.SymbolI2],[Zc,tau]]
            #Pravljenje Promenjivih
            #temp - I sending
            #temp2 - I receiving
            #temp3 - U sending
            #temp4 - U receiving
            #temp5 - temporary expression
            temp = sympy.Symbol(elem[3][0])
            temp2 = sympy.Symbol(elem[3][1])
            s = sympy.Symbol("s")
            #Dodavanje struje u jednacine cvorova
            #Sending
            if elem[1][0]!=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
            if elem[1][1]!=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
            #Receiving
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=temp2
                else:
                    eq1[elem[2][0]-1]+=temp2
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=-temp2
                else:
                    eq1[elem[2][1]-1]-=temp2
            #Dodavanje novih Jednacina
            #pravljenje leve strane za sending
            if elem[1][0]!=0:
                if elem[1][1]!=0:
                    temp3=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp3=exp1[elem[1][0]-1]
            elif elem[1][1]!=0:
                temp3=-exp1[elem[1][0]-1]
            #pravljenje leve strane za receiving
            if elem[2][0]!=0:
                if elem[2][1]!=0:
                    temp4=exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp4=exp1[elem[2][0]-1]
            elif elem[2][1]!=0:
                temp4=-exp1[elem[2][0]-1]
            
            #Ubacivanje jenacina
            temp5=sympy.Symbol(elem[4][0])*temp+sympy.Symbol(elem[4][0])*temp2*sympy.exp(-1*sympy.Symbol(elem[4][1])*s)+temp4*sympy.exp(-1*sympy.Symbol(elem[4][1])*s)
            eq1.append(temp3-temp5)#problematicno
            #Druga jednacina
            temp5=sympy.Symbol(elem[4][0])*temp2+sympy.Symbol(elem[4][0])*temp*sympy.exp(-1*sympy.Symbol(elem[4][1])*s)+temp3*sympy.exp(-1*sympy.Symbol(elem[4][1])*s)
            eq1.append(temp4-temp5)
            #Ubacivanje promenjivih
            exp1.append(temp)
            exp1.append(temp2)
        elif elem[0]=="T" and Phasor:#Forma ["T",[plusSending,minusSending],[plusReceiving,minusReceiving],[sympy.SymbolI1,sympy.SymbolI2],[Zc,tau]]
            #Pravljenje promenjivih
            #temp - I sending
            #temp2 - I receiving
            #temp3 - U sending
            #temp4 - U receiving
            #temp5 - temporary expression
            temp = sympy.Symbol(elem[3][0])
            temp2 = sympy.Symbol(elem[3][1])
            i = sympy.Symbol("i")
            #Dodavanje struje u jednacine cvorova#isto kao i bez Fazora
            #Sending
            if elem[1][0]!=0:
                if not eq1[elem[1][0]-1]:
                    eq1[elem[1][0]-1]=temp
                else:
                    eq1[elem[1][0]-1]+=temp
            if elem[1][1]!=0:
                if not eq1[elem[1][1]-1]:
                    eq1[elem[1][1]-1]=-temp
                else:
                    eq1[elem[1][1]-1]-=temp
            #Receiving
            if elem[2][0]!=0:
                if not eq1[elem[2][0]-1]:
                    eq1[elem[2][0]-1]=-temp2
                else:
                    eq1[elem[2][0]-1]-=temp2
            if elem[2][1]!=0:
                if not eq1[elem[2][1]-1]:
                    eq1[elem[2][1]-1]=temp2
                else:
                    eq1[elem[2][1]-1]+=temp2
            
            #Dodavanje novih Jednacina
            #pravljenje leve strane za sending#isto kao i bez Fazora
            if elem[1][0]!=0:
                if elem[1][1]!=0:
                    temp3=exp1[elem[1][0]-1]-exp1[elem[1][1]-1]
                else:
                    temp3=exp1[elem[1][0]-1]
            elif elem[1][1]!=0:
                temp3=-exp1[elem[1][0]-1]
            #pravljenje leve strane za receiving#isto kao i bez Fazora
            if elem[2][0]!=0:
                if elem[2][1]!=0:
                    temp4=exp1[elem[2][0]-1]-exp1[elem[2][1]-1]
                else:
                    temp4=exp1[elem[2][0]-1]
            elif elem[2][1]!=0:
                temp4=-exp1[elem[2][0]-1]
                
            #Ubacivanje jednacina
            temp5=sympy.cos(sympy.Symbol(elem[4][1]))*temp4+i*sympy.Symbol(elem[4][0])*sympy.sin(sympy.Symbol(elem[4][1]))*temp2
            eq1.append(temp3-temp5)#problematicno
            temp5=i*(1/sympy.Symbol(elem[4][0]))*sympy.sin(sympy.Symbol(elem[4][1]))*temp4+sympy.cos(sympy.Symbol(elem[4][1]))*temp2
            eq1.append(temp-temp5)
            #Dodavanje promenjivih
            exp1.append(temp)
            exp1.append(temp2)
            
            
    temp = sympy.nonlinsolve(eq1,exp1)
    print(eq1)
    
    if not temp:
        print("No solution")
        return temp
    
    pr = '{}'.format(list(temp)[0])
    pr = pr[1:-1]
    for itr, vr in enumerate(pr.split(', ')):
        print('{l} = {r}'.format(l=exp1[itr],r=vr))

    if LatexOutput==True:    
        s = '{}'.format(sympy.latex(list(temp)[0]))
        s = s[6:-7] 
        x = s.split(', ')


        plt.gcf().canvas.set_window_title('Results')
        ax = plt.axes([0,0.85,0.05,0.05]) #left,bottom,width,height 
        ax.set_xticks([]) 
        ax.set_yticks([]) 
        ax.axis('off') 
        plt.plot()

        for i,val in enumerate(x):
            s1 = '{l} = {r}'.format(l=sympy.latex(exp1[i]),r=val)    
            plt.text(0.1,-0.4*i, '${}$'.format(s1), size=20, ha='left') 

        
        axs = plt.axes([0.9,0.05,0.03,0.9]) #left,bottom,width,height 

        sliderMax = 0
        if len(x) > 5:
            sliderMax = len(x)
        else:
            sliderMax = 5
        
        sl = Slider(axs, '', 5, sliderMax, valinit=sliderMax,
                    facecolor='w', edgecolor='black', orientation='vertical')
        sl.valtext.set_visible(False)
        
        def update(val):
            pos = [0, 0.85 - (val - sliderMax)*0.20, 0.05,0.05]
            ax.set_position(pos)
            
        sl.on_changed(update)
        plt.show()
