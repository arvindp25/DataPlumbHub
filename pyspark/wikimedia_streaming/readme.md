https://stream.wikimedia.org/v2/stream/recentchange


```
id: [{"topic":"eqiad.mediawiki.recentchange","partition":0,"timestamp":1746030241001},{"topic":"codfw.mediawiki.recentchange","partition":0,"offset":-1}]
data: {"$schema":"/mediawiki/recentchange/1.0.0","meta":{"uri":"https://commons.wikimedia.org/wiki/File:Iranian_Army_Ground_Forces_New_Equipment_Ceremony_2017_(119).jpg","request_id":"c26c48fb-7966-41d9-84b4-9b6fb1816e19","id":"67a266c6-6bb9-4923-826c-2b6bd04553a2","dt":"2025-04-30T16:24:01Z","domain":"commons.wikimedia.org","stream":"mediawiki.recentchange","topic":"eqiad.mediawiki.recentchange","partition":0,"offset":5553294672},"id":2839844572,"type":"edit","namespace":6,"title":"File:Iranian Army Ground Forces New Equipment Ceremony 2017 (119).jpg","title_url":"https://commons.wikimedia.org/wiki/File:Iranian_Army_Ground_Forces_New_Equipment_Ceremony_2017_(119).jpg","comment":"Adding [[Category:Mizannews review needed]]","timestamp":1746030241,"user":"Vysotsky","bot":false,"notify_url":"https://commons.wikimedia.org/w/index.php?diff=1026187021&oldid=711357579&rcid=2839844572","minor":false,"patrolled":true,"length":{"old":2244,"new":2281},"revision":{"old":711357579,"new":1026187021},"server_url":"https://commons.wikimedia.org","server_name":"commons.wikimedia.org","server_script_path":"/w","wiki":"commonswiki","parsedcomment":"Adding <a href=\"/wiki/Category:Mizannews_review_needed\" title=\"Category:Mizannews review needed\">Category:Mizannews review needed</a>"}
```


Edit Activity Monitoring

    Volume of edits over time (e.g., per hour, per day).

    Compare activity across projects (e.g., English vs. French Wikipedia).

    Detect high activity spikes, which might indicate newsworthy events or vandalism.

2. User Behavior Analysis

    Breakdown of anonymous vs registered vs bot edits.

    Track frequent contributors or new user contributions.

    Detect possible suspicious accounts (new users making many edits quickly).

3. Content Change Analysis

    Analyze types of changes (edit, new page creation, deletion, etc.).

    Track changes to specific namespaces (e.g., main, user, talk, etc.).

    Monitor edits to specific topics or keywords.

4. Geopolitical or Topical Trends

    Use comment, title, or user fields to infer:

        Edits related to current events.

        Topics that are suddenly popular or controversial.

    Identify pages that are hotbeds of edit wars.

5. Vandalism Detection

    Combine patterns such as:

        High frequency of small, anonymous edits.

        Reverts or warning messages in edit comments.

        Edits from IP ranges previously flagged for vandalism.

6. Bot Activity Tracking

    Analyze which bots are most active.

    Breakdown of automated vs human edits.

    Study patterns in bot-created pages or content maintenance.

7. Real-Time Event Detection

    Build dashboards or alerting systems for:

        Breaking news edits.

        Edits to a list of monitored pages.

        Sudden surge in editing from a particular country/IP.

8. Network & Social Graphs

    Build interaction networks:

        Who edits the same pages?

        Who reverts whom?

        Co-editing behavior over time.

🛠️ Technical Features You Can Use

    Filter by:

        rcprop: title, user, timestamp, comment, flags, etc.

        rctype: edit, new, log, etc.

        rcshow: bot, anon, redirect, patrolled, etc.

        rclimit, rcstart, rcend: for time-based analysis.