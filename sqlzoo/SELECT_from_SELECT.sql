/*
Section 3
*/

/*
Q1
List each country name where the population is larger than that of 'Russia'.
*/

SELECT name FROM world
  WHERE population >
     (SELECT population FROM world
      WHERE name='Russia')

/*
Q2
Show the countries in Europe with a per capita GDP greater than 'United Kingdom'.
*/

SELECT name 
FROM world 
WHERE (gdp/population > 
(SELECT gdp/population FROM world
WHERE name = 'united kingdom'))
AND (continent = 'europe')

/*
Q3
List the name and continent of countries in the continents containing either Argentina or Australia. 
Order by name of the country.
*/

SELECT name, continent FROM world
WHERE continent in 
(SELECT continent FROM world
WHERE name IN ( 'argentina', 'australia' ))
ORDER BY name 

/*
Q4
Which country has a population that is more than Canada but less than Poland? 
Show the name and the population.
*/

SELECT name, population FROM world
WHERE ( population  > (SELECT population FROM world WHERE name = 'Canada') )
AND ( population < (SELECT population FROM world WHERE name = 'Poland'))

/*
Q5
Germany (population 80 million) has the largest population of the countries in Europe. 
Austria (population 8.5 million) has 11% of the population of Germany.
*/

SELECT name,
     CONCAT(ROUND(100*population/(SELECT population 
     FROM world WHERE name = 'Germany')),'%') 

FROM world
WHERE continent = 'europe'

/*
Q6
Which countries have a GDP greater than every country in Europe? 
[Give the name only.] (Some countries may have NULL gdp values)
*/

SELECT name 
FROM world 
WHERE gdp > ALL (SELECT gdp FROM world WHERE (continent = 'europe') AND 
(gdp > 0))

/*
Q7
Find the largest country (by area) in each continent, 
show the continent, the name and the area:
*/

SELECT continent, name, area FROM world x
  WHERE area >= ALL
    (SELECT area FROM world y
        WHERE y.continent=x.continent
          AND area>0)

/*
Q8
List each continent and the name of the country that comes first alphabetically.
*/

SELECT continent, name FROM world x
WHERE name = (SELECT name FROM world y 
WHERE y.continent = x.continent ORDER BY name LIMIT 1)

/*
Q9
Find the continents where all countries have a population <= 25000000. 
Then find the names of the countries associated with these continents. 
Show name, continent and population.
*/

SELECT name, continent, population
FROM world x
WHERE 25000000  > ALL(SELECT population FROM world y WHERE x.continent = y.continent AND y.population > 0)

/*
Q10
Some countries have populations more than three times that of any of their neighbours 
(in the same continent). Give the countries and continents
*/

SELECT name, continent FROM world x
WHERE population > ALL(SELECT 3*population FROM world y 
WHERE (y.name != x.name) AND (y.continent = x.continent))