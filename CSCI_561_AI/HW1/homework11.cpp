#include <iostream>
#include <fstream>
#include <stack>
#include <queue>
#include <ctime>
#include <string>
#include <vector> 
#include <stdlib.h>
#include <stdio.h>
#include <time.h> 
#include <math.h>

using namespace std;
const clock_t BEGIN = clock();

struct Node{
	vector<vector<int> > current; //2d vector for the matrix 
	signed long int lizards; // number of lizards 
	signed long int row; //row to be checked at the next iteration
};

// this function creates the output for output.txt
void createOutput(bool success, vector<vector<int> > *nursery){
	ofstream outputFile;
	outputFile.open("output.txt");
	if(success){
		vector<vector<int> > new_nursery = *nursery;
		outputFile << "OK" << endl;
		for(signed long int i = 0; i < new_nursery.size(); i++){
			for(signed long int j = 0; j < new_nursery.size(); j++){
				if(new_nursery[i][j] == 3){
					outputFile << 0;
				}
				else{
					outputFile << new_nursery[i][j];
				}
			}
			outputFile << endl;
		}
	}
	else{
		outputFile << "FAIL" << endl;
	}
	outputFile.close();
	return;
}

//helper function to print nursery
void printNursery(int n, vector<vector<int> > nursery){
	for(signed long int i = 0; i < n; i ++){
		for(signed long int j = 0; j < n; j++){
			if(nursery[i][j] == 3){
				cout << "0";
			}
			else{
				cout << nursery[i][j];
			}
		}
		cout << endl;
	}
	cout << "-------------------" << endl;
}

// function for making invalid spaces in the nursery. invalid spaces are the attack ranges of the lizard
// the number 3 signify the spot invalid because of the lizard placement
// x and y is the position where the lizard will be placed
vector<vector<int> > makeInvalid(signed long int x, signed long int y, signed long int n, vector<vector<int> > *nursery){
	long long int x_2 = x, y_2 = y;
	vector<vector<int > > new_nursery = * nursery;
	//filling in vertically and horizontally across
	while(true){
		if(new_nursery[x_2][y] == 2){
			break;
		}
		new_nursery[x_2][y] = 3; 
		x_2+=1;
		if(x_2 >= n){
			break;
		}
	}
	x_2 = x;
	while(true){
		if(new_nursery[x_2][y] == 2){
			break;
		}
		new_nursery[x_2][y] = 3;
		x_2-=1;
		if(x_2 < 0){
			break;
		}
	}
	y_2 = y;
	while(true){
		if(new_nursery[x][y_2] == 2){
			break;
		}
		new_nursery[x][y_2] = 3;
		y_2+=1;
		if(y_2 >= n){
			break;
		}
	}
	y_2 = y;

	while(true){
		if(new_nursery[x][y_2] == 2){
			break;
		}
		new_nursery[x][y_2] = 3;
		y_2-=1;
		if(y_2 < 0){
			break;
		}
	}
	y_2 = y;
	x_2 = x;

	//filling in upper right diagonal
	while(x_2+1 < n && y_2+1 < n){
		if(new_nursery[x_2+1][y_2+1] == 2){
			break;
		}
		new_nursery[x_2+1][y_2+1] = 3;
		x_2+=1;
		y_2+=1;
	}

	//filling in lower left diagonal
	x_2 = x, y_2 = y;
	while(x_2-1 >= 0 && y_2-1 >= 0){
		if(new_nursery[x_2-1][y_2-1] == 2){
			break;
		}
		new_nursery[x_2-1][y_2-1] = 3;
		x_2 -= 1;
		y_2 -= 1;
	}

	//filling in left upper diagonal 
	x_2 = x, y_2 = y;
	while(x_2-1 >= 0 && y_2+1 <n){
		if(new_nursery[x_2-1][y_2+1] == 2){
			break;
		}
		new_nursery[x_2-1][y_2+1] = 3;
		x_2 -= 1;
		y_2 += 1;
	}

	//filling in right lower diagonal 
	x_2 = x, y_2 = y;
	while(x_2+1 < n && y_2-1 >= 0){
		if(new_nursery[x_2+1][y_2-1] == 2){
			break;
		}
		new_nursery[x_2+1][y_2-1] = 3;
		x_2 += 1;
		y_2 -= 1;
	}

	new_nursery[x][y] = 1;
	// printNursery(n, nursery);
	return new_nursery;
}

