<form method="post" action="upload_exam" enctype="multipart/form-data">

Exam Name: <select name="exam_id">

{% for exam in exams %}
  <option value="{{exam.id}}">{{exam.name}}</option>
{% endfor %}

</select>
<p>
<input type=file name=csv_import>
<p>
<input type=submit value="Upload">
</form>
