select
    u.name as user_name, count(*)
from
    (
        select user_id, course_id, count(*)
        from (select distinct user_id, course_id, lesson_no, exercise_no
        from saves) unique_saves
        group by user_id, course_id having count(*) > 100
    ) finished_courses, users u
where
  1=1
  and finished_courses.user_id = u.id
 group by u.name;


