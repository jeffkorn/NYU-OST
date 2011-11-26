<html>
<head>
<title>Register</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<link rel="stylesheet" href="z.css">
<script language="JavaScript">
function Action() 
{  
   if( 	document.form1.sid.value == "" || document.form1.sid.value == null )
   {	alert("Please enter your Student ID");	return (false);
   }
   if (document.form1.sid.value.match(/^N\d\d\d\d\d\d\d\d$/)==null) 
   {	alert("StudentID should be N followed by 8 digits."); return false;
   }	 
   if(	document.form1.name.value == "" || document.form1.name.value == null
        || document.form1.name.value.indexOf(' ') == -1)
   {	alert("Please enter your Full Name");  return (false);
   }
   if(	document.form1.email.value == "" || document.form1.email.value == null )
   {	alert("Please enter your email address");  return (false);
   }
   if (document.form1.email.value.match(/^(.+)@(.+)\.(.+)$/)==null) 
   {	alert("Email address seems incorrect (check @ and .'s)"); return false;
   }	 
   document.form1.submit(); 
}
function Cancel()
{   history.back();
}
</script>
<body bgcolor="#ffffff" >

{% include "header.tpl" %}

{% if default_sid %}
<br>
{% include "menu.tpl" %}
{% endif %}

<font face="Arial, Helvetica, sans-serif"> 
<form name="form1" method="post"  action="grader.cgi" id="form1">
<input type=hidden name=command value=register>
  <table width="95%" border="0" cellpadding="1" cellspacing="0" bgcolor=black>
  <tr><td>
          <table width="100%" border="0" cellpadding="3" cellspacing="1" bgcolor=white>
            {% if not default_sid %}
            <tr> 
              <td width="12%">&nbsp;</td>
              <td colspan="2"> <font face="Arial, Helvetica, sans-serif">
              <b>Account register</b></font> <br>
                Please enter the following information. </td>
            </tr>
              {% endif %}
            <tr> 
              <td width="12%" height="9"> 
                <div align="right">Student ID</div>
              </td>
              <td width="29%" height="9"> 
              {% if default_sid %}
                <input type="hidden" name="sid" value="{{default_sid}}">
                <b>{{default_sid}}</b>
              {% else %}
                <input class="zfieldtext" type="text" name="sid" size=30 value="{{default_sid}}">
              {% endif %}
              </td>
              <td width="59%" height="9">
              {% if not default_sid %}
              * Your Student ID Number [format: <i>N12345678</i> ]
              {% endif %}
              </td>
            </tr>
            <tr> 
              <td width="12%"> 
                <div align="right">Name</div>
              </td>
              <td width="29%"> 
                <input class="zfieldtext" type="text" name="name" size=30 value="{{default_name}}">
              </td>
              <td width="59%">&nbsp;</td>
            </tr>
            <tr> 
              <td width="12%"> 
                <div align="right">Email</div>
              </td>
              <td width="29%"> 
                <input class="zfieldtext" type="text" name="email" size=30 value="{{default_email}}">
              </td>
              <td width="59%">* We will contact to you with this email</td>
            </tr>
            <tr> 
              <td width="12%">&nbsp;</td>
              <td width="29%"> 
                <div align="center"> 
                  <input class="zbutton" type="button" name="regist" value="   Submit   " onClick="Action()">
                  <input class="zbutton" type="button" name="cancel" value="  Cancel   " onClick="Cancel()">
                </div>
              </td>
              <td width="59%">&nbsp;</td>
            </tr>
          </table>
  </td></tr>
  </table>
  </form>

    <br><font face="trebuchet ms, Arial, Helvetica"><small><b><font size="1">
      Open Source Tools Course Homework submission system</font></b><font size=1><br>
      For problems or questions regarding this system contact <a 
      href="mailto:kornj@cs.nyu.edu?subject=Hw submission system problem.">Author</a></font></small></font>
    
</font>

</body>
</html>
