/*
Section 4
*/

/*
Q1
Show the total population of the world.
*/

SELECT SUM(population)
FROM world

/*
Q2
List all the continents - just once each.
*/

SELECT DISTINCT continent FROM world

/*
Q3
Give the total GDP of Africa
*/

SELECT SUM(gdp) FROM world x
WHERE (x.continent = 'africa')

/*
Q4
How many countries have an area of at least 1000000
*/

SELECT COUNT(name) FROM world x
WHERE (x.area > 1000000)

/*
Q5
What is the total population of ('Estonia', 'Latvia', 'Lithuania')
*/

SELECT SUM(population) FROM world x
WHERE(x.name in ('estonia','latvia','lithuania'))

/*
Q6
For each continent show the continent and number of countries.
*/

SELECT continent, COUNT(name)
FROM world
GROUP BY continent

/*
Q7
For each continent show the continent and number of countries with populations of at least 10 million.
*/

SELECT continent, COUNT(name)
FROM world x
WHERE (x.population > 10000000)
GROUP BY continent

/*
Q8
List the continents that have a total population of at least 100 million.
*/

SELECT continent FROM world x
WHERE (SELECT SUM(population) FROM world y WHERE x.continent = y.continent) > 100000000
GROUP BY continent

/* 
Extra: Sum and count on the Nobel table 
*/

/*
Q1
Show the total number of prizes awarded.
*/

SELECT COUNT(winner) FROM nobel

/*
Q2
List each subject - just once
*/

SELECT DISTINCT(subject) from nobel

/*
Q3
Show the total number of prizes awarded for Physics.
*/

SELECT COUNT(subject) from nobel x
WHERE (x.subject = 'physics')

/*
Q4
For each subject show the subject and the number of prizes.
*/

SELECT subject, COUNT(winner) FROM nobel
GROUP BY subject

/*
Q5
For each subject show the first year that the prize was awarded.
*/

SELECT subject, yr FROM nobel x
WHERE yr = (SELECT MIN(yr) from nobel y 
WHERE (y.subject = x.subject))
GROUP BY subject  

/*
Q6
For each subject show the number of prizes awarded in the year 2000.
*/

SELECT subject, COUNT(winner) FROM nobel 
WHERE yr = 2000
GROUP BY subject

/*
Q7
Show the number of different winners for each subject.
*/

SELECT subject, COUNT(DISTINCT winner) FROM nobel 
GROUP BY subject

/*
Q8
For each subject show how many years have had prizes awarded.
*/

SELECT subject, COUNT(distinct yr) FROM nobel
GROUP BY subject

/*
Q9
Show the years in which three prizes were given for Physics.
*/

SELECT yr  FROM nobel x
WHERE (x.subject = 'physics')
GROUP BY yr 
HAVING COUNT(yr) = 3

/*
Q10
Show winners who have won more than once.
*/

SELECT winner FROM nobel 
GROUP BY winner
HAVING COUNT(winner) > 1

/*
Q11
Show winners who have won more than once.
*/

SELECT winner, COUNT(DISTINCT(subject)) FROM nobel 
GROUP BY winner
HAVING COUNT(DISTINCT(subject)) > 1 