//helper function to check if the row contains any free spaces 
bool checkSpots(vector<int> row){
	for(signed long int i = 0; i < row.size(); i ++){
		if(row[i] == 0){
			return true;
		}
	}
	return false;
}

void runBFS(signed long int n, signed long int p, vector<vector<int> > *nursery){
	queue<Node> myQueue; //FIFO

	//creating initial node to push onto queue. inital node is the input nursery
	Node *myNode = new Node;
	myNode -> current = *nursery;
	myNode -> lizards = p;
	myNode -> row = 0;
	myQueue.push(*myNode);

	//implementing bfs algorithm here
	while(!myQueue.empty()){
		for(signed long int i = 0; i < n; i++){
			if(myQueue.empty())
				break;
			//grab the front node and pop it 
			Node curNode = myQueue.front();
			myQueue.pop();
			// printNursery(n, curNode.current);
			for(signed long int j = 0; j < n; j++){
				//checking to see if there is a spot to put a lizard in the current row 
				if(curNode.current[curNode.row][j] == 0){
					//check if this is the final lizard to placed. returns if it is 
					if(curNode.lizards - 1 == 0){
						// cout << "OK" << endl;
						curNode.current[curNode.row][j] = 1;
						// printNursery(n, curNode.current);
						createOutput(true, &curNode.current);
						return;
					}
					//creates new node to be pushed onto the queue
					Node *newNode = new Node;
					vector<vector<int> > temp_nursery = curNode.current;
					temp_nursery = makeInvalid(curNode.row, j, n, &temp_nursery);
					newNode -> current = temp_nursery;
					newNode -> lizards = curNode.lizards - 1;

					//checking if there are still any other valid spots in the current row
					if(checkSpots(temp_nursery[curNode.row])){
						newNode -> row = curNode.row;
					}
					else{
						if(curNode.row + 1 < n){ //boundary check
							newNode -> row = curNode.row + 1;
						}
						else{
							newNode -> row = curNode.row;
						}
					}
					myQueue.push(*newNode);
				}
			}
			if(curNode.row + 1 < n && myQueue.empty()){
				curNode.row += 1; 
				myQueue.push(curNode);
			}
		}
	}
	// cout << "FAIL" << endl;
	createOutput(false, NULL);
}

void runDFS(signed long int n,signed long int p, vector<vector<int> > *nursery){
	stack<Node> myStack; //LIFO
	//creating initial node to push onto stack. inital node is the input nursery
	Node *myNode = new Node;
	myNode -> current = *nursery;
	myNode -> lizards = p;
	myNode -> row = 0;

	myStack.push(*myNode);
	signed long int counter = 0;
	Node curNode;
	//implementing dfs algorithm here
	while(!myStack.empty()){
		for(signed long int i = 0; i < n; i++){
			if(myStack.empty())
				break;

			//grab top node and then pop it 
			curNode = myStack.top();
			myStack.pop();
			for(signed long int j = 0; j < n; j++){
				if(curNode.current[curNode.row][j] == 0){
					//checking if this spot fills up the nursery with the needed lizards 
					if(curNode.lizards - 1 == 0){
						// cout << "OK" << endl;
						curNode.current[curNode.row][j] = 1;
						createOutput(true, &curNode.current);
						// printNursery(n, curNode.current);
						return;
					}
					//creates new node to be pushed onto the stack 
					Node *newNode = new Node;
					vector<vector<int> > temp_nursery = curNode.current;
					temp_nursery = makeInvalid(curNode.row, j, n, &temp_nursery);
					newNode -> current = temp_nursery;
					newNode -> lizards = curNode.lizards - 1;
					//checking if there are still any extra valid spots in the current row
					if(checkSpots(temp_nursery[curNode.row]))
						newNode -> row = curNode.row;
					else{
						if(curNode.row + 1 < n) //boundary check
							newNode -> row = curNode.row + 1;
						else
							newNode -> row = curNode.row;
					}
					myStack.push(*newNode);
				}
			}
			if(curNode.row + 1 < n && myStack.empty()){
				curNode.row += 1; 
				myStack.push(curNode);
			}
		}
		if(curNode.row + 1 < n && checkSpots(curNode.current[curNode.row+1])){
			curNode.row += 1;
			myStack.push(curNode);
		}
	}
	// cout << "FAIL" << endl;
	createOutput(false, NULL);
}

