<form method="post" action="{{action}}" enctype="multipart/form-data">

Exam Name: <select name="exam_id">

<option value="">None</option>
{% for exam in exams %}
  <option value="{{exam.id}}">{{exam.name}}</option>
{% endfor %}

</select>

<p>

Homework Name: <select name="hw_id">

<option value="">None</option>
{% for hw in hws %}
  <option value="{{hw.id}}">{{hw.asgn}}</option>
{% endfor %}

</select>

<p>
<input type=file name=csv_import>
<p>
<input type=submit value="Upload">
</form>
