import random
temp2 = 0
while temp2 == 0:
    print("\nEnter 1 to Encode\nEnter 2 to Decode\nEnter 3 to Exit")
    condition = int(input("\nPlease make a choice:"))
    Efinal = []  
    match condition:
        # Encoder
        case 1:
            print("\nEnter 1 to Encode a text file\nEnter 2 to Encode a sentence")
            UserWish = int(input("Please make a choice:"))
            if(UserWish == 1):
              A = input("\nEnter the file location:")
              with open(A) as f:
                  UserInput = f.read()
            elif(UserWish == 2):
                UserInput = input("\nEnter the String:")
            words = UserInput.split(" ")
            for SingWord in words:
                range1 = list(range(65,91)) + list(range(97,123))
                w1 = chr(random.choice(range1))
                w2 = chr(random.choice(range1))
                w3 = chr(random.choice(range1))
                w4 = chr(random.choice(range1))
                if (len(SingWord)>=3):
                    ENewWord = w1 + w3 + SingWord[2:len(SingWord)] + SingWord[1] + SingWord[0] + w2 + w4
                else:
                    ENewWord = w3 + w4 + SingWord[::-1] + w1 + w2    
                Efinal.append(ENewWord)
            EFinalString = " ".join(Efinal)
            if(UserWish == 1):
                with open(A, "w") as f:
                    f.write(EFinalString)
                print("\nFile Encoaded SUCCESSFULLY!!!")
            elif(UserWish == 2):                            
                print(f"\nThe Encoaded STRING :-\n{EFinalString}")
       #Decoder
        case 2:
            print("\nEnter 1 to Decode a text file\nEnter 2 to Decode a sentence")
            UserWish = int(input("Please make a choice:"))
            if(UserWish == 1):
              A = input("\nEnter the file location:")
              with open(A) as f:
                  UserInput = f.read()
            elif(UserWish == 2):
                UserInput = input("\nEnter the String:")
            words = UserInput.split(" ")
            temp = 0
            DFinal = []
            DWord = UserInput.split(" ")
            for SingWord in DWord:
                if (len(SingWord) > 7):
                    DNewWord = ""+""+ SingWord[len(SingWord)-3] + SingWord[len(SingWord)-4] + SingWord[2:len(SingWord) -4] + "" + ""
                else :
                    DNewWord = "" + "" + SingWord[2:len(SingWord)-2] + "" + ""
                    DNewWord = DNewWord[::-1]
                DFinal.append(DNewWord)
            DFinalString = " ".join(DFinal)
            if(UserWish == 1):
                with open(A, "w") as f:
                    f.write(DFinalString)
                print("\nFile Decoaded SUCCESSFULLY!!!")
            elif(UserWish == 2):                            
                print(f"\nThe Encoaded STRING :-\n{DFinalString}")
        
        case 3:
            temp2 == 1
            break
    