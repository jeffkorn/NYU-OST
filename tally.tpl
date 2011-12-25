{% for s in students %}{% ifequal forloop.counter 1 %}Name,SID,{% for hw in s.grades %}{{hw.asgn}},{% endfor %}{% endifequal %}
{{s.name}},{{s.sid}},{% for hw in s.grades %}{{hw.score}},{% endfor %}{% endfor %}
