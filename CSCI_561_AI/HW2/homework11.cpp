#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
#include <limits>
#include <math.h>

using namespace std;

const clock_t BEGIN = clock();

struct Move{
	int col;
	int row;
	int score;
	vector<vector<int> > board;
};

Move maxMove(int n, Move * move, int alpha, int beta, int depth, int depth_limit);
Move minMove(int n, Move * move, int alpha, int beta, int depth, int depth_limit);
void printBoard(int n, vector<vector<int> > board); 
void createOutput(int n, Move * move, vector<vector<int> > *board_ptr); 
vector<vector<int> > gravity(vector<vector<int> > *board_ptr);
bool emptyBoard(vector<vector<int> > *board_ptr);
void playGame(int n,  vector<vector<int> > *board_ptr, int depth_limit);
Move calcScore(Move * move, int n);
Move checkHoriz(Move * move, int n, int value, int score);
Move checkVert(Move * move, int n, int value, int score);
int determineDepth(int n, int num_fruits, double time,int num_stars);

int main(){
	// opening intput.txt file for reading 
	ifstream inputFile;
	inputFile.open("input.txt");

	//declaring input.txt variables
	int n, num_fruits, counter = 0, num_stars = 0;
	double time;
	string line;
	vector<vector<int> > board;

	//reading file now and storing them in proper variables 
	while(inputFile >> line){
		if(counter == 0)
			n = stoi(line); //dimension
		else if(counter == 1)
			num_fruits = stoi(line); //number of fruit types
		else if(counter == 2)
			time = stod(line); //remaining time in seconds
		else{
			//storing board into 2d vector
			vector<int> row;
			for(int i = 0; i < line.size(); i++){
				if(line[i] == '*'){
					row.push_back(-1);
					num_stars += 1;
				}
				else{
					int temp = int(line[i]) - 48;
					row.push_back(temp);
				}
			}
			board.push_back(row);
		}
		counter += 1;
	}
	inputFile.close();

	int depth_limit = determineDepth(n, num_fruits, time, num_stars);
	playGame(n, &board, depth_limit);
	clock_t end = clock();
	double elapsed_time = double(end - BEGIN) / CLOCKS_PER_SEC;
	cout << "Time(seconds): " << elapsed_time << endl;
}

//helper function to print the board
void printBoard(int n, vector<vector<int> > board){
	for(int i = 0; i < n; i ++){
		for(int j = 0; j < n; j++){
			if(board[i][j] == -1){
				cout << "*";
			}
			else{
				cout << board[i][j];
			}
		}
		cout << endl;
	}
	cout << "-------------------" << endl;
}

//function to create output.txt file
void createOutput(int n, Move * move, vector<vector<int> > *board_ptr){
	vector<vector<int> > board = *board_ptr;
	ofstream outputFile;
	outputFile.open("output.txt");
	outputFile << (char)(move->col + 65) <<  move->row+1 << endl;
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			if(board[i][j] == -1){
				outputFile << "*";
			}
			else{
				outputFile << board[i][j];
			}
		}
		outputFile << endl;
	}
	outputFile.close();
	return;
}

//function to rearange fruits after a move 
vector<vector<int> > gravity(vector<vector<int> > *board_ptr){
	vector<vector<int> > board = *board_ptr;
	int n = board.size();

	for(int j = 0; j < n; j++){
		vector<int> temp_col;
		vector<int> stars;
		for(int i = 0; i < n; i++){
			if(board[i][j] != -1){
				temp_col.push_back(board[i][j]); //store numbers into a vector
			}
			else{
				stars.push_back(-1); //store stars into a vector 
			}
		}
		stars.insert(stars.end(), temp_col.begin(), temp_col.end()); //combine the vectors with stars in front
		for(int k = 0; k < n; k++){
			board[k][j] = stars[k]; //replace the column with the new vector values 
		}
	}
	return board;
}

//function to check if board is empty
bool emptyBoard(vector<vector<int> > *board_ptr){
	vector<vector<int> > board = *board_ptr;
	for(int i = 0; i < board.size(); i++){
		for(int j = 0; j < board.size(); j++){
			if(board[i][j] != -1){
				return false;
			}
		}
	}
	return true;
}

