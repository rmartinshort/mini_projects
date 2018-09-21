/*
Easy questions
*/

/*
Q1
Give the room id in which the event co42010.L01 takes place.
*/

SELECT room.id FROM room 
JOIN event ON (event.room = room.id)
WHERE event.id = 'co42010.L01'

/*
Q2
For each event in module co72010 show the day, the time and the place.
*/

SELECT dow, tod, room FROM event
JOIN modle ON (modle.id = event.modle)
WHERE modle.id = 'co72010'

/*
Q3
List the names of the staff who teach on module co72010.
*/

SELECT name FROM staff 
JOIN teaches ON (teaches.staff = staff.id)
JOIN event ON (event.id = teaches.event)
WHERE modle = 'co72010'
GROUP BY name

/*
Q4
Give a list of the staff and module number associated with events using room cr.132 on Wednesday, 
include the time each event starts.
*/

SELECT staff.name, event.modle, event.tod FROM staff
JOIN teaches ON (teaches.staff = staff.id)
JOIN event ON (event.id = teaches.event)
WHERE (dow = 'Wednesday' AND room = 'cr.132')


/*
Q5
Give a list of the student groups which take modules with the word 'Database' in the name.
*/

SELECT student.name as student_group_name FROM student
JOIN attends ON (attends.student = student.id)
JOIN event ON (event.id = attends.event)
JOIN modle ON (modle.id = event.modle)
WHERE modle.name LIKE '%Database%'
GROUP BY student.name 

/*
Medium questions
*/

/*
Q6
Show the 'size' of each of the co72010 events. Size is the total number of students attending each event.
*/

SELECT COUNT(student),event FROM attends
WHERE event IN

(SELECT id FROM event
WHERE modle = 'co72010')

GROUP BY event

/*
Q7
For each post-graduate module, show the size of the teaching team. (post graduate modules start with the code co7).
*/

SELECT modle, COUNT(staff) FROM teaches JOIN
event ON (event.id = teaches.event)
WHERE event in

(SELECT id FROM event
WHERE modle like 'co7%')

GROUP BY modle

/*
Q8
Give the full name of those modules which include events taught for fewer than 10 weeks.
*/

SELECT name FROM modle
JOIN event ON (event.modle = modle.id)
WHERE event.duration < 10
GROUP BY name

/*
Q9
Identify those events which start at the same time as one of the co72010 lectures.
*/

SELECT * FROM event 
WHERE tod IN

(SELECT tod FROM event
WHERE modle = 'co72010')

/*
Q10
How many members of staff have contact time which is greater than the average?
*/

SELECT COUNT(contact) as gt_average FROM
(
SELECT SUM(duration) as contact, staff FROM teaches
JOIN event ON (event.id = teaches.event)
GROUP BY staff
)
AS a 
WHERE contact > 
(
SELECT AVG(contact) FROM 
(
SELECT SUM(duration) as contact, staff FROM teaches
JOIN event ON (event.id = teaches.event)
GROUP BY staff
)
AS b
)
