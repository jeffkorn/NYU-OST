<HTML><HEAD><TITLE>G22.3033-004: Open Source Tools</TITLE>
<BODY>

{% include "header.tpl" %}

{% if sid %}
<br>
{% include "menu.tpl" %}
{% else %}
{% include "admin_menu.tpl" %}
{% endif %}

<table border=1>

{% for s in students %}
<tr>
<td title="{{s.name}}">{{s.sid}}</td>
  {% for hw in s.grades %}
    <td>
      {% ifequal hw.show_link '1' %}
      <a href="grader.cgi?command=admin&sid={{s.sid}}&hw={{hw.asgn}}">
      {% endifequal %}
        {% ifequal hw.score '' %}
          {% ifequal hw.submitted '1' %}
          <font color=black>{{hw.asgn}}</font>
          {% else %}
          <font color=gray>{{hw.asgn}}</font>
          {% endifequal %}
        {% else %}
        <font color=black>{{hw.asgn}} ({{hw.score}})</font>
        {% endifequal %}
      {% ifequal hw.show_link '1' %}
      </a>
      {% endifequal %}
    </td>
  {% endfor %}
</tr>
{% endfor %}

</table>

</BODY></HTML>