int determineDepth(int n, int num_fruits, double time, int num_stars){
	if(time <= 1){ //less than 1 second left 
		return 1;
	}
	if(time <= 5){ // less than 5 seconds 
		return 1;
	}
	if(time <= 10){ // less than 10 seconds 
		return 2;
	}
	if(time <= 30){ // less than 30 seconds
		if(n <= 10){
			return 4;
		} 
		if(n <= 15){ //less than board size 15
			return 3;
		}
		if(n <= 20){ //less than board size 20 
			return 2; 
		}
		if(n <= 26){ //less than board size 26 
			return 2;
		}
	}
	if(time <= 200){ //less than 200 seconds 
		if(n <= 10){
			return 10;
		}
		if(n <= 15){ //less than board size 15
			return 8;
		}
		if(n <= 20){ //less than board size 20 
			return 5; 
		}
		if(n <= 26){ //less than board size 26 
			return 4;
		}
	}
	if(time <= 300){ //first play of the game -- <= 300 seconds
		if(n <= 10){
			if(num_fruits <= 2){
				return 8;
			}
			return 12;
		}
		if(n <= 15){ //less than board size 15
			if(num_fruits <= 2){
				return 6;
			}
			return 10;
		}
		if(n <= 20){ //less than board size 20 
			if(num_fruits <= 2){
				return 6;
			}
			return 7; 
		}
		if(n <= 30){ //less than board size 26 
			if(num_fruits <= 2){
				return 6;
			}
			return 5;
		}
	}
	return 1;
}
//function to play the game. implements alpha-beta pruning
void playGame(int n,  vector<vector<int> > *board_ptr, int depth_limit){
	//setting up variables to send to maxMove function
	vector<vector<int> > board = *board_ptr;
	int bestScore = 0, alpha = -std::numeric_limits<int>::max(), beta = std::numeric_limits<int>::max();
	Move *tempMove = new Move;
	tempMove->board = board;
	tempMove->score = 0;
	//calling the maxMove function to calculate the best move to pick 
	Move bestMove = maxMove(n, tempMove, alpha, beta, 0, depth_limit);

	//readjust board to reflect max move
	bestMove.board = board;
	bestMove = calcScore(&bestMove, n);
	bestMove.board = gravity(&(bestMove.board));

	// printBoard(n, bestMove.board);
	// cout << "Score: " << bestMove.score << " Moves:" << bestMove.row << " " << bestMove.col << endl;
	createOutput(n, &bestMove, &(bestMove.board));
	delete tempMove;
	return;
}

Move maxMove(int n, Move * move, int alpha, int beta, int depth, int depth_limit){
	vector<vector<int> > board = move ->board;
	//return if empty board or depth limit reached
	if(emptyBoard(&board) || depth > depth_limit){
		return *move;
	}
	Move bestMove = *move;
	// bestMove.score = 0;
	for(int i = n-1; i >=0; i--){
		for(int j = n-1; j>=0; j--){
			if(board[i][j] != -1){ //if valid move then take it 
				move -> row = i;
				move -> col = j;
				move -> board = board;
				*(move) = calcScore(move, n); //calculate score of current move decision
				move->board = gravity(&(move->board)); //gravity function for the fruits based on decision
				Move curMove = minMove(n, move, alpha, beta, depth, depth_limit); 

				//keeping max move
				if(curMove.score > bestMove.score){ 
					bestMove = curMove;
					beta = bestMove.score;
				}
				//alpha beta pruning
				if(alpha >= beta){
					return bestMove;
				}
			}
			depth += 1;
		}
	}
	return bestMove;
}

Move minMove(int n, Move * move, int alpha, int beta, int depth, int depth_limit){
	vector<vector<int> > board = move ->board;
	//return if empty board or depth limit reached
	if(emptyBoard(&board) || depth > depth_limit){
		return *move;
	}
	Move bestMove = * move;
	bestMove.score = std::numeric_limits<int>::max();
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			if(board[i][j] != -1){ //if valid move then take it
				move -> row = i;
				move -> col = j;
				move -> board = board;
				*(move) = calcScore(move, n); //calculate score of current move decision
				move->board = gravity(&(move->board)); //gravity function for the fruits based on decision
				Move curMove = maxMove(n, move, alpha, beta, depth, depth_limit);
				//keeping min move 
				if(curMove.score < bestMove.score){
					bestMove = curMove;
					alpha = bestMove.score;
				}

				//alpha beta pruning
				if(beta <= alpha){
					return bestMove;
				}
			}
			depth += 1;
		}
	}
	return bestMove;
}

