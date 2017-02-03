set -e

trap ctrl_c INT
function ctrl_c() {
  rm -f *.class
  kill -INT $$
}

javac $1.java
java $1
rm -f *.class
