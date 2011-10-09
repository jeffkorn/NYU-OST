<HTML><HEAD><TITLE>G22.3033-006: Open Source Tools</TITLE>
<META http-equiv=Content-Type content="text/html; charset=windows-1252">
<META content="MSHTML 6.00.2800.1106" name=GENERATOR></HEAD>
<BODY>


{% include "header.tpl" %}

{% if sid %}
<br>
{% include "menu.tpl" %}
{% endif %}

<table border=1>

{% for s in students %}
<tr>
<td>{{s.sid}}</td>
  {% for hw in s.grades %}
    <td><a href="grader.cgi?command=admin&sid={{s.sid}}&hw={{hw.asgn}}">
        {% ifequal hw.score '' %}
          {% ifequal hw.submitted '1' %}
          <font color=black>{{hw.asgn}}</font>
          {% else %}
          <font color=gray>{{hw.asgn}}</font>
          {% endifequal %}
        {% else %}
        <font color=black>{{hw.asgn}} ({{hw.score}})</font>
        {% endifequal %}
</a>
    </td>
  {% endfor %}
</tr>
{% endfor %}

</table>

</BODY></HTML>
