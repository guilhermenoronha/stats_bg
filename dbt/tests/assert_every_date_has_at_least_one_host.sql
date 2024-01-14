-- Each session must has a host.
-- Therefore return records where the date has the sum of hosts = 0.
select distinct 
	date, 
	sum(case when is_host = true then 1 else 0 end) as host_count
from {{ref('attendances')}} 
group by date
having sum(case when is_host = true then 1 else 0 end) = 0