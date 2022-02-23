# Ratio Checker

<h3>Ratio Checker was a Twitter bot that looked for
attempted <a href="https://www.urbandictionary.com/define.php?term=ratio">"ratios"</a> and tried to determine if the
ratio was successful or not.</h2>
<h4>The bot has been permanently suspended by Twitter.</h4>
<h4>You can check out the bot's old Twitter account <a href="https://twitter.com/Ratio_Checker">here</a>.</h4>
<hr>

# How did it work?

<h3>This script has 2 phases: <u>harvesting</u> and <u>serving</u>.</h3>
<h2>Harvesting</h2>
<h4>During this phase, the script will scour Twitter, looking for tweets that meet the following requirements:
<ul>
    <li>Is a reply</li>
    <li>Has the word "ratio" in it</li>
</ul>
If the tweet meets these basic requirements (and a few other more specific requirements), information about that tweet is gathered and saved into a PostgreSQL database table.

![reply_tweet database table.](info/images/postgresql_database_table.png?raw=true)
</h4>

<h2>Serving</h2>
<h4>During this phase, the script will begin to fire off replies to the tweets that have been harvested that meet the
following requirements.
<ul>
    <li>Is at least 1 day old</li>
    <li>Is still accessible</li>
    <li>Parent tweet is still accessible</li>
    <li>Has met a tweet score threshold</li>
    <li>Parent tweet has met a predetermined tweet score threshold</li>
    <li>Difference of tweet score for tweet and parent tweet meet a predetermined threshold</li>
</ul>
If the tweet meets these basic requirements (and a few other more specific requirements), a reply is "served" to the tweet, stating whether the ratio was successful.
<br>
It also states the tweet score for both the tweet and the parent tweet.
<br>
A grade is also assigned based on the difference between the tweet scores.