//calculate score given move and board
//changes values to -1 to signify "*"
Move calcScore(Move *move, int n){
	// cout << "Calculating score " << move -> row << " " << move -> col << endl;
	Move curMove = *move;
	vector<vector<int> >  board = curMove.board;
	int score = 1, value = board[curMove.row][curMove.col];
	curMove.board[move->row][move->col] = -1;

	curMove = checkHoriz(&curMove, n, value, score);
	curMove.row = move->row;
	curMove.col = move->col;
	curMove = checkVert(&curMove, n, value, curMove.score);
	curMove.row = move->row;
	curMove.col = move->col;

	curMove.score = pow(curMove.score, 2);
	// cout << "Calculating score " << move -> row << " " << move -> col << " " << curMove.score << endl;
	return curMove;
}

// check horizontally left and right to add up scores. (next column and previous column but same row)
Move checkHoriz(Move * move, int n, int value, int score){
	Move curMove = *move;
	vector<vector<int> > board = curMove.board;
	int row = curMove.row, col = curMove.col;

	//check right side
	for(int j = col+1; j < n; j++){
		if(board[row][j] == value){
			score += 1;
			board[row][j] = -1;
			//check down/up to see if matching value exists
			if((row + 1 < n && board[row+1][j] == value) || (row -1 >= 0 && board[row-1][j] == value)){
				Move tempMove;
				tempMove.row = row;
				tempMove.col = j;
				tempMove.score = score;
				tempMove.board = board;
				curMove = checkVert(&tempMove, n, value, tempMove.score);
				score = curMove.score;
				board = curMove.board;
			}
		}
		else{
			break;
		}
	}

	//check left side 
	for(int j = col - 1; j >= 0; j--){
		if(board[row][j] == value){
			score += 1;
			board[row][j] = -1;
			//check down/up to see if matching value exists
			if((row + 1 < n && board[row+1][j] == value) || (row -1 >= 0 && board[row-1][j] == value)){
				Move tempMove;
				tempMove.row = row;
				tempMove.col = j;
				tempMove.score = score;
				tempMove.board = board;
				curMove = checkVert(&tempMove, n, value, tempMove.score);
				score = curMove.score;
				board = curMove.board;
			}
		}
		else{
			break;
		}
	}
	curMove.board = board;
	curMove.score = score;
	return curMove;
}

//check vertically up and down to add up scores (next row and previous row but same column)
Move checkVert(Move * move, int n, int value, int score){
	Move curMove = *move;
	vector<vector<int> > board = curMove.board;
	int row = curMove.row, col = curMove.col;

	//check down
	for(int i = row+1; i < n; i++){
		if(board[i][col] == value){
			score += 1;
			board[i][col] = -1;
			//check right/left if value matches
			if((col + 1 < n && board[i][col+1] == value) || (col-1 >= 0 && board[i][col-1] == value)){
				Move tempMove;
				tempMove.row = i;
				tempMove.col = col;
				tempMove.score = score;
				tempMove.board = board;
				curMove = checkHoriz(&tempMove, n, value, tempMove.score);
				score = curMove.score;
				board = curMove.board;
			}
		}
		else{
			break;
		}
	}

	//check up
	for(int i = row - 1; i >= 0; i--){
		if(board[i][col] == value){
			score += 1;
			board[i][col] = -1;
			//check right/left to see if matching value exists
			if((col+ 1 < n && board[i][col+1] == value) || (col - 1 >= 0 && board[i][col-1] == value)){
				Move tempMove;
				tempMove.row = i;
				tempMove.col = col;
				tempMove.score = score;
				tempMove.board = board;
				curMove = checkHoriz(&tempMove, n, value, tempMove.score);
				score = curMove.score;
				board = curMove.board;
			}
		}
		else{
			break;
		}
	}
	curMove.board = board;
	curMove.score = score;
	return curMove;
}














