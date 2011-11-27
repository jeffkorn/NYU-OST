<HTML><HEAD><TITLE>G22.3033-006: Open Source Tools</TITLE>
<META http-equiv=Content-Type content="text/html">
</HEAD>
<BODY>

{% include "header.tpl" %}

{% if sid %}
<br>
{% include "menu.tpl" %}
{% endif %}

<table>
<tr>
<td nowrap valign=top bgcolor=#cfcfcf>
<font size=+1><b>&nbsp;Assigned homeworks&nbsp;</b></font><br>

{% for h in hws %}

  <li>{% ifequal h.asgn hw.asgn %}<b>{% else %}<a href="grader.cgi?command=upload&asgn={{h.id}}">{% endifequal %}{{h.asgn}}{% ifequal h.asgn hw.asgn %}</b>{% else %}</a>{% endifequal %}

{% endfor %}

<ul id="asgn_list">
</ul>
</td>
<td valign=top>

  <center>
    <h3>
        <a id="asgn_url" href="{{hw.url}}">{{hw.asgn}}</a><br>
        Due: <span id="due_date">{{hw.due}}</span>
    </h3>
  </center>

  <link rel="stylesheet" href="z.css">
  <div id="message_html">
  </div>
  <form id="form1" name="form1" method="post" action="{{upload_url}}" enctype="multipart/form-data">
  <input type=hidden name=command value=uploadfile2>
  <input type="hidden" name="asgn" value="{{hw.id}}">
  <table width="95%" border="0" cellspacing="2" cellpadding="2">
    <tr>
      <td width="7%" valign=top><b>1</b></td>
      <td>
        <input class="zfieldtext" type="file" size=50 name="upload_file"><br>
      Or, to upload from the department server, run the following command:<br>
      &nbsp;&nbsp;<tt>/home/unixtool/bin/submit_hw {{sid}} {{sid_hash}} \<br>
      &nbsp;&nbsp;{{hw.id}} <i>filename</i></tt>
      <br>
        If you submitted this file before and want to overwrite it, you must
        first delete the old version and then resubmit the new one.
      </td>
    </tr>
    <tr>
      <td width="7%"><b>2</b></td>
      <td>Press the Upload button ONCE.
        <input class="zbutton" type="submit" name="uploadbtn"
               value=" Upload this file ">
      </td>
    </tr>
    <tr>
      <td width="7%" valign=top> <b>***</b></td>
      <td> If there are multiple files in your homework,
           please upload them one by one.
      </td>
    </tr>
  </table>
  </form>

  <form id="form2" name="form2" method="post" action="grader.cgi">
  <input type=hidden name=command value=uploadurl>
  <input type="hidden" name="asgn" value="{{hw.id}}">
  <table width="95%" border="0" cellspacing="2" cellpadding="2">
   {% if hw.submit_url %}
    <tr id="submiturl">
      <td width="7%"><b>3</b></td>
      <td>
        <input class="zfieldtext" type="text" size="50" id="upload_url" name="upload_url" value={{submitted_url}}>
                <input class="zbutton" type="submit" name="uploadbtn"
                       value="Submit this URL"><br>
        Some homeworks or projects (e.g. Final project) require turning
        in the URL.
      </td>
    </tr>
   {% endif %}
  </table>
  </form>

  {% if files %}
  <div id="file_list">
        <hr size="1">
        So far, the following files have been uploaded:
        <form name="form2" method="post" action="grader.cgi">
        <input type="hidden" name="command" value="rm">
        <input type="hidden" name="asgn" value="{{hw.id}}">
        <input type="hidden" name="filename" value="">
        <table id="table" width="95%%" border="1" cellspacing="0">
        <tr>
        <td width="18%"><b> File</b></td>
        <td width="34%"><b> Details</b></td>
        <td width="20%"><b> Submit time</b></td>
        <td width="28%"><b> Operation</b></td>
        </tr>
        {% for file in files %}
        <tr id="file">
           <td width="18%"> <tt>{{file.name}}</tt></td>
           <td width="34%"><xmp id="desc">Size: {{file.size}} bytes</xmp></td>
           <td width="20%" id="time" valign="top">{{file.date}}</td>
           <td width="28%" id="action" valign="top">
           <input class='zbutton' type=button name=Button%d
               value='Delete "{{file.name}}"' onClick='filename.value="{{file.name}}"; submit();'>
           </td> 
        </tr>
        {% endfor %}
        </table>
        </form>
  </div>
  {% endif %}

</td>
</tr>
</table>

</BODY></HTML>
