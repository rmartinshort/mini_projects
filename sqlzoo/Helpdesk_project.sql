/*
Easy questions
*/

/*
Q1
There are three issues that include the words "index" and "Oracle". 
Find the call_date for each of them
*/

SELECT call_date, call_ref FROM Issue
WHERE Detail LIKE '%Oracle%'
AND Detail LIKE '%index%'


/*
Q2
Samantha Hall made three calls on 2017-08-14. Show the date and time for each
*/

SELECT call_date, first_name, last_name FROM Issue
JOIN Caller ON (Issue.Caller_id = Caller.Caller_id)
WHERE First_name = 'Samantha' AND Last_name = 'Hall' AND call_date LIKE '2017-08-14%'

/*
Q3
There are 500 calls in the system (roughly). Write a query that shows the number that 
have each status
*/

SELECT Status,  COUNT(Status) AS Volume
FROM Issue
GROUP BY Status

/*
Q4
Calls are not normally assigned to a manager but it does happen. 
How many calls have been assigned to staff who are at Manager Level?
*/

SELECT COUNT(Manager) as mlcc 
FROM Issue 
JOIN Staff ON (Issue.Assigned_to = Staff.Staff_code)
JOIN Level ON (Level.Level_code = Staff.Level_code)

/*
Q5
Show the manager for each shift. Your output should include the 
shift date and type; also the first and last name of the manager.
*/

SELECT Shift_date, Shift_type, First_name, Last_name FROM Shift
JOIN Staff ON (Shift.manager = Staff.Staff_code)