//helper function for simmulated annealing jumps
bool yes(double prob){
	double r = ((double) rand() / (RAND_MAX));
	if(r < prob)
		return true;
	return false;
}

// -----------------------Functions beyond here are created for simulated annealing-------------------

//helper function to count conflicts of lizard at position x and y given nursery
int countCurConflicts(signed long int x, signed long int y, vector<vector<int> > *nursery){
	signed long int num_conflicts = 0;
	vector<vector<int> > new_nursery = *nursery;
	signed long int n = new_nursery.size();

	//counting horizontally (left and right)
	for(signed long int i = x + 1; i < n; i++){
		if(new_nursery[i][y] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[i][y] == 2){
			break;
		}
	}
	for(long long int i = x - 1; i >= 0; i--){
		if(new_nursery[i][y] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[i][y] == 2){
			break;
		}
	}

	//counting vertically (up and down)
	for(signed long int j = y+1; j < n; j++){
		if(new_nursery[x][j] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[x][j] == 2){
			break;
		}
	}
	for(long long int j = y - 1; j >= 0; j--){
		if(new_nursery[x][j] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[x][j] == 2){
			break;
		}
	}

	long long int x_2 = x;
	long long int y_2 = y;

	//counting in upper right diagonal
	while(x_2+1 < n && y_2+1 < n){
		if(new_nursery[x_2+1][y_2+1] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[x_2+1][y_2+1] == 2){
			break;
		}
		x_2+=1;
		y_2+=1;
	}

	//counting lower left diagonal
	x_2 = x, y_2 = y;
	while(x_2-1 >= 0 && y_2-1 >= 0){
		if(new_nursery[x_2-1][y_2-1] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[x_2-1][y_2-1] == 2){
			break;
		}
		x_2 -= 1;
		y_2 -= 1;
	}

	//counting left upper diagonal 
	x_2 = x, y_2 = y;
	while(x_2-1 >= 0 && y_2+1 <n){
		if(new_nursery[x_2-1][y_2+1] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[x_2-1][y_2+1] == 2){
			break;
		}		
		x_2 -= 1;
		y_2 += 1;
	}

	//counting right lower diagonal 
	x_2 = x, y_2 = y;
	while(x_2+1 < n && y_2-1 >= 0){
		if(new_nursery[x_2+1][y_2-1] == 1){
			num_conflicts += 1;
		}
		else if(new_nursery[x_2+1][y_2-1] == 2){
			break;
		}
		x_2 += 1;
		y_2 -= 1;
	}
	return num_conflicts;
}

//function counts all the conflicts of the nursery
int countAllConflicts(signed long int n, vector<vector<int> > *nursery){
	signed long int num_conflicts = 0;
	vector<vector<int> > new_nursery = *nursery;
	for(signed long int i = 0; i < n; i++){
		for(signed long int j = 0; j < n; j++){
			if(new_nursery[i][j] == 1){
				num_conflicts += countCurConflicts(i, j, &new_nursery);
			}
		}
	}
	// cout << "Total conflicts " << num_conflicts << endl;
	return num_conflicts;
}

//pick a random lizard and then moves it to a random spot 
//returns the new nursery
vector<vector<int> > moveLizard(vector<vector<int> > *nursery){
	vector<vector<int> > new_nursery = *nursery;
	signed long int lizard_x = 0, lizard_y = 0, rand_x = 0, rand_y = 0, n = new_nursery.size(), j;
	bool found_lizard = false;

	//pick a random row and check if there's a lizard there. store original cordinates
	while(!found_lizard){
		rand_x = rand() % n;
		for(j = 0; j < n; j ++){
			if(new_nursery[rand_x][j] == 1){
				lizard_x = rand_x; 
				lizard_y = j;
				found_lizard = true;
				break;
			}
		}
	}

	//jump lizard to a random spot 
	while(true){
		rand_x = rand() % n;
		rand_y = rand() % n;
		if(new_nursery[rand_x][rand_y] == 0){
			new_nursery[rand_x][rand_y] = 1;
			new_nursery[lizard_x][lizard_y] = 0;
			return new_nursery;
		}
	}
}

