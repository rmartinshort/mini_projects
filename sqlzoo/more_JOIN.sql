/*
Section 7
*/

/*
Q1
The first example shows the goal scored by a player with the last name 'Bender'. 
The * says to list all the columns in the table - a shorter way of saying matchid, 
teamid, player, gtime

Modify it to show the matchid and player name for all goals scored by Germany. 
To identify German players, check for: teamid = 'GER'
*/

SELECT matchid, player FROM goal 
  WHERE teamid = 'GER'

/*
Q2
Show id, stadium, team1, team2 for just game 1012
*/

SELECT id,stadium,team1,team2
  FROM game
WHERE id = 1012

/*
Q3
Modify it to show the player, teamid, stadium and mdate for every German goal.
*/

SELECT player, teamid, stadium, mdate
  FROM game JOIN goal ON (id=matchid)
  WHERE teamid = "GER"

/*
Q4
Show the team1, team2 and player for every goal scored by a player called Mario 
player LIKE 'Mario%'
*/

SELECT team1, team2, player from game JOIN goal ON (id=matchid)
WHERE player LIKE  'Mario%'

/*
Q5
Show player, teamid, coach, gtime for all goals scored in the first 10 minutes gtime<=10
*/

SELECT player, teamid, coach, gtime
  FROM goal JOIN eteam ON (teamid=id)
 WHERE gtime<=10

/*
Q6
List the the dates of the matches and the name of the team in which 
'Fernando Santos' was the team1 coach.
*/

SELECT mdate, teamname FROM game JOIN eteam ON (team1 = eteam.id)
WHERE coach = 'Fernando Santos'

/*
Q7
List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'
*/

SELECT player FROM goal JOIN game ON (game.id = goal.matchid)
WHERE stadium = 'National Stadium, Warsaw'

/*
Q8
Show the name of all players who scored a goal against Germany.
*/

SELECT DISTINCT(player)
FROM game
  JOIN goal ON matchid = id
WHERE ((team1='GER' OR team2='GER') AND teamid != 'GER')

/*
Q9
Show the total number of prizes awarded.
*/

SELECT teamname, COUNT(player)
  FROM eteam JOIN goal ON id=teamid
  GROUP BY teamname

/*
Q10
List each subject - just once
*/

SELECT stadium, COUNT(player) AS goals
FROM game
  JOIN goal ON (id=matchid)
GROUP BY stadium

/*
Q11
For every match involving 'POL', show the matchid, date and the number of goals scored
*/

SELECT matchid, mdate, COUNT(player) AS goals
FROM game
  JOIN goal ON (matchid=id AND (team1 = 'POL' OR team2 = 'POL'))
GROUP BY matchid, mdate

/*
Q12
For every match where 'GER' scored, show matchid, match date and the number 
of goals scored by 'GER'
*/

SELECT id, mdate, COUNT(player) AS GER_goals
FROM game
  JOIN goal ON (id=matchid)
WHERE (team1 = 'GER' OR team2 = 'GER') AND (teamid='GER')
GROUP BY id, mdate

/*
Q13
List every match with the goals scored by each team as shown.
*/

SELECT mdate,
  team1,
  SUM(CASE WHEN teamid=team1 THEN 1 ELSE 0 END) AS score1, 
  team2,
  SUM(CASE WHEN teamid=team2 THEN 1 ELSE 0 END) AS score2
  FROM game LEFT JOIN goal ON matchid = id
GROUP BY mdate,team1,team2
ORDER BY mdate, matchid, team1,team2

