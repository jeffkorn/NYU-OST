<HTML><HEAD><TITLE>G22.3033-004: Open Source Tools</TITLE>
<META http-equiv=Content-Type content="text/html">
</HEAD>
<BODY>

{% include "header.tpl" %}

{% if not admin %}
<br>
{% include "menu.tpl" %}
{% else %}
<a href="grader.cgi?command=admin">Grade list</a>
{% endif %}

<center>
{% if admin %}
<form action=grader.cgi method=post>
<input type=hidden name=command value=scores>
<input type=hidden name=store value=1>
<input type=hidden name=asgn value={{name}}>
<input type=hidden name=student_sid value={{student_sid}}>
{% endif %}

<table width="95%" border="2" cellspacing="1" cellpadding="10" bordercolor=wheat bgcolor="#FFFFFF">
<tr><td><center><font face="Arial, Helvetica, sans-serif">{{asgn}}</font><br>
	Grader:
{% if admin %}

<select name=grader>
<option value=""></option>
{% for n in graders %}
<option value="{{n}}"
{% ifequal n grader %}
selected=1
{% endifequal %}
>{{n}}</option>
{% endfor %}
</select>
<br>
Student: {{student_sid}}

{% else %}
{{grader}}
{% endif %}
	<hr noshade color="wheat">
	<table width="95%" border="0" cellspacing="0" cellpadding="3">
	<tr><td nowrap>Basic points:</td>
        <td>
{% if admin %}
<input type=text name=basic value="{{basic}}">
{% else %}
{{basic}}
{% endif %}
        </td></tr>
	<tr><td nowrap>Extra points:</td>
        <td>
{% if admin %}
<input type=text name=extra value="{{extra}}">
{% else %}
{{extra}}
{% endif %}
        </td></tr>
	<tr><td nowrap>Late penalty:</td>
        <td>
{% if admin %}
<input type=text name=penalty value="{{penalty}}">
{% else %}
{{penalty}}
{% endif %}
        </td></tr>
	<tr><td nowrap>Final points:</td>
        <td>
{% if admin %}
<input type=text name=final value="{{final}}">
{% else %}
{{final}}
{% endif %}
        </td></tr>
 	<tr><td nowrap valign=top>Comments:</td>
        <td valign=top>
{% if admin %}
<textarea length=60 name=comments>{{comments}}</textarea>
</td></tr>
<tr><td nowrap valign=top>Private Comments:</td>
<td valign=top>
<textarea length=60 name=private_comments>{{private_comments}}</textarea>
{% else %}
<xmp>{{comments}}</xmp>
{% endif %}
        </td></tr>
{% if admin %}
<tr><td nowrap valign=top>
<input type=submit value="Save">
</form>
</td></tr>
{% endif %}
	</table></center><br>&nbsp;
</td></tr>
</table>

</center>

</BODY></HTML>
