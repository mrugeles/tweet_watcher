select 
  folder, 
  tag,
  count(tag) as count
  from 
(select 
  explode(concat_tags(folder, HASHTAGS)) as tags,
  split(tags, " ")[0] as folder,
  split(tags, " ")[1] as tag
from tweets 
where HASHTAGS is not null) group by folder, tag