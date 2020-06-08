SELECT description FROM crime_scene_report
where date = 20180115 and type = 'murder' and city = 'SQL City';

-- Security footage shows that there were 2 witnesses.
-- The first witness lives at the last house on "Northwestern Dr".
-- The second witness, named Annabel, lives somewhere on "Franklin Ave".

-- 1st witness  Morty Schapiro --------------------------------------------------------

SELECT * 
FROM Person
WHERE address_street_name = 'Northwestern Dr'
ORDER BY address_number DESC
LIMIT 1;

-- "14887"	"Morty Schapiro"	"118009"	"4919"	"Northwestern Dr"	"111564949"

SELECT transcript
FROM interview
WHERE person_id = 14887;

-- I heard a gunshot and then saw a man run out.
-- He had a "Get Fit Now Gym" bag.
-- The membership number on the bag started with "48Z".
-- Only gold members have those bags.
-- The man got into a car with a plate that included "H42W".

SELECT p.id, p.name
FROM get_fit_now_member g JOIN person p 
       ON g.person_id = p.id
	 JOIN drivers_license l 
       ON p.license_id = l.id
WHERE membership_status = 'gold'
      AND g.id LIKE '48Z%'
	    AND l.plate_number LIKE '%H42W%';

-- "67318"	"Jeremy Bowers"
-- "48Z55"	"67318"	"Jeremy Bowers"	"20160101"	"gold"	"67318"	"Jeremy Bowers"	"423327"	"530"	"Washington Pl, Apt 3A"	"871539279"	"423327"	"30"	"70"	"brown"	"brown"	"male"	"0H42W2"	"Chevrolet"	"Spark LS"


-- 2nd witness Annabel Miller --------------------------------------------------------

SELECT * 
FROM Person
WHERE address_street_name = 'Franklin Ave'
	  AND name LIKE '%Annabel%';
    
-- "16371"	"Annabel Miller"	"490173"	"103"	"Franklin Ave"	"318771143"

SELECT transcript
FROM interview
WHERE person_id = 16371;

-- I saw the murder happen, and I recognized the killer from my gym when I was working out last week on January the 9th.

SELECT *
FROM get_fit_now_check_in c
     JOIN get_fit_now_member m
		ON c.membership_id = m.id
     JOIN person p 
	    ON m.person_id = p.id
WHERE check_in_date = 20180109
      AND c.membership_id <> '90081'
      AND check_out_time IN 
	  (SELECT check_out_time
	   FROM get_fit_now_check_in c2
	   WHERE c2.membership_id  = '90081' -- Annabel MILLER
	   )	  ;
	
"48Z55"	"20180109"	"1530"	"1700"	"48Z55"	"67318"	"Jeremy Bowers"	"20160101"	"gold"	"67318"	"Jeremy Bowers"	"423327"	"530"	"Washington Pl, Apt 3A"	"871539279"




-- Killer Jeremy Bowers --------------------------------------------------------

SELECT transcript
FROM interview
WHERE person_id = 67318;

-- I was hired by a woman with a lot of money.
-- I don't know her name but I know she's around 5'5" (65") or 5'7" (67").
-- She has red hair and she drives a Tesla Model S.
-- I know that she attended the SQL Symphony Concert 3 times in December 2017.

INSERT INTO solution VALUES (1, 'Jeremy Bowers');
SELECT * from solution;

-- Congrats, you found the murderer! But wait, there's more...
-- If you think you're up for a challenge, try querying the interview transcript of the murderer to find the real villian behind this crime.
-- If you feel especially confident in your SQL skills, try to complete this final step with no more than 2 queries.
-- Use this same INSERT statement with your new suspect to check your answer.


--  Real villian --------------------------------------------------------

SELECT *
FROM drivers_license l JOIN person p
     ON l.id = p.license_id
WHERE height BETWEEN 65 AND 67
      AND gender = 'female'
	  AND hair_color = 'red'
	  AND car_make = 'Tesla'
	  AND car_model = 'Model S';
	  
-- "78881"	"Red Korb"
-- "90700"	"Regina George"
-- "99716"	"Miranda Priestly"

SELECT person_id, event_id, count (*)
FROM facebook_event_checkin
WHERE event_name = 'SQL Symphony Concert'
      AND DATE BETWEEN 20171201 AND 20171231
GROUP BY person_id, event_id
HAVING count(*) = 3;

-- "24556"	"1143"	"3"
-- "99716"	"1143"	"3"


SELECT *
FROM income
WHERE ssn = '987756388';

-- "987756388"	"310000"


SELECT p.id, p.name
FROM drivers_license l
     JOIN person p ON l.id = p.license_id
     JOIN income i ON i.ssn = p.ssn
WHERE height BETWEEN 65 AND 67
      AND gender = 'female'
      AND hair_color = 'red'
      AND car_make = 'Tesla'
      AND car_model = 'Model S'
      AND annual_income > 100000
      AND p.id IN (
        SELECT person_id
        FROM facebook_event_checkin
        WHERE event_name = 'SQL Symphony Concert'
          AND DATE BETWEEN 20171201 AND 20171231
        GROUP BY person_id, event_id
        HAVING count(*) = 3	  
      );

--- "202298"	"68"	"66"	"green"	"red"	"female"	"500123"	"Tesla"	"Model S"	"99716"	"Miranda Priestly"	"202298"	"1883"	"Golden Ave"	"987756388"


INSERT INTO solution VALUES (1, 'Miranda Priestly');
SELECT * from solution;

