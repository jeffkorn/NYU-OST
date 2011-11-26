<form method="get" action="download">

Homework: <select name="asgn">

{% for hw in hws %}
  <option value="{{hw.id}}">{{hw.asgn}}</option>
{% endfor %}

</select>
<p>
<input type=submit value="Download">
</form>
