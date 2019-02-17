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


/* Medium questions */

/*
Q6
List the Company name and the number of calls for those companies with more than 18 calls.
*/

SELECT Company_name, COUNT(Caller.Caller_id) FROM Customer
JOIN Caller ON (Caller.Company_ref = Customer.Company_ref)
JOIN Issue ON (Issue.Caller_id = Caller.Caller_id)
GROUP BY Company_name
HAVING COUNT(Caller.Caller_id) > 18

/*
Q7
Find the callers who have never made a call. Show first name and last name
The trick here is to do a left join
*/
SELECT First_name, Last_name FROM Caller
LEFT JOIN Issue ON (Issue.Caller_id = Caller.Caller_id)
WHERE Issue.Caller_id is NULL

/*
Q8
For each customer show: Company name, contact name, number of calls where the number of calls is fewer than 5
*/
SELECT
	a.Company_name,
	b.first_name,
	b.last_name,
	a.nc
FROM
(SELECT
	Customer.Company_name,Customer.Contact_id,COUNT(*) AS nc
	FROM Customer
	JOIN Caller ON (Customer.Company_ref = Caller.Company_ref)
	JOIN Issue ON (Caller.Caller_id = Issue.Caller_id)
	GROUP BY Customer.Company_name, Customer.Contact_id
	HAVING COUNT(*) < 5
	)
	AS a
	JOIN Caller as b
	ON (a.Contact_id = b.Caller_id);

/*
Q9
For each shift show the number of staff assigned. Beware that some roles may be NULL 
and that the same person might have been assigned to multiple roles (The roles are 
'Manager', 'Operator', 'Engineer1', 'Engineer2').
*/
SELECT a.Shift_date, a.Shift_type, COUNT(role) as cw 
FROM
( 
SELECT Shift_date,Shift_type, Manager AS role FROM Shift
UNION ALL 
SELECT Shift_date,Shift_type, Operator AS role FROM Shift
UNION ALL
SELECT Shift_date,Shift_type, Engineer1 AS role FROM Shift
UNION ALL
SELECT Shift_date,Shift_type, Engineer2 AS role FROM Shift
)
AS a
GROUP BY a.Shift_date, a.Shift_type

/*
Another option, which does not take unique employees into account
*/
SELECT Shift_date, Shift_type, COUNT(DISTINCT Manager) + COUNT(DISTINCT Operator) + 
COUNT(DISTINCT Engineer2) + COUNT(DISTINCT Engineer1)
FROM Shift
GROUP BY Shift_date, Shift_type

/*
Q10
Caller 'Harry' claims that the operator who took his most recent call was 
abusive and insulting. Find out who took the call (full name) and when.
*/
SELECT Staff.first_name, Staff.last_name, call_date FROM Staff
JOIN Issue ON (Issue.taken_by = Staff.staff_code)
JOIN Caller ON (Caller.caller_id = Issue.caller_id)
WHERE Caller.first_name = 'Harry'
ORDER BY call_date DESC
LIMIT 1
