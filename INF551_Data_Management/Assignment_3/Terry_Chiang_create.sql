drop table if exists Candidates;
create table Candidates(
	CID int primary key, 
	name varchar(20), 
	affiliation varchar(20),
	year int
);

Drop table if exists Electoral;
create table Electoral(
	EID int primary key, 
	statename char(2), 
	year int, 
	affiliation varchar(20) references candidates,
	votes int default 0	
);

Drop table if exists Popular;
create table Popular(
	PID int primary key, 
	statename char(2), 
	year int, 
	affiliation varchar(20) references candidates,
	votes int default 0
);

create index E_votes on Electoral(votes);

create index P_vote on Popular(votes); 

create index candidate_year on Candidates(year);


/* 
I believe my design is good because the candidate year search would be quick since the year is stored in the candidates table. I also created an index on the year as well.  

The electoral and popular table would only store information if there were votes that existed. Therefore the information stored in those tables will always be full of data. Searching for the amount of votes would be quick because of this structure. I also created indexes on the votes for each type to speed that up as well. 

*/ 