void runSA(signed long int n, signed long int p, vector<vector<int> > *nursery, signed long int spots){
	//t is the number of iterations
	signed long int rand_x = 0, rand_y = 0, t=2, next_count = 0, cur_count = 0, loop_counter = 0, lizards = p, i =0;
	long double T, delta_e;
	vector<vector<int> > current = *nursery;
	vector<vector<int> > next;
	bool finished = false;
	// randomly putting lizards onto nursery 1 per row 
	while(!finished){
		for(i = 0; i < n; i++){
			rand_y = rand() % n;
			if(current[i][rand_y] == 0){
				current[i][rand_y] = 1;
				p -= 1;
				if(p == 0){
					finished = true;
					break;
				}
			}
		}
	}
	//edge case if lizards are placed with valid placement and don't attack each other
	if(countAllConflicts(n, &current) == 0){
		// cout << "OK" << endl;
		createOutput(true, &current);
		return;
	}
	else{
		if(spots == lizards){
			// cout << "FAIL" << endl;
			createOutput(false, NULL);
			return;
		}
	}

	//running SA algorithm now
	while(true){
		//temperature function and check
		T = (1 / log(t)/log(exp(1) ) ) * 1.5 * n;
		if(T == 0.0){
			// cout << "T reached 0" << endl;
			createOutput(false, NULL);
			return;
		}

		//creating possible successor and counting conflicts of that successor 
		next = moveLizard(&current);
		next_count = countAllConflicts(n, &next);
		// cout << next_count << endl;

		//goal state check
		if(next_count == 0){
			// cout << "OK" << endl;
			// printNursery(n, next);
			createOutput(true, &next);
			return;
		}

		//calculating delta E and picking successor 
		cur_count = countAllConflicts(n, &current);
		delta_e = double(next_count - cur_count);
		if(delta_e < 0 || yes(exp(-delta_e / T))){ 
			current = next;
		}
		t += 1;
		clock_t end_check = clock();
		double elapsed_time = double(end_check - BEGIN) / CLOCKS_PER_SEC;
		// time check
		if(t % 100000 == 0){
			cout << "Time elapsed in SA: " << elapsed_time << ", " << T << " " << t << endl;
		}
		if(elapsed_time > 290){
			// cout << "FAIL" << endl;
			createOutput(false, NULL);
			return;
		}
	}
}

int main(){
	//initialize random seed
	srand(time(NULL));

	// opening intput.txt file for reading 
	ifstream inputFile;
	inputFile.open("input.txt");

	//declaring variables for reading input file 
	string line, algorithm;
	signed long int counter = 0, y_counter = 0, p = 0, n = 0, min_val, spots = 0; // p = lizard count, n = dimension 
	vector<vector<int> > nursery;

	//reading file now and storing them in proper variables 
	while(inputFile >> line){
		if(counter == 0)
			algorithm = line;
		else if(counter == 1)
			n = stoi(line); //dimension 
		else if(counter == 2)
			p = stoi(line); //lizard 
		else{
			//storing nursery into 2d vector
			vector<int> row;
			for(signed long int i = 0; i < line.size(); i++){
				signed long int temp = int(line[i]) - 48;
				if(temp < min_val){
					min_val = temp;
				}
				if(temp == 0){
					spots += 1;
				}
				row.push_back(temp);
			}
			nursery.push_back(row);
		}
		counter += 1;
	}
	inputFile.close();

	if(min_val == 2 || spots < p){
		// cout << "FAIL" << endl;
		createOutput(false, NULL);
		exit(1);
	}

	//checking which algorithm and calling corresponding function to handle it
	if(algorithm == "BFS")
		runBFS(n, p, &nursery);
	else if(algorithm == "DFS")
		runDFS(n, p, &nursery);
	else if(algorithm == "SA")
		runSA(n, p, &nursery, spots);

	clock_t end = clock();
	double elapsed_time = double(end - BEGIN) / CLOCKS_PER_SEC;
	cout << "Time(seconds): " << elapsed_time << endl;
}