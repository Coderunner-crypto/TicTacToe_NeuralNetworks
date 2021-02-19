import numpy as np

from Train import TicTacToeModel


class TicTac:
    def __init__(self,matrix=np.zeros((3,3)),turn="Circle",winner=None):
        self.matrix=matrix
        self.turn=turn
        self.winner=winner

    def move(self,x,y):
        if self.turn=="Circle":
            if(self.game_continue()):
                if self.matrix[x][y]==0:
                    self.matrix[x][y]=1
                    self.turn="Cross"
                    self.winner=self.is_winner()
                    
                else:
                    print("Error")
            else:
                print("Game Ended")
        else:
            if(self.game_continue()):
                if self.matrix[x][y]==0:
                    self.matrix[x][y]=-1
                    self.turn="Circle"
                    self.winner=self.is_winner()
                    
                else:
                    print("Error")
            else:
                print("Game Ended")
            
    def game_continue(self):
        if(self.winner==None):
            for i in range(0,3):
                for j in range(0,3):
                    if self.matrix[i][j]==0:
                        return True
            self.winner="Draw"
            return False
        else:
            return False
    def is_winner(self):
        if self.turn=="Cross":
            row_sum=self.matrix.sum(axis=1)
            col_sum=self.matrix.sum(axis=0)
            for i in range(0,3):
                if(row_sum[i]==3 or col_sum[i]==3):
                    return "Circle"
            diagonal=0
            cross_diagonal=0
            for i in range(0,3):
                diagonal=diagonal+self.matrix[2-i][i]
                cross_diagonal=cross_diagonal+self.matrix[i][i]
            if(cross_diagonal==3 or diagonal==3):
                return "Circle"
                
        else:
            row_sum=self.matrix.sum(axis=1)
            col_sum=self.matrix.sum(axis=0)
            for i in range(0,3):
                if(row_sum[i]==-3 or col_sum[i]==-3):
                    return "Cross"
            diagonal=0
            cross_diagonal=0
            for i in range(0,3):
                diagonal=diagonal+self.matrix[2-i][i]
                cross_diagonal=cross_diagonal+self.matrix[i][i]
            if(cross_diagonal==-3 or diagonal==-3):
                return "Cross"
    def print_board(self):
        board=[["","",""]for i in range(0,3)]
        for i in range(0,3): 
            for j in range(0,3):
                if self.matrix[i][j]==0:
                    board[i][j]="_"
                elif self.matrix[i][j]==1:
                    board[i][j]="O"
                else:
                    board[i][j]="X"
        print('   |   |')
        print(' ' + board[0][0] + ' | ' + board[0][1] + ' | ' + board[0][2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1][0] + ' | ' + board[1][1] + ' | ' + board[1][2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[2][0] + ' | ' + board[2][1] + ' | ' + board[2][2])
        print('   |   |')
    def new(self):
        self.winner=None
        self.matrix=np.zeros((3,3))
        self.turn="Circle"
    def simulate_neural(self,player,model):
        if player=="Circle":
            board = np.copy(self.matrix)
            board1=np.copy(self.matrix)
            b=board.reshape((1,9))
            valid_index=[]
            for i in range(0,9):
                if b[0][i]==0:
                    valid_index.append(i)
            best_move=[]
    
            best_value=0
            for i in valid_index:
                board1=np.copy(self.matrix)
                board1[i//3][i%3]=1
                value=model.predict(board1,0)

                valueO=model.predict(board1,1)
                valueX=model.predict(board1,-1)
                print("X: ",valueX ,"Draw ",value,"O: ",valueO)
                if valueO==0:
                    valueO=0.0000001

                if valueO/(valueO+valueX)>=best_value:
                    best_value=valueO/(valueO+valueX)
                    
                    best_move=[i//3,i%3]
            return best_move
        else:
            board = np.copy(self.matrix)
            board1=np.copy(self.matrix)
            b=board.reshape((1,9))
            valid_index=[]
            for i in range(0,9):
                if b[0][i]==0:
                    valid_index.append(i)
            best_move=[]
    
            best_value=0
            for i in valid_index:
                board1=np.copy(self.matrix)
                board1[i//3][i%3]=-1
                value=model.predict(board1,0)

                valueO=model.predict(board1,1)
                valueX=model.predict(board1,-1)
                print("X: ",valueX ,"Draw ",value,"O: ",valueO)
                if valueX==0:
                    valueX=0.0000001
                if value==0:
                    value=0.0000001
                if max(valueX/(valueO+valueX),value/(valueO+value))>=best_value:
                    best_value=max(valueX/(valueO+valueX),value/(valueO+value))
                    
                    best_move=[i//3,i%3]
            return best_move
            
        
def simulate(Tic):
    A=np.random.permutation(9)
    Moves=[]
    data=[]
    for i in A:
        if Tic.winner==None:
            Tic.move(i//3,i%3)
            S=np.copy(Tic.matrix)
            Moves.append(S)
    if Tic.winner=="Circle":
        for i in range(len(Moves)):
            data.append((1,Moves[i]))
    elif Tic.winner=="Cross":
        for i in Moves:
            data.append((-1,i))
    else:
        for i in Moves:
            data.append((0,i))
    return data
Tic=TicTac()
data=[]
for i in range(0,10000):
    d=simulate(Tic)
    for j in range(0,len(d)):
        data.append(d[j])
    Tic.new()

for i in range(0,2100):
    if data[i][0]==1:
        data.pop(i)
        
        

np.save('data.npy',data)
    


data =np.load('data.npy',allow_pickle=True)
Tic=TicTac()
Tic.new()
ticTacToeModel = TicTacToeModel(9, 3, 100, 32)
ticTacToeModel.train(data)

while Tic.winner==None:
    if Tic.turn=="Cross":
        move=Tic.simulate_neural("Cross",ticTacToeModel)
        Tic.move(move[0],move[1])
        Tic.print_board()
        
    else:
        x=[int(x) for x in input().split(",")]
        Tic.move(x[0],x[1])
        Tic.print_board()
print("Winner : "+Tic.winner)

        
    
    


    
                
            
                
            
            
            

                
            
        
        
    
            
            
    