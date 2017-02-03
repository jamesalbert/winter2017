wget -O /tmp/csimForJava.jar.zip http://www.ics.uci.edu/~wayne/courses/cs115/CSIM/csimForJava.jar.zip;
DIR=$JAVA_HOME
if [ -f /usr/libexec/java_home ]
  then
    DIR=$(/usr/libexec/java_home)/jre
fi
tar xvf /tmp/csimForJava.jar.zip -C $DIR/lib/ext;
echo "csimForJava.jar has been placed in $(/usr/libexec/java_home)/jre/lib/ext"
