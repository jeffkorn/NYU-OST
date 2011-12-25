<HTML>
<HEAD><TITLE>G22.3033-006: Open Source Tools</TITLE>
<META http-equiv=Content-Type content="text/html">
</HEAD>
<BODY>

{% include "header.tpl" %}

{% if sid %}
<br>
{% include "menu.tpl" %}
{% endif %}

<table border=1 width=75%><tr>
<td width=30%><b>Assignment</b></td><td width=30%><b>Status</b></td>
<td><b>Grade</b></td></tr>

{% for hw in hws %}

<tr><td><a href="{{hw.url}}">{{hw.asgn}}</a></td>

{% if not hw.has_file %}
<td>unsubmitted</td>
<td>unavailable</td>
{% else %}
<td><a href="grader.cgi?command=upload&asgn={{hw.name}}">Files</a></td>
<td>
  {% if not hw.grades_released %}
  in grading
  {% else %}
    {% if hw.final_score %}
    <a href="grader.cgi?command=scores&asgn={{hw.name}}">Grade: {{hw.final_score}}</a>
    {% else %}
    not graded yet
    {% endif %}
  {% endif %}
{% endif %}
</tr>

{% endfor %}

{% for exam in exams %}
<tr>
<td><b>{{exam.name}}</b></td>
<td>&nbsp;</td>
<td>
{% if not exam.grades_released %}
  in grading
{% else %}
  {{exam.score}}
{% endif %}
</td>
  </tr>
{% endfor %}

<tr><td><b><font color=red>Final Grade</font></b></td>
<td>&nbsp;</td><td><b><font color=red>Avail in January</font></b></td></tr>

</table>
</BODY>
</HTML>
