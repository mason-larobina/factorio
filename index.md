---
layout: default
title: Mason's Factorio Blog
---

{% assign posts = site.pages | where: "layout", "post" | sort: "date" | reverse %}
{% for p in posts %}
- [{{ p.date | date: "%Y-%m-%d" }} - {{ p.title }}]({{ p.url | relative_url }})
{% endfor %}
