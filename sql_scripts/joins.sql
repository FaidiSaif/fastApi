select * from posts
inner join votes on posts.id = votes.post_id
inner join users on votes.user_id = users.id;  

/** number of votes by user ***/
select users.id , count(votes.post_id) from votes
right join users on users.id = votes.user_id 
group by (users.id); 


/** number of votes by post **/
select posts.id as post_id , posts.title,  count(votes.post_id) as number_of_votes from votes
right join posts on posts.id = votes.post_id 
group by (posts.id)

/** select numebr of posts per user **/ 
select users.id as user_id , count(posts.owner_id) from posts
left join users on users.id = posts.owner_id 
group by (users.id); 

/** select number of votes per user **/ 
select users.id as user_id , count (votes.user_id) from users 
left join votes on users.id = votes.user_id 
group by (users.id); 


/** test selecting all the posts votes with the associated user who made the vote **/
select * from posts 
right join votes on votes.post_id =  posts.id 
right join users on users.id = votes.user_id 
; 