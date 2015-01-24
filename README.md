# Coffee Report

Morning coffee runs are timed and reported to Twitter like this:

<blockquote class="twitter-tweet" lang="en"><p>My time is 6:01.90.</p>&mdash; Michal (@913coffee) <a href="https://twitter.com/913coffee/status/558807048880521216">January 24, 2015</a></blockquote>

These tweets can be <a href="https://support.twitter.com/articles/20170160-downloading-your-twitter-archive">
exported from Twitter</a>. The archive provided by Twitter contains files like `data/js/tweets/2015_01.js` which have bits of Javascript like this:

```javascript
Grailbird.data.tweets_2015_01 =
[ {
    "text" : "My time is 6:01.90.",
    "created_at" : "2015-01-24 02:02:37 +0000",
    ...
},
...
]
```

The scripts here will parse such Javascript files and produce a report.
