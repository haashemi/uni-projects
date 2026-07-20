-- TopClicks
select
    a.id        as ad_id,
    a.name      as ad_name,
    u.name      as user_name,
    count(c.id) as total_clicks,

    count(c.id) filter (where c.platform in ('android', 'ios'))     as mobile_clicks,
    count(c.id) filter (where c.platform not in ('android', 'ios')) as desktop_clicks
from ads   a
join users u           on a.user_id = u.id
left join  ad_clicks c on a.id = c.ad_id
group by
    a.id, a.name, u.name
order by
    total_clicks desc,
    ad_name asc;

-- TodayAds
select
    a.*
from ads a
left join payments p on p.ad_id = a.id
where
    p.status = 'completed'
    and a.since_date < now()
    and a.until_date > now()
    -- Optionally, to get ads for a specific audience:
    -- and 'programming' = ANY(a.audiences)
group by
    a.id;
